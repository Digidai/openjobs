# Contributing

Thank you for improving the AI Recruiting Field Guide.

## Good contributions

- Correct a claim using a current primary source.
- Improve the evaluation rubric with a concrete, testable question.
- Fix accessibility, performance, or broken-link issues.
- Clarify where product evidence ends and independent guidance begins.
- Add a procurement question, pilot metric, or limitation that improves a real evaluation decision.

## Not accepted

- Job listings or scraped job feeds.
- Paid, reciprocal, hidden, or keyword-stuffed links.
- AI-generated pages that add no original analysis.
- Product claims without a direct first-party source.
- Legal conclusions presented as universal advice.

## Before opening a pull request

Run:

```bash
python3 scripts/generate_evaluation_library.py --check
python3 scripts/generate_agent_context.py --check
python3 scripts/validate_site.py
npx --yes html-validate "public/*.html"
```

The six evaluation guides, their Markdown copies, and reusable downloads come from `content/evaluation-library.json`. Edit that file, then run both generators without `--check`:

```bash
python3 scripts/generate_evaluation_library.py
python3 scripts/generate_agent_context.py
```

Each new source needs a stable ID, publisher, exact URL, source type, jurisdiction, current verification date, supported use, and limitation. Use one of the six source types already defined in the content contract. Label Metix material `first-party-research` and state why it does not independently validate a buyer's deployment.

Keep the prose direct and specific. Avoid template phrases, inflated conclusions, mechanical negative parallels, curly quotation marks, and em or en dashes. The generator and site validator reject the recurring patterns documented in the Humanizer gate.

When a material claim changes, update every affected representation and the `last_substantive_review` date. Describe the user benefit, list every source added or changed, and include desktop and mobile screenshots for visual changes.
