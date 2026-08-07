# AI Recruiting Evaluation Library Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Publish six substantive, neutral AI recruiting evaluation pages with synchronized HTML, Markdown, CSV, and JSON resources, then expose them through the site, sitemap, and agent-readable indexes.

**Architecture:** Keep the site buildless at runtime. Store new library content in structured JSON, use a dependency-free Python generator to emit committed artifacts, and extend the fail-closed validator so CI rejects stale or incomplete content. Existing canonical pages remain hand-authored in this change.

**Tech Stack:** Static HTML/CSS, JSON-LD, JSON Schema Draft 2020-12, Python 3.12 standard library, Cloudflare Pages, GitHub Pages, GitHub Actions.

---

### Task 1: Add the generated-library contract

**Files:**
- Create: `content/evaluation-library.json`
- Create: `scripts/generate_evaluation_library.py`
- Modify: `scripts/validate_site.py`

**Step 1: Write the failing validation contract**

Add the six expected canonical files, Markdown copies, five downloadable assets, generator, and source-data file to `REQUIRED_FILES`, `CANONICALS`, and `MARKDOWN_REPRESENTATIONS`. Add checks that call the generator rendering functions and compare every committed output byte-for-byte.

**Step 2: Run validation to verify it fails**

Run: `python3 scripts/validate_site.py`

Expected: FAIL because the structured content, generator, and generated artifacts do not exist.

**Step 3: Implement the minimal generator shell**

The script must expose:

```python
ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "evaluation-library.json"

def render_outputs() -> dict[Path, str]:
    """Return every generated artifact without writing it."""

def main() -> int:
    """Write outputs or compare them when --check is supplied."""
```

It must use only Python standard-library modules, sort JSON keys where stable ordering helps review, write UTF-8 with final newlines, and report every stale path in `--check` mode.

**Step 4: Run syntax checks**

Run: `python3 -m py_compile scripts/generate_evaluation_library.py scripts/validate_site.py`

Expected: PASS.

**Step 5: Commit**

```bash
git add content/evaluation-library.json scripts/generate_evaluation_library.py scripts/validate_site.py
git commit -m "build: add evaluation library generation contract"
```

### Task 2: Author the six evidence-backed pages

**Files:**
- Modify: `content/evaluation-library.json`
- Create: `public/methodology.html`
- Create: `public/methodology.md`
- Create: `public/vendor-checklist.html`
- Create: `public/vendor-checklist.md`
- Create: `public/pilot-design.html`
- Create: `public/pilot-design.md`
- Create: `public/sourcing-evaluation.html`
- Create: `public/sourcing-evaluation.md`
- Create: `public/screening-evaluation.html`
- Create: `public/screening-evaluation.md`
- Create: `public/agent-reliability.html`
- Create: `public/agent-reliability.md`

**Step 1: Add content validation before authoring**

Require every page to have a unique slug, title, meta description, H1, summary, primary query, at least five substantive sections, at least four visible FAQs, two or more internal related-page links, and source references. Require each Metix reference to carry `evidence_type: first-party-research` and a visible limitation.

**Step 2: Run generator check to verify failure**

Run: `python3 scripts/generate_evaluation_library.py --check`

Expected: FAIL with missing or incomplete page definitions.

**Step 3: Author page content**

Write distinct content for:

- methodology and evidence levels;
- vendor procurement questions and red flags;
- real-role pilot baselines, samples, metrics, and stop conditions;
- sourcing and ranking metrics with false-positive and false-negative review;
- screening validity, structure, accessibility, accommodation, and review;
- agent permissions, trajectories, fallback, incidents, and drift.

Each page must distinguish requirements, regulator guidance, voluntary frameworks, professional practices, research findings, and first-party claims. Do not state that a checklist proves compliance.

**Step 4: Generate artifacts**

Run: `python3 scripts/generate_evaluation_library.py`

Expected: six HTML and six Markdown files written.

**Step 5: Validate generation**

Run: `python3 scripts/generate_evaluation_library.py --check`

Expected: `OK: evaluation library outputs are current`.

**Step 6: Commit**

```bash
git add content/evaluation-library.json public/*.html public/*.md
git commit -m "content: add AI recruiting evaluation library"
```

### Task 3: Add reusable checklist and pilot downloads

**Files:**
- Modify: `content/evaluation-library.json`
- Modify: `scripts/generate_evaluation_library.py`
- Create: `public/downloads/ai-recruiting-vendor-checklist.csv`
- Create: `public/downloads/ai-recruiting-pilot-template.csv`
- Create: `public/downloads/ai-recruiting-evidence-register.csv`
- Create: `public/data/vendor-checklist.json`
- Create: `public/data/pilot-metrics.json`

**Step 1: Extend validation with failing asset checks**

Require a minimum of 40 vendor questions across all evaluation categories, pilot metrics across quality, intent, time, labor, candidate impact, and reliability, and evidence-register rows with source type, jurisdiction, last-checked date, supported use, and limitation.

**Step 2: Run validation to verify failure**

Run: `python3 scripts/validate_site.py`

Expected: FAIL because download assets are absent.

**Step 3: Generate CSV and JSON assets**

Use `csv.DictWriter` and `json.dumps`. CSV columns must be stable and documented. JSON files include version, generated date, license, fields, and item arrays.

**Step 4: Verify parseability and content counts**

Run:

```bash
python3 -c 'import csv,json; from pathlib import Path; print(sum(1 for _ in csv.DictReader(open("public/downloads/ai-recruiting-vendor-checklist.csv")))); print(len(json.loads(Path("public/data/vendor-checklist.json").read_text())["items"]))'
```

Expected: both counts are at least 40 and equal.

**Step 5: Commit**

```bash
git add content/evaluation-library.json scripts/generate_evaluation_library.py public/downloads public/data
git commit -m "feat: add reusable evaluation downloads"
```

### Task 4: Expand human navigation and neutral link placement

**Files:**
- Modify: `public/index.html`
- Modify: `public/index.html.md`
- Modify: `public/evaluation-scorecard.html`
- Modify: `public/evaluation-scorecard.md`
- Modify: `public/sources.html`
- Modify: `public/sources.md`
- Modify: `public/assets/site.css`
- Modify: `README.md`

**Step 1: Add failing internal-link checks**

Require every canonical page to appear in homepage library navigation and every generated deep page to link to the scorecard, source ledger, and two related pages. Reject a promotional Metix CTA in global header navigation.

**Step 2: Run validation to verify failure**

Run: `python3 scripts/validate_site.py`

Expected: FAIL on missing library links and the existing global CTA.

**Step 3: Implement navigation and disclosure**

Add the six-page library directory to the homepage. Replace the global Metix CTA with a library or methodology link. Keep a restrained relationship disclosure in the footer and contextual first-party research links inside relevant sections. Add scorecard deep-reading links and expand the source ledger.

**Step 4: Add responsive content styles**

Add styles for breadcrumbs, table of contents, content prose, responsive tables, evidence labels, download panels, question groups, and FAQ details. Maintain reduced-motion and print rules.

**Step 5: Validate HTML and internal links**

Run:

```bash
npx --yes html-validate "public/*.html"
python3 scripts/validate_site.py
```

Expected: PASS.

**Step 6: Commit**

```bash
git add public/index.html public/index.html.md public/evaluation-scorecard.html public/evaluation-scorecard.md public/sources.html public/sources.md public/assets/site.css README.md
git commit -m "feat: connect the evaluation library"
```

### Task 5: Expand search and Agent discovery

**Files:**
- Modify: `public/sitemap.xml`
- Modify: `public/llms.txt`
- Modify: `public/llms-full.txt`
- Modify: `public/ai-index.json`
- Modify: `public/ai-index.schema.json`
- Modify: `public/_headers`
- Modify: `scripts/generate_agent_context.py`
- Modify: `scripts/validate_site.py`

**Step 1: Add failing discovery checks**

Require all nine canonical pages and all six Markdown copies in the sitemap, llms discovery, full context, and AI index. Require downloadable assets and their media types in the AI index. Require schema version 1.1.

**Step 2: Run discovery checks to verify failure**

Run:

```bash
python3 scripts/generate_agent_context.py --check
python3 scripts/validate_site.py
```

Expected: FAIL because discovery artifacts still describe three pages.

**Step 3: Update discovery artifacts**

Make the full-context generator consume all Markdown representations in deterministic order. Add all pages, sources, and downloads to `ai-index.json`; extend the schema; update `llms.txt`; update the sitemap. Add CORS, cache, content type, `nosniff`, and `noindex, follow` rules for JSON and CSV data files.

**Step 4: Generate full context**

Run:

```bash
python3 scripts/generate_evaluation_library.py
python3 scripts/generate_agent_context.py
```

Expected: generated outputs updated.

**Step 5: Validate JSON Schema**

Run:

```bash
npx --yes --package ajv-cli@5 --package ajv-formats@3 ajv validate --spec=draft2020 --strict=false -c ajv-formats -s public/ai-index.schema.json -d public/ai-index.json
```

Expected: `public/ai-index.json valid`.

**Step 6: Commit**

```bash
git add public/sitemap.xml public/llms.txt public/llms-full.txt public/ai-index.json public/ai-index.schema.json public/_headers scripts/generate_agent_context.py scripts/validate_site.py
git commit -m "feat: expose the full library to search and agents"
```

### Task 6: Update CI and maintenance documentation

**Files:**
- Modify: `.github/workflows/validate-site.yml`
- Modify: `CONTRIBUTING.md`
- Modify: `EDITORIAL_POLICY.md`
- Modify: `README.md`

**Step 1: Add the new generator to CI**

Run both generators in `--check` mode before the site validator. Watch `content/**` and the new generator path.

**Step 2: Document maintenance rules**

Explain source verification dates, evidence categories, first-party labeling, generation commands, content correction flow, and why global promotional links are avoided.

**Step 3: Run all local checks**

Run:

```bash
python3 scripts/generate_evaluation_library.py --check
python3 scripts/generate_agent_context.py --check
python3 scripts/validate_site.py
npx --yes html-validate "public/*.html"
git diff --check
```

Expected: PASS.

**Step 4: Commit**

```bash
git add .github/workflows/validate-site.yml CONTRIBUTING.md EDITORIAL_POLICY.md README.md
git commit -m "docs: document evaluation library maintenance"
```

### Task 7: Visual, preview, and release verification

**Files:**
- Modify only if verification finds a defect.

**Step 1: Run a local Pages server**

Run: `npx --yes --package wrangler@latest --package @cloudflare/workerd-darwin-arm64@latest wrangler pages dev public --port 8792`

Expected: local server loads all canonical, Markdown, CSV, and JSON resources.

**Step 2: Capture representative screenshots**

Check homepage, vendor checklist, sourcing evaluation, and pilot design at desktop and mobile widths. Confirm headings, tables, breadcrumbs, download panels, and footers do not overflow.

**Step 3: Verify response headers**

Check canonical HTML is indexable and machine/download copies have correct MIME, CORS, cache, ETag, `nosniff`, and `noindex, follow` behavior.

**Step 4: Audit external links**

Request every unique official and Metix URL with bounded timeouts. Record exceptions for endpoints that reject HEAD but succeed with GET. Confirm all Metix links use `https://metix.ai/` canonical host.

**Step 5: Push and open a draft PR**

Push `codex/evaluation-library`, open a draft PR, wait for validation and Cloudflare preview, and repeat the live endpoint and responsive checks on the preview URL.

**Step 6: Merge and verify production**

After green checks and preview validation, mark ready and squash merge. Wait for Cloudflare production and GitHub Pages production to point to the merge commit. Verify both public roots, all canonical pages, machine endpoints, legacy redirects, and representative crawler user agents.

**Step 7: Synchronize the original workspace**

Fast-forward `/Users/dai/Developer/CursorProjects/openjobs` to `origin/main`, rerun both generators and the validator, preserve the existing untracked `.claude/`, then remove the temporary worktree.
