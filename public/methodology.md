# AI Recruiting Evaluation Methodology

Canonical HTML: https://openjobs.genedai.me/methodology
Last substantive review: 2026-08-07

> OpenJobs AI is now Metix AI. This archive applies the same evidence rules to Metix first-party material and independent sources.

This methodology evaluates an AI recruiting system in the context of one defined workflow. It separates vendor claims from observed evidence, tests both successful and failed cases, and records what a source cannot establish before anyone assigns a score.

## Contents

- [Define the decision before collecting evidence.](#unit-of-evaluation)
- [Use an evidence ladder instead of treating every artifact equally.](#evidence-ladder)
- [Turn each important promise into a claim register.](#claim-register)
- [Score evidence maturity, then make the decision separately.](#scoring)
- [Neutrality means visible relationships and symmetric standards.](#neutrality)
- [Treat evaluation as a versioned record, not a one-time review.](#freshness)

## 1. Define the decision before collecting evidence.

The unit of evaluation is not a logo, model name, profile count, or polished demo. It is a named system performing a defined task for a particular role, employer, population, jurisdiction, and period. A sourcing assistant that proposes names has a different evidence burden from a system that rejects applicants or sends messages without per-action review.

Write the decision in one sentence: who will use which output to make or support what hiring decision? Then record the role family, seniority, locations, languages, data sources, review budget, external actions, and human owners. This context prevents evidence from one workflow being recycled as proof for another. It also makes a future change visible: replacing a model, data source, rubric, or approval path creates a new evaluated configuration.

The [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) treats context mapping as part of risk management. The UK recruitment guide similarly begins with purpose, functionality, resources, governance, and applicant impact. Neither source supplies a universal score; both support making the use case explicit before measuring it.

- **System boundary.** List models, retrieval sources, human services, integrations, and external channels included in the evaluated workflow.
- **Decision boundary.** State whether the output discovers, ranks, recommends, screens, communicates, schedules, or makes a selection decision.
- **Change boundary.** Name the changes that require re-testing rather than assuming prior evidence still applies.

## 2. Use an evidence ladder instead of treating every artifact equally.

A capability statement, a scripted demo, a benchmark, and a real-role outcome answer different questions. The library records the strongest available level for each claim and keeps lower-level evidence visible rather than silently promoting it. A demo can show that a control exists in one path; it cannot establish that the control is used consistently. A benchmark can compare models under a protocol; it cannot show the buyer's operating burden or candidate experience.

Evidence also needs provenance. Record who produced it, when, with which inputs, under what access, and whether unsuccessful cases were available. Vendor-supplied material remains useful when labeled first-party. The error is not using first-party evidence; it is presenting it as independent validation.

Table: Evidence levels used throughout the OpenJobs evaluation library

| Level | What it can support | What remains unresolved |
| --- | --- | --- |
| 0 — assertion | The vendor or reviewer states that a capability exists. | Whether it exists, works, or applies to the evaluated configuration. |
| 1 — artifact | Documentation, a screenshot, policy, or model card describes intended behavior. | Whether behavior matches the artifact in practice. |
| 2 — demonstration | A reviewer observes the workflow on prepared or buyer-provided examples. | Repeatability, selection effects, and real operating conditions. |
| 3 — controlled test | A pre-specified test includes successes, failures, and relevant comparison points. | Longitudinal behavior and downstream hiring outcomes. |
| 4 — operating evidence | The system produces repeatable results on real roles with auditable labor, errors, and outcomes. | Generalization to new roles, populations, jurisdictions, or changed components. |

## 3. Turn each important promise into a claim register.

Break broad promises such as “better candidates,” “bias-free screening,” or “fully automated recruiting” into observable claims. For each claim, record the owner, population, metric, comparison, time window, required artifact, known limitation, and decision that depends on it. If a claim cannot name a population or decision, it is probably too vague to score.

Request denominators and exclusions. Ten accepted candidates says little without knowing how many were retrieved, reviewed, contacted, interested, or rejected. A response rate needs sender, channel, audience, time window, bounce handling, follow-up rule, and definition of response. An accuracy number needs the task, label source, sample, threshold, and error distribution. This is especially important where automated output influences selection and the employer remains responsible for how it is used.

Negative evidence belongs in the same register. Document unsupported inferences, stale records, missing groups, accessibility failures, inconsistent explanations, duplicate messages, and cases where the human reviewer overrode the system. A method that captures only showcase cases measures presentation quality, not operational reliability.

1. **Write the claim precisely.** Replace “saves time” with the activity, baseline, people, period, and unit of labor expected to change.
2. **Name the confirming artifact.** Specify the log, sample, labeled set, interview outcome, time record, or candidate feedback needed.
3. **Pre-agree the disconfirming result.** Define which error, threshold, or missing record would weaken or reject the claim.
4. **Record the remaining uncertainty.** A passed test narrows uncertainty; it rarely removes every deployment or legal question.

## 4. Score evidence maturity, then make the decision separately.

This library uses ordinal scores to organize discussion, not to manufacture a universal ranking. A difference between 2 and 3 means the evidence moved from a limited pilot toward repeatable and auditable operation. It does not mean the system became exactly one unit safer, fairer, or more valuable. Weighting also belongs to the buyer: outreach control may be decisive for an agent that sends messages and irrelevant for an offline search benchmark.

Use gates before totals. An inaccessible candidate path, an unowned external action, missing selection-validity evidence, or inability to pause the system can stop deployment even if other dimensions score highly. Then compare alternatives using the same role and evidence request. Do not compensate for a critical zero by adding points from dashboard polish or feature breadth.

Decision language should remain conditional: stop; investigate; run a narrow reversible pilot; continue under named controls; or expand after new evidence. “Approved,” “compliant,” and “safe” require authorities and scopes that a general scorecard does not possess.

> **Scoring rule — No averaging across unknowns** Keep “not tested” distinct from a failed result. Missing evidence is a procurement risk, but it is not evidence that the system always fails.

## 5. Neutrality means visible relationships and symmetric standards.

OpenJobs AI is now Metix AI, so this archive has a relationship that readers should know. The site does not claim institutional independence. Instead, it publishes its method, links to primary sources, labels Metix material first-party, and states the limits of every cited artifact. The same questions about dataset scope, comparison, failures, operating labor, and external validation apply to Metix and to any other vendor.

The library does not accept paid rankings, sell score improvements, hide sponsorship in editorial copy, or place vendors on a league table without comparable evidence. It does not use the absence of public documentation as proof of poor performance; it records the evidence as unavailable. Corrections change the record, not the standard applied to the subject.

Contextual outbound links are chosen because they help evaluate the claim on the page. Official sources explain requirements or practices. First-party research illustrates a method or product architecture. Link placement is not an endorsement, and inclusion in the ledger is not a certification.

- **Symmetric questions.** Ask every evaluated provider for the same core evidence before adding workflow-specific questions.
- **Visible provenance.** Keep publisher, source type, scope, date, and evidence limit next to the citation.
- **Correction over deletion.** When a source changes, preserve what changed and update the verified interpretation.

## 6. Treat evaluation as a versioned record, not a one-time review.

Regulations, regulator guidance, products, models, and integrations change on different schedules. Every time-sensitive source in this library has a last-checked date. A date means the source was reviewed for the stated use; it does not mean every linked page changed that day. Material updates change the page's substantive-review date and the machine-readable evidence register.

Re-evaluate when intended purpose, decision authority, model, retrieval source, candidate population, language, jurisdiction, approval path, or integration changes. Also re-evaluate after an incident, a material error trend, a new accommodation issue, or unexplained movement in quality or override rates. Do not refresh only the date while leaving stale conclusions untouched.

Corrections should identify the affected claim, prior wording, new evidence, date, and downstream pages or assets updated. This makes the library citable as a maintained resource and gives agents enough context to avoid blending older requirements with current guidance.

1. **Verify the primary source.** Prefer the regulator, standards body, statute, or original research page over a summary article.
2. **Recheck the interpretation.** Confirm scope, legal force, effective date, definitions, and whether a draft became final.
3. **Update every representation.** Regenerate HTML, Markdown, CSV, JSON, sitemap, and agent context together.
4. **Record unresolved questions.** Do not convert uncertainty into a confident statement merely to complete a table.

## Sources and evidence limits

- **Voluntary Framework: [NIST — Artificial Intelligence Risk Management Framework 1.0](https://www.nist.gov/itl/ai-risk-management-framework)**
  - Supports: A lifecycle structure for governing, mapping, measuring, and managing AI risk and trustworthiness characteristics.
  - Does not prove: Use of the voluntary framework does not establish legal compliance, product quality, or fitness for a particular hiring process.
- **Voluntary Framework: [NIST — AI Risk Management Framework Playbook](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook)**
  - Supports: Suggested actions for applying the AI RMF functions across design, deployment, evaluation, and operation.
  - Does not prove: The suggested actions are optional and use-case agnostic; they are not a certification checklist or employment-law opinion.
- **Government Guidance: [U.S. Equal Employment Opportunity Commission — Employment Tests and Selection Procedures](https://www.eeoc.gov/laws/guidance/employment-tests-and-selection-procedures)**
  - Supports: Technical assistance on job-related selection procedures, discriminatory impact, validation, and employer responsibility.
  - Does not prove: The page describes federal considerations but does not determine whether a specific tool, employer, or use is lawful.
- **Government Guidance: [UK Department for Science, Innovation and Technology — Responsible AI in Recruitment](https://www.gov.uk/government/publications/responsible-ai-in-recruitment-guide/responsible-ai-in-recruitment)**
  - Supports: Procurement and deployment questions covering purpose, governance, accessibility, assurance, testing, pilots, transparency, and monitoring.
  - Does not prove: The guide expressly does not provide legal assurance and its examples are not universal deployment instructions.
- **Government Guidance: [UK Information Commissioner's Office — AI Tools Used in Recruitment — Audit Outcomes](https://ico.org.uk/action-weve-taken/audits-and-overview-reports/2024/11/ai-tools-used-in-recruitment/)**
  - Supports: Observed privacy and information-rights issues in recruitment sourcing, screening, and selection tools, plus remediation themes.
  - Does not prove: Consensual audits of selected providers do not establish prevalence, legal status, or performance of another product.
- **First-party research: [Agent Evaluation, Done Right](https://metix.ai/research/agent-evaluation-done-right)**
  - Context: Metix describes a component, trajectory, and outcome evaluation model that can be tested against this library's evidence ladder.
  - Does not prove: This is first-party engineering research, not independent assurance or proof of results in a buyer's workflow.

## Frequently asked questions

### Does a high evaluation score mean an AI recruiting system is compliant?

No. The score describes the maturity of evidence reviewed under a defined workflow. Legal obligations depend on facts, jurisdiction, role, system use, and accountable professional advice.

### Can vendor-provided evidence be used?

Yes, when it is labeled first-party and its method, scope, date, comparison, and limitations are visible. It should not be presented as independent validation.

### Why not publish a ranked list of AI recruiting vendors?

Products perform different tasks and expose different decision risks. A single ranking would hide role context, buyer priorities, missing evidence, and material workflow differences.

### When should an evaluation be repeated?

Repeat it after material changes to purpose, models, data sources, integrations, candidate populations, jurisdictions, controls, or observed failure patterns.

## Related evaluation guides

- [AI Recruiting Vendor Evaluation Checklist](https://openjobs.genedai.me/vendor-checklist)
- [AI Recruiting Pilot Design and Metrics](https://openjobs.genedai.me/pilot-design)
- [Evaluation Scorecard](https://openjobs.genedai.me/evaluation-scorecard)

Relationship disclosure: OpenJobs AI is now [Metix AI](https://metix.ai/about). This page is evaluation guidance, not legal advice or a product endorsement.
