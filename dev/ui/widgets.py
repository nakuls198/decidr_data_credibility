"""Shared Streamlit widgets — black / orange KPI tiles and rings."""
from __future__ import annotations

import math

import streamlit as st

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
        f'<div class="{cls}"><div class="kpi">{value}</div>'
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
        rng = f"{interval[0]:.2f}–{interval[1]:.2f}"
    mixed_kpis(
        [
            (status, "Verdict", "orange"),
            (f"{score:.2f}", "Score", "dark"),
            (confidence, "Confidence", "dark"),
            (rng, "Interval", "orange"),
        ]
    )
    st.markdown(f"{badge(status)} {badge(confidence)}", unsafe_allow_html=True)


def stages_strip() -> None:
    st.markdown(
        '<div class="stage">'
        "<span>1 Ingest</span><span>2 Extract</span><span>3 Retrieve</span>"
        "<span>4 Reason</span><span>5 Weight</span><span>6 Score</span>"
        "<span>7 Calibrate</span><span>8 Explain</span></div>",
        unsafe_allow_html=True,
    )
