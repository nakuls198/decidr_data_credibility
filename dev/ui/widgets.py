"""Shared Streamlit widgets — black / orange KPI tiles and rings."""
from __future__ import annotations

import math
from html import escape

import streamlit as st

from services.format_num import full_num
from ui.styles import badge


def hero(eyebrow: str, title: str, body: str) -> None:
    st.markdown(
        f'<div class="hero"><div class="eyebrow">{eyebrow}</div>'
        f'<h1 class="display">{title}</h1>'
        f"<p>{body}</p></div>",
        unsafe_allow_html=True,
    )


def _tile(value: str, label: str, variant: str = "dark") -> str:
    cls = "tile tile-orange" if variant == "orange" else "tile"
    return (
        f'<div class="{cls}"><div class="kpi num-full">{value}</div>'
        f'<div class="kpi-label">{label}</div></div>'
    )


def glass_kpis(items: list[tuple[str, str]]) -> None:
    """Four mixed dark / orange KPI tiles, like the reference boards."""
    html = ['<div class="kpi-grid">']
    for i, (value, label) in enumerate(items):
        variant = "orange" if i % 2 else "dark"
        html.append(_tile(value, label, variant))
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def mixed_kpis(items: list[tuple[str, str, str]]) -> None:
    html = ['<div class="kpi-grid">']
    for value, label, variant in items:
        html.append(_tile(value, label, variant))
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def ring_tile(percent: float, center: str, caption: str, tone: str = "orange") -> str:
    r = 46
    circ = 2 * math.pi * r
    pct = max(0.0, min(1.0, float(percent)))
    offset = circ * (1 - pct)
    cls = "prog white" if tone == "white" else "prog"
    return (
        f'<div class="ring-card"><div class="ring-svg">'
        f'<svg viewBox="0 0 120 120">'
        f'<circle class="track" cx="60" cy="60" r="{r}"/>'
        f'<circle class="{cls}" cx="60" cy="60" r="{r}" '
        f'stroke-dasharray="{circ:.2f}" stroke-dashoffset="{offset:.2f}"/>'
        f"</svg><div class=\"ring-val\">{center}</div></div>"
        f'<div class="ring-cap">{caption}</div></div>'
    )


def ring_row(items: list[tuple[float, str, str]]) -> None:
    html = ['<div class="ring-row">']
    for i, (percent, center, caption) in enumerate(items):
        tone = "white" if i % 2 else "orange"
        html.append(ring_tile(percent, center, caption, tone))
    html.append("</div>")
    st.markdown("".join(html), unsafe_allow_html=True)


def cream_note(title: str, body: str) -> None:
    st.markdown(
        f'<div class="panel-orange">'
        f"<h3 style='margin:0 0 .4rem;font-size:1.45rem;letter-spacing:-0.03em;'>{title}</h3>"
        f'<p style="margin:0;">{body}</p></div>',
        unsafe_allow_html=True,
    )


def orange_note(title: str, body: str) -> None:
    cream_note(title, body)


def status_line(status: str, score: float, confidence: str, interval=None) -> None:
    rng = "—"
    if interval:
        rng = f"{full_num(interval[0])} – {full_num(interval[1])}"
    mixed_kpis(
        [
            (escape(str(status)), "Verdict", "orange"),
            (full_num(score), "Score", "dark"),
            (escape(str(confidence)), "Confidence", "dark"),
            (rng, "Interval", "orange"),
        ]
    )
    st.markdown(f"{badge(status)} {badge(confidence)}", unsafe_allow_html=True)


def insight_panel(rich: dict) -> None:
    """Glorified, glanceable explanation of a scored claim."""
    if not rich:
        return
    paras = "".join(
        f'<p class="body-p">{escape(p)}</p>' for p in rich.get("paragraphs", [])
    )
    raised_items = rich.get("raised") or []
    lowered_items = rich.get("lowered") or []

    def _lis(rows):
        if not rows:
            return "<li>None of weight.</li>"
        out = []
        for r in rows:
            out.append(
                "<li><span class='wt'>"
                + escape(str(r.get("doc_id")))
                + "</span> · "
                + escape(str(r.get("type") or ""))
                + " · weight <span class='wt num-full'>"
                + escape(full_num(r.get("weight")))
                + "</span><br><span style='color:#8A8A8A;font-size:0.82rem;'>"
                + escape(str(r.get("preview") or "")[:160])
                + "</span></li>"
            )
        return "".join(out)

    html = (
        '<div class="insight-card">'
        '<div class="eyebrow">Result · read this first</div>'
        f'<h2>{escape(rich.get("headline") or "")}</h2>'
        f'<p class="lead">{escape(rich.get("insight") or "")}</p>'
        f"{paras}"
        '<div class="insight-split">'
        '<div class="insight-pane"><h4>Raised the score</h4><ul style="margin:0;padding-left:1.1rem;">'
        + _lis(raised_items)
        + "</ul></div>"
        '<div class="insight-pane"><h4>Lowered the score</h4><ul style="margin:0;padding-left:1.1rem;">'
        + _lis(lowered_items)
        + "</ul></div></div></div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def stages_strip() -> None:
    st.markdown(
        '<div class="stage">'
        "<span>1 Ingest</span><span>2 Extract</span><span>3 Retrieve</span>"
        "<span>4 Reason</span><span>5 Weight</span><span>6 Score</span>"
        "<span>7 Calibrate</span><span>8 Explain</span></div>",
        unsafe_allow_html=True,
    )
