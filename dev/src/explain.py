"""
Stage 8: Explanation.

Rich, evidence-cited account for the studio and reports. Template-based
and deterministic. A language model may rewrite prose later; it must never
choose the score.
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional


def _fmt(x: Any) -> str:
    from services.format_num import full_num

    return full_num(x)


def _top(evidence: List[Dict[str, Any]], n: int = 5) -> List[Dict[str, Any]]:
    return sorted(evidence, key=lambda e: float(e.get("final_weight") or 0), reverse=True)[:n]


def _insight_for_status(status: str, support_n: int, contradict_n: int) -> str:
    if status == "Supported":
        return (
            "Independent evidence leans the same way. The trail is strong enough to treat this "
            "sentence as the organisation's credible position at this layer — still inspect the files."
        )
    if status == "Likely":
        return (
            "The main sources agree, but something is still thin (one interview, a missing field, "
            "or a weaker second stream). Treat as probable, not locked."
        )
    if status == "Conflicted":
        return (
            "Meaningful weight sits on both sides. That is a finished answer on this pack — "
            "formal text and practised behaviour (or two strong streams) disagree. Do not average them."
        )
    if status == "Unlikely":
        return (
            "Some support exists, but stronger evidence points the other way. Prefer the heavier trail "
            "until a better first-hand file arrives."
        )
    if status == "Unsupported":
        return (
            "The claim is stated in the pack somewhere, but the files do not back it as current truth "
            "(or the gap is exactly that nobody is assigned)."
        )
    if status == "Not enough evidence":
        return (
            "Too little weighted evidence survived retrieval and reasoning. Widen the search, check the "
            "rulebook must-fetch IDs, or accept that the pack is silent."
        )
    return "Inspect the evidence table before acting on this status."


def explain_structured(
    claim_text: str,
    scored: Dict[str, Any],
    weighted_evidence: List[Dict[str, Any]],
) -> Dict[str, Any]:
    status = scored["status"]
    score = scored["credibility_score"]
    ci = scored.get("credible_interval")
    confidence = scored["confidence"]

    support = [e for e in weighted_evidence if e.get("stance") == "support"]
    contradict = [e for e in weighted_evidence if e.get("stance") == "contradict"]
    support_w = sum(float(e.get("final_weight") or 0) for e in support)
    contradict_w = sum(float(e.get("final_weight") or 0) for e in contradict)

    top_up = _top(support)
    top_down = _top(contradict)

    headline = f"{status} · score {_fmt(score)} · confidence {confidence}"
    if ci:
        headline += f" · interval {_fmt(ci[0])} – {_fmt(ci[1])}"

    raised = (
        [
            {
                "doc_id": e["doc_id"],
                "type": e.get("source_type"),
                "weight": e.get("final_weight"),
                "authority": e.get("authority_tier"),
                "preview": (e.get("text") or "")[:220].replace("\n", " "),
            }
            for e in top_up
        ]
        if top_up
        else []
    )
    lowered = (
        [
            {
                "doc_id": e["doc_id"],
                "type": e.get("source_type"),
                "weight": e.get("final_weight"),
                "authority": e.get("authority_tier"),
                "preview": (e.get("text") or "")[:220].replace("\n", " "),
            }
            for e in top_down
        ]
        if top_down
        else []
    )

    narrative = [
        f'Claim under test: “{claim_text}”',
        (
            f"Verdict {status} with credibility {_fmt(score)}"
            + (f" (bootstrap band {_fmt(ci[0])} to {_fmt(ci[1])})" if ci else "")
            + f" and {confidence} confidence on how complete the trail is."
        ),
        (
            f"Evidence kept after reasoning: {len(weighted_evidence)} chunks — "
            f"{len(support)} support (weight sum {_fmt(support_w)}), "
            f"{len(contradict)} contradict (weight sum {_fmt(contradict_w)})."
        ),
        _insight_for_status(status, len(support), len(contradict)),
    ]
    if raised:
        narrative.append(
            "What raised the score: "
            + "; ".join(
                f"{r['doc_id']} ({r['type']}, weight {_fmt(r['weight'])}, {r.get('authority') or 'tier n/a'})"
                for r in raised
            )
            + "."
        )
    else:
        narrative.append("What raised the score: nothing meaningful survived as support.")
    if lowered:
        narrative.append(
            "What lowered the score: "
            + "; ".join(
                f"{r['doc_id']} ({r['type']}, weight {_fmt(r['weight'])}, {r.get('authority') or 'tier n/a'})"
                for r in lowered
            )
            + "."
        )
    else:
        narrative.append("What lowered the score: no contradicting trail of weight.")

    narrative.append(
        "What would move this most: an approved, dated, first-hand document that names this exact rule "
        "or a CRM correction that closes the exception rows — not another copied Slack tip."
    )

    return {
        "headline": headline,
        "insight": _insight_for_status(status, len(support), len(contradict)),
        "paragraphs": narrative,
        "raised": raised,
        "lowered": lowered,
        "support_weight_sum": support_w,
        "contradict_weight_sum": contradict_w,
        "n_support": len(support),
        "n_contradict": len(contradict),
        "plain": " ".join(narrative),
    }


def explain_template(
    claim_text: str,
    scored: Dict[str, Any],
    weighted_evidence: List[Dict[str, Any]],
) -> str:
    return explain_structured(claim_text, scored, weighted_evidence)["plain"]


def explain_with_llm(
    claim_text: str,
    scored: Dict[str, Any],
    weighted_evidence: List[Dict[str, Any]],
    client=None,
) -> str:
    raise NotImplementedError("LLM-authored explanation not wired up yet; use explain_template().")
