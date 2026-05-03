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

# Hot-list nodes to scan. Update via CLI flag or expand here.
# Note: nodes the operator can travel to + currently-hunting clusters.
HOT_NODES = [86, 60, 73, 25, 62, 9, 30, 82]

# bpeon's striker roster (kept here for tactical-decision speed; refresh on respec).
STRIKERS = [
    {"idx": 12649, "V": 34, "H": 12, "max_hp": 170, "hand": "NORMAL", "atk_s": 300, "atk_r": 500},
    {"idx": 11224, "V": 36, "H": 11, "max_hp": 140, "hand": "EERIE",  "atk_s": 280, "atk_r": 500},
    {"idx": 10705, "V": 32, "H": 19, "max_hp": 240, "hand": "INSECT", "atk_s": 280, "atk_r": 250},
    {"idx": 6058,  "V": 31, "H": 18, "max_hp": 200, "hand": "SCRAP",  "atk_s": 280, "atk_r": 250},
    {"idx": 15540, "V": 31, "H": 21, "max_hp": 190, "hand": "NORMAL", "atk_s": 280, "atk_r": 250},
    {"idx": 12225, "V": 30, "H": 19, "max_hp": 220, "hand": "NORMAL", "atk_s": 260, "atk_r": 250},
]

# rtvvvvv was added to the no-touch list in session 80 (3 reverts in a row).
# Soft no-touch: not guild, but defended too well to chase.
SOFT_NO_TOUCH_OWNERS = {"rtvvvvv"}


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
      -- Cross-reference open harvest_id against any recent kill's harvest_id.
      SELECT DISTINCT harvest_id
      FROM kami_action
      WHERE action_type='harvest_liquidate'
        AND block_timestamp >= NOW() - INTERVAL 24 HOUR
        AND harvest_id IS NOT NULL
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
    WHERE hs.harvest_id NOT IN (SELECT harvest_id FROM killed_harvests)
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


def main():
    t0 = time.time()
    handles, accs = load_guild()
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

    # Filter to clean killable list (margin >= +5, no guild, no no-touch, no feed).
    killable = [c for c in all_candidates
                if c["margin"] >= 5
                and not c["guild_blocked"]
                and not c["no_touch_owner"]
                and not c["fresh_feed_since_start"]]
    killable.sort(key=lambda x: x["margin"], reverse=True)

    out = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scan_duration_sec": round(time.time() - t0, 2),
        "hot_nodes": HOT_NODES,
        "guild_blacklist_size": len(handles) + len(accs),
        "by_node": by_node,
        "killable_clean": killable[:50],  # top 50 across all nodes
    }

    tmp_path = OUTPUT_PATH.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(out, indent=2))
    tmp_path.rename(OUTPUT_PATH)

    n_killable = len(killable)
    print(f"world_targets.json refreshed: {n_killable} killable across {len(HOT_NODES)} nodes in {out['scan_duration_sec']}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
