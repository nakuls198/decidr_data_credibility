"""
Stage 8 — LLM explanation with visible thought process.

The score is NEVER chosen by the LLM — it only narrates the deterministic
pipeline result. Falls back to structured template when no API key is set.
"""

from __future__ import annotations

import json
import os
from typing import Any

from src.explain import explain_structured


def build_thought_process(
    claim_text: str,
    dispute_type: str,
    must_fetch: list[str],
    weighted: list[dict],
    scored: dict,
    rulebook_note: str = "",
) -> list[dict[str, str]]:
    """Step-by-step reasoning trace shown in the UI."""
    support = [e for e in weighted if e.get("stance") == "support"]
    contradict = [e for e in weighted if e.get("stance") == "contradict"]

    steps = [
        {
            "step": "1. Frame the claim",
            "detail": f'Under test: "{claim_text[:200]}{"..." if len(claim_text) > 200 else ""}"',
        },
        {
            "step": "2. Classify dispute type",
            "detail": f"Dispute type: {dispute_type}. {rulebook_note or 'Rulebook guides which sources should win.'}",
        },
        {
            "step": "3. Must-fetch documents",
            "detail": (
                "Rulebook linked set: " + ", ".join(must_fetch[:12])
                if must_fetch
                else "No process cluster matched — relying on BM25 retrieval only."
            ),
        },
        {
            "step": "4. Retrieve & reason",
            "detail": (
                f"Kept {len(weighted)} evidence chunks after stance filtering: "
                f"{len(support)} support, {len(contradict)} contradict."
            ),
        },
        {
            "step": "5. Weight evidence",
            "detail": (
                "Applied authority tier (policy > process > interview > comms), "
                "superseded/draft penalties, and independence collapse for duplicate Slack copies."
            ),
        },
        {
            "step": "6. Score & verdict",
            "detail": (
                f"Bayesian log-odds update → score {scored['credibility_score']:.3f}. "
                f"Status: {scored['status']} ({scored['confidence']} confidence)."
            ),
        },
    ]
    return steps


def explain_with_llm(
    claim_text: str,
    scored: dict[str, Any],
    weighted: list[dict[str, Any]],
    *,
    dispute_type: str = "RULE",
    must_fetch: list[str] | None = None,
    rulebook_note: str = "",
    model: str = "gpt-4o-mini",
) -> dict[str, Any]:
    """
    Returns {thought_process, narrative, source}.
    LLM rewrites narrative only; thought_process is always deterministic.
    """
    structured = explain_structured(claim_text, scored, weighted)
    thought = build_thought_process(
        claim_text,
        dispute_type,
        must_fetch or [],
        weighted,
        scored,
        rulebook_note,
    )

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {
            "thought_process": thought,
            "narrative": structured["plain"],
            "structured": structured,
            "source": "template",
        }

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        evidence_summary = json.dumps(
            [
                {
                    "doc_id": e.get("doc_id"),
                    "stance": e.get("stance"),
                    "weight": round(float(e.get("final_weight") or 0), 3),
                    "preview": (e.get("text") or "")[:180],
                }
                for e in sorted(weighted, key=lambda x: float(x.get("final_weight") or 0), reverse=True)[:8]
            ],
            indent=2,
        )

        prompt = f"""You are explaining a credibility assessment for organisational knowledge (Northfield / Decidr iLab project).

IMPORTANT: The verdict is ALREADY DECIDED. Do NOT change it.
Verdict: {scored['status']}
Score: {scored['credibility_score']:.3f}
Confidence: {scored['confidence']}
Dispute type: {dispute_type}

Claim: {claim_text}

Evidence (top weighted):
{evidence_summary}

Write 2-3 short paragraphs explaining WHY this verdict makes sense given the evidence.
Mention specific document IDs. If Conflicted, explain both sides fairly.
Do not invent evidence not listed above."""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You explain pre-computed credibility verdicts. Never change the verdict."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=600,
        )
        narrative = response.choices[0].message.content or structured["plain"]
        return {
            "thought_process": thought,
            "narrative": narrative,
            "structured": structured,
            "source": "llm",
        }
    except Exception as exc:
        return {
            "thought_process": thought,
            "narrative": structured["plain"] + f"\n\n(LLM unavailable: {exc})",
            "structured": structured,
            "source": "template",
        }
