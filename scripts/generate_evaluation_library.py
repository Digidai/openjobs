#!/usr/bin/env python3
"""Generate the static AI recruiting evaluation library."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "evaluation-library.json"


def render_outputs() -> dict[Path, str]:
    """Return every generated artifact without writing it."""

    return {}


def main() -> int:
    """Write outputs or compare them when --check is supplied."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = render_outputs()

    if args.check:
        stale = [path for path, expected in outputs.items() if not path.exists() or path.read_text(encoding="utf-8") != expected]
        if stale:
            for path in stale:
                print(f"ERROR: stale generated output: {path.relative_to(ROOT)}")
            return 1
        print("OK: evaluation library outputs are current")
        return 0

    for path, rendered in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
