"""SBP Insight — Organizational Behavior case study of the State Bank of Pakistan (Group 5, DUET)."""
import json
from datetime import date
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).parent
D = json.loads((ROOT / "sbp.json").read_text(encoding="utf-8"))
NLP_CSV = ROOT / "mps_nlp.csv"
NLP_TERMS = ROOT / "mps_terms.json"

G, GOLD, INK, MUTED, BG = "#2FA37A", "#D4AF37", "#EDE6D6", "#A39B88", "#0A0E0C"
GOLD2, EMER, PANEL = "#F1D68A", "#1F7A5A", "#111814"
MODE_COLOR = {"Competing": "#C0563F", "Collaborating": EMER, "Compromising": "#B08D2E", "Accommodating": "#3F6E9C", "Avoiding": "#5E6660", "—": "#5E6660"}
PALETTE = [GOLD, G, GOLD2, "#3F6E9C", "#B08D2E", "#7FBFA3", "#C0563F", "#8C7A4A", "#5FA8D3", "#E0C877", "#2C5E4A", "#9C8F6E"]

st.set_page_config(page_title="SBP Insight · OB Case Study", page_icon="🏦", layout="wide", initial_sidebar_state="collapsed")

st.markdown(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  html, body, [data-testid="stAppViewContainer"] {{ background: radial-gradient(1200px 600px at 10% -10%, #17322A 0%, {BG} 55%) fixed; color: {INK}; }}
  [data-testid="stHeader"] {{ background: transparent; }}
  .block-container {{ padding-top: 1.4rem; max-width: 1200px; }}
  html, body, p, li, label, .stMarkdown, [data-testid="stMarkdownContainer"] {{ font-family: 'Inter', system-ui, sans-serif; color: {INK}; }}
  h1, h2, h3, h4 {{ font-family: 'Cormorant Garamond', Georgia, serif !important; color: {INK} !important; letter-spacing: .01em; }}
  h3 {{ font-size: 1.85rem !important; }}
  .hero {{ position: relative; overflow: hidden; border-radius: 22px; padding: 34px 36px; margin-bottom: 22px;
           background: linear-gradient(135deg, rgba(212,175,55,.16), rgba(31,122,90,.18) 60%, rgba(10,14,12,.6));
           border: 1px solid rgba(212,175,55,.35); box-shadow: 0 20px 60px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.06); }}
  .hero:after {{ content: ""; position: absolute; inset: -40%; background: conic-gradient(from 180deg, transparent, rgba(212,175,55,.10), transparent 30%);
                 animation: spin 14s linear infinite; }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  .hero > * {{ position: relative; z-index: 1; }}
  .hero h1 {{ font-family: 'Cormorant Garamond', serif; font-size: 3.1rem; margin: 4px 0 6px 0; line-height: 1.05;
              background: linear-gradient(90deg, {GOLD2}, {GOLD} 45%, #FFF3C4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
  .hero p {{ margin: 0; color: #CFC7B3; font-size: 1.05rem; max-width: 760px; }}
  .eyebrow {{ color: {GOLD}; font-weight: 600; letter-spacing: .22em; text-transform: uppercase; font-size: .72rem; }}
  .divider {{ height: 1px; background: linear-gradient(90deg, transparent, rgba(212,175,55,.6), transparent); margin: 6px 0 18px 0; }}
  .card {{ background: linear-gradient(180deg, rgba(255,255,255,.035), rgba(255,255,255,.01)); border: 1px solid rgba(212,175,55,.22);
           border-radius: 16px; padding: 18px 20px; height: 100%; transition: transform .25s ease, border-color .25s ease, box-shadow .25s ease; }}
  .card:hover {{ transform: translateY(-3px); border-color: rgba(212,175,55,.6); box-shadow: 0 14px 34px rgba(0,0,0,.35); }}
  .card h4 {{ margin: 0 0 6px 0; color: {GOLD2} !important; font-size: 1.35rem; }}
  .card p {{ margin: 0; color: {MUTED}; font-size: .92rem; line-height: 1.5; }}
  .tag {{ display: inline-block; background: rgba(47,163,122,.14); color: #8FD9BC; border: 1px solid rgba(47,163,122,.35);
          border-radius: 999px; padding: 2px 10px; font-size: .74rem; margin-top: 10px; }}
  .quote {{ border: 1px solid rgba(212,175,55,.3); border-left: 4px solid {GOLD}; background: rgba(212,175,55,.06); padding: 16px 20px;
            border-radius: 12px; font-family: 'Cormorant Garamond', serif; font-size: 1.35rem; line-height: 1.35; color: #F3EBD6; }}
  .case {{ background: rgba(255,255,255,.025); border: 1px solid rgba(212,175,55,.2); border-radius: 16px; padding: 16px 20px; margin-bottom: 12px; }}
  .case p {{ color: #D8D0BD; }}
  .case .yr {{ color: {GOLD}; font-weight: 600; letter-spacing: .08em; }}
  .pill {{ display: inline-block; color: #fff; border-radius: 999px; padding: 2px 10px; font-size: .74rem; margin-left: 8px; }}
  .goal {{ display: flex; gap: 14px; align-items: flex-start; padding: 10px 0; border-bottom: 1px solid rgba(212,175,55,.12); }}
  .goal .n {{ font-family: 'Cormorant Garamond', serif; font-size: 1.8rem; color: {GOLD}; line-height: 1; min-width: 30px; }}
  .stTabs [data-baseweb="tab-list"] {{ gap: 6px; border-bottom: 1px solid rgba(212,175,55,.2); flex-wrap: wrap; }}
  .stTabs [data-baseweb="tab"] {{ background: rgba(255,255,255,.03); border: 1px solid rgba(212,175,55,.18); border-radius: 999px; padding: 6px 14px; color: #CFC7B3; }}
  .stTabs [aria-selected="true"] {{ background: linear-gradient(90deg, rgba(212,175,55,.25), rgba(47,163,122,.2)); color: #FFF3C4 !important; border-color: rgba(212,175,55,.6); }}
  .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{ display: none; }}
  div[data-testid="stMetric"] {{ background: rgba(255,255,255,.03); border: 1px solid rgba(212,175,55,.22); border-radius: 14px; padding: 12px 16px; }}
  div[data-testid="stMetricValue"] {{ font-family: 'Cormorant Garamond', serif; color: {GOLD2}; font-size: 2.2rem; }}
  div[data-testid="stMetricLabel"] p {{ color: {MUTED}; letter-spacing: .08em; text-transform: uppercase; font-size: .72rem; }}
  [data-testid="stDataFrame"] {{ border: 1px solid rgba(212,175,55,.2); border-radius: 12px; }}
  .stAlert {{ background: rgba(47,163,122,.08) !important; border: 1px solid rgba(47,163,122,.3) !important; border-radius: 12px; }}
  .footer {{ text-align: center; color: {MUTED}; font-size: .8rem; margin-top: 30px; }}
  @media (max-width: 640px) {{ .hero h1 {{ font-size: 2.2rem; }} .hero {{ padding: 22px; }} .quote {{ font-size: 1.15rem; }} }}
</style>
""", unsafe_allow_html=True)


def chart(fig, h=420, m=None):
    fig.update_layout(height=h, margin=m or dict(l=10, r=10, t=40, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#D8D0BD", family="Inter, Arial"), legend=dict(orientation="h", y=-0.15), colorway=PALETTE,
                      hoverlabel=dict(bgcolor="#141B17", bordercolor=GOLD, font_color="#F3EBD6"))
    fig.update_xaxes(gridcolor="rgba(212,175,55,.10)", zerolinecolor="rgba(212,175,55,.25)")
    fig.update_yaxes(gridcolor="rgba(212,175,55,.10)", zerolinecolor="rgba(212,175,55,.25)")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ---------------- header ----------------
st.markdown("""<div class="hero"><div class="eyebrow">Organizational Behavior · Group 5 · DUET Karachi</div>
<h1>SBP Insight</h1><div class="divider"></div><p>An analysis of organizational behavior and dynamics: a case study of the State Bank of Pakistan.</p></div>""",
            unsafe_allow_html=True)

tabs = st.tabs(["🏛️ Overview", "🧩 Structure", "🌱 Culture", "📢 Communication", "🧭 Leadership", "⚖️ Power & Conflict", "📊 SWOT", "ℹ️ About"])

# ---------------- Overview ----------------
with tabs[0]:
    cols = st.columns(4)
    for c, (k, v) in zip(cols, D["facts"]):
        c.markdown(f'<div class="card"><div class="eyebrow">{k}</div><h4>{v}</h4></div>', unsafe_allow_html=True)
    st.write("")
    a, b = st.columns(2)
    a.markdown("#### Vision"); a.markdown(f'<div class="quote">“{D["vision"]}”</div>', unsafe_allow_html=True)
    b.markdown("#### Mission"); b.markdown(f'<div class="quote">“{D["mission"]}”</div>', unsafe_allow_html=True)
    st.markdown("### Core values")
    for row in range(2):
        cs = st.columns(3)
        for c, (name, desc, ob) in zip(cs, D["values"][row * 3:(row + 1) * 3]):
            c.markdown(f'<div class="card"><h4>{name}</h4><p>{desc}</p><span class="tag">OB: {ob}</span></div>', unsafe_allow_html=True)
        st.write("")
    st.markdown("### Strategic Plan 2023–28: SBP Vision 2028")
    st.markdown("".join(f'<div class="goal"><div class="n">{i:02d}</div><div>{gl}</div></div>' for i, gl in enumerate(D["goals"], 1)), unsafe_allow_html=True)
    st.caption("Cross-cutting themes: " + " · ".join(D["themes"]))

# ---------------- Structure ----------------
with tabs[1]:
    st.markdown("### Functional groups and departments")
    st.caption("Click a group to zoom in. Size = number of departments.")
    rows = [("SBP", g, d) for g, ds in D["groups"].items() for d in ds]
    df = pd.DataFrame(rows, columns=["root", "group", "department"]); df["n"] = 1
    fig = px.sunburst(df, path=["root", "group", "department"], values="n", color="group",
                      color_discrete_sequence=PALETTE)
    fig.update_traces(insidetextorientation="radial", hovertemplate="%{label}<extra></extra>")
    chart(fig, 560)
    st.markdown("### Who decides what")
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card"><h4>Board of Directors</h4><p>Governor (chair), 8 non-executive directors and the Finance Secretary (non-voting since 2022). Oversees governance, budget and strategy.</p></div>', unsafe_allow_html=True)
    c2.markdown('<div class="card"><h4>Monetary Policy Committee</h4><p>10 members: Governor, 3 SBP executives, 3 Board members, 3 external experts. Alone decides the policy rate.</p></div>', unsafe_allow_html=True)
    c3.markdown('<div class="card"><h4>Executive Committee</h4><p>Governor, 3 Deputy Governors and Executive Directors. Runs day-to-day policy and administration.</p></div>', unsafe_allow_html=True)
    st.markdown("### Structure through OB models")
    st.dataframe(pd.DataFrame([
        ["Work specialization", "High", "Experts in narrow fields"],
        ["Chain of command", "Clear and long", "Governor → DGs → EDs → Directors → staff"],
        ["Centralization", "High", "Policy rate and regulations decided at the top"],
        ["Formalization", "Very high", "Written rules, circulars, legal procedures"],
        ["Mintzberg type", "Machine bureaucracy", "with a professional (expert) core"],
    ], columns=["Dimension", "SBP", "Meaning"]), hide_index=True, use_container_width=True)

# ---------------- Culture ----------------
with tabs[2]:
    a, b = st.columns([1.1, 1])
    with a:
        st.markdown("### Pakistan's national culture (Hofstede)")
        h = D["hofstede"]; k = list(h)
        fig = go.Figure(go.Scatterpolar(r=list(h.values()) + [list(h.values())[0]], theta=k + [k[0]], fill="toself",
                                        line=dict(color=GOLD, width=2), fillcolor="rgba(212,175,55,.22)"))
        fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(range=[0, 100], showticklabels=True, gridcolor="rgba(212,175,55,.15)"), angularaxis=dict(gridcolor="rgba(212,175,55,.15)")), showlegend=False)
        chart(fig, 420, dict(l=90, r=90, t=40, b=40))
        st.caption("Scores (0–100): " + " · ".join(f"{a} {v}" for a, v in h.items()))
    with b:
        st.markdown("### Schein's three levels at SBP")
        for t, d in [("Artifacts", "Historic head office and museum, formal dress and titles, circulars, bilingual publications."),
                     ("Espoused values", "Integrity, accountability, innovation, inclusion, people-centric, environment."),
                     ("Basic assumptions", "Stability first; decisions must be data-driven and defensible; respect for hierarchy.")]:
            st.markdown(f'<div class="card"><h4>{t}</h4><p>{d}</p></div>', unsafe_allow_html=True); st.write("")
    st.info("**Culture in change:** Vision 2028 aims for a *high-tech, people-centric* SBP, and the Banking on Equality policy (2021) targets 20% women "
            "in the financial-sector workforce, a move from a pure *role culture* towards a more open *task culture*.")

# ---------------- Communication ----------------
with tabs[3]:
    st.markdown("### How SBP talks to the world")
    ch = [("Monetary Policy Statement", "English + Urdu after every MPC meeting"), ("Advance MPC calendar", "All meeting dates published a year ahead"),
          ("MPC minutes", "Published within 4 weeks"), ("Analyst briefing deck", "Online one day after each meeting (FY27)"),
          ("Governor's press conference", "Raised from 2 to 4 a year (FY27)"), ("Reports, speeches, podcast", "Annual reports, Monetary Policy Report, social media")]
    for row in range(2):
        cs = st.columns(3)
        for c, (t, d) in zip(cs, ch[row * 3:(row + 1) * 3]):
            c.markdown(f'<div class="card"><h4>{t}</h4><p>{d}</p></div>', unsafe_allow_html=True)
        st.write("")
    st.markdown("### 🔬 Data Science: text analysis of Monetary Policy Statements")
    if NLP_CSV.exists():
        n = pd.read_csv(NLP_CSV, parse_dates=["date"])
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Statements analysed", len(n)); m2.metric("Years covered", f"{n.date.dt.year.min()}–{n.date.dt.year.max()}")
        m3.metric("Avg. grade level", f"{n.fk_grade.mean():.1f}"); m4.metric("Avg. length", f"{int(n.words.mean())} words")
        metric = st.radio("Show", ["Readability (grade level)", "Tone vs policy rate", "Length (words)"], horizontal=True)
        if metric.startswith("Readability"):
            fig = px.scatter(n, x="date", y="fk_grade", color="governor", hover_data=["title", "words"], labels={"fk_grade": "Flesch–Kincaid grade", "date": ""})
            fig.add_hline(y=12, line_dash="dot", line_color=GOLD, annotation_text="Grade 12 (end of school)")
            chart(fig, 430)
        elif metric.startswith("Tone"):
            fig = go.Figure()
            fig.add_bar(x=n.date, y=n.tone, name="Net tone (hawkish +, dovish −)", marker_color=[("#C0563F" if v > 0 else "#3F6E9C") for v in n.tone])
            if "rate" in n and n.rate.notna().any():
                fig.add_scatter(x=n.date, y=n.rate, name="Policy rate (%)", yaxis="y2", mode="lines+markers", line=dict(color=GOLD, width=3))
                fig.update_layout(yaxis2=dict(overlaying="y", side="right", title="Policy rate %"))
            fig.update_layout(yaxis_title="Net tone")
            chart(fig, 430)
        else:
            fig = px.bar(n, x="date", y="words", color="governor", labels={"words": "Words", "date": ""}); chart(fig, 430)
        if NLP_TERMS.exists():
            terms = json.loads(NLP_TERMS.read_text())
            era = st.selectbox("Most frequent words by governor era", list(terms))
            tdf = pd.DataFrame(terms[era], columns=["word", "count"]).head(15)
            fig = px.bar(tdf[::-1], x="count", y="word", orientation="h", color_discrete_sequence=[GOLD]); chart(fig, 420)
        st.caption("Method: text extracted from SBP's published PDF statements; readability = Flesch–Kincaid grade; tone = (hawkish − dovish words) ÷ total tone words using a small central-bank word list.")
    else:
        st.warning("NLP data file not found (data/mps_nlp.csv).")

# ---------------- Leadership ----------------
with tabs[4]:
    st.markdown("### Governors of SBP (1948 – today)")
    g = pd.DataFrame(D["governors"], columns=["Governor", "Start", "End"])
    g["End"] = g["End"].replace("2026-11-11", str(date.today()))
    g["Start"] = pd.to_datetime(g.Start); g["End"] = pd.to_datetime(g.End)
    g["Years"] = ((g.End - g.Start).dt.days / 365.25).round(1)
    fig = px.timeline(g, x_start="Start", x_end="End", y="Governor", color="Years", color_continuous_scale=["#2C5E4A", GOLD2], hover_data=["Years"])
    fig.update_yaxes(autorange="reversed", title=""); chart(fig, 620)
    st.markdown("### Leadership style today")
    st.dataframe(pd.DataFrame([
        ["Transactional", "Rule-based decisions, clear 5–7% target, formal MPC votes", "Strong"],
        ["Transformational", "Vision 2028: high-tech, people-centric SBP", "Present"],
        ["Bureaucratic", "Authority from law and position; strict procedures", "Strong"],
        ["Participative", "10-member MPC with external experts; consultation for Vision 2028", "Moderate"],
    ], columns=["Theory", "Evidence", "Our assessment"]), hide_index=True, use_container_width=True)
    st.success("**Jameel Ahmad**: SBP career insider since 1991, former Deputy Governor and Saudi Central Bank adviser, appointed Governor in August 2022 for five years.")

# ---------------- Power & conflict ----------------
with tabs[5]:
    st.markdown("### Stakeholder power–interest grid")
    s = pd.DataFrame(D["stakeholders"], columns=["Stakeholder", "Interest", "Power", "Why"])
    fig = px.scatter(s, x="Interest", y="Power", text="Stakeholder", hover_data=["Why"], color_discrete_sequence=[GOLD])
    fig.update_traces(textposition="top center", marker=dict(size=15, line=dict(color="#FFF3C4", width=1)), textfont=dict(color="#F3EBD6"))
    for x0, y0, t in [(0, 5, "Keep satisfied"), (5, 5, "Manage closely"), (0, 0, "Monitor"), (5, 0, "Keep informed")]:
        fig.add_shape(type="rect", x0=x0, y0=y0, x1=x0 + 5, y1=y0 + 5, line=dict(color="rgba(212,175,55,.3)"), fillcolor="rgba(47,163,122,.07)" if y0 else "rgba(212,175,55,.05)", layer="below")
        fig.add_annotation(x=x0 + 0.25, y=y0 + 4.7, text=t, showarrow=False, xanchor="left", font=dict(color=MUTED, size=12))
    fig.update_xaxes(range=[0, 10], showticklabels=False, title="Interest in SBP decisions →"); fig.update_yaxes(range=[0, 10], showticklabels=False, title="Power over SBP →")
    chart(fig, 560)
    st.markdown("### Real cases, 2022–2026")
    modes = ["All"] + sorted({c["mode"] for c in D["cases"]})
    pick = st.radio("Filter by conflict-handling mode (Thomas–Kilmann)", modes, horizontal=True)
    for c in D["cases"]:
        if pick != "All" and c["mode"] != pick:
            continue
        st.markdown(f'<div class="case"><span class="yr">{c["year"]}</span> · <b>{c["title"]}</b>'
                    f'<span class="pill" style="background:{MODE_COLOR.get(c["mode"], MUTED)}">{c["mode"]}</span>'
                    f'<p style="margin:8px 0 4px 0">{c["text"]}</p><span class="tag">Power lens: {c["power"]}</span></div>', unsafe_allow_html=True)
    st.markdown("### SBP's power bases (French & Raven)")
    st.dataframe(pd.DataFrame([["Legitimate", "SBP Act gives legal authority"], ["Coercive", "Fines banks, cancels licences"],
                               ["Reward", "Incentive and refinance schemes"], ["Expert", "Specialist economists and supervisors"],
                               ["Referent", "Credibility and history since 1948"]], columns=["Power base", "How SBP holds it"]),
                 hide_index=True, use_container_width=True)

# ---------------- SWOT ----------------
with tabs[6]:
    colors = {"Strengths": "rgba(47,163,122,.10)", "Weaknesses": "rgba(192,86,63,.10)", "Opportunities": "rgba(63,110,156,.12)", "Threats": "rgba(212,175,55,.08)"}
    for pair in [("Strengths", "Weaknesses"), ("Opportunities", "Threats")]:
        cs = st.columns(2)
        for c, k in zip(cs, pair):
            items = "".join(f"<li>{x}</li>" for x in D["swot"][k])
            c.markdown(f'<div class="card" style="background:{colors[k]}"><h4>{k}</h4><ul style="margin:0;padding-left:18px">{items}</ul></div>', unsafe_allow_html=True)
        st.write("")
    st.markdown("### Recommendations")
    for i, r in enumerate(["Publish a plain-language English/Urdu summary with every policy statement.",
                           "Use cross-department project teams for digital and Islamic-banking goals.",
                           "Run and publish regular employee engagement surveys.",
                           "Set fixed timelines and succession plans for top posts.",
                           "Explain executive pay changes and link them to performance.",
                           "Adopt a formal stakeholder-engagement framework."], 1):
        st.markdown(f"**{i}.** {r}")

# ---------------- About ----------------
with tabs[7]:
    a, b = st.columns([1, 3])
    a.image("https://upload.wikimedia.org/wikipedia/en/thumb/6/68/Dawood_University_Of_Engineering_%26_Technology_LOGO.png/330px-Dawood_University_Of_Engineering_%26_Technology_LOGO.png", width=150)
    b.markdown("**Dawood University of Engineering & Technology, Karachi**  \nDepartment of Data Science · Organizational Behavior · Batch 25/F, Section C")
    st.markdown("#### Group 5")
    st.dataframe(pd.DataFrame([["Muhammad Abdul Rahman Khan", "25F-DS-106"], ["Muhammad Huzaifa Shamsi", "25F-DS-135"],
                           ["Basit Mirza", "25F-DS-140"], ["Muhammad Hashir", "25F-DS-152"]], columns=["Name", "Roll number"]), hide_index=True, use_container_width=True)
    st.caption("Sources: SBP website and Strategic Plan 2023–28, SBP Act, Dawn, Express Tribune, Business Recorder, Profit, ProPakistani. "
               "Secondary research only; internal-culture statements are the group's analysis.")

st.markdown('<div class="footer">SBP Insight · Group 5 · Department of Data Science, DUET Karachi · Secondary research, November 2026</div>', unsafe_allow_html=True)
