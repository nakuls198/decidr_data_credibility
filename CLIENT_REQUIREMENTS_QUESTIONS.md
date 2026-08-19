# Client Requirements Questions

## Purpose

This document is a structured question set for clarifying the requirements of the **Assessing the Credibility of Organisational Knowledge from Fragmented Data** project. It is intended to help the team confirm the problem definition, expected outputs, dataset assumptions, evaluation criteria, technical constraints, and delivery expectations before committing to a design.

Questions marked **Priority** should be answered first because they can materially change the scope or architecture of the project.

## 1. Problem definition and project scope

1. **Priority:** What is the main outcome you expect from this project: a research framework, a working prototype, an evaluated model, an interactive application, or a combination of these?
2. **Priority:** Who is the intended end user of the framework: knowledge managers, compliance teams, executives, auditors, general employees, or researchers?
3. **Priority:** What decisions should the framework help those users make?
4. What is the most important problem the client wants the project to solve?
5. Is the project primarily about assessing whether a claim is true, whether it is formally authorised, whether it is followed in practice, or all three?
6. Should the framework assess only current organisational knowledge, or also historical claims and changes over time?
7. Should we focus only on the eight Northfield business processes, or design a general framework that can transfer to other organisations and domains?
8. Are there any claim categories that must be included or excluded—for example, policies, responsibilities, process steps, system states, events, or employee opinions?
9. What would make the project unsuccessful even if the technical prototype works?
10. Are there any approaches the client specifically wants us to investigate or avoid?

## 2. Definition of a knowledge claim

11. **Priority:** How does the client define an “organisational knowledge claim”?
12. **Priority:** Should a claim be a single atomic proposition, or may it contain multiple related statements?
13. Should claims include normative statements about what **should** happen, descriptive statements about what **does** happen, and historical statements about what **did** happen?
14. Should the framework distinguish explicitly between formal truth and observed operational practice?
15. How should claims with vague language such as “usually,” “often,” “promptly,” or “significant” be represented?
16. How should the framework handle exact boundary differences, such as “above 15%” versus “15% or greater”?
17. Must every claim include a validity period, responsible role, organisational scope, and known exceptions?
18. Should the system generate claims automatically, allow users to submit claims manually, or support both?
19. At what level of detail should claims be extracted—for example, one claim per sentence, policy requirement, process step, or decision right?
20. Should duplicate or semantically equivalent claims be merged into one canonical claim while preserving their original wording and sources?

## 3. Meaning of credibility

21. **Priority:** What does “credible” mean for this project, and how is it different from “true,” “authoritative,” “current,” or “well-supported”?
22. **Priority:** Should credibility be represented as a numerical probability, a score, a category, a multidimensional profile, or some combination?
23. Should the framework produce separate assessments for:
    - formal validity;
    - actual adherence in practice;
    - evidence quality;
    - confidence or uncertainty; and
    - overall credibility?
24. What result labels should the system use—for example, strongly supported, supported with exceptions, contested, outdated, contradicted, or unresolved?
25. Should the system be allowed to abstain or return “insufficient evidence” rather than forcing a conclusion?
26. Are some errors more serious than others—for example, accepting a false compliance claim versus leaving a true claim unresolved?
27. Is the goal to rank claims by credibility, classify them, estimate probabilities, or support a human reviewer without making the final decision?
28. How should undocumented but consistently followed practices be assessed relative to approved policies?
29. How should an approved but overdue, outdated, or frequently violated policy affect the credibility of a claim?
30. Should the system recommend corrective actions when formal rules and actual practice disagree?

## 4. Evidence and source treatment

31. **Priority:** Which source types will be supplied in later phases—policies, emails, meeting records, chat messages, system logs, tickets, spreadsheets, interviews, or other formats?
32. **Priority:** Is there an expected source-authority hierarchy, or should the team develop and justify one?
33. Which evidence attributes should influence credibility: approval status, ownership, recency, directness, specificity, independence, corroboration, or others?
34. Should a formal policy automatically outweigh interviews and operational records, or should weighting depend on the type of claim being assessed?
35. How should the system distinguish evidence that supports, contradicts, qualifies, or merely provides context for a claim?
36. Should missing evidence reduce confidence, or should it be treated neutrally unless a record was expected to exist?
37. How should we identify sources that are copied from, summarise, or depend on one another so they are not double-counted?
38. Should employee seniority, role relevance, firsthand involvement, expressed uncertainty, or possible self-interest affect interview evidence weight?
39. Should users be able to override source weights or evidence classifications?
40. Must every result link to the exact source passage, page, table row, message, or system record that influenced it?
41. What should happen when two formally approved documents contradict each other?
42. What should happen when the latest document is less authoritative than an older approved document?

## 5. Dataset and ground truth

43. **Priority:** When will the remaining phases of the dataset be released, and what types and approximate volumes of records will they contain?
44. **Priority:** Will the client provide a complete labelled reference set, or is creating the labels part of the team's work?
45. Are the currently missing references—such as `INT-03`, `INT-07`, `INT-08`, `MTG-01`, `MTG-04`, `MTG-05`, and `COMMS-12`—intentionally reserved for later releases?
46. Is the missing superseded 2023 org chart expected in a later release, or should we report it as a dataset defect?
47. Are all Northfield materials fictional and safe to process using third-party or hosted AI services?
48. Will later data contain personal, confidential, commercially sensitive, or legally regulated information?
49. Will there be a fixed train/development/test split, or should the team create one?
50. Who determines the authoritative reference status when reasonable experts disagree?
51. Will claims be labelled by more than one person so inter-rater agreement can be measured?
52. Is there an annotation guide already, or should the team design one?
53. Should the framework be evaluated only on the supplied dataset or also on team-created edge cases and adversarial examples?
54. May the team correct apparent inconsistencies in the source corpus, or must the original files remain unchanged as evidence?
55. Will the final system need to ingest new documents incrementally after the initial dataset is processed?

## 6. Expected system behaviour

56. **Priority:** What are the minimum capabilities required in the final demonstration?
57. Should a user be able to enter a claim and retrieve an assessment, or should the system first discover all claims in a collection automatically?
58. Should the system process one claim at a time, an entire document collection, or both?
59. Should newly added evidence automatically trigger reassessment of affected claims?
60. Should the system detect changes in validity over time and preserve previous assessments?
61. Should users be able to search and filter by claim category, process, role, status, date, or confidence?
62. Should the interface display an evidence graph, evidence table, written explanation, confidence visualisation, or all of these?
63. Should users be able to accept, reject, edit, or annotate extracted claims and evidence links?
64. Should the system show why two sources are considered contradictory rather than simply flagging a conflict?
65. Should the system identify the missing evidence that would most reduce uncertainty?
66. Should the prototype generate reports or export results to formats such as CSV, JSON, PDF, or Markdown?
67. Is multilingual content within scope?
68. Are scanned documents, images, handwriting, audio, or video within scope, or only machine-readable text?

## 7. Explainability and human oversight

69. **Priority:** What level of explanation is required for a result to be considered defensible?
70. Who must be able to understand the explanation: technical reviewers, domain experts, executives, or all of them?
71. Should the system expose the full scoring calculation and source weights?
72. Should explanations include alternative interpretations and sensitivity to modelling assumptions?
73. Must a human approve every extracted claim and final assessment, or only low-confidence/high-risk cases?
74. Should the system record all human edits and overrides for auditability?
75. How should the framework communicate uncertainty without overwhelming a non-technical user?
76. Does the client want natural-language explanations generated by an LLM, deterministic explanation templates, or both?
77. Should explanations cite only supplied evidence, with no use of external knowledge?

## 8. Technical expectations and constraints

78. **Priority:** Are there required technologies, languages, models, databases, or platforms?
79. **Priority:** Are external APIs and hosted LLMs permitted, or must processing run locally?
80. Is there a preferred approach among information retrieval, knowledge graphs, Bayesian modelling, explainable machine learning, LLM-assisted analysis, or a hybrid?
81. Does the client expect the use of a knowledge graph, or is it only one optional implementation choice?
82. Must the system work without internet access?
83. Are there cost limits for model/API usage during development and demonstration?
84. Are there minimum performance targets for processing time, response time, or dataset size?
85. Must results be reproducible when the same data and configuration are used again?
86. Should model versions, prompts, retrieval settings, priors, and evidence weights be version-controlled?
87. Is integration with any existing platform, document store, database, or identity system required?
88. What deployment environment is expected: a local notebook, command-line tool, web application, university server, or cloud service?
89. Does the client require automated tests, continuous integration, containerisation, or a deployment script?
90. Are there accessibility or browser/device compatibility requirements for a user interface?

## 9. Privacy, security, ethics, and governance

91. **Priority:** What privacy, security, data-retention, and data-residency requirements apply?
92. May project data be uploaded to third-party AI, embedding, or storage services?
93. Must sensitive fields be removed, masked, or pseudonymised before processing?
94. What access-control roles are required if the prototype has multiple users?
95. Should users see all evidence, or can some source material be restricted while its effect on a result remains visible?
96. How long should source data, extracted claims, model outputs, and audit logs be retained?
97. Are there ethical requirements for detecting or mitigating bias against particular employees, roles, or departments?
98. Should the framework flag potentially harmful source policies separately from assessing whether claims about them are credible?
99. Who is accountable for approving a high-impact conclusion produced by the system?
100. Are there legal, compliance, or university ethics approvals that must be completed before using later-phase data?

## 10. Evaluation and acceptance criteria

101. **Priority:** What specific criteria will the client use to decide that the project has succeeded?
102. **Priority:** Which component matters most in evaluation: claim extraction, evidence retrieval, credibility judgement, calibration, explainability, usability, or generalisability?
103. Is there a target level for precision, recall, F1, accuracy, or retrieval recall?
104. Should probabilistic outputs be evaluated using Brier score, log loss, expected calibration error, or another calibration measure?
105. How should unresolved/abstained cases be scored?
106. Should evaluation distinguish low-, medium-, and high-difficulty claims?
107. Should the team compare several approaches, such as rules, retrieval plus heuristics, Bayesian modelling, and LLM-based assessment?
108. Is a simple baseline required to demonstrate the value added by the final method?
109. Who will perform the qualitative review of explanations, and what rubric should they use?
110. Should the project measure whether the framework improves human decision accuracy, consistency, or review time?
111. How important is generalisation beyond Northfield relative to performance on the supplied corpus?
112. Are robustness, adversarial, sensitivity, and ablation tests expected?

## 11. Deliverables and documentation

113. **Priority:** What exact deliverables are expected, and in what formats?
114. Is the team expected to deliver source code, notebooks, trained models, labelled data, an application, an API, a report, a presentation, and a demonstration?
115. Is a formal requirements specification expected before implementation?
116. What level of technical documentation is required for installation, architecture, data schema, model methodology, testing, and maintenance?
117. Is a user guide required for non-technical users?
118. Should the final report include rejected approaches and negative experimental results?
119. Are there required report templates, page limits, citation styles, or marking rubrics?
120. Should the team provide a reproducible experiment package so the client can rerun all results?
121. Who will own the code, data transformations, annotations, and generated artefacts after completion?
122. May the team publish the repository, methodology, results, or screenshots in a portfolio or academic paper?

## 12. Timeline, communication, and change management

123. **Priority:** What are the key milestones, review dates, and final delivery date?
124. Which decisions must be approved by the client before the team proceeds to implementation?
125. Who is the primary client contact and final decision-maker for requirement disputes?
126. How frequently would the client like progress updates or demonstrations?
127. What response time should the team expect when clarification is needed?
128. How should decisions and requirement changes be documented and approved?
129. Is there a deadline after which scope changes should be deferred to a future version?
130. Are there dependencies on other teams, data providers, university staff, or external services?
131. What risks or constraints is the client already concerned about?
132. Would the client prefer incremental prototypes for feedback or one integrated prototype near the end?

## 13. Scenario-based clarification questions

These scenarios can help the client make abstract requirements more concrete.

1. If a current approved policy says an action is mandatory, but several reliable operational records show it is routinely bypassed, should the output be “credible,” “not credible,” or two separate conclusions about policy and practice?
2. If an employee accurately describes common practice but lacks formal decision authority, how should their evidence be weighted?
3. If the only source is an old approved document whose review date has passed, should the claim be considered supported, outdated, or unresolved?
4. If two interviews agree but appear to repeat the same second-hand information, should they count as one line of evidence or two?
5. If a claim is correct except for one boundary value—for example, “above 15%” instead of “15% or greater”—should it be marked incorrect, partially supported, or automatically normalised?
6. If no document assigns a decision right, should the system conclude that nobody has it, or only that the available evidence does not identify an owner?
7. If a draft document matches current practice better than the approved process, should it influence operational credibility while remaining invalid as formal policy?
8. If evidence is withheld until a later dataset phase, should the system preserve an unresolved result and update it when the new evidence arrives?
9. If the model is highly confident but its evidence retrieval missed a contradictory source, how should confidence be corrected or guarded against?
10. If a user's manual judgement differs from the model, should the system preserve both, replace the model result, or create a reviewed final status with an audit trail?

## 14. Suggested questions for the first client meeting

If meeting time is limited, begin with these questions:

1. What exact final outcome and deliverables do you expect?
2. Who will use the solution, and what decision should it help them make?
3. How do you define a knowledge claim and its credibility?
4. Do you want separate conclusions for formal rules and actual practice?
5. What output format should represent credibility and uncertainty?
6. What later data and ground-truth labels will be provided, and when?
7. What minimum workflow must the final prototype demonstrate?
8. What level of traceability and explanation is mandatory?
9. Are hosted LLMs or external APIs allowed for the dataset?
10. What metrics and acceptance criteria will determine success?
11. What privacy, security, and data-governance constraints apply?
12. What milestones require client review or approval?

## 15. Client decision record template

Use this table after each meeting so answers become traceable requirements rather than remaining only in notes.

| ID | Question/decision | Client answer | Requirement or constraint | Owner | Due date | Status |
|---|---|---|---|---|---|---|
| D-001 |  |  |  |  |  | Open |
| D-002 |  |  |  |  |  | Open |
| D-003 |  |  |  |  |  | Open |

