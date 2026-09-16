"""
Stage 8: Explanation.

The score plus a short, evidence-cited account: the conclusion, what
raised it, what lowered it, how sure we should be, and what extra file
would change the call (Section 4.1). This module is template-based and
deterministic -- no LLM required to run the pipeline end-to-end -- with
a clearly marked hook for swapping in an LLM to write the prose.

Hard rule, repeated here because it matters: if an LLM is used, it may
only rewrite this prose. It must never be allowed to change the score or
the status. If the two disagree, the score stands and the explanation is
regenerated (Section 4.1: "If the explanation and the score ever
disagree, the score stands and the prose is rewritten").

Owner: shared -- Kushal Joshi surfaces this output in reports/demo;
Prathamesh's evaluation harness should spot-check that explanations never
silently contradict the status they are attached to.
"""

from __future__ import annotations

from typing import List, Dict, Any


def explain_template(claim_text: str, scored: Dict[str, Any],
                      weighted_evidence: List[Dict[str, Any]]) -> str:
    status = scored["status"]
    score = scored["credibility_score"]
    ci = scored.get("credible_interval")
    confidence = scored["confidence"]

    support = [e for e in weighted_evidence if e["stance"] == "support"]
    contradict = [e for e in weighted_evidence if e["stance"] == "contradict"]

    lines = []
    lines.append(f'Claim: "{claim_text}"')
    ci_str = f" (range {ci[0]:.2f}-{ci[1]:.2f})" if ci else ""
    lines.append(f"Status: {status}. Credibility score: {score:.2f}{ci_str}. Confidence: {confidence}.")

    if support:
        top = sorted(support, key=lambda e: e["final_weight"], reverse=True)[:3]
        cited = ", ".join(f"{e['doc_id']} (weight {e['final_weight']:.2f})" for e in top)
        lines.append(f"Raised by: {cited}.")
    else:
        lines.append("Raised by: no supporting evidence found.")

    if contradict:
        top = sorted(contradict, key=lambda e: e["final_weight"], reverse=True)[:3]
        cited = ", ".join(f"{e['doc_id']} (weight {e['final_weight']:.2f})" for e in top)
        lines.append(f"Lowered by: {cited}.")
    else:
        lines.append("Lowered by: no contradicting evidence found.")

    if status == "Conflicted":
        lines.append("This claim is marked Conflicted because meaningful weight sits on both "
                      "sides. That is the honest answer on this pack, not a failure of the method.")
    elif status == "Not enough evidence":
        lines.append("Too little weighted evidence was found either way to call this claim; "
                      "more retrieval or a different query may be needed.")

    lines.append("An extra approved, dated, first-hand document naming this exact rule would "
                  "move this status the most.")

    return " ".join(lines)


def explain_with_llm(claim_text: str, scored: Dict[str, Any],
                      weighted_evidence: List[Dict[str, Any]], client=None) -> str:
    """
    TODO: swap in an LLM call that is given `scored` and `weighted_evidence`
    as fixed context and asked only to write better prose around them.
    The score/status/evidence lists themselves must come from score.py,
    never from the LLM's own judgement -- see module docstring.
    """
    raise NotImplementedError("LLM-authored explanation not wired up yet; use explain_template().")
