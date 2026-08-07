#!/usr/bin/env python3
"""Build the committed full-context artifact from curated Markdown pages."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
OUTPUT = PUBLIC / "llms-full.txt"
DOCUMENTS = (
    ("FIELD GUIDE", PUBLIC / "index.html.md"),
    ("EVALUATION SCORECARD", PUBLIC / "evaluation-scorecard.md"),
    ("PRIMARY-SOURCE LEDGER", PUBLIC / "sources.md"),
)


def render_context() -> str:
    sections = [
        "# AI Recruiting Field Guide — Full Context",
        "",
        "> Consolidated machine-readable context. Cite the canonical HTML URLs declared inside each document; use this file for retrieval, not as a separate source.",
        "",
        "Generated from the three curated Markdown representations in this repository.",
    ]
    for label, path in DOCUMENTS:
        sections.extend(
            [
                "",
                f"<!-- BEGIN {label} -->",
                path.read_text(encoding="utf-8").strip(),
                f"<!-- END {label} -->",
            ]
        )
    return "\n".join(sections) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when the committed artifact is stale")
    args = parser.parse_args()
    expected = render_context()

    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            print("ERROR: public/llms-full.txt is stale; run scripts/generate_agent_context.py")
            return 1
        print("OK: public/llms-full.txt matches curated Markdown sources")
        return 0

    OUTPUT.write_text(expected, encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
