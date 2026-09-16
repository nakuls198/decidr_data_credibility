# How we score Northfield claims

*One page. Assessment date: 31 July 2026. Every claim on the project uses this sheet.*

---

## What a claim is

A claim is **one testable sentence** about how the company works: **who** (a role) may or must do **what**, **under which condition**. Add the **system** and **exceptions** if they are part of the point.

| This is a claim | This is not a claim — split it or drop it |
|---|---|
| Head of Finance must approve new-business discounts of 15% or more in the CRM before Closed Won. | “Discounting is a mess.” |
| New customers follow a 6-week onboarding owned by Customer Success. | “POL-01 says Finance is involved.” (that describes a document, not the organisation) |
| Sev 1 issues must be ticketed before Engineering is engaged. | Two ideas in one sentence. Split them. |

If you cannot name the role, the action, and the condition, it is not a claim yet.

---

## Always split the layer (do this before scoring)

The same topic can be two claims with two different scores. Never mix them in one row.

| Layer | Meaning | Example |
|---|---|---|
| **Formal** | What an approved, in-force document says | POL-01: Harriet approves ≥15% |
| **Practised** | What people and systems actually do | Diane signs urgent deals on Slack |
| **Gap** | Nobody is assigned | Who has the final call when Sales and CS disagree on a renewal |
| **Draft / pilot** | Talked about, not in force | POL-04 draft; informal escalation pilot |
| **Stale leftover** | An older doc that was never updated | PROC-02 (2022) still names the Financial Controller |

---

## Fill this card for every claim

```
Claim ID:
Process (P1–P8):
Layer (formal / practised / gap / draft / stale):
The claim (one sentence):
Valid from / to (document dates):

Supports it (list source IDs):
Contradicts it (list source IDs):
Copies of the same thing (count as one):

Status:          Supported / Likely / Conflicted / Unlikely / Unsupported / Not enough evidence
Confidence:      High / Medium / Low
One-line why:
What would change our mind:
```

---

## How to choose Status and Confidence

**Status** = how much we should believe *this sentence, at this layer*.  
**Confidence** = how complete the evidence is. You can be confident that something is conflicted.

| Status | Use when |
|---|---|
| Supported | Independent sources of different kinds agree (e.g. policy + meeting + records). No serious contradiction. |
| Likely | The main sources agree, but something is thin (one interview, a missing field, an overdue review). |
| Conflicted | Good evidence on both sides, or formal and practised clearly disagree. **This is a valid answer.** |
| Unlikely | Some support exists, but stronger evidence goes the other way. |
| Unsupported | The claim is stated, but the files do not back it. |
| Not enough evidence | We would need a source we do not have. Do not guess. |

| Confidence | Use when |
|---|---|
| High | Two or more *different kinds* of source (document, interview, meeting, CRM/audit). Direct and dated. |
| Medium | One solid source, or several sources from the same team. |
| Low | Hearsay, slogan, draft, or a single Slack message. |

**Five checks, in this order**

1. **In force?** Draft, superseded, or last-updated *before* a conflicting policy change → that source is weak.
2. **Specific?** Named role, number, system, field beats “that’s how we do it.”
3. **Independent?** Policy + CRM beats two Sales people saying the same thing.
4. **Copied?** Slack messages that repeat one workaround count as **one** source, not three.
5. **Docs vs practice?** If they disagree, score two claims. Do not average them into one number.

Do not invent a 0–100 score. Status + confidence + one-line why is the score.

---

## Worked example (do yours the same way)

**Claim A — formal.** *Head of Finance must approve new-business discounts ≥15% in the CRM before Closed Won.*  
Supports: POL-01 (approved, 1 Mar 2025). Contradicts (as formal rule): nothing of equal weight. PROC-02 is older (2022) so it does not outrank POL-01 on the written rule.  
→ **Likely / High.** Formal rule is clear. PROC-02 is a stale leftover, not a second current policy.

**Claim B — practised.** *Every ≥15% deal is approved by Finance in the CRM, with no exceptions.*  
Supports: some CRM rows list Harriet. Contradicts: Diane’s Slack bypass (COMMS-01, 02); the same workaround copied to others (COMMS-03, 04 = copies, count once); deals with Slack/email/no approval (e.g. DEAL-014, 027, 041).  
→ **Conflicted / High.** We are sure practice is not the policy. We are not sure how often the bypass happens until we count the CRM.

That pair is a finished result. You do not have to pick a single winner.
