# Project Explanation: Assessing the Credibility of Organisational Knowledge from Fragmented Data

## 1. Executive summary

This repository is the starting point for a university capstone project about **how an organisation can decide whether a knowledge claim is credible when its evidence is incomplete, outdated, duplicated, or contradictory**.

The project is not yet a working software system. At the current stage, the repository contains:

- the project brief and team administration documents;
- a deliberately imperfect, fictional organisational dataset for **Northfield Software Ltd**;
- four sample labelled claims showing the expected claim representation; and
- early planning material for a future claim-extraction, evidence-linking, credibility-scoring, and evaluation pipeline.

The intended outcome is an **explainable assessment framework**, not a black-box true/false classifier. For each organisational claim, the framework should expose the evidence for and against it, account for source quality and time, distinguish formal rules from actual practice, quantify confidence where appropriate, and allow a claim to remain unresolved when the evidence is insufficient.

## 2. The central research problem

Organisations distribute knowledge across policies, process documents, interviews, communications, and operational systems. A statement can appear authoritative without being current or followed in practice. Conversely, an informal statement may describe real practice accurately while having no formal authority.

The project's core research question is:

> Given multiple, incomplete, and potentially conflicting data points, how should the credibility of an organisational knowledge claim be assessed?

An example is the claim that Finance approves every new-business discount at or above 15%. The approved policy supports this rule, but interviews reveal an informal urgent-deal workaround, and an older process document names a different Finance role as approver. A useful system must preserve all of those distinctions rather than simply choosing whichever document looks most official.

## 3. Current repository state

As of this snapshot, this is primarily a **research and dataset repository**, not an implemented application:

- There is no `src/`, notebook, test suite, dependency manifest, executable pipeline, model, database, or user interface in the checked-in files.
- The root `README.md` contains only the repository title.
- `project_description.md` contains the substantive project brief.
- `phase1_framework_development/` contains the Phase 1 evidence corpus.
- `Docs/` contains the group charter, an initial meeting record, and one Week 2 individual report.

The Week 2 report says the repository was created and organised to unblock collaboration, while technical implementation and the precise definition of an extractable claim were still being scoped. Any architecture described below is therefore the direction implied by the brief and role assignments, not code that already exists.

## 4. The fictional organisation used as the case study

Northfield Software Ltd is a fictional, privately held software company founded in 2020. It sells **Northfield OS**, a scheduling, compliance-tracking, and invoicing platform for trades and facilities-services businesses with roughly 5–200 field employees.

The dataset describes the organisation as at **31 July 2026** and covers activity from **1 August 2025 to 31 July 2026**. Northfield has 29 people across five functions:

1. Leadership
2. Sales
3. Customer Success & Delivery
4. Engineering & Product
5. Finance & People Ops

The evidence focuses on eight business processes:

| Code | Process | Main functions |
|---|---|---|
| P1 | Customer discount approval | Sales, Finance |
| P2 | Customer onboarding / implementation | Customer Success & Delivery |
| P3 | Product change / feature request intake | Engineering & Product |
| P4 | Expense approval | Finance & People Ops |
| P5 | Support escalation | Customer Success & Delivery, Engineering & Product |
| P6 | New-hire onboarding | People Ops |
| P7 | Invoicing and collections | Finance & People Ops |
| P8 | Contract renewal and churn-risk review | Sales, Customer Success & Delivery |

The company materials are intentionally inconsistent. That imperfection is the experimental material for the credibility framework, not a dataset-quality accident.

## 5. What each repository area contributes

### Root files

- `README.md`: repository name only; it does not yet onboard a contributor.
- `project_description.md`: defines the problem, research question, permissible technical approaches, and expected skills.
- `.gitignore`: ignores macOS `.DS_Store` files.

### `phase1_framework_development/00_overview/`

This folder supplies organisational context needed to interpret evidence:

- `company_overview.md` defines Northfield, the dataset period, and the eight processes.
- `org_chart_and_roster.md` gives reporting lines, roles, start dates, tenure, remote status, and one departure.
- `role_descriptions.md` maps relevant roles to responsibilities, system access, process participation, decision rights, and missing backups.
- `decision_rights_table.md` compares formal authority with observed practice and highlights undocumented or ambiguous ownership.

These are useful both as evidence and as entity-resolution context. For example, they let a pipeline connect “Harriet,” “Head of Finance & People Ops,” and “discount approver” to the same person and organisational role.

### `phase1_framework_development/02_policies/`

The seven policy files express formal or proposed rules:

- **POL-01:** new-business discounts of **15% or greater** require prior approval from the Head of Finance & People Ops and a CRM approval record.
- **POL-03:** standard customer onboarding takes six weeks, is assigned to an Implementation Specialist, and ends with checklist completion and Support handover. It permits complex-account extensions but does not name the approver.
- **POL-04:** an explicitly unapproved draft proposing direct Slack escalation for Severity 1 issues followed by a retrospective ticket.
- **POL-05:** permits temporary customer-data exports to personal devices for offline work if deleted within 24 hours; its review is overdue.
- **POL-06:** caps renewal discounts at 10% and gives the responsible Account Executive the decision, in consultation with Customer Success.
- **POL-07:** expenses over $500 require approval from the Head of Finance & People Ops; smaller claims may be approved by the direct manager.
- **POL-08:** new hires must complete a checklist within two weeks, and the People Ops Lead is the sole probation approver.

Document metadata such as owner, version, approval status, effective date, review date, applicability, and supersession is critical evidence. A draft, an expired review date, and an approved current policy should not receive identical treatment.

### `phase1_framework_development/03_process_docs/`

The seven process documents describe operational triggers, steps, roles, inputs, outputs, systems, approvals, timing, and exceptions:

- **PROC-01:** six-week onboarding from Closed Won to Support handover.
- **PROC-02:** discount approval, but it is old and incorrectly names the Financial Controller rather than the current policy's Head of Finance & People Ops.
- **PROC-03:** feature requests enter via Trello, receive P1–P4 priority, and require Engineering sign-off for P1 sprint entry.
- **PROC-04:** expense submission and approval through a shared spreadsheet, while noting an undocumented standing travel exception.
- **PROC-05:** the formally approved ticket-first support escalation path, while acknowledging that Severity 1 issues often go directly to engineers in Slack.
- **PROC-06:** invoice generation after both Closed Won and onboarding completion, followed by 15-, 30-, and 45-day collection actions.
- **PROC-07:** renewal and churn-risk handling, but with no accountable owner or tie-breaker when Sales and Customer Success disagree.

### `phase1_framework_development/04_interviews/`

The three interviews provide first-hand but subjective evidence:

- **Diane Okafor, Head of Sales:** states the formal Finance approval rule, then admits that urgent deals may proceed on her informal approval with Finance reconciled later.
- **Callum Reyes, Senior Account Executive:** initially claims there are no exceptions, but becomes uncertain when asked about a Slack-based approval on his own deal.
- **Adaeze Nwosu, Implementation Specialist:** confirms the normal six-week flow while describing invisible email work, an outdated local checklist, informal timeline approvals, direct Engineering contact, and implicitly pre-approved onboarding travel.

The interviews demonstrate why credibility assessment must consider firsthand knowledge, role competence, specificity, uncertainty, possible self-interest, internal consistency, and corroboration.

### `phase1_framework_development/labelled_claims_sample.csv`

The CSV supplies four example records with this schema:

- claim identifier and category;
- canonical claim text;
- reference status;
- validity interval;
- responsible role;
- known exceptions;
- expected supporting and contradictory sources; and
- difficulty level.

All four examples are labelled “Formal truth.” They demonstrate data shape, not a complete training or evaluation set. Several cited sources are not included in the current release, reinforcing that Phase 1 is partial.

### `Docs/`

- The group charter defines a six-person team, communication channels, a weekly Wednesday meeting, a 24-hour response expectation, and technical ownership.
- The 5 August 2026 meeting record documents initial setup tasks: GitHub, Slack, the charter, meeting records, and resolution of a timetable clash.
- Nakul Sidiginamola's Week 2 report records repository setup and plans to scope claim extraction and NLP requirements.

The assigned project leads are:

| Person | Responsibility |
|---|---|
| Kushal Joshi | Documentation, visualisation, and coordination |
| Bhavika Lalwani | Data and evidence pipeline |
| Rohan Chaudhary | Evidence linking and retrieval |
| Nakul Sidiginamola | Claim extraction and NLP |
| Shreyash Narayane | Bayesian/probabilistic credibility modelling |
| Prathamesh Nemade | Calibration and evaluation |

## 6. The important evidence conflicts

The following conflicts are likely intended as test cases for the framework:

### Formal rule versus real practice

- New-business discounts at or above 15% formally need prior Finance approval in the CRM, but the Head of Sales sometimes authorises urgent deals first and reconciles later.
- Support escalation is formally ticket-first, but Severity 1 incidents often begin in Slack. An unapproved draft partially formalises this practice.
- Expenses over $500 formally need Finance approval, but managers sometimes pre-approve them informally and onboarding travel is treated as a standing exception.
- Six-week onboarding is formal, but extensions are informally cleared with Helena Cho and much customer-contact effort is not recorded in the project system.

### Current policy versus stale process documentation

- POL-01 v3 names the Head of Finance & People Ops as discount approver, while the older PROC-02 names the Financial Controller.
- PROC-03 still names Trello, while current Product Manager role descriptions name Linear. This suggests tool migration or stale documentation.

### Assigned responsibility versus genuine governance gap

- No role has formal tie-breaking authority when Sales and Customer Success disagree on renewal strategy.
- No formal owner approves onboarding timeline extensions.
- The Product/Engineering boundary between prioritisation and technical feasibility is incompletely documented.
- The QA Lead's authority to block a release is not defined.
- Critical roles lack backups, including billing-integration knowledge and deployment sign-off.

### Formal policy versus exceptions or edge cases

- Renewal discounts are capped at 10% with no exceptions, but the decision-rights table says at least one undocumented exception occurred.
- The new-hire policy assumes in-person onboarding despite two remote engineers.
- The data-export policy is overdue for review and allows personal-device exports, so “approved” does not automatically mean “current and low-risk.”

### Wording and boundary inconsistencies

- POL-01 says **15% or greater**, while the sample claim and several role summaries say **above 15%**. A 15% discount is therefore a boundary-value test: a literal system could incorrectly treat it as not requiring approval.

These examples show that credibility is multidimensional. A claim may be formally valid but operationally violated, descriptively accurate but unauthorised, historically true but no longer current, or too broadly worded to be defensible.

## 7. A suitable definition of an organisational knowledge claim

A practical definition for this project is:

> An organisational knowledge claim is a specific, testable proposition about the organisation's rules, responsibilities, processes, systems, events, people, or operating practices, scoped to a relevant time period and context.

A useful canonical claim should normally identify:

- **subject:** who or what the claim concerns;
- **predicate:** the asserted relationship, action, state, or obligation;
- **object/value:** the other entity, threshold, status, or outcome;
- **modality:** must, may, usually, did, owns, approves, and so on;
- **scope:** new business versus renewals, Severity 1 versus all issues, remote versus all staff;
- **time:** effective date or observation period;
- **provenance:** source and precise source location; and
- **exceptions/qualifiers:** known conditions under which the statement changes.

For example, “Finance approves discounts” is too vague. A defensible canonical version is: “For new-business deals from 1 March 2025, discounts of 15% or greater require written approval from the Head of Finance & People Ops before Closed Won, recorded in the CRM approval field.”

## 8. Proposed end-to-end framework

The brief permits retrieval, knowledge graphs, probabilistic methods, LLM-assisted analysis, or hybrids. A sensible explainable hybrid pipeline would be:

1. **Ingest and preserve documents**
   - Parse Markdown, CSV, DOCX, PDF, and later-phase sources.
   - Retain document identifiers, owners, versions, dates, approval states, headings, and exact source spans.

2. **Normalise entities and time**
   - Resolve people, roles, process codes, policy codes, systems, thresholds, and dates.
   - Preserve role-at-time rather than assuming the current org chart applies historically.

3. **Extract candidate claims**
   - Use rules and/or an LLM to convert source passages into atomic propositions.
   - Split compound statements and retain modality, negation, quantities, temporal scope, and exceptions.
   - Require every extracted claim to link back to its source text.

4. **Canonicalise and cluster claims**
   - Group semantically equivalent claims while preserving meaningful differences such as “above 15%” versus “15% or greater,” policy versus observed practice, and new business versus renewal.

5. **Retrieve and link evidence**
   - For every claim, locate supporting, contradicting, qualifying, and context-only evidence.
   - Record the relationship type explicitly rather than treating all retrieved passages as support.

6. **Assess each evidence item**
   - Score or describe authority, approval status, recency, temporal applicability, source proximity, specificity, independence, internal consistency, corroboration, and completeness.
   - Treat source type as one feature, not an absolute hierarchy. An approved policy is strongest for what should happen; an operational record may be strongest for what did happen.

7. **Aggregate credibility and uncertainty**
   - Combine evidence through a transparent weighted model, Bayesian model, or both.
   - Keep separate dimensions for formal validity and observed adherence when the question demands it.
   - Return calibrated probabilities or bands, plus an unresolved state where evidence is inadequate.

8. **Generate an explanation**
   - Show the canonical claim, scope, status, supporting evidence, contradictions, exceptions, source weights, calculation, confidence, and the evidence that would most reduce uncertainty.

9. **Evaluate and calibrate**
   - Compare predictions with a larger expert-labelled reference set.
   - Measure extraction accuracy, evidence-link precision/recall, classification performance, probability calibration, explanation quality, and sensitivity to modelling assumptions.

Human review should remain available at claim extraction, evidence classification, and final adjudication, especially for ambiguous scope or high-impact claims.

## 9. A possible credibility model

The team could score each evidence item on dimensions such as:

| Dimension | Question |
|---|---|
| Authority | Is the source authorised to define or know this matter? |
| Approval/status | Is it approved, draft, superseded, or informal? |
| Recency | Is it current enough for the claim's time? |
| Directness | Is it a firsthand record or hearsay? |
| Specificity | Does it address the exact threshold, actor, process, and scope? |
| Independence | Is it genuinely separate evidence or copied from another source? |
| Corroboration | Do independent sources agree? |
| Consistency | Is the source internally consistent and appropriately qualified? |
| Completeness | Are important records or perspectives missing? |

Each item would also receive a stance such as **supports**, **contradicts**, **qualifies**, or **context only**. One illustrative aggregation is a weighted log-odds update:

```text
posterior_log_odds
  = prior_log_odds
  + sum(evidence_reliability × stance_strength × independence_discount)
```

This is only a design option. The important requirement is that weights are justified, dependence between sources is not double-counted, results are tested through sensitivity analysis, and the displayed confidence is calibrated against held-out labels.

A useful output taxonomy could include:

- **Strongly supported**
- **Supported with exceptions**
- **Formally valid but weakly followed**
- **Contested**
- **Outdated/superseded**
- **Insufficient evidence / unresolved**

This is richer and more useful than a single “true” or “false” label.

## 10. Worked example from the corpus

Consider the claim:

> New-business discounts of 15% or greater require approval from the Head of Finance & People Ops before the deal closes, with the approval recorded in the CRM.

Evidence assessment:

- **POL-01 v3 strongly supports it:** approved, current for the dataset period, specific, and owned by the named approver.
- **The role descriptions and Diane's interview support the formal rule.**
- **PROC-02 partially conflicts:** it describes the same process but names the Financial Controller; its 2022 date makes it stale relative to the 2025 policy.
- **Diane's interview contradicts universal adherence:** she describes urgent deals that proceed before formal Finance approval.
- **Callum's interview initially supports universal adherence but weakens under a specific challenge**, suggesting limited knowledge or overconfidence.

A good output would therefore avoid one undifferentiated answer:

- **Formal validity:** high.
- **Confidence that the rule is followed without exception:** materially lower.
- **Overall explanation:** current formal rule, known informal workaround, and stale procedural documentation.

## 11. Evaluation strategy

The project should evaluate the full pipeline rather than only the final credibility label:

### Claim extraction

- Precision, recall, and F1 for identifying claim-bearing passages.
- Accuracy of subject, predicate, object, threshold, negation, modality, time, and exception extraction.
- Error analysis for compound claims and vague language.

### Evidence retrieval and stance

- Recall@k and mean reciprocal rank for relevant evidence retrieval.
- Precision/recall for support, contradiction, qualification, and context labels.
- Tests for entity aliases, outdated documents, and missing references.

### Credibility judgement

- Accuracy or macro-F1 over expert status labels.
- Brier score, log loss, expected calibration error, and reliability diagrams for probabilities.
- Coverage-risk analysis for an abstain/unresolved option.
- Sensitivity tests showing how results change when source weights or priors change.

### Explainability and human usefulness

- Whether reviewers can trace every conclusion to exact evidence.
- Whether explanations identify major conflicts and exceptions.
- Inter-rater agreement and time-to-decision with and without the framework.

The four-row sample CSV is far too small for meaningful quantitative evaluation. A larger labelled set, an annotation guide, double annotation, disagreement resolution, and a train/development/test split will be needed.

## 12. Risks and methodological pitfalls

- **Automation bias:** an articulate LLM explanation can sound more certain than its evidence warrants.
- **Circular evidence:** role tables, summaries, and policies may derive from one another and must not be counted as independent confirmations.
- **Authority confusion:** a policy proves a formal requirement, not that employees complied with it.
- **Temporal leakage:** a newer policy must not be applied to an older event without checking effective dates.
- **Retrieval bias:** missing contradictory evidence can create falsely high confidence.
- **Boundary loss:** normalisation can erase meaningful distinctions such as `>15%` versus `>=15%`.
- **Subjectivity in weights:** credibility dimensions and priors require documentation and sensitivity analysis.
- **Label ambiguity:** “formal truth” is not the same as “descriptively true in every observed case.”
- **Privacy and governance:** later real-world data could contain personal or customer information and require access controls and careful retention.

## 13. Gaps and inconsistencies in the current repository

The following observations matter for anyone continuing the work:

- The Phase 1 README says a superseded 2023 org chart is included, and the current org chart links to it, but that file/directory is absent.
- The labelled sample cites `INT-03`, `INT-07`, `INT-08`, `MTG-01`, and `COMMS-12`, none of which are present in this release. Other documents mention `MTG-04` and `MTG-05`, also absent.
- Policy numbering skips POL-02 because POL-01 says it supersedes an earlier POL-02; that historical document is not present.
- Process coverage has no separate PROC document for P6 new-hire onboarding; only POL-08 covers it.
- The corpus says Northfield has 29 employees but the roster table contains 30 named people and then states that Wei Zhang left during the period. This can be reconciled as 29 employees at period end, but automated counts must use employment dates.
- The roster calls Wei Zhang one of the remote engineers even though he left before period end; temporal representation is necessary.
- PROC-03 uses Trello while the Product Manager role description says Linear is current.
- The root README is too minimal to explain setup, structure, contribution expectations, or project status.
- `.DS_Store` files are already committed even though `.gitignore` excludes them going forward.
- The Week 2 report refers to standard `src`, `data`, and `notebooks` folders, but those folders are not present in the current checked-in snapshot.

Some missing sources may be intentional because the Phase 1 README says further materials will arrive later. The framework should treat “not in the current release” as missing evidence, not as evidence that the referenced source does not exist.

## 14. Recommended next steps

1. Define an annotation guide for atomic claims, scope, time, modality, exceptions, evidence stance, and credibility status.
2. Expand the labelled dataset beyond four low-difficulty formal claims and include contradictions, outdated claims, informal practices, and unresolved cases.
3. Add stable document and passage identifiers so every prediction is traceable.
4. Create the implementation structure described in the weekly report: ingestion, extraction, entity resolution, retrieval, scoring, evaluation, notebooks, and tests.
5. Build a simple rule-based baseline before introducing embeddings or LLMs.
6. Implement a transparent evidence table and an initial weighted/Bayesian model with sensitivity analysis.
7. Separate formal validity, observed adherence, and overall confidence in the data model and interface.
8. Define evaluation metrics and a held-out test set before tuning the credibility model.
9. Improve the root README with installation, dataset, architecture, workflow, and contribution guidance once implementation begins.
10. Track dataset releases explicitly so intentionally withheld Phase 2/3 sources are distinguishable from broken references.

## 15. Bottom line

This project is trying to turn fragmented organisational evidence into **traceable, calibrated, and defensible knowledge claims**. The Northfield corpus is a controlled testbed designed to make simplistic approaches fail: official documents can be stale, interviews can be overconfident, informal workarounds can be real but unauthorised, and some questions genuinely have no settled answer.

The strongest eventual solution will not merely output a credibility score. It will show exactly what the claim means, which evidence supports or challenges it, why each source was weighted as it was, how time and exceptions affect the judgement, how sensitive the result is to assumptions, and when the responsible answer is “unresolved.”
