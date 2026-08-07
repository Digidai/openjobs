#!/usr/bin/env python3
"""Fail-closed checks for the static AI Recruiting Field Guide."""

from __future__ import annotations

from html.parser import HTMLParser
import csv
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

from generate_evaluation_library import render_outputs as render_library_outputs
from generate_agent_context import OUTPUT as FULL_CONTEXT, render_context


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

CANONICALS = {
    "index.html": "https://openjobs.genedai.me/",
    "evaluation-scorecard.html": "https://openjobs.genedai.me/evaluation-scorecard",
    "sources.html": "https://openjobs.genedai.me/sources",
    "methodology.html": "https://openjobs.genedai.me/methodology",
    "vendor-checklist.html": "https://openjobs.genedai.me/vendor-checklist",
    "pilot-design.html": "https://openjobs.genedai.me/pilot-design",
    "sourcing-evaluation.html": "https://openjobs.genedai.me/sourcing-evaluation",
    "screening-evaluation.html": "https://openjobs.genedai.me/screening-evaluation",
    "agent-reliability.html": "https://openjobs.genedai.me/agent-reliability",
}

MARKDOWN_REPRESENTATIONS = {
    "index.html": "https://openjobs.genedai.me/index.html.md",
    "evaluation-scorecard.html": "https://openjobs.genedai.me/evaluation-scorecard.md",
    "sources.html": "https://openjobs.genedai.me/sources.md",
    "methodology.html": "https://openjobs.genedai.me/methodology.md",
    "vendor-checklist.html": "https://openjobs.genedai.me/vendor-checklist.md",
    "pilot-design.html": "https://openjobs.genedai.me/pilot-design.md",
    "sourcing-evaluation.html": "https://openjobs.genedai.me/sourcing-evaluation.md",
    "screening-evaluation.html": "https://openjobs.genedai.me/screening-evaluation.md",
    "agent-reliability.html": "https://openjobs.genedai.me/agent-reliability.md",
}

MACHINE_ENDPOINTS = {
    "llms": "https://openjobs.genedai.me/llms.txt",
    "full_context": "https://openjobs.genedai.me/llms-full.txt",
    "index": "https://openjobs.genedai.me/ai-index.json",
    "schema": "https://openjobs.genedai.me/ai-index.schema.json",
}

REQUIRED_FILES = {
    ROOT / "README.md",
    ROOT / "EDITORIAL_POLICY.md",
    ROOT / "_config.yml",
    ROOT / "sitemap.xml",
    ROOT / ".github/workflows/validate-site.yml",
    ROOT / "content/evaluation-library.json",
    ROOT / "scripts/generate_agent_context.py",
    ROOT / "scripts/generate_evaluation_library.py",
    PUBLIC / "index.html",
    PUBLIC / "evaluation-scorecard.html",
    PUBLIC / "sources.html",
    PUBLIC / "methodology.html",
    PUBLIC / "vendor-checklist.html",
    PUBLIC / "pilot-design.html",
    PUBLIC / "sourcing-evaluation.html",
    PUBLIC / "screening-evaluation.html",
    PUBLIC / "agent-reliability.html",
    PUBLIC / "404.html",
    PUBLIC / "assets/site.css",
    PUBLIC / "assets/scorecard.js",
    PUBLIC / "favicon.svg",
    PUBLIC / "og-image.svg",
    PUBLIC / "og-image.png",
    PUBLIC / "manifest.json",
    PUBLIC / "robots.txt",
    PUBLIC / "sitemap.xml",
    PUBLIC / "llms.txt",
    PUBLIC / "llms-full.txt",
    PUBLIC / "index.html.md",
    PUBLIC / "evaluation-scorecard.md",
    PUBLIC / "sources.md",
    PUBLIC / "methodology.md",
    PUBLIC / "vendor-checklist.md",
    PUBLIC / "pilot-design.md",
    PUBLIC / "sourcing-evaluation.md",
    PUBLIC / "screening-evaluation.md",
    PUBLIC / "agent-reliability.md",
    PUBLIC / "downloads/ai-recruiting-vendor-checklist.csv",
    PUBLIC / "downloads/ai-recruiting-pilot-template.csv",
    PUBLIC / "downloads/ai-recruiting-evidence-register.csv",
    PUBLIC / "data/vendor-checklist.json",
    PUBLIC / "data/pilot-metrics.json",
    PUBLIC / "ai-index.json",
    PUBLIC / "ai-index.schema.json",
    PUBLIC / "_headers",
    PUBLIC / "_redirects",
}

RETIRED_FILES = {
    ROOT / "scripts/update_readme.py",
    ROOT / ".github/workflows/update-jobs.yml",
    ROOT / "requirements.txt",
    PUBLIC / "rss.xml",
    PUBLIC / "stats.json",
}

FORBIDDEN_RUNTIME_PATTERNS = {
    "legacy OpenJobs job URL": r"https://(?:www\.)?openjobs-ai\.com/jobs/",
    "legacy OpenJobs XML feed": r"https://(?:www\.)?openjobs-ai\.com/xml/",
    "legacy deep-search URL": r"https://(?:www\.)?openjobs-ai\.com/deepsearch",
    "new disallowed hostname": r"https://openjobs\.metix\.ai",
    "job-list schema": r'"@type"\s*:\s*"JobPosting"',
    "virtual category sitemap": r"\?category=",
    "retired job-list heading": r"Latest Job Openings",
    "retired aggregate CTA": r"Browse All Jobs",
}


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.canonicals: list[str] = []
        self.descriptions: list[str] = []
        self.h1_count = 0
        self.links: list[str] = []
        self.markdown_alternates: list[tuple[str, str]] = []
        self.described_by: list[tuple[str, str]] = []
        self.json_ld: list[str] = []
        self._in_json_ld = False
        self._json_buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag == "a" and attr.get("href"):
            self.links.append(attr["href"] or "")
        rel = set((attr.get("rel") or "").split())
        if tag == "link" and "canonical" in rel and attr.get("href"):
            self.canonicals.append(attr["href"] or "")
        if tag == "link" and "alternate" in rel and attr.get("type") == "text/markdown" and attr.get("href"):
            self.markdown_alternates.append((attr["href"] or "", attr.get("title") or ""))
        if tag == "link" and "describedby" in rel and attr.get("href") and attr.get("type"):
            self.described_by.append((attr["href"] or "", attr["type"] or ""))
        if tag == "meta" and attr.get("name") == "description" and attr.get("content"):
            self.descriptions.append(attr["content"] or "")
        if tag == "script" and attr.get("type") == "application/ld+json":
            self._in_json_ld = True
            self._json_buffer = []

    def handle_data(self, data: str) -> None:
        if self._in_json_ld:
            self._json_buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_json_ld:
            self.json_ld.append("".join(self._json_buffer).strip())
            self._in_json_ld = False
            self._json_buffer = []


def local_target(href: str) -> Path | None:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or href.startswith(("mailto:", "tel:")):
        return None
    path = parsed.path
    if not path:
        return None
    if path == "/":
        return PUBLIC / "index.html"
    if path.startswith("/"):
        candidate = PUBLIC / path.lstrip("/")
    else:
        candidate = PUBLIC / path
    if candidate.is_dir():
        candidate = candidate / "index.html"
    elif not candidate.suffix and candidate.with_suffix(".html").exists():
        candidate = candidate.with_suffix(".html")
    return candidate


def validate_html(
    path: Path,
    canonical: str | None,
    errors: list[str],
    *,
    require_description: bool = True,
    markdown: str | None = None,
) -> DocumentParser:
    parser = DocumentParser()
    text = path.read_text(encoding="utf-8")
    parser.feed(text)

    if parser.h1_count != 1:
        errors.append(f"{path.relative_to(ROOT)}: expected one h1, found {parser.h1_count}")
    if require_description and (
        len(parser.descriptions) != 1 or not 120 <= len(parser.descriptions[0]) <= 170
    ):
        sizes = [len(item) for item in parser.descriptions]
        errors.append(f"{path.relative_to(ROOT)}: meta description must be 120-170 chars, found {sizes}")
    if canonical is not None and parser.canonicals != [canonical]:
        errors.append(f"{path.relative_to(ROOT)}: canonical {parser.canonicals!r}, expected {[canonical]!r}")
    if markdown is not None and parser.markdown_alternates != [(markdown, "Markdown version")]:
        errors.append(f"{path.relative_to(ROOT)}: Markdown alternate does not match {markdown}")
    if markdown is not None:
        expected_described_by = {
            (MACHINE_ENDPOINTS["llms"], "text/plain"),
            (MACHINE_ENDPOINTS["index"], "application/json"),
        }
        if set(parser.described_by) != expected_described_by:
            errors.append(f"{path.relative_to(ROOT)}: machine discovery links are incomplete")
    for block in parser.json_ld:
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON-LD: {exc}")
    for href in parser.links:
        target = local_target(href)
        if target is not None and not target.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken local link {href} -> {target.relative_to(ROOT)}")
    return parser


def validate_markdown(path: Path, canonical: str, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    h1s = [line for line in text.splitlines() if line.startswith("# ")]
    if len(h1s) != 1:
        errors.append(f"{path.relative_to(ROOT)}: expected one Markdown h1, found {len(h1s)}")
    if f"Canonical HTML: {canonical}" not in text:
        errors.append(f"{path.relative_to(ROOT)}: canonical HTML declaration missing")
    if "Last substantive review: 2026-08-07" not in text:
        errors.append(f"{path.relative_to(ROOT)}: substantive review date missing")
    if "<script" in text.lower():
        errors.append(f"{path.relative_to(ROOT)}: Markdown representation contains executable markup")


def main() -> int:
    errors: list[str] = []

    for path in sorted(REQUIRED_FILES):
        if not path.exists():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")
    for path in sorted(RETIRED_FILES):
        if path.exists():
            errors.append(f"retired file still exists: {path.relative_to(ROOT)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    try:
        for path, expected in render_library_outputs().items():
            if path.read_text(encoding="utf-8") != expected:
                errors.append(f"{path.relative_to(ROOT)}: generated evaluation-library output is stale")
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        errors.append(f"evaluation library content is invalid: {exc}")

    try:
        vendor_data = json.loads((PUBLIC / "data/vendor-checklist.json").read_text(encoding="utf-8"))
        pilot_data = json.loads((PUBLIC / "data/pilot-metrics.json").read_text(encoding="utf-8"))
        with (PUBLIC / "downloads/ai-recruiting-vendor-checklist.csv").open(encoding="utf-8", newline="") as handle:
            vendor_rows = list(csv.DictReader(handle))
        with (PUBLIC / "downloads/ai-recruiting-pilot-template.csv").open(encoding="utf-8", newline="") as handle:
            pilot_rows = list(csv.DictReader(handle))
        with (PUBLIC / "downloads/ai-recruiting-evidence-register.csv").open(encoding="utf-8", newline="") as handle:
            evidence_rows = list(csv.DictReader(handle))
        if len(vendor_rows) < 40 or len(vendor_rows) != len(vendor_data.get("items", [])):
            errors.append("vendor checklist CSV and JSON need the same 40+ questions")
        if len(pilot_rows) < 18 or len(pilot_rows) != len(pilot_data.get("items", [])):
            errors.append("pilot template CSV and JSON need the same 18+ metrics")
        if {row.get("family") for row in pilot_rows} != {"quality", "intent", "time", "labor", "candidate-impact", "reliability"}:
            errors.append("pilot template does not cover every required metric family")
        if len(evidence_rows) < 12 or any(not row.get("limitation") for row in evidence_rows):
            errors.append("evidence register needs 12+ sources with explicit limitations")
    except (csv.Error, json.JSONDecodeError) as exc:
        errors.append(f"generated evaluation data is invalid: {exc}")

    all_links: list[str] = []
    runtime_files = [PUBLIC / name for name in CANONICALS]
    runtime_files.extend(
        [
            PUBLIC / "404.html",
            PUBLIC / "sitemap.xml",
            PUBLIC / "llms.txt",
            PUBLIC / "llms-full.txt",
            *(PUBLIC / urlsplit(url).path.lstrip("/") for url in MARKDOWN_REPRESENTATIONS.values()),
            PUBLIC / "ai-index.json",
        ]
    )
    runtime_text = "\n".join(path.read_text(encoding="utf-8") for path in runtime_files)
    for label, pattern in FORBIDDEN_RUNTIME_PATTERNS.items():
        if re.search(pattern, runtime_text, flags=re.IGNORECASE):
            errors.append(f"runtime contains {label}")

    for filename, canonical in CANONICALS.items():
        parser = validate_html(
            PUBLIC / filename,
            canonical,
            errors,
            markdown=MARKDOWN_REPRESENTATIONS[filename],
        )
        all_links.extend(parser.links)
        validate_markdown(
            PUBLIC / urlsplit(MARKDOWN_REPRESENTATIONS[filename]).path.lstrip("/"),
            canonical,
            errors,
        )
    validate_html(PUBLIC / "404.html", None, errors, require_description=False)

    llms = (PUBLIC / "llms.txt").read_text(encoding="utf-8")
    nonempty_llms_lines = [line for line in llms.splitlines() if line.strip()]
    if not nonempty_llms_lines or not nonempty_llms_lines[0].startswith("# "):
        errors.append("public/llms.txt: first non-empty line must be an h1")
    if len(nonempty_llms_lines) < 2 or not nonempty_llms_lines[1].startswith("> "):
        errors.append("public/llms.txt: second non-empty line must be a blockquote summary")
    for endpoint in [*MARKDOWN_REPRESENTATIONS.values(), *MACHINE_ENDPOINTS.values()]:
        if endpoint not in llms:
            errors.append(f"public/llms.txt: missing machine endpoint {endpoint}")

    if FULL_CONTEXT.read_text(encoding="utf-8") != render_context():
        errors.append("public/llms-full.txt: generated context is stale")

    try:
        ai_schema = json.loads((PUBLIC / "ai-index.schema.json").read_text(encoding="utf-8"))
        ai_index = json.loads((PUBLIC / "ai-index.json").read_text(encoding="utf-8"))
        if ai_schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append("public/ai-index.schema.json: expected JSON Schema Draft 2020-12")
        if ai_index.get("$schema") != MACHINE_ENDPOINTS["schema"]:
            errors.append("public/ai-index.json: schema URL is incorrect")
        if ai_index.get("schema_version") != "1.0":
            errors.append("public/ai-index.json: unsupported schema version")
        entrypoints = ai_index.get("preferred_entrypoints", {})
        expected_entrypoints = {
            "discovery": MACHINE_ENDPOINTS["llms"],
            "full_context": MACHINE_ENDPOINTS["full_context"],
            "structured_index": MACHINE_ENDPOINTS["index"],
        }
        if entrypoints != expected_entrypoints:
            errors.append("public/ai-index.json: preferred entrypoints are incorrect")
        indexed_pages = {
            page.get("canonical_url"): page.get("markdown_url")
            for page in ai_index.get("pages", [])
            if isinstance(page, dict)
        }
        expected_pages = {
            CANONICALS[filename]: MARKDOWN_REPRESENTATIONS[filename]
            for filename in CANONICALS
        }
        if indexed_pages != expected_pages:
            errors.append("public/ai-index.json: canonical and Markdown page map is incomplete")
        access_policy = ai_index.get("access_policy", {})
        if access_policy.get("search_and_retrieval") != "allowed":
            errors.append("public/ai-index.json: search and retrieval policy must be explicit")
        if access_policy.get("model_development") != "allowed":
            errors.append("public/ai-index.json: model-development policy must be explicit")
        indexed_sources = [source for source in ai_index.get("sources", []) if isinstance(source, dict)]
        source_types = {source.get("source_type") for source in indexed_sources}
        if source_types != {"public-framework", "government-guidance", "first-party-research"}:
            errors.append("public/ai-index.json: source-type coverage is incomplete")
        if len(indexed_sources) != 8 or any(not source.get("does_not_prove") for source in indexed_sources):
            errors.append("public/ai-index.json: all eight ledger sources need explicit evidence limits")
    except json.JSONDecodeError as exc:
        errors.append(f"machine-readable JSON is invalid: {exc}")

    metix_links = [href for href in all_links if href.startswith("https://metix.ai")]
    if len(set(metix_links)) < 6:
        errors.append(f"expected at least six distinct contextual Metix links, found {len(set(metix_links))}")
    for href in metix_links:
        parsed = urlsplit(href)
        if parsed.netloc != "metix.ai":
            errors.append(f"non-canonical Metix hostname: {href}")
        if parsed.path.startswith("/jobs/") and not re.fullmatch(r"/jobs/[a-z0-9]+(?:-[a-z0-9]+)*", parsed.path):
            errors.append(f"Metix job URL does not preserve a canonical slug: {href}")

    try:
        manifest = json.loads((PUBLIC / "manifest.json").read_text(encoding="utf-8"))
        if manifest.get("start_url") != "/":
            errors.append("public/manifest.json: start_url must be /")
    except json.JSONDecodeError as exc:
        errors.append(f"public/manifest.json: invalid JSON: {exc}")

    expected_public_urls = set(CANONICALS.values())
    for sitemap, expected in [
        (PUBLIC / "sitemap.xml", expected_public_urls),
        (ROOT / "sitemap.xml", {"https://digidai.github.io/openjobs/"}),
    ]:
        try:
            tree = ET.parse(sitemap)
            found = {loc.text for loc in tree.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
            if found != expected:
                errors.append(f"{sitemap.relative_to(ROOT)}: URLs {sorted(found)} do not match {sorted(expected)}")
        except ET.ParseError as exc:
            errors.append(f"{sitemap.relative_to(ROOT)}: invalid XML: {exc}")

    robots = (PUBLIC / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap: https://openjobs.genedai.me/sitemap.xml" not in robots:
        errors.append("public/robots.txt: canonical sitemap declaration missing")
    required_agents = {
        "OAI-SearchBot",
        "Claude-SearchBot",
        "PerplexityBot",
        "ChatGPT-User",
        "Claude-User",
        "Perplexity-User",
        "GPTBot",
        "ClaudeBot",
        "Google-Extended",
        "*",
    }
    declared_agents = set(re.findall(r"^User-agent:\s*(\S+)\s*$", robots, flags=re.MULTILINE))
    if declared_agents != required_agents:
        errors.append(f"public/robots.txt: crawler groups {sorted(declared_agents)} do not match expected policy")
    for agent in required_agents:
        if not re.search(rf"^User-agent:\s*{re.escape(agent)}\s*\nAllow:\s*/\s*$", robots, flags=re.MULTILINE):
            errors.append(f"public/robots.txt: {agent} is not explicitly allowed")
    if re.search(r"^Disallow:", robots, flags=re.MULTILINE):
        errors.append("public/robots.txt: unexpected disallow rule")

    headers = (PUBLIC / "_headers").read_text(encoding="utf-8")
    for route in ["/llms.txt", "/llms-full.txt", "/ai-index.json", "/ai-index.schema.json", "/*.md"]:
        if not re.search(rf"^{re.escape(route)}\s*$", headers, flags=re.MULTILINE):
            errors.append(f"public/_headers: missing rule for {route}")
    if headers.count("Access-Control-Allow-Origin: *") != 5:
        errors.append("public/_headers: all machine-readable route groups must allow cross-origin reads")
    if headers.count("X-Robots-Tag: noindex, follow") != 5:
        errors.append("public/_headers: machine-readable copies must stay out of the search index")
    for media_type in ["text/plain", "text/markdown", "application/json", "application/schema+json"]:
        if f"Content-Type: {media_type}; charset=utf-8" not in headers:
            errors.append(f"public/_headers: missing media type {media_type}")

    redirects = {
        line.strip()
        for line in (PUBLIC / "_redirects").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    expected_redirects = {"/rss.xml / 301", "/stats.json / 301"}
    if redirects != expected_redirects:
        errors.append("public/_redirects: legacy RSS and stats URLs must redirect permanently to /")

    workflow = (ROOT / ".github/workflows/validate-site.yml").read_text(encoding="utf-8")
    if "contents: read" not in workflow or "contents: write" in workflow:
        errors.append("validation workflow must be read-only")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "no longer publishes or aggregates job listings" not in readme:
        errors.append("README must state that job aggregation is retired")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"OK: validated {len(CANONICALS)} canonical pages")
    print(f"OK: found {len(set(metix_links))} distinct contextual metix.ai links")
    print(f"OK: validated {len(MARKDOWN_REPRESENTATIONS)} Markdown representations and AI resource index")
    print("OK: retired job-board runtime and write-enabled workflow are absent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
