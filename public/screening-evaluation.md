# How to Evaluate AI Candidate Screening Guide

Canonical HTML: https://openjobs.genedai.me/screening-evaluation
Last substantive review: 2026-08-07

> OpenJobs AI is now Metix AI. This archive applies the same evidence rules to Metix first-party material and independent sources.

AI screening evaluation starts with the job, not the model. Define the construct and decision, use structured and inspectable administration, examine validity and error evidence, test accessibility and accommodations, and preserve meaningful human review and contestability.

## Contents

- [Identify what the screening output changes in the hiring process.](#decision-role)
- [Connect every scored dimension to current job evidence.](#job-analysis)
- [Structure the core questions and scoring without erasing necessary accommodation.](#structured-administration)
- [Ask whether the evidence supports the score's intended use.](#validity-reliability)
- [Examine selection impact and error patterns without turning one ratio into a compliance verdict.](#impact-analysis)
- [Test the complete process for accessibility, accommodation, and alternative paths.](#accessibility)
- [Give reviewers evidence, time, authority, and a reason to disagree.](#human-review)
- [Monitor score movement, candidate impact, overrides, and process change together.](#monitoring)

## 1. Identify what the screening output changes in the hiring process.

Screening can mean eligibility questions, resume ranking, work samples, structured interviews, conversational assessment, transcription, summarization, or a recommendation. Write whether the output informs review, orders a queue, advances a person, rejects them, or triggers another assessment. The same model output creates different consequences under different employer use.

Map inputs, generated or inferred features, score or narrative output, thresholds, human reviewers, and downstream status changes. Ask whether a person can be rejected solely from the system, whether a reviewer sees underlying evidence, and whether the candidate can request another path. A human who only confirms a score under time pressure may not provide meaningful oversight.

Determine which jurisdictions, roles, and candidate populations are in scope before applying a legal or professional framework. The NYC AEDT materials and EU AI Act explanations illustrate how definitions and intended purpose matter; this guide does not determine coverage. Record the verified source date and seek qualified advice for the actual deployment.

- **Input.** Resume, application answer, assessment response, audio, video, behavioral data, or inferred feature.
- **Construct.** The job-related knowledge, skill, ability, competency, or eligibility condition intended to be measured.
- **Output.** Score, label, rank, summary, recommendation, explanation, or automatic status change.
- **Consequence.** Review priority, additional test, advance, rejection, communication, or final selection support.

## 2. Connect every scored dimension to current job evidence.

Use a current job analysis to identify important tasks, competencies, context, and minimum qualifications. The OPM job-analysis guidance describes this foundation, while EEOC materials address job-related selection procedures. A generic model score such as "leadership," "culture fit," or "communication" is not self-validating; define the behavior, why it matters for this role, and what evidence can support it.

Distinguish minimum eligibility, trainable skill, preference, and speculative predictor. Avoid treating education, employer prestige, career continuity, accent, facial behavior, typing style, or vocabulary as a competency without a defensible link to the work. Proxy variables can appear objective while measuring access or background rather than ability to perform the job.

Freeze the role version and rubric before evaluating candidates. Record who approved each dimension, how it is weighted or gated, acceptable alternative evidence, and how missing information is handled. Revalidate when duties, level, location, technology, or decision use changes.

1. **Analyze the job.** Identify important tasks, competencies, context, and consequences using current role information.
2. **Define the construct.** Describe the capability in observable terms and separate it from convenient proxies.
3. **Choose evidence.** Specify which answers, work samples, or experiences can support the construct and acceptable alternatives.
4. **Approve the rubric.** Set questions, anchors, thresholds, unknown handling, and reviewer authority before live use.

## 3. Structure the core questions and scoring without erasing necessary accommodation.

Structured interviews use predetermined job-related questions and common rating standards so candidates receive comparable opportunities to provide evidence. An AI conversation can still be structured: define core questions, permitted probes, time behavior, response channels, scoring anchors, and the conditions under which a human follows up.

Consistency is not identical wording at any cost. A reasonable accommodation, clarification, language support, or recovery from a technical failure may require a different path. Record the change and preserve the construct being measured rather than penalizing the candidate for the delivery mechanism. ADA.gov warns against tests that measure disability instead of job skill.

Test prompt and conversation variation. Re-run semantically equivalent responses, order changes, irrelevant details, concise and verbose answers, uncertainty, non-native language patterns, interruptions, and adversarial or nonsensical input. Inspect whether scoring remains anchored to role evidence or drifts toward style, confidence, or demographic proxy.

Table: Structure to define before an AI-assisted screen

| Element | Define | Test |
| --- | --- | --- |
| Question | Job-related purpose, required wording, and allowed clarification. | Whether variants change the construct or candidate opportunity. |
| Probe | When the system may ask for detail and when it must stop. | Over-questioning, leading prompts, and unequal depth. |
| Rating | Behavioral anchors, evidence rules, unknown state, and threshold. | Agreement, borderline cases, and unsupported inference. |
| Delivery | Time, channel, language, accessibility, interruption, and recovery. | Whether interface behavior affects the score. |
| Review | What evidence the human sees and what they can correct or override. | Automation bias, time pressure, and auditability. |

## 4. Ask whether the evidence supports the score's intended use.

Validity concerns the interpretation and use of the screening output for the stated decision. Request the argument connecting job analysis, construct, content, response, scoring, threshold, and relevant outcome. Evidence for one occupation, language, population, or use may not transfer to another. A general LLM benchmark does not validate an employment screen.

Reliability and consistency support but do not replace validity. Test repeated scoring, reviewer agreement, model-version movement, and sensitivity to irrelevant changes. A perfectly consistent measure of the wrong construct remains unsuitable. Conversely, legitimate open-ended evidence can contain uncertainty that should be represented rather than hidden behind excessive decimal precision.

Review the sample and label source. Who decided which answers were strong? Were raters trained and blinded? Were disagreements adjudicated? Are protected or relevant subgroups represented well enough for the reported analysis? Are thresholds chosen before or after seeing outcomes? Request limitations and negative results alongside the aggregate accuracy number.

- **Content evidence.** Does the assessment represent important parts of the work and competency definition?
- **Response process.** Do candidates and the system engage with the question as intended?
- **Internal consistency.** Are ratings and items coherent without collapsing distinct competencies?
- **Relations to outcomes.** Do scores relate to relevant external evidence under an appropriate design?
- **Consequences.** What errors, exclusions, burdens, or adaptations arise from the chosen use?

## 5. Examine selection impact and error patterns without turning one ratio into a compliance verdict.

Review advancement, score, error, and missing-data patterns for relevant groups where lawful, appropriate, and statistically supportable. The Uniform Guidelines and official NYC materials illustrate that impact analysis has defined contexts and methods. A vendor's generic fairness dashboard or one favorable ratio cannot determine compliance for the buyer's use.

Inspect false positives and false negatives alongside selection rates. A system can produce similar aggregate rates while making different kinds of errors or measuring a proxy differently. Examine intersectional and accessibility-sensitive cases where sample design permits, and record when data is unavailable or too sparse for a stable estimate.

Investigate causes across job definition, question content, training data, labels, missingness, interface, transcription, language, scoring model, threshold, reviewer behavior, and downstream use. Mitigation should address the failure rather than tune a number until one report passes. Re-test after mitigation and monitor in operation.

> **Interpretation limit: A bias audit is not a universal approval** Confirm scope, auditor independence, data period, selection process, groups, metrics, exclusions, and whether the audited configuration matches the proposed use.

## 6. Test the complete process for accessibility, accommodation, and alternative paths.

Evaluate the candidate journey from notice through completion, correction, and human contact. Test keyboard use, focus order, labels, status messages, text alternatives, contrast, reflow, time limits, captions or transcripts, screen-reader behavior, error recovery, mobile use, and low bandwidth. WCAG 2.2 provides testable web criteria but does not cover every hiring-process need.

Explain the technology and evaluated information early enough for a candidate to decide whether to request an accommodation. Make the request path easy to find, confidential as appropriate, and operationally staffed. Test that requesting or receiving an accommodation does not itself reduce the score or reveal unnecessary disability-related information to evaluators.

Provide an alternative that measures the same job-related construct when the standard path creates a barrier. Do not simply remove the candidate from consideration or substitute an unrelated test. Technical support is not the same as accommodation ownership, and a chatbot that routes in circles is not a human escalation path.

1. **Inform.** Describe the technology, task, timing, evaluated information, and available support before the screen.
2. **Request.** Offer a clear accommodation route that reaches an accountable person.
3. **Adapt.** Use an accessible or alternative method that preserves the job-related construct.
4. **Verify.** Test the complete adapted journey, scoring, records, and downstream review rather than only the interface.

## 7. Give reviewers evidence, time, authority, and a reason to disagree.

Human review is meaningful when the reviewer understands the system's role, can inspect candidate evidence, knows limitations, has time to evaluate, can change the result, and is accountable for the next action. A mandatory confirmation click or unexplained score does not meet that practical standard.

Design the interface to separate source evidence, model inference, rubric rating, confidence or uncertainty, and final human decision. Ask reviewers to give a reason for material overrides and sample non-overridden cases for automation bias. Monitor whether reviewers increasingly accept recommendations without reading evidence as volume grows.

Give candidates and internal users routes to contest, correct, or escalate consequential errors. Preserve the original output and the corrected record so the organization can learn without leaving harmful data active. Communicate outcomes and limits in language appropriate to the process; do not expose proprietary internals when a clear job-related explanation is possible.

- **Evidence access.** The reviewer can trace a rating or recommendation to the candidate response and rubric.
- **Decision authority.** The reviewer can correct, override, pause, or request another method.
- **Time and training.** The workflow does not turn review into rubber-stamping under an unrealistic queue.
- **Contestability.** Candidate and user concerns reach an owner and can change relevant records or actions.

## 8. Monitor score movement, candidate impact, overrides, and process change together.

After deployment, monitor score distributions, advancement, error samples, reviewer disagreement, overrides, missing data, accommodation use, technical failures, candidate feedback, completion, and downstream interview evidence. Segment by role, version, language, channel, and other relevant dimensions where analysis is lawful and supported.

Version prompts, questions, rubrics, thresholds, models, transcription, interface, and integrations. A vendor update can change candidate opportunity even when the product name is unchanged. Establish change notification and re-testing triggers in the agreement and operating process.

Create incident paths for inaccessible sessions, incorrect status changes, corrupted or exposed data, repeated questions, unsupported inferences, group performance concerns, and candidate complaints. Preserve evidence, contain impact, correct records, communicate with affected people where appropriate, and decide whether the system may resume under narrower controls.

Table: Screening monitoring signals and investigation questions

| Signal | Investigate | Possible action |
| --- | --- | --- |
| Score distribution shift | Role mix, model, rubric, prompts, language, data, and candidate population. | Pause threshold use, sample cases, or revalidate. |
| Override change | Reviewer training, queue pressure, system quality, and automation bias. | Review cases, interface, staffing, and rubric. |
| Completion or accommodation issue | Interface, notice, timing, support, alternative path, and downstream scoring. | Fix access, offer reassessment, and limit exposure. |
| Group or error concern | Sample, labels, missing data, threshold, construct, and workflow use. | Escalate qualified review, contain use, and retest. |
| Integration incident | Incorrect writes, retries, duplicates, permissions, and audit trail. | Disable writes, reconcile records, and use fallback. |

## Sources and evidence limits

- **Government Guidance: [U.S. Equal Employment Opportunity Commission: Employment Tests and Selection Procedures](https://www.eeoc.gov/laws/guidance/employment-tests-and-selection-procedures)**
  - Supports: Technical assistance on job-related selection procedures, discriminatory impact, validation, and employer responsibility.
  - Does not prove: The page describes federal considerations but does not determine whether a specific tool, employer, or use is lawful.
- **Binding Rule: [Electronic Code of Federal Regulations: 29 CFR Part 1607: Uniform Guidelines on Employee Selection Procedures](https://www.ecfr.gov/current/title-29/subtitle-B/chapter-XIV/part-1607)**
  - Supports: The federal text governing documentation, impact, and validity evidence for covered employee selection procedures.
  - Does not prove: Reading the regulation does not resolve coverage, statistical sufficiency, defenses, or obligations in a particular matter.
- **Government Guidance: [ADA.gov, U.S. Department of Justice: Algorithms, Artificial Intelligence, and Disability Discrimination in Hiring](https://www.ada.gov/resources/ai-guidance/)**
  - Supports: Guidance on disability-related screening risk, accommodations, accessibility, notice, and measuring job skills rather than disability.
  - Does not prove: The informal guidance is not a final agency action and cannot decide whether a particular process complies with the ADA.
- **Professional Practice: [U.S. Office of Personnel Management: Job Analysis](https://www.opm.gov/policy-data-oversight/assessment-and-selection/job-analysis/)**
  - Supports: A practical account of job analysis as the foundation for defining tasks, competencies, and assessment content.
  - Does not prove: Federal personnel practice does not by itself validate a private-sector role brief or every automated assessment.
- **Professional Practice: [U.S. Office of Personnel Management: Structured Interviews](https://www.opm.gov/policy-data-oversight/assessment-and-selection/structured-interviews/)**
  - Supports: Guidance on using predetermined job-related questions, consistent administration, and common rating standards.
  - Does not prove: Structure improves comparability but does not guarantee validity, fairness, accessibility, or a correct hiring decision.
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
- **First-party research: [When AI Meets Recruiting: Opportunities, Challenges, and Future Directions](https://metix.ai/research/ai-meets-recruiting)**
  - Context: The Metix literature review maps sourcing, matching, and assessment across a recruitment lifecycle and identifies bias, explainability, feedback, and oversight as open deployment questions.
  - Does not prove: This first-party review does not validate a screening construct, product, employer process, or legal outcome.

## Downloads

- [Evidence register](https://openjobs.genedai.me/downloads/ai-recruiting-evidence-register.csv): A CSV ledger covering selection guidance, accessibility, public rules, standards, and first-party research. (text/csv)

## Frequently asked questions

### Is resume ranking an employment selection procedure?

Its treatment depends on the facts, jurisdiction, definitions, and how the employer uses it. Record the actual decision effect and obtain qualified advice rather than relying on a product label.

### Does consistent AI scoring prove the screen is valid?

No. Consistency can support reliability, but validity requires evidence that the score interpretation and use relate appropriately to the job and decision.

### Is WCAG conformance enough for an accessible screening process?

No. WCAG addresses web content. The full process also needs timely notice, accommodation handling, suitable alternatives, human support, and downstream treatment.

### Can a human reviewer fix every AI screening risk?

No. Review can help only when the person has evidence, competence, time, authority, and a functioning correction path. Some unsuitable constructs or inaccessible methods should not be used.

## Related evaluation guides

- [How to Evaluate AI Candidate Sourcing and Ranking](https://openjobs.genedai.me/sourcing-evaluation)
- [AI Recruiting Pilot Design and Metrics Guide](https://openjobs.genedai.me/pilot-design)
- [AI Recruiting Agent Reliability Evaluation](https://openjobs.genedai.me/agent-reliability)

Relationship disclosure: OpenJobs AI is now [Metix AI](https://metix.ai/about). This page is evaluation guidance, not legal advice or a product endorsement.
