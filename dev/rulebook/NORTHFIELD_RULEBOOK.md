# Northfield Rulebook

**iLab 14-01 / Decidr**  
**Assessment date:** 31 July 2026  
**Source of inventory:** Data Atlas → `data/outputs/documents.jsonl` (45 files) + claims register  
**Purpose:** Cross-reference map so retrieval does not rely on keyword luck alone. For each topic, this book says which Atlas files belong together, which document outranks which, and which source wins for which kind of dispute.

This is the team document to rely on. It is not a chatbot answer. It is not a second copy of the chunk store.

---

## 0. How to use this book (always)

### Step A — Name the topic
Pick one process: P1 … P8. Open that cluster below.

### Step B — Name the dispute type
Ask only one of these at a time:

| Dispute type | Question | Winner (Kai / Bianca guidance) |
|---|---|---|
| **RULE** | What is the official written rule? | Approved, **in-force** policy (then meeting that created it). Stale process docs and drafts lose. |
| **HAPPENED** | Did this deal / approval / incident actually get recorded? | **CRM** (and audit / task rows when they are the system of record). Kai: CRM is source of truth for occurrence. Interviews/Slack do not override a CRM field. |
| **PRACTICE** | What do people actually do? | Interviews + meetings + Slack/email, checked against CRM where practice leaves a record. Copied Slack threads count as **one** source. |
| **GAP** | Is anyone formally assigned? | If no in-force doc names an owner → status is gap / Unsupported as assignment. Do not invent an owner. |

### Step C — Split layers
Formal and practised of the same topic are **two claims**. Never average them.

### Step D — Retrieval must-fetch
When scoring a claim in that cluster, the pipeline should fetch every ID in **Linked set**, not only BM25 hits. Missing a must-fetch ID is a retrieval failure.

### Step E — Conflicted is finished
If RULE and PRACTICE disagree with good evidence on both sides, status = **Conflicted**. Do not pick a silent winner.

---

## 1. Global supersession board (Atlas truth)

| Doc ID | Atlas type | Status at 31 Jul 2026 | Outranked by / notes |
|---|---|---|---|
| POL-01 | policy | **In force** (v3 from 2025-03-01) | Current discount rule. Harriet Doyle. ≥15%. |
| POL-02 | policy | **Superseded** | Old 10% threshold. Atlas flag: superseded. |
| PROC-02 | process_doc | **Stale leftover** (last updated 2022) | Still names Financial Controller (Victor). Does **not** outrank POL-01 for RULE. |
| POL-04 | policy | **DRAFT — not in force** | Support escalation pilot talk. Must never win as approved policy. |
| ORG-CHART-2023-02-SUPERSEDED | overview | **Superseded** | Use ORG-CHART-AND-ROSTER. |
| POL-06 | policy | In force but **review overdue** (due 2026-06-01 missed) | Renewal 10% cap still written rule; overdue review is a note, not a cancelled policy. |
| PROC-03 | process_doc | Stale for live tooling | Still says Trello; operations moved to Linear (MTG-03, Apr 2025). |

**Cross-validation (Kai):** do not trust formality alone. Always check RULE against HAPPENED (CRM) and PRACTICE (people). One variable is not enough.

---

## 2. Dispute-priority cheat sheet (encode Kai)

```
IF dispute == RULE:
    prefer: approved in-force policy > creating meeting > process doc dated after policy change
    demote: superseded policy, draft policy, stale process leftover, Slack copies of old thresholds

IF dispute == HAPPENED:
    prefer: CRM row (approval_record, stage, discount fields) > audit log > project tasks
    demote: "I think we skipped it" in Slack when CRM shows a record (or vice versa: CRM empty wins over "I'm sure Finance signed")

IF dispute == PRACTICE:
    prefer: meeting decision + independent CRM exceptions + interview from the actor
    collapse: COMMS copies of the same workaround → weight as ONE source
    demote: single Slack tip with no CRM / meeting backup

IF dispute == GAP:
    prefer: decision-rights table + process "accountable" field
    if empty → Gap is Supported; named-owner claim is Unsupported
```

---

## 3. Process clusters (one row per process)

### P1 — Customer discount approval

| Field | Value |
|---|---|
| **topic_id** | P1 |
| **topic_name** | Customer discount approval |
| **Linked docs** | POL-01, POL-02, PROC-02, MTG-01, MTG-02, INT-02, INT-03, INT-04, INT-05, INT-09, DECISION-RIGHTS-TABLE, ROLE-DESCRIPTIONS, COMMUNICATIONS-LOG, CRM-DEALS |
| **Linked deals (must watch)** | DEAL-014, DEAL-027, DEAL-041 (exceptions); Harriet/CRM examples e.g. DEAL-001, 021, 032, 058, 066 |
| **Linked comms** | COMMS-01, COMMS-02, COMMS-03, COMMS-04 (**one workaround cluster**), COMMS-05 (stale 10%), COMMS-08 |
| **Supersedes** | POL-01 supersedes POL-02; POL-01 outranks PROC-02 for RULE |
| **Superseded_by** | POL-02 ← POL-01; PROC-02 leftover ← POL-01 |
| **In-force RULE** | POL-01 (+ MTG-01 created the 15% change) |
| **PRACTICE sources** | MTG-02, INT-02, INT-03, INT-09, COMMS-01–04 (count once), CRM exception deals |
| **CRM truth sources** | CRM-DEALS (`approval_record`, discount %, Closed Won) |
| **Notes** | Kai: for “was approval recorded?” CRM wins. Formal “no exceptions” vs practised bypass → Conflicted is valid. |

#### P1 layer sub-rows

| topic_id | layer | claim focus | must_fetch | expected human status |
|---|---|---|---|---|
| P1-F | formal | Harriet / Finance / ≥15% / CRM before Closed Won | POL-01, MTG-01, INT-02, INT-03; caveat PROC-02 | Supported |
| P1-S | stale | Victor / Financial Controller is approver | PROC-02 vs POL-01, MTG-01 | Unsupported as current RULE |
| P1-P-no-exceptions | practised | Every ≥15% deal Finance-approved in CRM, no exceptions | POL-01 + CRM exceptions + COMMS-01–04 (once) | Conflicted |
| P1-P-urgent | practised | Diane may approve urgent ≥15% outside CRM | MTG-02, COMMS-01, DEAL-014, DEAL-041, INT-02/03 | Likely / Conflicted vs POL-01 |
| P1-P-10pct | practised belief | Staff still treat threshold as 10% | COMMS-05, INT-05 vs POL-01 | Belief likely; rule Unlikely |

---

### P2 — Customer onboarding

| Field | Value |
|---|---|
| **topic_id** | P2 |
| **topic_name** | Customer onboarding (6-week) |
| **Linked docs** | POL-03, PROC-01, INT-06, DECISION-RIGHTS-TABLE, PROJECT-TASKS, COMMUNICATIONS-LOG, CRM-DEALS |
| **Linked deals** | Any Closed Won that should spawn onboarding (watch DEAL-050 with P7) |
| **Linked comms** | COMMS-13 (shadow checklist via Slack) |
| **Supersedes** | POL-03 + PROC-01 are current formal pair |
| **Superseded_by** | — |
| **In-force RULE** | POL-03, PROC-01 |
| **PRACTICE sources** | INT-06, COMMS-13, PROJECT-TASKS |
| **CRM truth sources** | CRM-DEALS + PROJECT-TASKS for “was onboarding opened?” |
| **Notes** | Extension authority is a GAP (not named in POL-03). |

#### P2 layer sub-rows

| topic_id | layer | claim focus | must_fetch | expected human status |
|---|---|---|---|---|
| P2-F | formal | Standard 6-week CS-owned onboarding | POL-03, PROC-01, INT-06 | Supported |
| P2-G | gap | Who may approve timeline deviation is formally assigned | POL-03, DECISION-RIGHTS-TABLE, INT-06 | Unsupported (gap) |
| P2-P | practised | Project system is complete picture of effort | POL-03 vs INT-06, COMMS-13 | Conflicted |

---

### P3 — Product change / feature intake

| Field | Value |
|---|---|
| **topic_id** | P3 |
| **topic_name** | Feature / product change intake |
| **Linked docs** | PROC-03, MTG-03, INT-10, PROJECT-TASKS (e.g. TASK-140), COMMUNICATIONS-LOG, DECISION-RIGHTS-TABLE |
| **Linked deals** | — |
| **Linked comms** | COMMS-11 |
| **Supersedes** | Live ops: Linear since MTG-03 (2025-04-22) |
| **Superseded_by** | PROC-03 Trello wording is stale for PRACTICE |
| **In-force RULE** | PROC-03 still written; treat tooling clause as stale |
| **PRACTICE sources** | MTG-03, INT-10, COMMS-11, PROJECT-TASKS |
| **CRM truth sources** | — (not a CRM dispute) |
| **Notes** | PM split / Product vs Eng tie-break = GAP. |

#### P3 layer sub-rows

| topic_id | layer | claim focus | must_fetch | expected human status |
|---|---|---|---|---|
| P3-F-trello | formal/stale | Feature requests on Trello board | PROC-03 | Doc Supported; ops Unlikely after Apr 2025 |
| P3-P-linear | practised | Feature requests in Linear since Apr 2025 | MTG-03, INT-10, COMMS-11 | Supported |
| P3-G | gap | Documented PM split / Product–Eng tie-break | PROC-03, INT-10, DECISION-RIGHTS-TABLE | Unsupported |

---

### P4 — Expense approval

| Field | Value |
|---|---|
| **topic_id** | P4 |
| **topic_name** | Expense approval |
| **Linked docs** | POL-07, PROC-04, MTG-09, INT-03, INT-06, COMMUNICATIONS-LOG |
| **Linked deals** | — |
| **Linked comms** | COMMS-09 |
| **Supersedes** | POL-07 is in-force RULE |
| **Superseded_by** | — |
| **In-force RULE** | POL-07 (>\$500 → Head of Finance; ≤\$500 → manager; receipt) |
| **PRACTICE sources** | PROC-04 exceptions paragraph, INT-03, INT-06, MTG-09, COMMS-09 |
| **CRM truth sources** | — (expenses not in CRM-DEALS; treat system records if present later) |
| **Notes** | Onboarding travel bypass is practised and admitted, not in POL-07. |

#### P4 layer sub-rows

| topic_id | layer | claim focus | must_fetch | expected human status |
|---|---|---|---|---|
| P4-F | formal | >\$500 needs Harriet; ≤\$500 manager | POL-07, PROC-04 | Supported |
| P4-P-travel | practised | Onboarding-visit travel booked without Finance sign-off | PROC-04, INT-06, INT-03 | Likely |
| P4-P-manager | practised | Some >\$500 approved by manager / Head of Eng | MTG-09, COMMS-09, INT-03 | Likely |

---

### P5 — Support escalation

| Field | Value |
|---|---|
| **topic_id** | P5 |
| **topic_name** | Support → Engineering escalation |
| **Linked docs** | PROC-05, POL-04, MTG-04, INT-07, INT-08, INT-10, COMMUNICATIONS-LOG, DECISION-RIGHTS-TABLE |
| **Linked deals** | — |
| **Linked comms** | COMMS-06, COMMS-07 |
| **Supersedes** | PROC-05 is written in-force process |
| **Superseded_by** | POL-04 must **not** supersede PROC-05 (DRAFT) |
| **In-force RULE** | PROC-05 (ticket path; Support Lead closes) |
| **PRACTICE sources** | INT-07, INT-08, INT-10, COMMS-07, MTG-04 pilot |
| **CRM truth sources** | — |
| **Notes** | Helena did not sign POL-04 as official (COMMS-06). Pilot ≠ approved. |

#### P5 layer sub-rows

| topic_id | layer | claim focus | must_fetch | expected human status |
|---|---|---|---|---|
| P5-F | formal | Ticket-first severity path (PROC-05) | PROC-05 | Supported as written |
| P5-D | draft | POL-04 v2 is approved process | POL-04, MTG-04, COMMS-06 | Unsupported as approved |
| P5-P-slack | practised | Sev 1 Slack-first, ticket later | PROC-05 notes, INT-07/08, COMMS-07 | Likely |
| P5-P-close | practised | Reps close without Engineering | INT-07 vs INT-08, PROC-05 | Conflicted |

---

### P6 — New-hire onboarding / probation

| Field | Value |
|---|---|
| **topic_id** | P6 |
| **topic_name** | New-hire onboarding & probation |
| **Linked docs** | POL-08, COMMUNICATIONS-LOG, DECISION-RIGHTS-TABLE, ORG-CHART-AND-ROSTER |
| **Linked deals** | — |
| **Linked comms** | COMMS-12 |
| **Supersedes** | POL-08 in force |
| **Superseded_by** | — |
| **In-force RULE** | POL-08 (2-week checklist; People Ops Lead probation) |
| **PRACTICE sources** | COMMS-12 (Yusuf day-10 complete) |
| **CRM truth sources** | — |
| **Notes** | Checklist assumes office; remote hires = policy gap, not failed instance. |

#### P6 layer sub-rows

| topic_id | layer | claim focus | must_fetch | expected human status |
|---|---|---|---|---|
| P6-F | formal | Checklist in first two weeks; People Ops owns | POL-08, COMMS-12, DECISION-RIGHTS-TABLE | Supported |

---

### P7 — Invoicing / billing-touching production changes

| Field | Value |
|---|---|
| **topic_id** | P7 |
| **topic_name** | Billing / invoicing / CRM–billing integration |
| **Linked docs** | PROC-06, ROLE-DESCRIPTIONS, DECISION-RIGHTS-TABLE, MTG-07, MTG-08, INT-10, COMMUNICATIONS-LOG, CRM-DEALS, PROJECT-TASKS |
| **Linked deals** | DEAL-050 (invoice/onboarding mismatch) |
| **Linked comms** | COMMS-07, COMMS-14, COMMS-15 |
| **Supersedes** | Head of Eng sign-off for billing-touching prod (roles / decision-rights) |
| **Superseded_by** | — |
| **In-force RULE** | ROLE-DESCRIPTIONS + DECISION-RIGHTS-TABLE (not a POL-xx) |
| **PRACTICE sources** | MTG-07, INT-10, COMMS-07, COMMS-14 |
| **CRM truth sources** | CRM-DEALS vs invoice/onboarding existence |
| **Notes** | Ana = key-person risk. Feb 2026 fix: no clear Eng sign-off record. |

#### P7 layer sub-rows

| topic_id | layer | claim focus | must_fetch | expected human status |
|---|---|---|---|---|
| P7-F | formal | Billing-touching prod needs Head of Eng | ROLE-DESCRIPTIONS, DECISION-RIGHTS-TABLE | Likely |
| P7-P-feb2026 | practised | Feb 2026 fix had clear Eng sign-off | MTG-07, COMMS-07, INT-10, DECISION-RIGHTS-TABLE | Unlikely |
| P7-P-ana | practised | Ana sole billing-integration knowledge | INT-10, MTG-07, COMMS-14 | Supported |
| P7-P-match | practised | Every Closed Won has invoice + onboarding project | CRM-DEALS, COMMS-15, DEAL-050 | Unlikely |

---

### P8 — Contract renewal & churn risk

| Field | Value |
|---|---|
| **topic_id** | P8 |
| **topic_name** | Contract renewal / churn |
| **Linked docs** | POL-06, PROC-07, MTG-05, MTG-10, INT-02, DECISION-RIGHTS-TABLE, CRM-DEALS, COMMUNICATIONS-LOG |
| **Linked deals** | DEAL-063 (18%), Ashgrove via MTG-10 (12%), DEAL-064 (stalled / Sales–CS disagreement) |
| **Linked comms** | COMMS-10 |
| **Supersedes** | POL-06 written RULE (10% cap, no exceptions) |
| **Superseded_by** | — (review overdue, still in force) |
| **In-force RULE** | POL-06 |
| **PRACTICE sources** | MTG-10, COMMS-10, MTG-05, INT-02, DEAL-063 |
| **CRM truth sources** | CRM-DEALS renewal discount fields |
| **Notes** | No named tie-break when Sales vs CS disagree = GAP. |

#### P8 layer sub-rows

| topic_id | layer | claim focus | must_fetch | expected human status |
|---|---|---|---|---|
| P8-F | formal | Renewal cap 10%, no exceptions | POL-06 | Supported as written |
| P8-P-cap | practised | All renewals stay within 10% | POL-06, DEAL-063, MTG-10, COMMS-10 | Unsupported |
| P8-G | gap | Named final call when Sales/CS disagree | PROC-07, DECISION-RIGHTS-TABLE, MTG-05, DEAL-064 | Unsupported (gap) |

---

## 4. Copied-source clusters (never triple-count)

| Cluster ID | Members | Count as |
|---|---|---|
| P1-DIANE-BYPASS | COMMS-01, COMMS-02, COMMS-03, COMMS-04 (+ INT-09 restating) | **1** practised workaround |
| P3-TRELLO-DEAD | COMMS-11 + PROC-03 Trello wording vs MTG-03 Linear | Stale vs live ops |

---

## 5. Atlas document index (all 45 — rely on these IDs)

| doc_id | source_type | atlas note |
|---|---|---|
| POL-01 … POL-08 | policy | POL-02 superseded; POL-04 draft |
| PROC-01 … PROC-07 | process_doc | PROC-02 stale vs POL-01; PROC-03 stale tooling |
| MTG-01 … MTG-10 | meeting | |
| INT-01 … INT-10 | interview | |
| COMMUNICATIONS-LOG | comms | Threads COMMS-01 … COMMS-15 |
| CRM-DEALS | crm | 75 deal chunks DEAL-001 … |
| PROJECT-TASKS | tasks | |
| SYSTEM-AUDIT-LOG | audit_log | |
| COMPANY-OVERVIEW | overview | |
| DECISION-RIGHTS-TABLE | overview | Gaps + rights |
| ORG-CHART-AND-ROSTER | overview | Current |
| ORG-CHART-2023-02-SUPERSEDED | overview | Superseded |
| ROLE-DESCRIPTIONS | overview | |
| LABELLED-CLAIMS-SAMPLE | labelled_sample | Format only — not gold probabilities |

---

## 6. Files that go with this book

| File | What |
|---|---|
| `rulebook_process_master.csv` | One row per process P1–P8 (sheet columns you asked for) |
| `rulebook_layer_rows.csv` | Layer sub-rows (formal / practised / stale / draft / gap) |
| `rulebook_dispute_rules.csv` | Kai dispute-type → winner table |
| `NORTHFIELD_RULEBOOK.md` | This visual book |

**Machine use later (not required to edit Streamlit now):** retrieval should union BM25 hits with `linked_doc_ids` / deals / comms for the claim’s `topic_id`.

---

## 7. Version

| Field | Value |
|---|---|
| Version | 1.0 |
| Built from | Data Atlas documents.jsonl + phase2_claims_register + Kai/Bianca meeting (CRM truth; no single-variable formality; link occurrences) |
| Do not treat as | Trained model output, legal advice, or gold probabilities for calibration |
