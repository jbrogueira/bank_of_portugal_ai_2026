#!/usr/bin/env python3
"""PreToolUse hook: log every Read of a file under data/raw/.

Reads the hook payload from stdin (JSON), and if the Read targets a path
inside data/raw/, appends a timestamped line to logs/data_raw_access.log.

Exits 0 unconditionally so it never blocks the read — it only records.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # malformed payload: never block the tool

    file_path = payload.get("tool_input", {}).get("file_path")
    if not file_path:
        return 0

    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
    raw_dir = project_dir / "data" / "raw"

    try:
        target = Path(file_path).resolve()
        target.relative_to(raw_dir)  # raises ValueError if not under data/raw/
    except ValueError:
        return 0  # not a data/raw read — ignore

    log_path = project_dir / "logs" / "data_raw_access.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rel = target.relative_to(project_dir)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp}\tRead\t{rel}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
