"""Danske Bank brand palette and shared styling constants."""

# ── Core palette ──────────────────────────────────────────────────────────────
DB_NAVY      = "#003F63"   # Primary — Pantone 2955 C
DB_BLUE      = "#005E8E"   # Mid blue — interactive elements
DB_LIGHT     = "#E8F1F8"   # Tint of primary for panel backgrounds
DB_WHITE     = "#FFFFFF"
DB_OFFWHITE  = "#F4F7FA"   # Page background
DB_BORDER    = "#D0DCE8"   # Card borders and dividers
DB_TEXT      = "#1A2B3C"   # Primary text (near-black navy)
DB_MUTED     = "#6B7A8D"   # Secondary / caption text

# ── Semantic colours ──────────────────────────────────────────────────────────
DB_GREEN     = "#1B7340"   # Positive / on track
DB_AMBER     = "#B76E00"   # Caution / approaching target
DB_RED       = "#B5221B"   # At risk / below target
DB_GREEN_BG  = "#EAF5EE"
DB_AMBER_BG  = "#FDF3E3"
DB_RED_BG    = "#FAEAEA"

# ── Chart colour sequence ─────────────────────────────────────────────────────
MARKET_COLORS = {
    "Denmark": DB_NAVY,
    "Sweden":  DB_BLUE,
    "Finland": "#00839E",
    "Norway":  "#6BBBCA",
}

SEGMENT_COLORS = [DB_NAVY, DB_BLUE, "#6BBBCA"]

# ── Plotly layout base ────────────────────────────────────────────────────────
PLOTLY_BASE = dict(
    paper_bgcolor=DB_WHITE,
    plot_bgcolor=DB_WHITE,
    font=dict(family="Inter, Arial, sans-serif", color=DB_TEXT, size=13),
    margin=dict(l=16, r=16, t=36, b=16),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(size=11)),
    xaxis=dict(showgrid=False, linecolor=DB_BORDER, tickcolor=DB_BORDER),
    yaxis=dict(gridcolor=DB_BORDER, linecolor=DB_BORDER, tickcolor=DB_BORDER),
)

# ── Streamlit CSS injection ───────────────────────────────────────────────────
PAGE_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', Arial, sans-serif;
    background-color: {DB_OFFWHITE};
    color: {DB_TEXT};
}}

/* Top header bar */
.db-header {{
    background-color: {DB_NAVY};
    color: white;
    padding: 18px 32px;
    border-radius: 0;
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;
}}
.db-header h1 {{
    margin: 0;
    font-size: 1.4rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: white;
}}
.db-header .subtitle {{
    font-size: 0.85rem;
    opacity: 0.75;
    font-weight: 300;
    color: white;
}}

/* KPI cards */
.kpi-card {{
    background: {DB_WHITE};
    border: 1px solid {DB_BORDER};
    border-radius: 8px;
    padding: 18px 20px;
    height: 100%;
}}
.kpi-card .label {{
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: {DB_MUTED};
    margin-bottom: 6px;
}}
.kpi-card .value {{
    font-size: 2rem;
    font-weight: 700;
    color: {DB_TEXT};
    line-height: 1.1;
}}
.kpi-card .delta {{
    font-size: 0.8rem;
    margin-top: 4px;
    font-weight: 500;
}}
.kpi-card .target-line {{
    font-size: 0.72rem;
    color: {DB_MUTED};
    margin-top: 2px;
}}

/* Section headers */
.section-header {{
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: {DB_MUTED};
    padding: 12px 0 8px 0;
    border-bottom: 2px solid {DB_NAVY};
    margin-bottom: 16px;
}}

/* RAG badge */
.rag-on   {{ color: {DB_GREEN}; background: {DB_GREEN_BG}; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; }}
.rag-watch {{ color: {DB_AMBER}; background: {DB_AMBER_BG}; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; }}
.rag-risk  {{ color: {DB_RED};   background: {DB_RED_BG};   padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; }}

/* Action table */
.action-table {{ width: 100%; border-collapse: collapse; font-size: 0.82rem; }}
.action-table th {{
    background: {DB_NAVY};
    color: white;
    font-weight: 500;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 8px 12px;
    text-align: left;
}}
.action-table td {{ padding: 8px 12px; border-bottom: 1px solid {DB_BORDER}; vertical-align: top; }}
.action-table tr:hover td {{ background: {DB_LIGHT}; }}

/* Status pills */
.status-done      {{ color: {DB_GREEN}; background: {DB_GREEN_BG}; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; white-space: nowrap; }}
.status-progress  {{ color: {DB_AMBER}; background: {DB_AMBER_BG}; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; white-space: nowrap; }}
.status-notstart  {{ color: {DB_MUTED}; background: {DB_BORDER}; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 600; white-space: nowrap; }}

/* Progress bar */
.progress-wrap {{ background: {DB_BORDER}; border-radius: 100px; height: 6px; margin-top: 8px; overflow: hidden; }}
.progress-fill  {{ height: 6px; border-radius: 100px; background: {DB_NAVY}; }}
.progress-fill-warn {{ height: 6px; border-radius: 100px; background: {DB_AMBER}; }}
.progress-fill-risk {{ height: 6px; border-radius: 100px; background: {DB_RED}; }}

/* Card panels */
.panel {{
    background: {DB_WHITE};
    border: 1px solid {DB_BORDER};
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
}}

/* Hide Streamlit chrome */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 0 24px 40px 24px !important; max-width: 1280px; }}
div[data-testid="stDecoration"] {{ display: none; }}
</style>
"""


def rag_badge(status: str) -> str:
    mapping = {"On Track": "rag-on", "Watch": "rag-watch", "At Risk": "rag-risk"}
    return f'<span class="{mapping.get(status, "rag-watch")}">{status}</span>'


def status_pill(status: str) -> str:
    mapping = {
        "Completed":   "status-done",
        "In progress": "status-progress",
        "Not started": "status-notstart",
    }
    return f'<span class="{mapping.get(status, "status-notstart")}">{status}</span>'


def progress_bar(pct: float, color: str = "default") -> str:
    pct = min(max(pct, 0), 100)
    cls = "progress-fill"
    if color == "warn":
        cls = "progress-fill-warn"
    elif color == "risk":
        cls = "progress-fill-risk"
    return f'<div class="progress-wrap"><div class="{cls}" style="width:{pct:.1f}%"></div></div>'
