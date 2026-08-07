# AI Recruiting Vendor Evaluation Checklist

Canonical HTML: https://openjobs.genedai.me/vendor-checklist
Last substantive review: 2026-08-07

> OpenJobs AI is now Metix AI. This archive applies the same evidence rules to Metix first-party material and independent sources.

Use this checklist before a contract or broad pilot. It asks vendors to demonstrate one real workflow, disclose evidence and limitations, expose candidate-impact controls, and account for the labor and systems the buyer must still operate.

## Contents

- [Define the problem before the product category.](#before-the-demo)
- [Classify the system by the decision it changes.](#classify-the-system)
- [Ask for artifacts that could disconfirm the sales claim.](#proof-not-promises)
- [Trace where candidate and evaluation data comes from and where it goes.](#data-and-provenance)
- [Evaluate the process from the candidate's side, including the exit path.](#candidate-impact)
- [Test permissions, writes, messages, and fallback under failure.](#actions-and-integrations)
- [Price the full operating model, including the work outside the software.](#operations-and-commercials)
- [End with a decision record, open risks, and a testable pilot.](#decision-record)

## 1. Define the problem before the product category.

Start with the hiring bottleneck and the decision owner, not a feature list. A team that needs more qualified passive candidates is evaluating a different system from one that needs structured applicant screening, scheduling, or end-to-end managed delivery. If the category remains vague, every vendor can appear complete while solving a different step.

Document the current workflow in enough detail to create a comparison: role approval, sourcing channels, people reviewed, outreach, replies, screening, interviews, recruiter time, manager rework, candidate complaints, and integrations. Note what the team will not delegate. This baseline becomes the anchor for demonstrations, reference calls, security review, pilot design, and total cost.

Invite talent acquisition, the hiring manager, people operations, IT or security, data or privacy owners, accessibility expertise, procurement, and counsel as appropriate. One person can coordinate the review, but a vendor should not be allowed to answer a security question with a recruiting metric or a validity question with a compliance badge.

- **Purpose.** What exact delay, quality problem, workload, or candidate issue should change?
- **Boundary.** Which decisions remain with humans, and which external actions may the system take?
- **Baseline.** Which recent comparable role supplies current time, volume, quality, and labor data?
- **Owner.** Who can approve scope, stop the system, answer candidates, and accept residual risk?

## 2. Classify the system by the decision it changes.

AI recruiting products often combine several layers: job-description assistance, search, ranking, enrichment, messaging, chat, assessment, scheduling, analytics, or human delivery. Ask the vendor to draw the production workflow, including third-party models, data providers, human reviewers, ATS writes, email or messaging channels, and manual exception handling. A box labeled "AI" is not an architecture.

Then identify the highest-impact output. A tool that drafts a Boolean query under review presents different risks from one that filters applicants, scores an interview, or sends candidate communications. The evaluation depth should follow the consequence and reversibility of the action. High volume does not automatically mean high risk, but it can multiply a small error quickly.

Ask which functions are generally available, optional, beta, region-limited, partner-delivered, or dependent on a particular plan. Record the evaluated version and configuration. Demonstrating an adjacent product or future roadmap item does not satisfy a requirement for the purchased workflow.

Table: Recruiting system categories and the evidence they most need

| System role | Primary evaluation question | Common hidden dependency |
| --- | --- | --- |
| Sourcing and ranking | Does the system retrieve relevant people within the review budget without hiding exclusions? | Coverage, refresh, enrichment, and human labeling. |
| Screening and assessment | Is the evaluated construct job-related, consistently administered, accessible, and reviewable? | Job analysis, rubric design, accommodations, and employer use. |
| Engagement agent | Are sender, message, channel, timing, suppression, and approval controls enforceable? | Provider policy, identity, contact data, and reply handling. |
| Workflow automation | Can writes, tool calls, and handoffs be traced, reversed, and paused? | ATS permissions, integration behavior, and manual fallback. |
| Managed outcome service | What result is delivered, who performs hidden work, and how are misses remedied? | Human operations, service boundaries, and commercial terms. |

## 3. Ask for artifacts that could disconfirm the sales claim.

A useful answer identifies an artifact, owner, scope, and limitation. "We are accurate" is not an answer; a test report with task definition, labeled sample, threshold, group results, failure cases, and date may be. "We keep humans in the loop" is not an answer; a permissions screen, approval log, rejected action, and manual takeover can show how the control works.

Request examples that are difficult rather than merely diverse in appearance: borderline qualifications, title ambiguity, career gaps, international experience, nontraditional paths, stale records, contradictory sources, accessibility needs, and uncertain replies. Ask to inspect rejected or lower-ranked cases. Selecting only high-confidence successes inflates the apparent quality of every system.

Separate company-level assurances from workflow evidence. Security reports, privacy documentation, policies, and certifications may support governance questions; they do not establish candidate relevance, assessment validity, or hiring outcomes. A model card may document intended use and known limitations; it does not prove the buyer will use the system as intended.

1. **Claim.** Write the promise using the vendor's words without broadening it.
2. **Artifact.** Name the report, log, configuration, sample, or operating record needed.
3. **Failure case.** Ask what result would cause the vendor and buyer to reject or narrow the claim.
4. **Transfer test.** Explain why evidence from one customer, role, or benchmark should apply to this workflow. If it does not, mark the gap.

## 4. Trace where candidate and evaluation data comes from and where it goes.

For sourcing, ask which sources are searched, licensed, inferred, enriched, or supplied by the buyer; how often they refresh; which geographies and populations are weak; and how a person can correct or remove data. A large profile count is inventory, not evidence of current coverage or permission for every downstream use.

For assessment, identify training, validation, configuration, and production data separately. Ask whether protected or sensitive characteristics are collected, inferred, proxied, or excluded; how labels were created; and what the system does when data is missing or contradictory. The ICO's recruitment audits show why purpose, minimization, transparency, retention, and inference deserve direct procurement questions.

Map every transfer and retention location, including model providers, subprocessors, analytics, logs, exports, support tools, and backups. Record customer controls for deletion, retention, model training, human review, and regional processing. Do not infer that a general privacy page describes the contracted configuration.

- **Provenance.** Can a reviewer distinguish buyer data, public or licensed sources, vendor inference, and model-generated text?
- **Freshness.** Are record dates and confidence visible where staleness could change the recruiting decision?
- **Purpose.** Is each field necessary for the stated workflow, or collected because it might be useful later?
- **Control.** Can the buyer export, correct, delete, restrict, and audit data under the actual agreement?

## 5. Evaluate the process from the candidate's side, including the exit path.

Ask what candidates are told about AI use, what information is evaluated, how they request an accommodation, whether an alternative path exists, how they correct relevant data, and how they reach a person. Notice is not meaningful when it arrives after a consequential action or uses language that the candidate cannot connect to the actual process.

Test the complete candidate journey with keyboard navigation, assistive technology where appropriate, mobile and low-bandwidth conditions, multiple languages, time limits, interruptions, and error recovery. WCAG can inform web testing, while ADA.gov emphasizes that hiring technology should measure job skills rather than disability and should support reasonable accommodations. Neither is replaced by a vendor saying its interface is "accessible."

Inspect how the system treats uncertain or incomplete data and how human reviewers see confidence. Ask whether candidates can be rejected solely from automated output, whether reviewers can access the underlying evidence, and whether an appeal or reassessment changes the record. A human click does not create meaningful oversight if the person lacks time, authority, or explanation.

> **Procurement gate: No invisible dead end** A candidate-facing workflow should have a visible route for accommodation, correction, questions, and human escalation before the pilot begins.

## 6. Test permissions, writes, messages, and fallback under failure.

Ask the vendor to demonstrate the exact ATS, CRM, calendar, identity, and communication flows the buyer will use. Inspect field mappings, duplicate handling, retries, idempotency, permissions, error states, audit logs, and what happens when the downstream system is unavailable. A connector logo does not prove production depth or data fidelity.

For agents that communicate externally, test sender authorization, message approval, channel restrictions, timing, suppression, opt-out handling, uncertain replies, follow-up limits, and kill switches. Distinguish a recommendation from an executed action in logs and user interfaces. Require a manual path that can complete the hiring workflow without losing context when automation pauses.

Apply least privilege. A search agent does not need permission to reject an applicant; a scheduling tool may not need access to an entire candidate record. Ask how tool permissions are provisioned, reviewed, revoked, and changed by plan or feature updates. Include support access and human service teams in the same map.

- **Read scope.** Which records and fields can each component retrieve?
- **Write scope.** Which statuses, notes, messages, events, or decisions can it create or modify?
- **Approval scope.** Which actions require review, and can that policy be enforced rather than merely recommended?
- **Recovery scope.** Can the team replay, reverse, reconcile, or finish failed work without data loss or duplicate contact?

## 7. Price the full operating model, including the work outside the software.

Build total cost around the evaluated workflow: subscription or usage, implementation, integration, data, model or communication overages, security review, training, change management, recruiter operation, manager review, quality assurance, candidate support, compliance work, and switching. Ask which labor is performed by the vendor, the buyer, or a partner and whether that boundary changes by plan.

Compare remedy terms to the promised outcome. A credit for a failed search, a rerun, a replacement, service support, and a refund are different. Record definitions for a role, candidate, introduction, contact, screen, interview, usage unit, and expiration. Do not turn a marketing phrase into a contractual commitment unless the governing order form or terms say the same thing.

Evaluate viability without pretending to predict the company. Review support coverage, incident communication, roadmap dependency, data portability, exit assistance, subcontractors, and business continuity. Reference calls should ask what required manual work, what broke, how long remediation took, and what the customer would scope differently. Whether they "like the AI" is less useful.

Table: Cost categories to include in a vendor comparison

| Category | Measure | Common omission |
| --- | --- | --- |
| Commercial | Fixed, variable, minimum, overage, renewal, and remedy terms. | Credits or services excluded from headline price. |
| Implementation | Internal and vendor hours to configure, integrate, test, and train. | Hiring-manager and security-review time. |
| Operation | Weekly recruiter, reviewer, QA, support, and exception-handling labor. | Manual cleanup hidden behind an automated interface. |
| Outcome | Cost per qualified review, interested candidate, completed screen, or interview under agreed definitions. | Counting activity instead of delivered progress. |
| Exit | Export, transition, retraining, contract overlap, and lost workflow context. | Assuming data portability equals operational portability. |

## 8. End with a decision record, open risks, and a testable pilot.

The output of evaluation is not a completed spreadsheet. It is a decision record naming the selected scope, evidence reviewed, unresolved questions, rejected alternatives, accountable owners, required controls, commercial assumptions, and conditions for stopping or expanding. Missing evidence can be an explicit risk acceptance, a pilot question, or a reason not to proceed; it should not disappear into an average score.

Translate the remaining uncertainty into a narrow pilot. Choose one or a small number of representative roles, preserve a current baseline, predefine quality, sample both selected and rejected cases, limit candidate exposure, measure human labor, and schedule review checkpoints. The [pilot design guide](/pilot-design) gives a protocol instead of a generic "try it and see."

Download the question bank and adapt weights only after the gating questions are answered. The template is intentionally vendor-neutral and contains no pre-filled vendor scores. Evidence links and notes remain with the buyer rather than being submitted to this site.

> **Red flags: Pause before contract** Pause when the vendor will not define the evaluated system, show failure cases, identify data sources, explain external-action controls, support a bounded pilot, or put material commercial promises in the governing agreement.

## Sources and evidence limits

- **Voluntary Framework: [NIST: Artificial Intelligence Risk Management Framework 1.0](https://www.nist.gov/itl/ai-risk-management-framework)**
  - Supports: A lifecycle structure for governing, mapping, measuring, and managing AI risk and trustworthiness characteristics.
  - Does not prove: Use of the voluntary framework does not establish legal compliance, product quality, or fitness for a particular hiring process.
- **Government Guidance: [U.S. Equal Employment Opportunity Commission: Employment Tests and Selection Procedures](https://www.eeoc.gov/laws/guidance/employment-tests-and-selection-procedures)**
  - Supports: Technical assistance on job-related selection procedures, discriminatory impact, validation, and employer responsibility.
  - Does not prove: The page describes federal considerations but does not determine whether a specific tool, employer, or use is lawful.
- **Government Guidance: [ADA.gov, U.S. Department of Justice: Algorithms, Artificial Intelligence, and Disability Discrimination in Hiring](https://www.ada.gov/resources/ai-guidance/)**
  - Supports: Guidance on disability-related screening risk, accommodations, accessibility, notice, and measuring job skills rather than disability.
  - Does not prove: The informal guidance is not a final agency action and cannot decide whether a particular process complies with the ADA.
- **Government Guidance: [UK Department for Science, Innovation and Technology: Responsible AI in Recruitment](https://www.gov.uk/government/publications/responsible-ai-in-recruitment-guide/responsible-ai-in-recruitment)**
  - Supports: Procurement and deployment questions covering purpose, governance, accessibility, assurance, testing, pilots, transparency, and monitoring.
  - Does not prove: The guide expressly does not provide legal assurance and its examples are not universal deployment instructions.
- **Government Guidance: [UK Information Commissioner's Office: AI Tools Used in Recruitment: Audit Outcomes](https://ico.org.uk/action-weve-taken/audits-and-overview-reports/2024/11/ai-tools-used-in-recruitment/)**
  - Supports: Observed privacy and information-rights issues in recruitment sourcing, screening, and selection tools, plus remediation themes.
  - Does not prove: Consensual audits of selected providers do not establish prevalence, legal status, or performance of another product.
- **Technical Standard: [World Wide Web Consortium: Web Content Accessibility Guidelines 2.2](https://www.w3.org/TR/WCAG22/)**
  - Supports: Testable web-content accessibility criteria across perceivability, operability, understandability, and robustness.
  - Does not prove: WCAG conformance covers web content and does not by itself prove that an end-to-end hiring process is accessible or lawful.
- **Binding Rule: [New York City Department of Consumer and Worker Protection: Automated Employment Decision Tools](https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page)**
  - Supports: Official access to Local Law 144 materials on covered AEDT use, bias audits, public summaries, and candidate or employee notices.
  - Does not prove: The overview does not determine whether a system or use falls within the law's definitions or satisfies its requirements.
- **Government Guidance: [European Commission: Navigating the AI Act](https://digital-strategy.ec.europa.eu/en/faqs/navigating-ai-act)**
  - Supports: Current Commission explanations of scope, risk classification, employment use cases, obligations, and implementation timing.
  - Does not prove: The FAQ is explanatory, timing can change, and classification depends on intended purpose and the facts of a deployment.
- **First-party research: [Hiring Outcomes, Not More Software](https://metix.ai/blog/hiring-outcomes-not-software)**
  - Context: Metix offers a first-party view of an outcome-delivery model that buyers can subject to the same workflow, labor, remedy, and pilot questions in this checklist.
  - Does not prove: This is a vendor perspective, not an independent comparison or proof of return on investment.

## Downloads

- [Vendor checklist spreadsheet](https://openjobs.genedai.me/downloads/ai-recruiting-vendor-checklist.csv): Forty-eight procurement questions with evidence requests, red flags, gates, and use-case scope. (text/csv)
- [Vendor question bank](https://openjobs.genedai.me/data/vendor-checklist.json): The same question set as structured JSON for agents, internal tools, and procurement systems. (application/json)
- [Evidence register](https://openjobs.genedai.me/downloads/ai-recruiting-evidence-register.csv): A CSV ledger of source type, jurisdiction, review date, supported use, and limitation. (text/csv)

## Frequently asked questions

### How many vendors should a team compare?

Compare only enough vendors to test materially different approaches and a credible status-quo option. A large list adds work without improving evidence if products solve different stages.

### Should every checklist question receive a numeric score?

No. Use gates for non-negotiable controls and evidence, ordinal scores for maturity, and narrative notes for unresolved transfer or jurisdiction questions.

### Is a security certification enough for AI recruiting procurement?

No. It may support a security-control question, but it does not establish selection validity, accessibility, candidate experience, sourcing quality, or operating outcomes.

### What is the best way to verify a vendor claim?

Define the claim, request the relevant artifact, test it on a buyer-controlled case, inspect failures and exclusions, and record what the result still cannot establish.

## Related evaluation guides

- [AI Recruiting Evaluation Methodology Guide](https://openjobs.genedai.me/methodology)
- [AI Recruiting Pilot Design and Metrics Guide](https://openjobs.genedai.me/pilot-design)
- [Evaluation Scorecard](https://openjobs.genedai.me/evaluation-scorecard)

Relationship disclosure: OpenJobs AI is now [Metix AI](https://metix.ai/about). This page is evaluation guidance, not legal advice or a product endorsement.
