from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from services import engine
from ui.styles import CSS, badge
from ui.widgets import cream_note, glass_kpis, hero, mixed_kpis, ring_row, stages_strip, status_line

ROOT = Path(__file__).resolve().parent

PLOT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#F4F4F4", family="Outfit"),
    margin=dict(l=10, r=10, t=36, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#A3A3A3")),
    colorway=["#FF6A12", "#FF4E00", "#FFFFFF", "#8A8A8A", "#3F3F3F"],
)
BAR_ORANGE = "#FF6A12"

PRESET_CLAIMS = [
    "Head of Finance and People Ops must approve new-business discounts of 15 percent or more in the CRM before Closed Won.",
    "Every new-business discount of 15 percent or more is approved by Finance in the CRM before close, with no exceptions.",
    "The Financial Controller Victor is the accountable approver for discounts at or above threshold.",
    "On genuinely urgent deals, Head of Sales may approve discounts of 15 percent or more outside the CRM, with paperwork later.",
    "New customer onboarding follows a standard 6-week implementation process owned by the Customer Success and Delivery team.",
    "Customer-reported issues must be escalated from Support to Engineering via a ticket before Engineering is engaged.",
]


def _style_fig(fig):
    fig.update_layout(**PLOT)
    fig.update_xaxes(gridcolor="#1F1F1F", zeroline=False, linecolor="#1F1F1F", tickfont=dict(color="#8A8A8A"))
    fig.update_yaxes(gridcolor="#1F1F1F", zeroline=False, linecolor="#1F1F1F", tickfont=dict(color="#8A8A8A"))
    return fig


@st.cache_resource(show_spinner=False)
def _stores():
    chunks = engine.load_chunks()
    documents = engine.load_documents()
    roster = engine.load_roster()
    retriever = engine.build_retriever(chunks)
    profile = engine.corpus_profile(chunks, documents, roster)
    gold = engine.load_gold()
    return chunks, documents, roster, retriever, profile, gold


def page_overview(profile: dict) -> None:
    hero(
        "iLab 14-01  ·  Decidr  ·  Northfield Software",
        "Credibility<br>Studio",
        "Organisational knowledge here is split across policies, Slack, CRM and leftover process docs. "
        "This studio runs the eight-stage method from the group proposal: find a claim, fetch evidence, "
        "weigh sources, and return a status a teammate can inspect — including when the honest answer is Conflicted.",
    )
    stages_strip()
    mixed_kpis(
        [
            (f"{profile['document_count']}", "Source files", "dark"),
            (f"{profile['chunk_count']}", "Searchable chunks", "orange"),
            (f"{profile['roster_count']}", "People on roster", "dark"),
            (profile["assessment_date"], "Assessment date", "orange"),
        ]
    )
    c1, c2 = st.columns((1.15, 1))
    with c1:
        cream_note(
            "What this is not",
            "It is not a chatbot that hides disagreement. A language model may later write the explanation, "
            "but it does not choose the score. Calibration is refused until enough labels exist.",
        )
        st.markdown(
            '<div class="glass"><div class="eyebrow">The tension</div>'
            "<p class='small'>POL-01 (March 2025) says Harriet must approve new-business discounts of 15%+ in the CRM. "
            "PROC-02 (2022) still names Victor. Diane’s Slack workaround is copied through COMMS-02–04. "
            "Some CRM rows follow policy; DEAL-014 / 027 / 041 do not. Formal and practised are two claims.</p></div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="glass"><div class="eyebrow">How to use this studio</div>'
            "<p class='small'><b>Command centre</b> — pack numbers.<br>"
            "<b>Data atlas</b> — files and people.<br>"
            "<b>Claim workbench</b> — score one sentence.<br>"
            "<b>Evidence chat</b> — ask in plain language.<br>"
            "<b>Pipeline trace</b> — every stage, visible.<br>"
            "<b>Evaluation</b> — recall vs the gold list.<br>"
            "<b>Method</b> — why each stage exists.</p></div>",
            unsafe_allow_html=True,
        )


def page_dashboard(profile: dict, chunks, roster) -> None:
    hero(
        "Command centre",
        "KPI<br>Dashboard",
        "Counts from the ingested store. They describe the files, not credibility.",
    )
    mixed_kpis(
        [
            (str(profile["chunk_count"]), "Chunks", "dark"),
            (str(profile["document_count"]), "Documents", "orange"),
            (str(profile["superseded_chunks"]), "Superseded chunks", "dark"),
            (str(len(profile["chunk_types"])), "Source types", "orange"),
        ]
    )
    total = max(int(profile["chunk_count"]), 1)
    top_types = sorted(profile["chunk_types"].items(), key=lambda kv: kv[1], reverse=True)[:4]
    ring_row(
        [
            (n / total, f"{n / total:.0%}", name.replace("_", " "))
            for name, n in top_types
        ]
    )
    df = pd.DataFrame(
        {"source": list(profile["chunk_types"].keys()), "chunks": list(profile["chunk_types"].values())}
    ).sort_values("chunks", ascending=False)
    left, right = st.columns(2)
    with left:
        fig = px.bar(df, x="source", y="chunks")
        fig.update_traces(marker_color=BAR_ORANGE, marker_line_width=0)
        fig.update_layout(title=dict(text="Chunks by source type", font=dict(size=16, color="#FFFFFF")))
        st.plotly_chart(_style_fig(fig), use_container_width=True, config={"displayModeBar": False})
    with right:
        fig_line = px.line(df, x="source", y="chunks", markers=True)
        fig_line.update_traces(line=dict(color=BAR_ORANGE, width=3), marker=dict(color="#FFFFFF", size=8))
        fig_line.update_layout(title=dict(text="Source mix (same counts, line view)", font=dict(size=16, color="#FFFFFF")))
        st.plotly_chart(_style_fig(fig_line), use_container_width=True, config={"displayModeBar": False})

    c1, c2 = st.columns(2)
    with c1:
        fig2 = px.pie(
            names=list(profile["phases"].keys()),
            values=list(profile["phases"].values()),
            hole=0.72,
            color_discrete_sequence=["#FF6A12", "#2A2A2A", "#FF4E00", "#8A8A8A"],
        )
        fig2.update_traces(textinfo="label+value", textfont_color="#FFFFFF", marker=dict(line=dict(color="#0A0A0A", width=2)))
        fig2.update_layout(title=dict(text="Chunks by phase", font=dict(size=16, color="#FFFFFF")))
        st.plotly_chart(_style_fig(fig2), use_container_width=True, config={"displayModeBar": False})
    with c2:
        weights = engine.authority_legend()
        wdf = pd.DataFrame({"source": list(weights.keys()), "weight": list(weights.values())}).sort_values("weight")
        fig3 = px.bar(wdf, x="weight", y="source", orientation="h", color_discrete_sequence=[BAR_ORANGE])
        fig3.update_traces(marker_color=BAR_ORANGE, marker_line_width=0)
        fig3.update_layout(title=dict(text="Starting authority weights", font=dict(size=16, color="#FFFFFF")))
        st.plotly_chart(_style_fig(fig3), use_container_width=True, config={"displayModeBar": False})
        st.caption("An in-force policy is not equal to a Slack tip.")

    if roster:
        rdf = pd.DataFrame(roster)
        if "function" in rdf.columns:
            counts = rdf["function"].value_counts().reset_index()
            counts.columns = ["function", "people"]
            fig4 = px.bar(counts, x="function", y="people", color_discrete_sequence=[BAR_ORANGE])
            fig4.update_traces(marker_color=BAR_ORANGE, marker_line_width=0)
            fig4.update_layout(title=dict(text="Roster by function", font=dict(size=16, color="#FFFFFF")))
            st.plotly_chart(_style_fig(fig4), use_container_width=True, config={"displayModeBar": False})


def page_atlas(chunks, documents, roster) -> None:
    hero("Data atlas", "What was ingested", "Raw Phase 1 lives in data/phase1. Raw Phase 2 lives in data/phase2 (folder, not a zip). The working store is data/outputs after local ingest: overlapping files keep the Phase 2 copy.")
    tab1, tab2, tab3 = st.tabs(["Chunks", "Documents", "Roster"])
    cdf = pd.DataFrame(
        [
            {
                "chunk_id": c.chunk_id,
                "doc_id": c.doc_id,
                "source_type": c.source_type,
                "phase": c.phase,
                "heading": c.heading,
                "superseded": c.metadata.get("superseded"),
                "chars": len(c.text or ""),
                "preview": (c.text or "")[:180].replace("\n", " "),
            }
            for c in chunks
        ]
    )
    ddf = pd.DataFrame(
        [
            {
                "doc_id": d.doc_id,
                "source_type": d.source_type,
                "phase": d.phase,
                "n_chunks": d.n_chunks,
                "path": d.path,
                "superseded": d.metadata.get("superseded"),
            }
            for d in documents
        ]
    )
    with tab1:
        f1, f2 = st.columns(2)
        src = f1.multiselect("Source type", sorted(cdf.source_type.unique()), default=[])
        q = f2.text_input("Search text")
        view = cdf
        if src:
            view = view[view.source_type.isin(src)]
        if q:
            view = view[view.preview.str.contains(q, case=False, na=False) | view.doc_id.str.contains(q, case=False, na=False)]
        st.dataframe(view, use_container_width=True, hide_index=True, height=420)
        st.caption(f"{len(view)} of {len(cdf)} chunks")
    with tab2:
        st.dataframe(ddf, use_container_width=True, hide_index=True, height=420)
    with tab3:
        if roster:
            st.dataframe(pd.DataFrame(roster), use_container_width=True, hide_index=True, height=420)
        else:
            st.info("Roster file not found.")


def _claim_id_from_text(text: str) -> str:
    digest = hashlib.sha1(text.encode()).hexdigest()[:6].upper()
    return f"LIVE-{digest}"


def _show_result(result: dict) -> None:
    sc = result["scored"]
    status_line(sc["status"], sc["credibility_score"], sc["confidence"], sc.get("credible_interval"))
    st.markdown(f"<p class='small'>{result['explanation']}</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Retrieved", result["n_retrieved"])
    c2.metric("Kept after reasoning", result["n_kept"])
    c3.metric("Dropped as unrelated", result["n_dropped"])
    if result["weighted"]:
        wdf = pd.DataFrame(
            [
                {
                    "doc_id": e["doc_id"],
                    "type": e["source_type"],
                    "stance": e["stance"],
                    "weight": e.get("final_weight"),
                    "authority": e.get("authority_tier"),
                    "independence": e.get("independence_weight"),
                    "preview": (e.get("text") or "")[:160].replace("\n", " "),
                }
                for e in result["weighted"]
            ]
        )
        st.dataframe(wdf, use_container_width=True, hide_index=True, height=280)


def page_workbench(chunks, retriever, gold) -> None:
    hero(
        "Claim workbench",
        "Score one testable sentence",
        "A claim needs a role, an action and a condition. Formal and practised versions of the same topic are two rows.",
    )
    options = ["Type a claim"] + [f"{c['claim_id']} · {c['claim_text']}" for c in gold["claims"]]
    choice = st.selectbox("Gold list", options)
    default = PRESET_CLAIMS[0]
    if choice != "Type a claim":
        default = choice.split(" · ", 1)[1]
    claim = st.text_area("Claim", value=default, height=90)
    c1, c2, c3 = st.columns(3)
    top_k = c1.slider("Retrieve top-k", 5, 30, 15)
    method = c2.selectbox("Score method", ["bayesian", "weighted_checklist"])
    prior = c3.slider("Prior (Bayesian)", 0.1, 0.9, 0.5, 0.05)
    go_btn = st.button("Run pipeline", type="primary", use_container_width=True)
    if go_btn and claim.strip():
        with st.spinner("Retrieving and scoring…"):
            result = engine.run_claim(
                claim.strip(),
                _claim_id_from_text(claim),
                retriever,
                chunks,
                top_k=top_k,
                prior=prior,
                method=method,
            )
        st.session_state.last_trace = result
        hist = st.session_state.setdefault("history", [])
        hist.append(
            {
                "claim": claim.strip(),
                "status": result["scored"]["status"],
                "score": result["scored"]["credibility_score"],
            }
        )
        _show_result(result)
        with st.expander("Retrieval shortlist (including unrelated)"):
            hdf = pd.DataFrame(result["hits"])
            if not hdf.empty:
                hdf["preview"] = hdf["text"].str.replace("\n", " ").str[:180]
                st.dataframe(
                    hdf[["doc_id", "source_type", "retrieval_score", "stance", "kept", "preview"]],
                    use_container_width=True,
                    hide_index=True,
                )
        st.info(result["calibration"])
    if st.session_state.get("history"):
        st.markdown("##### Session scores")
        st.dataframe(pd.DataFrame(st.session_state["history"]), use_container_width=True, hide_index=True)


def page_chat(chunks, retriever) -> None:
    hero(
        "Evidence chat",
        "Ask how Northfield actually works",
        "Your message is treated as a claim. The reply is a status, a score, and the files that moved it — not a free-form chatbot paragraph.",
    )
    st.markdown(
        "<div class='glass'><div class='eyebrow'>Try</div><p class='small'>"
        + "<br>".join(f"· {p}" for p in PRESET_CLAIMS[:4])
        + "</p></div>",
        unsafe_allow_html=True,
    )
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "text": "Ask a Northfield claim. I will search the chunk store, drop unrelated hits, weigh policy above Slack, and return a status you can inspect.",
                "result": None,
            }
        ]
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["text"])
            if msg.get("result"):
                _show_result(msg["result"])
                st.session_state.last_trace = msg["result"]

    chips = st.columns(3)
    for i, chip in enumerate(PRESET_CLAIMS[:3]):
        if chips[i].button(chip[:42] + "…", key=f"chip{i}"):
            st.session_state._queued = chip

    prompt = st.chat_input("Type a claim about how Northfield works…")
    queued = st.session_state.pop("_queued", None)
    user_text = prompt or queued
    if user_text:
        st.session_state.messages.append({"role": "user", "text": user_text, "result": None})
        result = engine.run_claim(
            user_text.strip(),
            _claim_id_from_text(user_text),
            retriever,
            chunks,
            top_k=15,
        )
        sc = result["scored"]
        reply = (
            f"**{sc['status']}** · score {sc['credibility_score']:.2f} · confidence {sc['confidence']}. "
            f"Kept {result['n_kept']} of {result['n_retrieved']} retrieved chunks."
        )
        st.session_state.messages.append({"role": "assistant", "text": reply, "result": result})
        st.rerun()


def page_trace() -> None:
    hero(
        "Pipeline trace",
        "Every stage, left visible",
        "If retrieval misses POL-01, later stages must not invent a score. Open a claim in Workbench or Chat first.",
    )
    result = st.session_state.get("last_trace")
    if not result:
        st.warning("Run a claim in the workbench or chat to fill this trace.")
        return
    steps = [
        ("1 · Ingest", "Already done from data/phase1 + data/phase2. Later stages read chunks.jsonl, they do not re-parse the pack."),
        ("2 · Claim", result["claim_text"]),
        ("3 · Retrieve", f"BM25, top_k={result['top_k']}. Tokens: {', '.join(result['query_tokens'][:18])}"),
        ("4 · Reason", f"{result['n_kept']} kept, {result['n_dropped']} unrelated dropped."),
        ("5 · Weight", "Policy > process > meeting > interview > CRM > Slack. Copies share independence weight."),
        ("6 · Score", f"{result['method']} · prior {result['prior']}"),
        ("7 · Calibrate", result["calibration"]),
        ("8 · Explain", "Template prose. The model does not choose the score."),
    ]
    for title, body in steps:
        st.markdown(
            f'<div class="glass trace-step"><b>{title}</b><p class="small">{body}</p></div>',
            unsafe_allow_html=True,
        )
    _show_result(result)
    fig = go.Figure()
    kept = [h for h in result["hits"] if h["kept"]]
    dropped = [h for h in result["hits"] if not h["kept"]]
    if kept:
        fig.add_bar(
            x=[h["doc_id"] for h in kept],
            y=[h["retrieval_score"] for h in kept],
            name="kept",
            marker_color="#FF6A12",
        )
    if dropped:
        fig.add_bar(
            x=[h["doc_id"] for h in dropped],
            y=[h["retrieval_score"] for h in dropped],
            name="unrelated",
            marker_color="#3F3F3F",
        )
    st.plotly_chart(_style_fig(fig), use_container_width=True, config={"displayModeBar": False})
    st.caption("Heuristic stance can mis-label a policy that uses contrast language. That is a known gap, shown here rather than hidden.")


def page_eval(chunks, retriever) -> None:
    hero(
        "Evaluation",
        "Does search recover the files we already know?",
        "Recall is measured against the human gold list. Status match uses the current heuristic reasoner — disagreement is useful, not something to paper over.",
    )
    top_k = st.slider("k", 5, 30, 15, key="eval_k")
    if st.button("Run gold evaluation", type="primary"):
        with st.spinner("Scoring gold claims…"):
            rows = engine.evaluate_gold(retriever, chunks, top_k=top_k)
        st.session_state.eval_rows = rows
    rows = st.session_state.get("eval_rows")
    if not rows:
        st.info("Run the evaluation to fill this table. It uses BM25 + the current reasoner.")
        return
    df = pd.DataFrame(rows)
    n = len(df)
    match = int(df["match"].sum())
    rec = float(df["retrieval_recall"].mean())
    glass_kpis(
        [
            (f"{rec:.0%}", "Mean recall @ k"),
            (f"{match}/{n}", "Status matches"),
            (str(n), "Gold claims"),
        ]
    )
    show = df[
        ["claim_id", "layer", "expected_status", "actual_status", "score", "confidence", "retrieval_recall", "match"]
    ]
    st.dataframe(show, use_container_width=True, hide_index=True)
    fig = px.bar(
        df,
        x="claim_id",
        y="retrieval_recall",
        color="match",
        color_discrete_map={True: "#FF6A12", False: "#3F3F3F"},
    )
    st.plotly_chart(_style_fig(fig), use_container_width=True, config={"displayModeBar": False})
    from src.calibrate import enough_labels_to_calibrate

    _, msg = enough_labels_to_calibrate(n)
    cream_note("Calibration gate", msg)


def page_extract(chunks) -> None:
    hero(
        "Claim extraction",
        "Rule-based candidates",
        "Sentences with must / shall / required. Unreviewed. An LLM may propose later; a human still has to keep role, action, condition.",
    )
    limit = st.slider("Show first N", 10, 80, 30)
    with st.spinner("Extracting…"):
        rows, total = engine.candidate_claims(chunks, limit=limit)
    st.caption(f"{total} candidates in the pack. Showing {len(rows)}.")
    df = pd.DataFrame(rows)
    keep = [c for c in ["claim_id", "claim_text", "responsible_role", "layer", "origin_doc_id", "extraction_confidence"] if c in df.columns]
    st.dataframe(df[keep] if keep else df, use_container_width=True, hide_index=True, height=460)


def page_method() -> None:
    hero(
        "Method",
        "Eight stages, one trail",
        "Borrowed from automated fact-checking (claim → evidence → verdict), adapted for a 29-person company whose files disagree on purpose.",
    )
    stages = [
        ("1. Ingest", "Policies, meetings, Slack, CRM, tasks, audit log → one chunk store with source id, type, superseded flag. Markdown splits on headings; each CSV row is a chunk."),
        ("2. Extract", "One testable sentence. Split formal vs practised. Rule-based baseline now; LLM hook exists but is not trusted alone."),
        ("3. Retrieve", "BM25 keyword baseline. Meaning search is optional. If known ids for the discount claim do not return, vectors are not progress."),
        ("4. Reason", "Support / contradict / unrelated. Unrelated is dropped, not averaged. Current classifier is lexical + negation cues — inspect POL-01 carefully."),
        ("5. Weight", "Approved policy outweighs Slack. Recency is still a stub. Copied workarounds share independence weight so COMMS-02/03/04 are not three confirmations."),
        ("6. Score", "Bayesian log-odds update from a prior, or a weighted checklist. Status is separate from confidence. Conflicted is a finished answer."),
        ("7. Calibrate", "If it says 80% it should be right four times in five. Code exists. It will not run a pretty plot on four sample rows."),
        ("8. Explain", "Score + who raised it + who lowered it. Prose may be rewritten by a model. The number must not move."),
    ]
    for t, b in stages:
        st.markdown(f'<div class="glass"><b>{t}</b><p class="small">{b}</p></div>', unsafe_allow_html=True)
    cream_note(
        "Hard rules",
        "Do not invent a 0–100 that the files cannot support. Copied Slack is one source. Drafts are down-weighted, not deleted. "
        "This is not a legally defensible audit tool.",
    )


def main() -> None:
    st.set_page_config(
        page_title="Northfield Credibility Studio",
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

    chunks, documents, roster, retriever, profile, gold = _stores()

    with st.sidebar:
        st.markdown(
            "<div class='eyebrow'>DECIDR × ILAB 14-01</div>"
            "<h2 style='font-family:Outfit,sans-serif;font-weight:800;margin:.2rem 0 .6rem;letter-spacing:-0.04em;'>Northfield</h2>",
            unsafe_allow_html=True,
        )
        page = st.radio(
            "Navigate",
            [
                "Overview",
                "Command centre",
                "Data atlas",
                "Claim workbench",
                "Evidence chat",
                "Pipeline trace",
                "Claim extraction",
                "Evaluation",
                "Method",
            ],
            label_visibility="collapsed",
        )
        st.markdown(
            f"<p class='small'>Working store: <code>data/outputs/chunks.jsonl</code><br>"
            f"{profile['document_count']} files · {profile['chunk_count']} chunks · assessment {profile['assessment_date']}<br>"
            "Raw Phase 2 on disk: <code>data/phase2/</code></p>",
            unsafe_allow_html=True,
        )

    routes = {
        "Overview": lambda: page_overview(profile),
        "Command centre": lambda: page_dashboard(profile, chunks, roster),
        "Data atlas": lambda: page_atlas(chunks, documents, roster),
        "Claim workbench": lambda: page_workbench(chunks, retriever, gold),
        "Evidence chat": lambda: page_chat(chunks, retriever),
        "Pipeline trace": page_trace,
        "Claim extraction": lambda: page_extract(chunks),
        "Evaluation": lambda: page_eval(chunks, retriever),
        "Method": page_method,
    }
    routes[page]()


if __name__ == "__main__":
    main()
