#!/usr/bin/env python3
"""World-targets background refresher.

Scans HARVESTING victims across hot-list nodes, applies guild + heal-event
filters, projects HP via canonical formulas, computes margin against each
of bpeon's 6 strikers, writes the result to predator/world_targets.json.

Atomic write (.tmp → rename) so partial reads never see truncated JSON.
Designed to run on a 5-min cron without any LLM in the loop.
"""

import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from executor.hp_projection import compute_current_hp, kill_threshold

ORACLE_URL = "https://136-112-224-147.sslip.io"
ORACLE_TOKEN = "pV6WYI4HUSLWK95cSg_YJbDlD6rTdCDaYCCMqhQvTl8"

OUTPUT_PATH = REPO_ROOT / "predator" / "world_targets.json"
GUILD_PATH = REPO_ROOT / "predator" / "guild-no-touch.csv"

# FLOOR_NODES = always-watch set used as a safety floor when oracle is down
# OR as a baseline that dynamic discovery merges on top of. Player traffic
# shifts continually; a static list goes blind to new clusters (Sacrarium /
# acheron / Assassins, observed 2026-05-03).
FLOOR_NODES = [
    86, 60, 73, 25, 62, 9, 82,           # original (minus dead node 30)
    16, 88, 89, 10, 15, 83, 33, 76, 35, 34,  # session-106 additions
    87,                                  # Sacrarium (added 2026-05-03 R1.5)
]
MAX_ACTIVE_NODES = 50
ACTIVITY_WINDOW_HOURS = 6

# HOT_NODES is populated at runtime by discover_active_nodes(); kept as a
# module-level mutable for backward compatibility with helpers that read it.
HOT_NODES = list(FLOOR_NODES)

# bpeon's striker roster (kept here for tactical-decision speed; refresh on respec).
STRIKERS = [
    {"idx": 12649, "V": 34, "H": 12, "max_hp": 170, "hand": "NORMAL", "atk_s": 400, "atk_r": 500},
    {"idx": 11224, "V": 36, "H": 11, "max_hp": 140, "hand": "EERIE",  "atk_s": 280, "atk_r": 500},
    {"idx": 10705, "V": 32, "H": 19, "max_hp": 240, "hand": "INSECT", "atk_s": 280, "atk_r": 250},
    {"idx": 6058,  "V": 31, "H": 18, "max_hp": 200, "hand": "SCRAP",  "atk_s": 280, "atk_r": 250},
    {"idx": 15540, "V": 31, "H": 21, "max_hp": 190, "hand": "NORMAL", "atk_s": 280, "atk_r": 250},
    {"idx": 12225, "V": 30, "H": 19, "max_hp": 220, "hand": "NORMAL", "atk_s": 260, "atk_r": 250},
]

# rtvvvvv was added to the no-touch list in session 80 (3 reverts in a row).
# Soft no-touch: not guild, but defended too well to chase.
SOFT_NO_TOUCH_OWNERS = {"rtvvvvv"}

# Known suspect owners — always heat-checked so the snapshot exposes their
# anti_predator_automation status even when they have no HARVESTING candidates
# at scan time (their automation often empties the node before we look).
# Aenne added session 111 after the session-110 22-second sync-stop discovery.
ANTI_PREDATOR_WATCH = {"aenne", "stefan97", "stefan96", "foden", "dias", "rtvvvvv"}


def oracle_sql(sql, limit=4000):
    body = json.dumps({"q": sql, "limit": limit}).encode()
    req = urllib.request.Request(
        f"{ORACLE_URL}/sql",
        data=body,
        headers={
            "Authorization": f"Bearer {ORACLE_TOKEN}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        j = json.loads(r.read())
    return [dict(zip(j["columns"], row)) for row in j["rows"]]


def load_guild():
    handles, accs = set(), set()
    with open(GUILD_PATH) as f:
        for line in f:
            line = line.rstrip()
            if not line or line.startswith("#") or line.startswith("account_id"):
                continue
            parts = line.split(",")
            if len(parts) >= 2:
                acc = parts[0].strip()
                handle = parts[1].strip().lower()
                if acc:
                    accs.add(acc)
                if handle:
                    handles.add(handle)
    return handles, accs


def get_node_affinities():
    nids = ",".join(f"'{n}'" for n in HOT_NODES)
    rows = oracle_sql(
        f"SELECT node_index, room_index, name, affinity FROM nodes_catalog WHERE node_index IN ({nids})",
        limit=200,
    )
    out = {}
    for r in rows:
        aff = (r.get("affinity") or "NORMAL").upper()
        parts = [p.strip() for p in aff.replace("/", ",").split(",") if p.strip()]
        out[int(r["node_index"])] = {
            "room": int(r["room_index"]),
            "name": r["name"],
            "affinities": parts or ["NORMAL"],
        }
    return out


def scan_node(node_id, node_meta, handles, accs):
    """Return list of candidate dicts for this node, sorted by margin desc."""
    sql = f"""
    WITH last_actions AS (
      SELECT kami_id, action_type, block_timestamp, node_id, harvest_id,
        ROW_NUMBER() OVER (PARTITION BY kami_id ORDER BY block_timestamp DESC) AS rn
      FROM kami_action
      WHERE action_type IN ('harvest_start','harvest_stop','harvest_collect','harvest_liquidate','feed','revive')
        AND block_timestamp >= NOW() - INTERVAL 24 HOUR
    ),
    hs_open AS (
      SELECT kami_id, block_timestamp AS start_ts, node_id, harvest_id
      FROM last_actions
      WHERE rn=1 AND action_type='harvest_start' AND node_id='{node_id}'
    ),
    killed_harvests AS (
      -- harvest_liquidate rows have target's harvest entity in harvest_id but
      -- target_kami_id is NULL; victims show no terminating action of their own.
      -- Cross-reference open harvest_id against any recent SUCCESSFUL kill's
      -- harvest_id. status=1 only — reverted attempts (status=0, e.g. cooldown-
      -- lock) keep the harvest open. harvest entity IDs are recycled across
      -- kill+revive+restart cycles, so also require kill_ts > open start_ts.
      SELECT harvest_id, MAX(block_timestamp) AS last_kill_ts
      FROM kami_action
      WHERE action_type='harvest_liquidate'
        AND status=1
        AND block_timestamp >= NOW() - INTERVAL 24 HOUR
        AND harvest_id IS NOT NULL
      GROUP BY harvest_id
    ),
    feeds AS (
      SELECT kami_id, COUNT(*) AS n_feeds, MAX(block_timestamp) AS last_feed
      FROM kami_action f
      WHERE f.action_type='feed'
        AND f.block_timestamp >= (SELECT MIN(start_ts) FROM hs_open)
      GROUP BY kami_id
    )
    SELECT
      hs.kami_id, hs.start_ts, hs.harvest_id,
      ks.kami_index, ks.name, ks.account_name, ks.account_id, ks.level,
      ks.total_health, ks.base_health, ks.total_power, ks.total_violence, ks.total_harmony,
      ks.body_affinity, ks.hand_affinity,
      ks.strain_boost, ks.harvest_intensity_boost,
      ks.harvest_fertility_boost, ks.harvest_bounty_boost,
      ks.defense_threshold_shift, ks.defense_threshold_ratio,
      EXTRACT(EPOCH FROM (NOW() - hs.start_ts)) AS elapsed_sec,
      COALESCE(fd.n_feeds, 0) AS n_feeds_after_start
    FROM hs_open hs
    JOIN kami_static ks ON ks.kami_id=hs.kami_id
    LEFT JOIN feeds fd ON fd.kami_id=hs.kami_id AND fd.last_feed >= hs.start_ts
    WHERE NOT EXISTS (
      SELECT 1 FROM killed_harvests kh
      WHERE kh.harvest_id = hs.harvest_id
        AND kh.last_kill_ts > hs.start_ts
    )
    """
    rows = oracle_sql(sql, limit=4000)
    node_aff = node_meta["affinities"]

    candidates = []
    for r in rows:
        acct = (r.get("account_name") or "").lower()
        acc_id = str(r.get("account_id") or "")
        guild_blocked = acct in handles or acc_id in accs
        no_touch = acct in SOFT_NO_TOUCH_OWNERS
        fed = (r.get("n_feeds_after_start") or 0) > 0
        elapsed = int(r.get("elapsed_sec") or 0)
        if elapsed < 60:
            continue  # not enough strain; skip noise

        v_total_hp = int(r.get("total_health") or 0)
        v_base_hp = int(r.get("base_health") or 0)
        proj = compute_current_hp(
            state="HARVESTING",
            sync_hp=v_total_hp,
            base_hp=v_base_hp,
            shift_hp=v_total_hp - v_base_hp,
            boost_hp=0, last_action_ts=0, now_ts=elapsed, harvest_start_ts=0,
            power=int(r.get("total_power") or 0),
            violence=int(r.get("total_violence") or 0),
            harmony=int(r.get("total_harmony") or 0),
            body_affinity=(r.get("body_affinity") or "NORMAL"),
            hand_affinity=(r.get("hand_affinity") or "NORMAL"),
            node_affinities=node_aff,
            strain_boost=int(r.get("strain_boost") or 0),
            bounty_boost=int(r.get("harvest_bounty_boost") or 0),
            fertility_boost=int(r.get("harvest_fertility_boost") or 0),
            intensity_boost_pct=int(r.get("harvest_intensity_boost") or 0),
        )
        proj_hp = proj.projected_hp

        best = None
        for s in STRIKERS:
            kt = kill_threshold(
                attacker_violence=s["V"],
                victim_harmony=int(r.get("total_harmony") or 1),
                victim_max_hp=v_total_hp,
                atk_threshold_shift=s["atk_s"],
                atk_threshold_ratio=s["atk_r"],
                def_threshold_shift=int(r.get("defense_threshold_shift") or 0),
                def_threshold_ratio=int(r.get("defense_threshold_ratio") or 0),
                attacker_hand=s["hand"],
                victim_body=(r.get("body_affinity") or "NORMAL"),
            )
            margin = kt["kill_zone"] - proj_hp
            if best is None or margin > best["margin"]:
                best = {
                    "striker_idx": s["idx"],
                    "kill_zone": float(kt["kill_zone"]),
                    "margin": float(margin),
                    "efficacy": float(kt["efficacy"]),
                }

        candidates.append({
            "v_idx": int(r.get("kami_index")) if r.get("kami_index") else None,
            "v_acct": r.get("account_name"),
            "v_lv": int(r.get("level") or 0),
            "v_V": int(r.get("total_violence") or 0),
            "v_H": int(r.get("total_harmony") or 0),
            "v_strain_boost": int(r.get("strain_boost") or 0),
            "v_HP": v_total_hp,
            "v_body": r.get("body_affinity"),
            "v_hand": r.get("hand_affinity"),
            "v_dts": int(r.get("defense_threshold_shift") or 0),
            "v_dtr": int(r.get("defense_threshold_ratio") or 0),
            "elapsed_h": round(elapsed / 3600, 2),
            "elapsed_sec": elapsed,
            "proj_hp": round(proj_hp, 1),
            "node_id": node_id,
            "guild_blocked": guild_blocked,
            "no_touch_owner": no_touch,
            "fresh_feed_since_start": fed,
            **best,
        })

    candidates.sort(key=lambda x: x["margin"], reverse=True)
    return candidates


def owner_heat_check(owners):
    """For each owner, compute heat-check signals used by Plan-104 P0 v2 +
    Plan-111 P0 sync-stop burst detector:
      - minutes_idle: minutes since last action
      - distinct_kamis_5min: how many distinct kamis acted in the past 5 min
      - distinct_kamis_60min: ditto past 60 min
      - bulk_stop_windows_6h: count of 1-second windows with >=5 kamis
        starting or stopping a harvest
      - sync_stop_bursts_6h: count of clusters where 3+ harvest_stops fall
        inside a 5-second window (Aenne automation signature, session 110)
      - sync_feed_bursts_6h: count of clusters where 3+ feeds fall inside
        a 5-second window (vuongdung1198 sync-heal signature, session 115:
        15 kamis fed via item 11001 in 15s after 14-kill cumulative pressure)
      - anti_predator_automation: True if sync_stop_bursts_6h >= 1
        OR sync_feed_bursts_6h >= 1

    Returns: { owner_lower: {…, anti_predator_automation: bool} }
    Defensive cycle = blacklist if ANY:
      - minutes_idle < 10 AND distinct_kamis_5min >= 3
      - bulk_stop_windows_6h >= 3
      - anti_predator_automation == True (sync_stop OR sync_feed bursts)
      - owner == 'stefan97' AND minutes_idle < 240 (4h)
    """
    if not owners:
        return {}
    quoted = ",".join(f"'{o}'" for o in sorted(set(owners)))
    # NOTE: lowercase compare on both sides — owners are normalized to
    # lowercase upstream but oracle stores names with original case
    # (e.g. 'Aenne'), so a strict-equality filter would silently miss them.
    sql = f"""
    WITH a AS (
      SELECT LOWER(ks.account_name) AS owner, a.action_type, a.kami_id, a.block_timestamp
      FROM kami_action a
      JOIN kami_static ks ON a.kami_id = ks.kami_id
      WHERE LOWER(ks.account_name) IN ({quoted})
        AND a.block_timestamp >= NOW() - INTERVAL 6 HOUR
    ),
    bulk AS (
      SELECT owner, date_trunc('second', block_timestamp) AS sec,
             COUNT(DISTINCT kami_id) AS n_kamis
      FROM a
      WHERE action_type IN ('harvest_start','harvest_stop')
      GROUP BY 1, 2
      HAVING n_kamis >= 5
    ),
    -- Sync-stop burst detector (Plan-111 P0, tightened session 111):
    -- count clusters where 3+ distinct kamis are harvest_stop'd by the
    -- same owner within a 5-second window. The Aenne automation pattern
    -- is sub-second (span_sec=0.0); a 60s window incidentally caught
    -- normal manual cycling (3 stops over 59s). 5s threshold cleanly
    -- isolates atomic-batch automation.
    stops AS (
      SELECT owner, kami_id, block_timestamp AS ts
      FROM a
      WHERE action_type = 'harvest_stop'
    ),
    burst_windows AS (
      SELECT s1.owner, s1.ts AS anchor_ts,
             COUNT(DISTINCT s2.kami_id) AS n_kamis_in_window
      FROM stops s1
      JOIN stops s2
        ON s1.owner = s2.owner
       AND s2.ts BETWEEN s1.ts AND s1.ts + INTERVAL 5 SECOND
      GROUP BY s1.owner, s1.ts
      HAVING COUNT(DISTINCT s2.kami_id) >= 3
    ),
    -- Collapse overlapping anchors: keep only anchors that are NOT within
    -- 5s of an earlier anchor (gap-based island detection).
    burst_islands AS (
      SELECT owner, anchor_ts,
             LAG(anchor_ts) OVER (PARTITION BY owner ORDER BY anchor_ts) AS prev_anchor
      FROM burst_windows
    ),
    burst_count AS (
      SELECT owner, COUNT(*) AS sync_stop_bursts_6h
      FROM burst_islands
      WHERE prev_anchor IS NULL
         OR anchor_ts > prev_anchor + INTERVAL 5 SECOND
      GROUP BY owner
    ),
    -- Sync-feed burst detector (Plan-115 P0, session 115):
    -- vuongdung1198 fed 15 kamis in 15s using item 11001 after 14-kill
    -- cumulative pressure. Same atomic-batch signature as sync-stop, but
    -- the defensive primitive is mass-healing, not mass-stopping.
    feeds AS (
      SELECT owner, kami_id, block_timestamp AS ts
      FROM a
      WHERE action_type = 'feed'
    ),
    feed_burst_windows AS (
      SELECT f1.owner, f1.ts AS anchor_ts,
             COUNT(DISTINCT f2.kami_id) AS n_kamis_in_window
      FROM feeds f1
      JOIN feeds f2
        ON f1.owner = f2.owner
       AND f2.ts BETWEEN f1.ts AND f1.ts + INTERVAL 5 SECOND
      GROUP BY f1.owner, f1.ts
      HAVING COUNT(DISTINCT f2.kami_id) >= 3
    ),
    feed_burst_islands AS (
      SELECT owner, anchor_ts,
             LAG(anchor_ts) OVER (PARTITION BY owner ORDER BY anchor_ts) AS prev_anchor
      FROM feed_burst_windows
    ),
    feed_burst_count AS (
      SELECT owner, COUNT(*) AS sync_feed_bursts_6h
      FROM feed_burst_islands
      WHERE prev_anchor IS NULL
         OR anchor_ts > prev_anchor + INTERVAL 5 SECOND
      GROUP BY owner
    )
    SELECT
      a.owner,
      MAX(a.block_timestamp) AS last_action,
      EXTRACT(EPOCH FROM (NOW() - MAX(a.block_timestamp)))/60.0 AS minutes_idle,
      COUNT(DISTINCT CASE WHEN a.block_timestamp >= NOW() - INTERVAL 5 MINUTE
                          THEN a.kami_id END) AS distinct_kamis_5min,
      COUNT(DISTINCT CASE WHEN a.block_timestamp >= NOW() - INTERVAL 60 MINUTE
                          THEN a.kami_id END) AS distinct_kamis_60min,
      (SELECT COUNT(*) FROM bulk b WHERE b.owner = a.owner) AS bulk_stop_windows_6h,
      COALESCE((SELECT sync_stop_bursts_6h FROM burst_count bc WHERE bc.owner = a.owner), 0)
        AS sync_stop_bursts_6h,
      COALESCE((SELECT sync_feed_bursts_6h FROM feed_burst_count fbc WHERE fbc.owner = a.owner), 0)
        AS sync_feed_bursts_6h
    FROM a
    GROUP BY a.owner
    """
    rows = oracle_sql(sql, limit=500)
    out = {}
    for r in rows:
        owner_lower = (r.get("owner") or "").lower()
        minutes_idle = float(r.get("minutes_idle") or 9999)
        distinct_5 = int(r.get("distinct_kamis_5min") or 0)
        distinct_60 = int(r.get("distinct_kamis_60min") or 0)
        bulk_6h = int(r.get("bulk_stop_windows_6h") or 0)
        sync_bursts = int(r.get("sync_stop_bursts_6h") or 0)
        sync_feed_bursts = int(r.get("sync_feed_bursts_6h") or 0)
        anti_predator = sync_bursts >= 1 or sync_feed_bursts >= 1

        defensive = False
        reasons = []
        if minutes_idle < 10 and distinct_5 >= 3:
            defensive = True
            reasons.append(f"sync_active(idle={minutes_idle:.1f}min,kamis_5min={distinct_5})")
        if bulk_6h >= 3:
            defensive = True
            reasons.append(f"bulk_stop_x{bulk_6h}_in_6h")
        if sync_bursts >= 1:
            defensive = True
            reasons.append(f"sync_stop_bursts(x{sync_bursts})")
        if sync_feed_bursts >= 1:
            defensive = True
            reasons.append(f"sync_feed_bursts(x{sync_feed_bursts})")
        if owner_lower == "stefan97" and minutes_idle < 240:
            defensive = True
            reasons.append(f"stefan97_idle_lt_4h({minutes_idle:.0f}min)")

        out[owner_lower] = {
            "minutes_idle": round(minutes_idle, 1),
            "distinct_kamis_5min": distinct_5,
            "distinct_kamis_60min": distinct_60,
            "bulk_stop_windows_6h": bulk_6h,
            "sync_stop_bursts_6h": sync_bursts,
            "sync_feed_bursts_6h": sync_feed_bursts,
            "anti_predator_automation": anti_predator,
            "defensive_cycle": defensive,
            "defensive_reasons": reasons,
        }
    return out


def discover_active_nodes():
    """Replace the hardcoded HOT_NODES with a dynamic merge of FLOOR_NODES
    and any node with harvest_start activity in the last ACTIVITY_WINDOW_HOURS.

    Round 1.5 (2026-05-03): static HOT_NODES went blind to Sacrarium / acheron
    despite that node having 23 harvest_starts in 24h; dynamic discovery makes
    the watcher self-correcting.

    Returns FLOOR_NODES on oracle failure so the watcher always produces a
    snapshot.
    """
    try:
        rows = oracle_sql(
            "SELECT node_id, COUNT(DISTINCT kami_id) AS harvesters "
            "FROM kami_action "
            "WHERE action_type='harvest_start' "
            f"  AND block_timestamp > NOW() - INTERVAL {ACTIVITY_WINDOW_HOURS} HOUR "
            "GROUP BY node_id "
            "ORDER BY harvesters DESC",
            limit=200,
        )
        active = []
        for r in rows:
            nid = r.get("node_id")
            if nid is None:
                continue
            try:
                active.append(int(nid))
            except (TypeError, ValueError):
                continue
    except Exception as e:
        print(f"discover_active_nodes oracle error: {e}; falling back to FLOOR_NODES", file=sys.stderr)
        return list(FLOOR_NODES)
    # Merge: FLOOR_NODES first (so they always appear), then active not already in floor.
    merged = list(FLOOR_NODES) + [n for n in active if n not in FLOOR_NODES]
    return merged[:MAX_ACTIVE_NODES]


def get_hot_battlegrounds(window_hours=3, top_n=20):
    """Recent liquidations world-wide, grouped by node, with attacker /
    victim attribution. Surfaces clusters where OTHER predators are succeeding
    so we can follow the heat instead of grinding our own cluster.

    Recovers node_id via self-join to harvest_start (harvest_liquidate.node_id
    is NULL — see ideas_to_founder.md item 4b). Returns [] on oracle failure.
    """
    sql = (
        "WITH liq AS ("
        "  SELECT harvest_id "
        "  FROM kami_action "
        f"  WHERE action_type='harvest_liquidate' AND harvest_id IS NOT NULL "
        f"    AND block_timestamp > NOW() - INTERVAL {window_hours} HOUR"
        "), "
        "start_ranked AS ("
        "  SELECT h.harvest_id, h.node_id, h.kami_id, "
        "    ROW_NUMBER() OVER (PARTITION BY h.harvest_id ORDER BY h.block_timestamp DESC) AS rn "
        "  FROM kami_action h "
        "  WHERE h.action_type='harvest_start' "
        "    AND h.harvest_id IN (SELECT harvest_id FROM liq)"
        "), "
        "start_resolved AS ("
        "  SELECT s.harvest_id, s.node_id, ks.account_name AS victim_account "
        "  FROM start_ranked s "
        "  LEFT JOIN kami_static ks ON ks.kami_id = s.kami_id "
        "  WHERE s.rn = 1"
        ") "
        "SELECT sr.node_id, "
        "  COUNT(*) AS kills, "
        "  COUNT(DISTINCT sr.victim_account) AS distinct_victims, "
        "  MAX(sr.victim_account) AS sample_victim "
        "FROM liq l "
        "JOIN start_resolved sr ON sr.harvest_id = l.harvest_id "
        "WHERE sr.node_id IS NOT NULL "
        "GROUP BY sr.node_id "
        "ORDER BY kills DESC "
        f"LIMIT {top_n}"
    )
    try:
        rows = oracle_sql(sql, limit=top_n)
    except Exception as e:
        print(f"get_hot_battlegrounds oracle error: {e}", file=sys.stderr)
        return []
    out = []
    for r in rows:
        nid = r.get("node_id")
        if nid is None:
            continue
        try:
            out.append({
                "node_id": int(nid),
                "kills_in_window": int(r.get("kills") or 0),
                "distinct_victims": int(r.get("distinct_victims") or 0),
                "sample_victim": r.get("sample_victim"),
                "window_hours": window_hours,
            })
        except (TypeError, ValueError):
            continue
    return out


def main():
    t0 = time.time()
    handles, accs = load_guild()
    # Round 1.5: dynamic node discovery replaces static HOT_NODES.
    global HOT_NODES
    HOT_NODES = discover_active_nodes()
    node_meta = get_node_affinities()

    by_node = {}
    all_candidates = []
    for node_id in HOT_NODES:
        if node_id not in node_meta:
            continue
        cands = scan_node(node_id, node_meta[node_id], handles, accs)
        by_node[node_id] = {
            "room": node_meta[node_id]["room"],
            "name": node_meta[node_id]["name"],
            "affinities": node_meta[node_id]["affinities"],
            "total_scanned": len(cands),
            "killable_count": sum(1 for c in cands if c["margin"] >= 5
                                  and not c["guild_blocked"]
                                  and not c["no_touch_owner"]
                                  and not c["fresh_feed_since_start"]),
            "top10": cands[:10],
        }
        all_candidates.extend(cands)

    # Heat-check pass: gather signals for every owner present in the candidate
    # pool plus a fixed watch list of known-suspect owners (so their
    # automation status is visible even when they have no HARVESTING
    # candidates at scan time).
    owners_in_pool = {(c["v_acct"] or "").lower() for c in all_candidates if c["v_acct"]}
    heat = owner_heat_check(owners_in_pool | ANTI_PREDATOR_WATCH)
    for c in all_candidates:
        owner_lower = (c.get("v_acct") or "").lower()
        h = heat.get(owner_lower)
        c["heat"] = h or {
            "minutes_idle": None,
            "distinct_kamis_5min": 0,
            "distinct_kamis_60min": 0,
            "bulk_stop_windows_6h": 0,
            "defensive_cycle": False,
            "defensive_reasons": [],
        }

    # Filter to clean killable list (margin >= +5, no guild, no no-touch, no feed).
    killable = [c for c in all_candidates
                if c["margin"] >= 5
                and not c["guild_blocked"]
                and not c["no_touch_owner"]
                and not c["fresh_feed_since_start"]]
    killable.sort(key=lambda x: x["margin"], reverse=True)

    # killable_v2: heat-check filtered. Removes defensive-cycle owners.
    killable_v2 = [c for c in killable if not c["heat"].get("defensive_cycle")]

    # Round 1.5: competitor-predator activity feed. Where are OTHER hunters
    # succeeding right now? Independent signal from where harvesters happen
    # to be in our HOT_NODES.
    hot_battlegrounds = get_hot_battlegrounds(window_hours=3, top_n=20)

    out = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scan_duration_sec": round(time.time() - t0, 2),
        "hot_nodes": HOT_NODES,
        "hot_nodes_source": "dynamic_discovery_v1",
        "floor_nodes": FLOOR_NODES,
        "guild_blacklist_size": len(handles) + len(accs),
        "by_node": by_node,
        "hot_battlegrounds": hot_battlegrounds,
        "killable_clean": killable[:50],  # top 50 across all nodes (legacy field)
        "killable_v2": killable_v2[:50],  # heat-check filtered (defensive owners removed)
        "owner_heat": heat,  # per-owner heat-check signals
    }

    tmp_path = OUTPUT_PATH.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(out, indent=2))
    tmp_path.rename(OUTPUT_PATH)

    n_killable = len(killable)
    n_v2 = len(killable_v2)
    n_defensive_owners = sum(1 for h in heat.values() if h.get("defensive_cycle"))
    n_battlegrounds = len(hot_battlegrounds)
    print(f"world_targets.json refreshed: {n_killable} killable ({n_v2} after heat-check), {n_defensive_owners} defensive owners, {n_battlegrounds} hot battlegrounds, across {len(HOT_NODES)} nodes in {out['scan_duration_sec']}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
