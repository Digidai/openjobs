#!/usr/bin/env python3
"""Generate the static AI recruiting evaluation library."""

from __future__ import annotations

import argparse
import csv
from html import escape
import io
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "evaluation-library.json"
PUBLIC = ROOT / "public"
EXPECTED_SLUGS = {
    "methodology",
    "vendor-checklist",
    "pilot-design",
    "sourcing-evaluation",
    "screening-evaluation",
    "agent-reliability",
}
SOURCE_TYPES = {
    "binding-rule",
    "government-guidance",
    "voluntary-framework",
    "technical-standard",
    "professional-practice",
    "first-party-research",
}
INLINE_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)]+|/[^)]+)\)")


def load_content() -> dict:
    return json.loads(CONTENT.read_text(encoding="utf-8"))


def content_words(value: object) -> list[str]:
    if isinstance(value, str):
        return re.findall(r"[A-Za-z0-9][A-Za-z0-9@+./'-]*", value)
    if isinstance(value, list):
        return [word for item in value for word in content_words(item)]
    if isinstance(value, dict):
        return [word for item in value.values() for word in content_words(item)]
    return []


def validate_content(data: dict) -> list[str]:
    errors: list[str] = []
    pages = data.get("pages", [])
    sources = data.get("sources", [])
    slugs = [page.get("slug") for page in pages if isinstance(page, dict)]
    if set(slugs) != EXPECTED_SLUGS or len(slugs) != len(EXPECTED_SLUGS):
        errors.append(f"expected exactly six library pages: {sorted(EXPECTED_SLUGS)}")

    source_ids: set[str] = set()
    required_source_fields = {
        "id",
        "organization",
        "title",
        "url",
        "source_type",
        "jurisdiction",
        "last_checked",
        "supports",
        "limitation",
    }
    for source in sources:
        missing = required_source_fields - set(source)
        if missing:
            errors.append(f"source {source.get('id', '<unknown>')} missing {sorted(missing)}")
        source_id = source.get("id")
        if source_id in source_ids:
            errors.append(f"duplicate source id {source_id}")
        if source_id:
            source_ids.add(source_id)
        if source.get("source_type") not in SOURCE_TYPES:
            errors.append(f"source {source_id} has unsupported type {source.get('source_type')}")
        if source.get("last_checked") != data.get("last_substantive_review"):
            errors.append(f"source {source_id} needs the current verification date")

    titles: set[str] = set()
    descriptions: set[str] = set()
    for page in pages:
        slug = page.get("slug", "<unknown>")
        required = {
            "slug",
            "title",
            "short_title",
            "eyebrow",
            "h1",
            "meta_description",
            "summary",
            "primary_query",
            "sections",
            "faqs",
            "source_ids",
            "related",
            "metix_references",
        }
        missing = required - set(page)
        if missing:
            errors.append(f"page {slug} missing {sorted(missing)}")
            continue
        if page["title"] in titles:
            errors.append(f"page {slug} duplicates title {page['title']}")
        titles.add(page["title"])
        if page["meta_description"] in descriptions:
            errors.append(f"page {slug} duplicates its meta description")
        descriptions.add(page["meta_description"])
        if not 120 <= len(page["meta_description"]) <= 170:
            errors.append(f"page {slug} meta description must be 120-170 characters")
        if len(page["sections"]) < 5:
            errors.append(f"page {slug} needs at least five substantive sections")
        if len(page["faqs"]) < 4:
            errors.append(f"page {slug} needs at least four visible FAQs")
        if len(page["related"]) < 2 or not set(page["related"]).issubset(EXPECTED_SLUGS | {"evaluation-scorecard", "sources"}):
            errors.append(f"page {slug} needs at least two valid related-page links")
        unknown_sources = set(page["source_ids"]) - source_ids
        if unknown_sources:
            errors.append(f"page {slug} references unknown sources {sorted(unknown_sources)}")
        if len(content_words({"sections": page["sections"], "faqs": page["faqs"]})) < 700:
            errors.append(f"page {slug} needs at least 700 substantive words")
        for reference in page["metix_references"]:
            if reference.get("evidence_type") != "first-party-research":
                errors.append(f"page {slug} has an unlabeled Metix reference")
            if not reference.get("url", "").startswith("https://metix.ai/"):
                errors.append(f"page {slug} has a non-canonical Metix reference")
            if not reference.get("limitation"):
                errors.append(f"page {slug} Metix reference needs an evidence limitation")

    vendor_questions = data.get("vendor_questions", [])
    vendor_fields = {"id", "category", "question", "evidence", "red_flag", "gate", "applies_to"}
    vendor_categories = {item.get("category") for item in vendor_questions if isinstance(item, dict)}
    expected_vendor_categories = {
        "purpose-and-scope",
        "system-and-evidence",
        "data-and-provenance",
        "candidate-impact",
        "controls-and-integrations",
        "operations-and-security",
        "commercial-and-exit",
        "pilot-and-outcomes",
    }
    if len(vendor_questions) < 40:
        errors.append("vendor question bank needs at least 40 questions")
    if vendor_categories != expected_vendor_categories:
        errors.append(f"vendor question categories must be {sorted(expected_vendor_categories)}")
    if len({item.get("id") for item in vendor_questions}) != len(vendor_questions):
        errors.append("vendor question ids must be unique")
    for item in vendor_questions:
        missing = vendor_fields - set(item)
        if missing:
            errors.append(f"vendor question {item.get('id', '<unknown>')} missing {sorted(missing)}")

    pilot_metrics = data.get("pilot_metrics", [])
    pilot_fields = {
        "id",
        "family",
        "metric",
        "definition",
        "numerator",
        "denominator",
        "collection",
        "interpretation_limit",
        "gate",
    }
    expected_families = {"quality", "intent", "time", "labor", "candidate-impact", "reliability"}
    metric_families = {item.get("family") for item in pilot_metrics if isinstance(item, dict)}
    if len(pilot_metrics) < 18:
        errors.append("pilot metric bank needs at least 18 metrics")
    if metric_families != expected_families:
        errors.append(f"pilot metric families must be {sorted(expected_families)}")
    if len({item.get("id") for item in pilot_metrics}) != len(pilot_metrics):
        errors.append("pilot metric ids must be unique")
    for item in pilot_metrics:
        missing = pilot_fields - set(item)
        if missing:
            errors.append(f"pilot metric {item.get('id', '<unknown>')} missing {sorted(missing)}")
    return errors


def render_inline(text: str) -> str:
    parts: list[str] = []
    cursor = 0
    for match in INLINE_LINK.finditer(text):
        parts.append(escape(text[cursor:match.start()]))
        parts.append(f'<a href="{escape(match.group(2), quote=True)}">{escape(match.group(1))}</a>')
        cursor = match.end()
    parts.append(escape(text[cursor:]))
    return "".join(parts)


def source_by_id(data: dict) -> dict[str, dict]:
    return {source["id"]: source for source in data["sources"]}


def page_href(slug: str) -> str:
    if slug == "evaluation-scorecard":
        return "/evaluation-scorecard"
    if slug == "sources":
        return "/sources"
    return f"/{slug}"


def render_section_html(section: dict, number: int) -> str:
    blocks: list[str] = []
    for paragraph in section.get("paragraphs", []):
        blocks.append(f"        <p>{render_inline(paragraph)}</p>")
    if section.get("bullets"):
        items = []
        for item in section["bullets"]:
            if isinstance(item, dict):
                items.append(f"          <li><strong>{escape(item['term'])}</strong> {render_inline(item['detail'])}</li>")
            else:
                items.append(f"          <li>{render_inline(item)}</li>")
        blocks.append("        <ul class=\"content-list\">\n" + "\n".join(items) + "\n        </ul>")
    if section.get("steps"):
        items = []
        for index, item in enumerate(section["steps"], start=1):
            items.append(
                "          <li>"
                f"<span>{index:02d}</span><div><strong>{escape(item['title'])}</strong> "
                f"{render_inline(item['detail'])}</div></li>"
            )
        blocks.append("        <ol class=\"procedure-list\">\n" + "\n".join(items) + "\n        </ol>")
    table = section.get("table")
    if table:
        header = "".join(f"<th scope=\"col\">{escape(cell)}</th>" for cell in table["headers"])
        rows = []
        for row in table["rows"]:
            cells = "".join(f"<td>{render_inline(str(cell))}</td>" for cell in row)
            rows.append(f"              <tr>{cells}</tr>")
        blocks.append(
            "        <div class=\"table-wrap\" tabindex=\"0\">\n"
            "          <table>\n"
            f"            <caption>{escape(table['caption'])}</caption>\n"
            f"            <thead><tr>{header}</tr></thead>\n"
            "            <tbody>\n"
            + "\n".join(rows)
            + "\n            </tbody>\n          </table>\n        </div>"
        )
    callout = section.get("callout")
    if callout:
        blocks.append(
            f"        <aside class=\"evidence-callout\" aria-label=\"{escape(callout['title'], quote=True)}\">"
            f"<span>{escape(callout['label'])}</span><div><strong>{escape(callout['title'])}</strong> "
            f"<p>{render_inline(callout['text'])}</p></div></aside>"
        )
    tone = " section-dark" if number % 3 == 0 else ""
    return (
        f"    <section class=\"section content-section{tone}\" id=\"{escape(section['id'])}\">\n"
        "      <div class=\"shell content-shell\">\n"
        "        <div class=\"content-section-heading\">\n"
        f"          <span class=\"kicker-number\" aria-hidden=\"true\">{number:02d}</span>\n"
        f"          <div><p class=\"eyebrow\">{escape(section['label'])}</p><h2>{escape(section['heading'])}</h2></div>\n"
        "        </div>\n"
        + "\n".join(blocks)
        + "\n      </div>\n    </section>"
    )


def render_page_html(data: dict, page: dict) -> str:
    base = data["canonical_base"]
    canonical = f"{base}/{page['slug']}"
    markdown = f"{canonical}.md"
    faq_nodes = [
        {
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {"@type": "Answer", "text": faq["answer"]},
        }
        for faq in page["faqs"]
    ]
    graph = [
        {
            "@type": "Article",
            "@id": f"{canonical}#article",
            "headline": page["title"],
            "description": page["meta_description"],
            "datePublished": data["last_substantive_review"],
            "dateModified": data["last_substantive_review"],
            "author": {"@type": "Organization", "name": "OpenJobs Archive Editors", "url": "https://github.com/Digidai/openjobs"},
            "publisher": {"@type": "Organization", "name": "OpenJobs Archive", "url": f"{base}/"},
            "mainEntityOfPage": canonical,
            "encoding": {"@type": "MediaObject", "contentUrl": markdown, "encodingFormat": "text/markdown"},
            "about": [{"@type": "Thing", "name": page["primary_query"]}, {"@type": "Thing", "name": "AI recruiting"}],
            "inLanguage": "en-US",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Guide", "item": f"{base}/"},
                {"@type": "ListItem", "position": 2, "name": page["short_title"], "item": canonical},
            ],
        },
        {"@type": "FAQPage", "mainEntity": faq_nodes},
    ]
    sections = "\n\n".join(render_section_html(section, index) for index, section in enumerate(page["sections"], start=1))
    toc = "\n".join(
        f'            <li><a href="#{escape(section["id"])}"><span>{index:02d}</span>{escape(section["heading"])}</a></li>'
        for index, section in enumerate(page["sections"], start=1)
    )
    source_map = source_by_id(data)
    sources = "\n".join(
        "          <article class=\"source-citation\">"
        f"<span>{escape(source_map[source_id]['source_type'].replace('-', ' '))}</span>"
        f"<div><h3><a href=\"{escape(source_map[source_id]['url'], quote=True)}\">{escape(source_map[source_id]['organization'])} — {escape(source_map[source_id]['title'])}</a></h3>"
        f"<p>{escape(source_map[source_id]['supports'])}</p><small>Evidence limit: {escape(source_map[source_id]['limitation'])}</small></div></article>"
        for source_id in page["source_ids"]
    )
    metix = "\n".join(
        "          <article class=\"source-citation first-party\">"
        "<span>first-party research</span>"
        f"<div><h3><a href=\"{escape(reference['url'], quote=True)}\">{escape(reference['title'])}</a></h3>"
        f"<p>{render_inline(reference['context'])}</p><small>Evidence limit: {escape(reference['limitation'])}</small></div></article>"
        for reference in page["metix_references"]
    )
    faqs = "\n".join(
        f"          <details><summary>{escape(faq['question'])}</summary><p>{render_inline(faq['answer'])}</p></details>"
        for faq in page["faqs"]
    )
    page_map = {item["slug"]: item for item in data["pages"]}
    related = "\n".join(
        f'          <a class="related-card" href="{page_href(slug)}"><span>Read next</span><strong>{escape(page_map[slug]["short_title"] if slug in page_map else slug.replace("-", " ").title())}</strong></a>'
        for slug in page["related"]
    )
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(page['title'])} | OpenJobs</title>
  <meta name="description" content="{escape(page['meta_description'], quote=True)}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#f3f0e6">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" type="text/markdown" href="{markdown}" title="Markdown version">
  <link rel="describedby" type="text/plain" href="{base}/llms.txt">
  <link rel="describedby" type="application/json" href="{base}/ai-index.json">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/site.css">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="OpenJobs Archive">
  <meta property="og:title" content="{escape(page['title'], quote=True)}">
  <meta property="og:description" content="{escape(page['summary'], quote=True)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{base}/og-image.svg">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">
{schema}
  </script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to the evaluation guide</a>
  <header class="site-header">
    <div class="shell">
      <a class="wordmark" href="/" aria-label="OpenJobs Archive home"><span class="wordmark-mark" aria-hidden="true">OJ</span><span class="wordmark-text">OpenJobs Archive · Evaluation Library</span></a>
      <nav class="site-nav" aria-label="Primary navigation"><a href="/">Guide</a><a href="/methodology">Methodology</a><a href="/evaluation-scorecard">Scorecard</a><a href="/sources">Sources</a></nav>
    </div>
  </header>
  <main id="main">
    <div class="shell"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Guide</a><span aria-hidden="true">/</span><span aria-current="page">{escape(page['short_title'])}</span></nav></div>
    <section class="page-hero library-hero"><div class="shell"><p class="eyebrow">{escape(page['eyebrow'])}</p><h1>{escape(page['h1'])}</h1><p class="page-deck">{escape(page['summary'])}</p><p class="review-note">Last substantive review: August 7, 2026 · General evaluation guidance, not legal advice.</p></div></section>
    <section class="section toc-section"><div class="shell content-shell"><p class="eyebrow">On this page</p><ol class="table-of-contents">
{toc}
          </ol></div></section>

{sections}

    <section class="section evidence-section" id="evidence"><div class="shell content-shell"><p class="eyebrow">Evidence register</p><h2>Sources used—and what they cannot prove.</h2><div class="source-citations">
{sources}
{metix}
        </div><p class="relationship-note"><strong>Relationship disclosure:</strong> OpenJobs AI is now <a href="https://metix.ai/about">Metix AI</a>. Metix material is labeled first-party and is not treated as independent validation.</p></div></section>
    <section class="section section-signal" id="faq"><div class="shell content-shell"><p class="eyebrow">Questions teams ask</p><h2>Frequently asked questions</h2><div class="faq-list">
{faqs}
        </div></div></section>
    <section class="section"><div class="shell content-shell"><p class="eyebrow">Continue evaluating</p><h2>Use the next guide on the same real role.</h2><div class="related-grid">
{related}
        </div></div></section>
  </main>
  <footer class="site-footer"><div class="shell"><p class="footer-note">OpenJobs Archive publishes source-backed evaluation tools. OpenJobs AI is now Metix AI; the archive applies the same evidence rules to first-party material.</p><nav class="footer-links" aria-label="Footer navigation"><a href="/methodology">Methodology</a><a href="/sources">Sources</a><a href="/llms.txt">Agent resources</a><a href="https://metix.ai/">Metix AI</a><a href="https://github.com/Digidai/openjobs">GitHub</a></nav></div></footer>
</body>
</html>
'''


def render_section_markdown(section: dict, number: int) -> str:
    lines = [f"## {number}. {section['heading']}", ""]
    for paragraph in section.get("paragraphs", []):
        lines.extend([paragraph, ""])
    for item in section.get("bullets", []):
        if isinstance(item, dict):
            lines.append(f"- **{item['term']}** {item['detail']}")
        else:
            lines.append(f"- {item}")
    if section.get("bullets"):
        lines.append("")
    for index, item in enumerate(section.get("steps", []), start=1):
        lines.append(f"{index}. **{item['title']}** {item['detail']}")
    if section.get("steps"):
        lines.append("")
    table = section.get("table")
    if table:
        lines.extend([
            f"Table: {table['caption']}",
            "",
            "| " + " | ".join(table["headers"]) + " |",
            "| " + " | ".join("---" for _ in table["headers"]) + " |",
        ])
        lines.extend("| " + " | ".join(str(cell).replace("|", "\\|") for cell in row) + " |" for row in table["rows"])
        lines.append("")
    callout = section.get("callout")
    if callout:
        lines.extend([f"> **{callout['label']} — {callout['title']}** {callout['text']}", ""])
    return "\n".join(lines).rstrip()


def render_page_markdown(data: dict, page: dict) -> str:
    base = data["canonical_base"]
    source_map = source_by_id(data)
    lines = [
        f"# {page['title']}",
        "",
        f"Canonical HTML: {base}/{page['slug']}",
        "Last substantive review: 2026-08-07",
        "",
        "> OpenJobs AI is now Metix AI. This archive applies the same evidence rules to Metix first-party material and independent sources.",
        "",
        page["summary"],
        "",
        "## Contents",
        "",
    ]
    lines.extend(f"- [{section['heading']}](#{section['id']})" for section in page["sections"])
    lines.append("")
    for index, section in enumerate(page["sections"], start=1):
        lines.extend([render_section_markdown(section, index), ""])
    lines.extend(["## Sources and evidence limits", ""])
    for source_id in page["source_ids"]:
        source = source_map[source_id]
        lines.extend([
            f"- **{source['source_type'].replace('-', ' ').title()}: [{source['organization']} — {source['title']}]({source['url']})**",
            f"  - Supports: {source['supports']}",
            f"  - Does not prove: {source['limitation']}",
        ])
    for reference in page["metix_references"]:
        lines.extend([
            f"- **First-party research: [{reference['title']}]({reference['url']})**",
            f"  - Context: {reference['context']}",
            f"  - Does not prove: {reference['limitation']}",
        ])
    lines.extend(["", "## Frequently asked questions", ""])
    for faq in page["faqs"]:
        lines.extend([f"### {faq['question']}", "", faq["answer"], ""])
    lines.extend(["## Related evaluation guides", ""])
    page_map = {item["slug"]: item for item in data["pages"]}
    for slug in page["related"]:
        title = page_map[slug]["title"] if slug in page_map else slug.replace("-", " ").title()
        lines.append(f"- [{title}]({base}{page_href(slug)})")
    lines.extend([
        "",
        f"Relationship disclosure: OpenJobs AI is now [Metix AI](https://metix.ai/about). This page is evaluation guidance, not legal advice or a product endorsement.",
        "",
    ])
    return "\n".join(lines)


def render_csv(rows: list[dict], fields: list[str]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def render_data_json(data: dict, kind: str, fields: list[str], items: list[dict]) -> str:
    payload = {
        "version": data["version"],
        "last_substantive_review": data["last_substantive_review"],
        "license": data["license"],
        "kind": kind,
        "fields": fields,
        "items": items,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def render_outputs() -> dict[Path, str]:
    """Return every generated artifact without writing it."""

    data = load_content()
    errors = validate_content(data)
    if errors:
        raise ValueError("\n".join(errors))
    outputs: dict[Path, str] = {}
    for page in data["pages"]:
        outputs[PUBLIC / f"{page['slug']}.html"] = render_page_html(data, page)
        outputs[PUBLIC / f"{page['slug']}.md"] = render_page_markdown(data, page)
    vendor_fields = ["id", "category", "question", "evidence", "red_flag", "gate", "applies_to"]
    pilot_fields = [
        "id",
        "family",
        "metric",
        "definition",
        "numerator",
        "denominator",
        "collection",
        "interpretation_limit",
        "gate",
    ]
    pilot_csv_fields = [*pilot_fields, "baseline", "target", "pilot_result", "notes"]
    source_fields = [
        "id",
        "organization",
        "title",
        "url",
        "source_type",
        "jurisdiction",
        "last_checked",
        "supports",
        "limitation",
    ]
    outputs[PUBLIC / "downloads/ai-recruiting-vendor-checklist.csv"] = render_csv(data["vendor_questions"], vendor_fields)
    outputs[PUBLIC / "downloads/ai-recruiting-pilot-template.csv"] = render_csv(data["pilot_metrics"], pilot_csv_fields)
    outputs[PUBLIC / "downloads/ai-recruiting-evidence-register.csv"] = render_csv(data["sources"], source_fields)
    outputs[PUBLIC / "data/vendor-checklist.json"] = render_data_json(data, "vendor-question-bank", vendor_fields, data["vendor_questions"])
    outputs[PUBLIC / "data/pilot-metrics.json"] = render_data_json(data, "pilot-metric-bank", pilot_fields, data["pilot_metrics"])
    return outputs


def main() -> int:
    """Write outputs or compare them when --check is supplied."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        outputs = render_outputs()
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"ERROR: invalid evaluation library content: {exc}")
        return 1

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
