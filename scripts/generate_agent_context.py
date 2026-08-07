#!/usr/bin/env python3
"""Build committed agent context and the structured AI resource index."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
CONTENT = ROOT / "content" / "evaluation-library.json"
OUTPUT = PUBLIC / "llms-full.txt"
AI_INDEX = PUBLIC / "ai-index.json"
BASE = "https://openjobs.genedai.me"
DOCUMENTS = (
    ("FIELD GUIDE", PUBLIC / "index.html.md"),
    ("EVALUATION METHODOLOGY", PUBLIC / "methodology.md"),
    ("VENDOR CHECKLIST", PUBLIC / "vendor-checklist.md"),
    ("PILOT DESIGN", PUBLIC / "pilot-design.md"),
    ("SOURCING EVALUATION", PUBLIC / "sourcing-evaluation.md"),
    ("SCREENING EVALUATION", PUBLIC / "screening-evaluation.md"),
    ("AGENT RELIABILITY", PUBLIC / "agent-reliability.md"),
    ("EVALUATION SCORECARD", PUBLIC / "evaluation-scorecard.md"),
    ("PRIMARY-SOURCE LEDGER", PUBLIC / "sources.md"),
)


def load_library() -> dict:
    return json.loads(CONTENT.read_text(encoding="utf-8"))


def render_context() -> str:
    sections = [
        "# AI Recruiting Evaluation Library: Full Context",
        "",
        "> Consolidated machine-readable context. Cite the canonical HTML URL declared inside each document. Use this file for retrieval rather than as a separate source.",
        "",
        "Generated from the nine curated Markdown representations in this repository.",
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


def render_ai_index() -> str:
    data = load_library()
    page_overrides = {
        "field-guide": {
            "title": "The AI Recruiting Field Guide",
            "canonical_url": f"{BASE}/",
            "markdown_url": f"{BASE}/index.html.md",
            "summary": "Library directory and decision framework covering hiring outcomes, evidence, human control, contextual risk, and reversible pilots.",
            "topics": ["AI recruiting", "hiring outcomes", "human control", "pilot design"],
            "downloads": [],
        },
        "evaluation-scorecard": {
            "title": "AI Recruiting Evaluation Scorecard",
            "canonical_url": f"{BASE}/evaluation-scorecard",
            "markdown_url": f"{BASE}/evaluation-scorecard.md",
            "summary": "Eight dimensions scored from zero to three, with stop, narrow-pilot, and real-role-validation interpretations.",
            "topics": ["evaluation rubric", "evidence", "candidate experience", "auditability"],
            "downloads": [],
        },
        "primary-source-ledger": {
            "title": "AI Recruiting Source and Evidence Ledger",
            "canonical_url": f"{BASE}/sources",
            "markdown_url": f"{BASE}/sources.md",
            "summary": "Eighteen annotated public and first-party sources with jurisdiction, review date, supported use, and evidence limits.",
            "topics": ["source provenance", "employment selection", "accessibility", "AI governance"],
            "downloads": [f"{BASE}/downloads/ai-recruiting-evidence-register.csv"],
        },
    }
    pages = []
    pages.append({"id": "field-guide", **page_overrides["field-guide"]})
    for page in data["pages"]:
        pages.append(
            {
                "id": page["slug"],
                "title": page["title"],
                "canonical_url": f"{BASE}/{page['slug']}",
                "markdown_url": f"{BASE}/{page['slug']}.md",
                "summary": page["summary"],
                "topics": list(dict.fromkeys([page["primary_query"], "AI recruiting evaluation"])),
                "downloads": [f"{BASE}{download['href']}" for download in page["downloads"]],
            }
        )
    pages.extend(
        [
            {"id": "evaluation-scorecard", **page_overrides["evaluation-scorecard"]},
            {"id": "primary-source-ledger", **page_overrides["primary-source-ledger"]},
        ]
    )

    download_descriptions: dict[str, dict] = {}
    for page in data["pages"]:
        for download in page["downloads"]:
            download_descriptions.setdefault(download["href"], download)
    download_descriptions.setdefault(
        "/downloads/ai-recruiting-pilot-template.csv",
        {
            "title": "Pilot measurement template",
            "description": "Metric definitions plus blank baseline, target, result, and notes fields.",
            "href": "/downloads/ai-recruiting-pilot-template.csv",
            "format": "text/csv",
        },
    )
    downloads = [
        {
            "id": Path(path).stem,
            "title": item["title"],
            "url": f"{BASE}{path}",
            "media_type": item["format"],
            "description": item["description"],
            "license": data["license"],
        }
        for path, item in sorted(download_descriptions.items())
    ]

    payload = {
        "$schema": f"{BASE}/ai-index.schema.json",
        "schema_version": "1.1",
        "canonical_site": f"{BASE}/",
        "name": "AI Recruiting Evaluation Library",
        "description": "A source-backed library for evaluating AI recruiting systems, vendors, pilots, sourcing, screening, and agent reliability.",
        "language": "en",
        "last_substantive_review": data["last_substantive_review"],
        "preferred_entrypoints": {
            "discovery": f"{BASE}/llms.txt",
            "full_context": f"{BASE}/llms-full.txt",
            "structured_index": f"{BASE}/ai-index.json",
        },
        "citation_guidance": "Cite canonical_url for claims from this site. Use markdown_url to load page context. Preserve each source's type, jurisdiction, and evidence limit. Label Metix material as first-party research.",
        "limitations": [
            "The library is not legal advice or a compliance determination.",
            "A score does not prove fairness, effectiveness, or business value.",
            "First-party Metix research is not independent validation.",
            "Retired OpenJobs job-board content must not be used to infer current product capabilities.",
        ],
        "access_policy": {
            "robots": f"{BASE}/robots.txt",
            "search_and_retrieval": "allowed",
            "model_development": "allowed",
        },
        "entities": [
            {
                "name": "Metix AI",
                "url": "https://metix.ai/",
                "relationship": "Current customer-facing product and brand; formerly OpenJobs AI.",
            },
            {
                "name": "OpenJobs Archive",
                "url": f"{BASE}/",
                "relationship": "Source-backed evaluation resource maintained in the Digidai/openjobs repository.",
            },
        ],
        "pages": pages,
        "downloads": downloads,
        "sources": [
            {
                "id": source["id"],
                "organization": source["organization"],
                "title": source["title"],
                "url": source["url"],
                "source_type": source["source_type"],
                "jurisdiction": source["jurisdiction"],
                "last_checked": source["last_checked"],
                "supports": source["supports"],
                "does_not_prove": source["limitation"],
            }
            for source in data["sources"]
        ],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail when a committed artifact is stale")
    args = parser.parse_args()
    expected = {OUTPUT: render_context(), AI_INDEX: render_ai_index()}

    if args.check:
        stale = [path for path, rendered in expected.items() if not path.exists() or path.read_text(encoding="utf-8") != rendered]
        if stale:
            for path in stale:
                print(f"ERROR: {path.relative_to(ROOT)} is stale; run scripts/generate_agent_context.py")
            return 1
        print("OK: agent context and AI index match curated sources")
        return 0

    for path, rendered in expected.items():
        path.write_text(rendered, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
