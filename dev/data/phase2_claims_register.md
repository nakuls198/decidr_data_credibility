# Phase 2 — Claims register

**Pack:** Northfield Software Ltd, full Phase 2 materials.  
**Assessment date:** 31 July 2026.  
**Method:** [how_we_score_claims.md](how_we_score_claims.md) (Phase 1), applied and refined below.

This is the Phase 2 task: extract organisational knowledge claims, attach supporting and contradicting evidence, and give a **status** and a **confidence** for each. Ingest/spaCy was only preparation. Streamlit can wait.

---

## 1. What Phase 2 added to the method

Phase 1 gave us the scoring sheet and showed that formal vs practised must be **two claims**. Phase 2 lets us test those claims against records.

Refinements used here:

1. **CRM / audit / tasks are a different kind of source** from interviews. A Slack slogan plus three Sales interviews is still one team talking. A CRM `approval_record` is independent of that.
2. **COMMS-02, COMMS-03, COMMS-04 count as one workaround**, copied. Priya and Ester restating Diane’s rule does not add three independent confirmations.
3. **Stale staff knowledge is evidence of practice, not of the current rule.** Callum telling Jonah “10%” in May 2025 (COMMS-05) after POL-01 moved to 15% on 1 March 2025 does not revive the old policy.
4. **Conflicted is a finished answer.** We do not average a clean policy with messy CRM into one number.
5. **A gap is a claim.** “No role has the final call on renewal disagreements” is scorable.

Status = how much to believe *this sentence at this layer*.  
Confidence = how complete the evidence is. You can be **Conflicted / High**.

---

## 2. Register (by process)

Each row is one atomic claim. Sample IDs C01 / C09 / C27 / C32 from `labelled_claims_sample.csv` are included as the **formal** member of a pair, then scored against Phase 2 records.

### P1 — Customer discount approval

#### P1-F1 (sample C01) — Formal

| Field | Value |
|---|---|
| Claim | Head of Finance & People Ops must approve new-business discounts of 15% or more in the CRM `approval_record` before Closed Won. |
| Layer | Formal |
| Valid from | 2025-03-01 (POL-01 v3). Before that the threshold was 10% (POL-02). |
| Supports | POL-01 (approved); MTG-01 (decision 2025-02-24); INT-02 Diane restates 15%; INT-03 Harriet: she approves what comes to her. |
| Contradicts (as formal rule) | PROC-02 (2022) still names the Financial Controller — **stale leftover**, weaker than POL-01 on the written rule. |
| Copies | — |
| **Status / confidence** | **Supported / High** |
| Why | Approved policy + the meeting that created it. PROC-02 does not outrank a 2025 policy. |
| What would change our mind | A later approved POL-01 that names a different approver or threshold. |

#### P1-S1 — Stale leftover

| Field | Value |
|---|---|
| Claim | The Financial Controller (Victor) is the accountable approver for discounts at or above threshold. |
| Layer | Stale leftover (what PROC-02 still says) |
| Valid from / to | PROC-02 last updated 2022-08-15; POL-01 v3 from 2025-03-01 names Harriet. |
| Supports | PROC-02 text. |
| Contradicts | POL-01; MTG-01; CRM rows that name Harriet Doyle, not Victor. |
| **Status / confidence** | **Supported / High** *as a description of the old process doc*; **Unsupported** *as current formal truth*. |
| Why | The leftover exists. It is not the in-force rule. |

#### P1-P1 — Practised

| Field | Value |
|---|---|
| Claim | Every new-business discount ≥15% is approved by Finance in the CRM before close, with no exceptions. |
| Layer | Practised |
| Supports | Several CRM rows: DEAL-001, 021, 032, 058, 066 (Harriet, Recorded in CRM). INT-02: “I’d be surprised if deals were slipping through.” |
| Contradicts | COMMS-01 + DEAL-014 (Slack, Diane, 18%); DEAL-041 (Diane Slack, 25%); DEAL-027 (20%, None found) + COMMS-08 Victor cannot confirm; INT-03 Harriet does not have full visibility; decision-rights table. |
| Copies | COMMS-02 / 03 / 04 / INT-09 = one Diane-bypass rule, restated. Count once. |
| **Status / confidence** | **Conflicted / High** |
| Why | Some deals follow the policy. Enough independent CRM + Slack evidence shows exceptions. We are sure practice is not “no exceptions.” |
| What would change our mind | A complete CRM extract showing DEAL-014/027/041 were later corrected in `approval_record` by Harriet. They are not. |

#### P1-P2 — Practised

| Field | Value |
|---|---|
| Claim | On genuinely urgent deals, Head of Sales may approve ≥15% outside the CRM, with paperwork later. |
| Layer | Practised |
| Supports | MTG-02 (Diane, 2025-06-12); COMMS-01, DEAL-014; DEAL-041; INT-02, INT-03, INT-09. |
| Contradicts | POL-01 (no exceptions); Diane in INT-02 also claims the team is “pretty disciplined.” |
| Copies | COMMS-02, 03, 04 count as one broadcast of the same rule. |
| **Status / confidence** | **Likely / High** |
| Why | Meeting + CRM + Harriet’s awareness. Framed as temporary in MTG-02; still in use into 2026 (DEAL-041). No later meeting withdrew it. |

#### P1-P3 — Practised (stale knowledge)

| Field | Value |
|---|---|
| Claim | Staff currently treat the Finance threshold as 10%. |
| Layer | Practised (what some people believe) |
| Supports | COMMS-05 (Callum → Jonah, 2025-05-19, after POL-01 change); INT-05 Jonah still says 10% in June 2026. |
| Contradicts | POL-01; MTG-01; INT-02 Diane says 15%; most ≥15% CRM rows. |
| **Status / confidence** | **Likely / High** *that Jonah/Callum held the 10% figure*; **Unlikely** *that 10% is the organisation’s current rule*. |
| Why | Two dated sources on the misconception. They do not override POL-01. |

**CRM count used for P1:** 13 deals with discount ≥15%. Among Closed Won: several Harriet/CRM; DEAL-014 and DEAL-041 via Diane/Slack; DEAL-027 none found; DEAL-035 is `150` with a note it is probably a typo for 15.

---

### P2 — Customer onboarding

#### P2-F1 (sample C09) — Formal

| Field | Value |
|---|---|
| Claim | New-customer onboarding is a standard 6-week process owned by Customer Success & Delivery. |
| Layer | Formal |
| Valid from | POL-03 2024-01-15; PROC-01 2024-01-20. |
| Supports | POL-03; PROC-01; INT-06 Adaeze describes the same six-week path. |
| Contradicts (as formal) | Nothing of equal weight. |
| **Status / confidence** | **Supported / High** |

#### P2-G1 — Gap

| Field | Value |
|---|---|
| Claim | Who may approve a deviation from the 6-week timeline is formally assigned. |
| Layer | Gap (the claim as stated is what we test) |
| Supports (that it is assigned) | — |
| Contradicts (shows unassigned) | POL-03 Exceptions: extensions exist, authority not named. Decision-rights table: not formally assigned. INT-06: Adaeze clears longer jobs with Helena by habit. |
| **Status / confidence** | **Unsupported / High** as a formal assignment; **Likely / Medium** that Helena does it in practice. |
| Why | Split the layers. Do not invent a documented owner. |

#### P2-P1 — Practised

| Field | Value |
|---|---|
| Claim | Onboarding is complete only when the current checklist is marked complete in the project system, and that system shows the real effort. |
| Layer | Practised |
| Supports | POL-03 requirement 4. |
| Contradicts | INT-06: email work untracked; Ruth used an older locally saved checklist; COMMS-13 Ben sends Ruth `Onboarding_Checklist_v2.docx` by Slack. |
| **Status / confidence** | **Conflicted / High** |
| Why | The completion rule is documented. Practice includes shadow artefacts. |

---

### P3 — Product change / feature intake

#### P3-F1 — Formal (what the process doc still says)

| Field | Value |
|---|---|
| Claim | Feature requests are captured on the Feature Requests Trello board. |
| Layer | Formal (PROC-03, last updated 2023-11-02) |
| Supports | PROC-03. |
| Contradicts as operations | MTG-03 (2025-04-22) migrate to Linear; TASK-140; INT-10 Ana: Linear for over a year; COMMS-11 Trello already “unusable” in Feb 2025. |
| **Status / confidence** | **Supported / High** *that PROC-03 still says Trello*; **Unlikely / High** *that Trello is the live system after April 2025*. |

#### P3-P1 — Practised

| Field | Value |
|---|---|
| Claim | Since April 2025, feature requests are tracked in Linear. |
| Layer | Practised |
| Supports | MTG-03; completed archive/re-enter actions; INT-10. |
| Contradicts | PROC-03 (not updated — stale doc, not a second live system). |
| **Status / confidence** | **Supported / High** |

#### P3-G1 — Gap

| Field | Value |
|---|---|
| Claim | There is a documented rule for how the two PMs split intake, and for Product vs Engineering when they disagree. |
| Layer | Gap |
| Supports (that a rule exists) | PROC-03: PMs jointly prioritise; Head of Engineering on P1s. No split rule. |
| Contradicts | INT-10: split by bandwidth/customer; “I genuinely don’t know” a clean Product/Eng answer. Decision-rights table. |
| **Status / confidence** | **Unsupported / High** (no such documented rule). Informal talking-out is **Likely / Medium**. |

---

### P4 — Expense approval

#### P4-F1 — Formal

| Field | Value |
|---|---|
| Claim | Expense claims over $500 require Head of Finance & People Ops approval; $500 or less may be approved by the direct manager; itemised receipt required. |
| Layer | Formal |
| Supports | POL-07; PROC-04 steps 2–3. |
| Contradicts (as formal exceptions) | POL-07 lists none. |
| **Status / confidence** | **Supported / High** |

#### P4-P1 — Practised

| Field | Value |
|---|---|
| Claim | Onboarding-visit travel is booked without a separate Finance sign-off. |
| Layer | Practised |
| Supports | PROC-04 exceptions paragraph (admits the practice); INT-06 Adaeze; INT-03 Harriet (“ridiculous admin”). |
| Contradicts | POL-07 “none documented.” |
| **Status / confidence** | **Likely / High** |
| Why | Policy owner and the people who book the travel agree. Still not in POL-07. |

#### P4-P2 — Practised

| Field | Value |
|---|---|
| Claim | Some expenses over $500 are approved by the employee’s manager (or Head of Engineering) instead of Harriet. |
| Layer | Practised |
| Supports | MTG-09 Victor flags manager-approved claims; INT-03; COMMS-09 Lior approves Nadia’s ~$650 conference travel, not routed to Finance. |
| Contradicts | POL-07. |
| **Status / confidence** | **Likely / Medium** |
| Why | Meeting + Slack example. Victor did not table exact claim IDs in MTG-09. Policy still unchanged as at 31 July 2026. |

---

### P5 — Support escalation

#### P5-F1 (sample C27) — Formal

| Field | Value |
|---|---|
| Claim | Customer-reported issues are escalated from Support to Engineering via a ticket, on a documented severity path; Support Lead closes after customer confirm. |
| Layer | Formal |
| Supports | PROC-05 v1 (approved, 2021-02-10). POL-04 v2 is **draft, not in force**. |
| Contradicts as formal | Nothing in force. |
| **Status / confidence** | **Supported / High** as the written current process. |

#### P5-D1 — Draft / pilot

| Field | Value |
|---|---|
| Claim | POL-04 v2 (Slack-first Sev 1; reps may close without Engineering) is the approved process. |
| Layer | Draft / unofficial pilot |
| Supports (pilot happened) | MTG-04 informal quarter pilot; COMMS-06 Helena “not signing off as official”; INT-07 Sam speaks as if Helena signed it off. |
| Contradicts (approved) | POL-04 header: DRAFT, not in force; MTG-04 option 3 was pilot not approval; no later review meeting. |
| **Status / confidence** | **Unsupported / High** as approved policy. **Likely / High** that a pilot has been running since Sep 2025. |

#### P5-P1 — Practised

| Field | Value |
|---|---|
| Claim | For urgent / Sev 1 production issues, Support messages Engineering on Slack first and tickets afterwards. |
| Layer | Practised |
| Supports | PROC-05 itself notes Slack-first is common; INT-07; INT-08; COMMS-07 (Feb 2026 billing, ticket retrospective); INT-10 Ana. |
| Contradicts | PROC-05 steps 2–4 as written. |
| **Status / confidence** | **Likely / High** |

#### P5-P2 — Practised

| Field | Value |
|---|---|
| Claim | Support Reps close escalated tickets themselves once the customer confirms, without Engineering sign-off. |
| Layer | Practised |
| Supports | INT-07 Sam; POL-04 draft. |
| Contradicts | PROC-05: Support Lead confirms and closes; INT-08 Ines still checks with Sam, especially if Engineering was involved. |
| **Status / confidence** | **Conflicted / High** |
| Why | Lead and a rep on the same team do not describe the same close rule. Pilot ≠ uniform practice. |

---

### P6 — New-hire onboarding

#### P6-F1 (sample C32) — Formal

| Field | Value |
|---|---|
| Claim | All new hires complete a documented onboarding checklist within the first two weeks, owned by People Ops; People Ops Lead is sole probation approver. |
| Layer | Formal |
| Supports | POL-08; COMMS-12 Naomi confirms Yusuf’s checklist complete on day 10 (2025-09-05). Decision-rights table: probation consistently followed. |
| Contradicts | POL-08 itself: checklist assumes in-person office; Yusuf and Paul are remote — policy gap, not a failed Yusuf instance. |
| **Status / confidence** | **Supported / High** as the formal rule and as followed for Yusuf’s checklist. **Likely / Medium** that the checklist is incomplete for remote setup. |

---

### P7 — Invoicing, collections, billing-touching changes

#### P7-F1 — Formal

| Field | Value |
|---|---|
| Claim | Production changes touching customer billing require Head of Engineering sign-off. |
| Layer | Formal (role description / decision-rights table) |
| Supports | Decision-rights table; role description for Head of Engineering. |
| Contradicts as a complete control | No named delegate. |
| **Status / confidence** | **Likely / Medium** (documented in roles, not a numbered policy like POL-01). |

#### P7-P1 — Practised

| Field | Value |
|---|---|
| Claim | The February 2026 billing-integration fix had a clear Head of Engineering sign-off record before production change. |
| Layer | Practised |
| Supports | MTG-07 exists as a next-day review; Ana did the fix. |
| Contradicts | COMMS-07 Slack-first; INT-10 no clean paper trail of what changed vs the ticket; decision-rights table: that incident “no clear sign-off record.” |
| **Status / confidence** | **Unlikely / High** |

#### P7-P2 — Practised (key-person)

| Field | Value |
|---|---|
| Claim | Ana Kowalski is the only engineer with working production knowledge of the CRM-billing integration. |
| Layer | Practised |
| Supports | INT-10; MTG-07 Sofia and Lior; COMMS-14 Wei: Ana knows billing; documentation task from MTG-07 not completed. |
| **Status / confidence** | **Supported / High** |

#### P7-P3 — Practised (data quality)

| Field | Value |
|---|---|
| Claim | Every Closed Won CRM deal has a matching invoice and onboarding project. |
| Layer | Practised |
| Supports | Implied by P2/P7 process docs. |
| Contradicts | COMMS-15 Sofia on DEAL-050; CRM notes; no recorded resolution. |
| **Status / confidence** | **Unlikely / Medium** (one named break, no follow-up in the pack). |

---

### P8 — Contract renewal and churn-risk

#### P8-F1 — Formal

| Field | Value |
|---|---|
| Claim | Renewal discounts are capped at 10% off current rate, decided by the AE with CS input, with no exceptions. |
| Layer | Formal |
| Supports | POL-06 (approved 2024-06-01). Review date 2026-06-01 **missed**. |
| Contradicts as formal | None in POL-06. |
| **Status / confidence** | **Supported / High** as written rule. Note overdue review. |

#### P8-P1 — Practised

| Field | Value |
|---|---|
| Claim | All renewal discounts stay within the 10% cap. |
| Layer | Practised |
| Supports | POL-06; some renewals at or under 10%. |
| Contradicts | DEAL-063 Vantage Point renewal 18% (Diane, email/verbal, COMMS-10); MTG-10 Ashgrove Trades **12%** two-year (Diane + Helena agreed). Decision-rights table: at least one undocumented exception. |
| **Status / confidence** | **Unsupported / High** |
| Why | Two independent records above the cap. Ashgrove is even a **joint** Sales/CS exception, so “CS always blocks over-cap” is also false. |

#### P8-G1 — Gap

| Field | Value |
|---|---|
| Claim | A named role has the final call on renewal terms when Sales and Customer Success disagree. |
| Layer | Gap |
| Supports (that someone is named) | — |
| Contradicts | PROC-07 accountable “not specified”; decision-rights table; MTG-05 Ridgeway: no decision, no tie-break; DEAL-064 notes renewal stalled past contract end, Sales and CS haven’t agreed. INT-02 Diane downplays Ridgeway. |
| **Status / confidence** | **Unsupported / High** (no named owner). The gap is **Supported / High**. |

---

## 3. Summary table

| ID | Process | Layer | Claim (short) | Status | Conf. |
|---|---|---|---|---|---|
| P1-F1 / C01 | P1 | Formal | Finance approves new-business ≥15% in CRM before close | Supported | High |
| P1-S1 | P1 | Stale | PROC-02 still names Financial Controller as approver | Leftover, not current rule | High |
| P1-P1 | P1 | Practised | Every ≥15% deal is Finance-approved in CRM, no exceptions | Conflicted | High |
| P1-P2 | P1 | Practised | Urgent ≥15% may go via Diane outside CRM | Likely | High |
| P1-P3 | P1 | Practised | Some AEs still believe the threshold is 10% | Belief likely; rule unlikely | High |
| P2-F1 / C09 | P2 | Formal | Standard 6-week CS-owned onboarding | Supported | High |
| P2-G1 | P2 | Gap | Extension authority is formally assigned | Unsupported (gap) | High |
| P2-P1 | P2 | Practised | Project system is a complete picture of onboarding | Conflicted | High |
| P3-F1 | P3 | Formal/stale | Feature requests live on Trello | Doc yes; operations no | High |
| P3-P1 | P3 | Practised | Feature requests live in Linear since Apr 2025 | Supported | High |
| P3-G1 | P3 | Gap | Documented PM split / Product vs Eng tie-break | Unsupported | High |
| P4-F1 | P4 | Formal | >$500 needs Head of Finance | Supported | High |
| P4-P1 | P4 | Practised | Onboarding travel booked without Finance sign-off | Likely | High |
| P4-P2 | P4 | Practised | Managers sometimes approve over $500 | Likely | Medium |
| P5-F1 / C27 | P5 | Formal | Ticket-first escalation path (PROC-05) | Supported | High |
| P5-D1 | P5 | Draft | POL-04 v2 is approved | Unsupported | High |
| P5-P1 | P5 | Practised | Sev 1 is Slack-first, ticket later | Likely | High |
| P5-P2 | P5 | Practised | Reps close without Engineering | Conflicted | High |
| P6-F1 / C32 | P6 | Formal | 2-week checklist, People Ops owns | Supported | High |
| P7-P1 | P7 | Practised | Feb 2026 billing fix had clear Eng sign-off | Unlikely | High |
| P7-P2 | P7 | Practised | Ana is sole billing-integration owner | Supported | High |
| P8-F1 | P8 | Formal | Renewal cap 10%, no exceptions | Supported | High |
| P8-P1 | P8 | Practised | All renewals stay within 10% | Unsupported | High |
| P8-G1 | P8 | Gap | Named final call when Sales/CS disagree | Unsupported (gap) | High |

---

## 4. How this meets the Phase 2 brief

| Brief | What we did |
|---|---|
| Apply the methodology across the full pack | Same sheet as Phase 1; CRM, comms, meetings, remaining interviews now attached |
| Refine it | Independence, copied Slack, stale 10% knowledge, Conflicted as a valid output |
| Identify claims | Atomic, layered, bound to P1–P8 |
| Supporting and contradicting evidence | Source IDs on every card |
| Credibility and confidence | Status + confidence, not a fake 0–100 |

**Not required by the brief, and not done here:** a website, hybrid RAG, or a model that picks the score.

If the team wants a next build step after this register, it is a search UI that *retrieves the evidence rows above* — it should not replace this table.
