#!/usr/bin/env python3
"""Fetch Discord liquidation alerts and append to predator/world-liquidations.jsonl.

Read-only feed for kami-zero self-audit. Runs on cron every 10 min.
Token from ~/kami-zero/.env (DISCORD_AUTH_TOKEN). Cursor in
predator/.discord-liq-cursor (snowflake ID; 48h lookback on first run).

Output schema (one JSON object per line, append-only):
  {"ts","msg_id","victim_kami","victim_account","node_name","node_id",
   "attacker_kami","attacker_account","musu","is_self"}
"""
import json
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path("/home/anatolyzaytsev/kami-zero")
ENV_FILE = REPO / ".env"
CURSOR_FILE = REPO / "predator" / ".discord-liq-cursor"
OUTPUT = REPO / "predator" / "world-liquidations.jsonl"
NODES_CSV = REPO / "catalogs" / "nodes.csv"
SELF_ACCOUNT = "bpeon"
CHANNEL_ID = "1379106475082780825"
DISCORD_EPOCH = 1420070400000
LOOKBACK_HOURS = 48

ALERT_RE = re.compile(
    r"\*\*(?P<victim_kami>.+?)\*\*, belonging to \*\*(?P<victim_account>.+?)\*\* was just liquidated at "
    r"\*\*(?P<node_name>.+?)\*\* by \*\*(?P<attacker_kami>.+?)\*\*, under the control of \*\*(?P<attacker_account>.+?)\*\*!"
    r".*?The kill was worth \*\*(?P<musu>\d+)\*\* Musu",
    re.DOTALL,
)


def load_token():
    if not ENV_FILE.exists():
        print(f"ERROR: {ENV_FILE} missing — create with DISCORD_AUTH_TOKEN=<token>", file=sys.stderr)
        sys.exit(1)
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line.startswith("DISCORD_AUTH_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    print("ERROR: DISCORD_AUTH_TOKEN not in .env", file=sys.stderr)
    sys.exit(1)


def load_node_lookup():
    out = {}
    if not NODES_CSV.exists():
        return out
    text = NODES_CSV.read_text()
    for i, line in enumerate(text.splitlines()):
        if i == 0 or not line.strip():
            continue
        parts = line.split(",")
        if len(parts) >= 2:
            try:
                nid = int(parts[0])
                name = parts[1].strip().strip('"')
                out[name.lower()] = nid
            except (ValueError, IndexError):
                continue
    return out


def snowflake_for_hours_ago(hours):
    past_ms = int((datetime.now(timezone.utc) - timedelta(hours=hours)).timestamp() * 1000)
    return (past_ms - DISCORD_EPOCH) << 22


def load_cursor():
    if CURSOR_FILE.exists():
        s = CURSOR_FILE.read_text().strip()
        if s:
            try:
                return int(s)
            except ValueError:
                pass
    return snowflake_for_hours_ago(LOOKBACK_HOURS)


def save_cursor(message_id):
    CURSOR_FILE.parent.mkdir(parents=True, exist_ok=True)
    CURSOR_FILE.write_text(str(message_id))


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def fetch_batch(token, after_id):
    url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages?limit=100&after={after_id}"
    req = urllib.request.Request(url, headers={
        "Authorization": token,
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://discord.com/channels/@me",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode()[:300]
        except Exception:
            pass
        print(f"HTTP {e.code} from Discord: {body}", file=sys.stderr)
        if e.code == 401:
            print("--> Token invalid or expired. Rotate and update .env.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Discord fetch error: {e}", file=sys.stderr)
        return None


def parse_alert(message, node_lookup):
    content = message.get("content", "") or ""
    if not content and "embeds" in message:
        for e in message["embeds"]:
            content = (e.get("description") or "") + " " + (e.get("title") or "")
            if content.strip():
                break
    m = ALERT_RE.search(content)
    if not m:
        return None
    g = m.groupdict()
    node_name = g["node_name"].strip()
    nid = node_lookup.get(node_name.lower())
    return {
        "ts": message.get("timestamp"),
        "msg_id": message.get("id"),
        "victim_kami": g["victim_kami"].strip(),
        "victim_account": g["victim_account"].strip(),
        "node_name": node_name,
        "node_id": nid,
        "attacker_kami": g["attacker_kami"].strip(),
        "attacker_account": g["attacker_account"].strip(),
        "musu": int(g["musu"]),
        "is_self": g["attacker_account"].strip() == SELF_ACCOUNT,
    }


def main():
    token = load_token()
    node_lookup = load_node_lookup()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    initial_cursor = load_cursor()
    cursor = initial_cursor
    new_max_id = initial_cursor
    new_records = 0
    pages = 0

    while True:
        batch = fetch_batch(token, cursor)
        if batch is None:
            sys.exit(2)
        if not batch:
            break
        batch.reverse()  # Discord returns newest-first; chronological for processing
        records = []
        for msg in batch:
            try:
                mid = int(msg["id"])
            except (KeyError, ValueError):
                continue
            if mid > new_max_id:
                new_max_id = mid
            rec = parse_alert(msg, node_lookup)
            if rec is not None:
                records.append(rec)
        if records:
            with OUTPUT.open("a", encoding="utf-8") as f:
                for r in records:
                    f.write(json.dumps(r) + "\n")
            new_records += len(records)
        cursor = batch[-1]["id"]
        pages += 1
        time.sleep(1)
        if pages > 50:  # safety bound
            print("WARN: paginated past 50 batches; bailing", file=sys.stderr)
            break

    if new_max_id > initial_cursor:
        save_cursor(new_max_id)
    print(f"discord-liq fetch: {new_records} new alerts appended ({pages} pages); cursor={new_max_id}")


if __name__ == "__main__":
    main()
