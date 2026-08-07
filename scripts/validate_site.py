#!/usr/bin/env python3
"""Fail-closed checks for the static AI Recruiting Field Guide."""

from __future__ import annotations

from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

CANONICALS = {
    "index.html": "https://openjobs.genedai.me/",
    "evaluation-scorecard.html": "https://openjobs.genedai.me/evaluation-scorecard",
    "sources.html": "https://openjobs.genedai.me/sources",
}

REQUIRED_FILES = {
    ROOT / "README.md",
    ROOT / "EDITORIAL_POLICY.md",
    ROOT / "_config.yml",
    ROOT / "sitemap.xml",
    ROOT / ".github/workflows/validate-site.yml",
    PUBLIC / "index.html",
    PUBLIC / "evaluation-scorecard.html",
    PUBLIC / "sources.html",
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
        self.json_ld: list[str] = []
        self._in_json_ld = False
        self._json_buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if tag == "h1":
            self.h1_count += 1
        if tag == "a" and attr.get("href"):
            self.links.append(attr["href"] or "")
        if tag == "link" and attr.get("rel") == "canonical" and attr.get("href"):
            self.canonicals.append(attr["href"] or "")
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

    all_links: list[str] = []
    runtime_files = [PUBLIC / name for name in CANONICALS]
    runtime_files.extend([PUBLIC / "404.html", PUBLIC / "sitemap.xml", PUBLIC / "llms.txt"])
    runtime_text = "\n".join(path.read_text(encoding="utf-8") for path in runtime_files)
    for label, pattern in FORBIDDEN_RUNTIME_PATTERNS.items():
        if re.search(pattern, runtime_text, flags=re.IGNORECASE):
            errors.append(f"runtime contains {label}")

    for filename, canonical in CANONICALS.items():
        parser = validate_html(PUBLIC / filename, canonical, errors)
        all_links.extend(parser.links)
    validate_html(PUBLIC / "404.html", None, errors, require_description=False)

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
    print("OK: retired job-board runtime and write-enabled workflow are absent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
