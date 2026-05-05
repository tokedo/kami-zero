"""Structured anomaly emitter. The executor's only output channel
besides runs.jsonl is this — anomalies are how it tells the optimizer
"I saw something I don't know how to handle."

Anomaly types are open-ended strings; the optimizer filters on `kind`.
Each anomaly is a single JSON line with a stable schema.
"""

import json
import time
from pathlib import Path


def emit(path: Path, kind: str, **payload) -> None:
    record = {
        "ts": int(time.time()),
        "kind": kind,
        **payload,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(record, default=str) + "\n")
