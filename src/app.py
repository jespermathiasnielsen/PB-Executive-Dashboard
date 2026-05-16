"""
Private Banking & Investments — Executive Performance Dashboard
Danske Bank Forward'28 Strategy Tracker
"""

import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np

from data import (
    generate_aum_history, generate_kpi_history, generate_commercial_metrics,
    generate_client_segments, generate_actions,
    TARGETS_2028, ACTUALS_Q1_2026, QUARTERS
)
from theme import (
    PAGE_CSS, PLOTLY_BASE, SEGMENT_COLORS, MARKET_COLORS,
    DB_NAVY, DB_BLUE, DB_TEXT, DB_MUTED, DB_BORDER, DB_WHITE, DB_OFFWHITE,
    DB_GREEN, DB_AMBER, DB_RED, DB_LIGHT,
    rag_badge, status_pill, progress_bar
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PB&I Executive Dashboard — Danske Bank",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(PAGE_CSS, unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
aum_df   = generate_aum_history()
kpi_df   = generate_kpi_history()
comm_df  = generate_commercial_metrics()
seg_df   = generate_client_segments()
actions  = generate_actions()

latest_q    = QUARTERS[-1]
prev_q      = QUARTERS[-2]
aum_latest  = aum_df[aum_df["quarter"] == latest_q]
aum_prev    = aum_df[aum_df["quarter"] == prev_q]
kpi_latest  = kpi_df[kpi_df["quarter"] == latest_q].iloc[0]
kpi_prev    = kpi_df[kpi_df["quarter"] == prev_q].iloc[0]
comm_latest = comm_df[comm_df["quarter"] == latest_q]

total_aum_now  = aum_latest["aum"].sum()
total_aum_prev = aum_prev["aum"].sum()
total_nnm      = aum_latest["nnm"].sum()


# ── Helpers ───────────────────────────────────────────────────────────────────
def plotly_layout(**overrides):
    cfg = {**PLOTLY_BASE}
    cfg.update(overrides)
    return go.Layout(**cfg)


def delta_str(now, prev, fmt=".1f", invert=False):
    diff = now - prev
    up = diff >= 0
    if invert:
        up = not up
    arrow = "▲" if up else "▼"
    color = DB_GREEN if up else DB_RED
    return f'<span style="color:{color};font-size:0.78rem;font-weight:600">{arrow} {abs(diff):{fmt}}</span>'


def rag_from_progress(pct, direction="higher_better"):
    if direction == "higher_better":
        if pct >= 80:
            return "On Track"
        if pct >= 55:
            return "Watch"
        return "At Risk"
    else:
        if pct <= 60:
            return "On Track"
        if pct <= 80:
            return "Watch"
        return "At Risk"


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="db-header">
  <div>
    <div style="font-size:1.1rem;font-weight:700;letter-spacing:-0.01em;color:white;">
      &#9632;&nbsp; Danske Bank
    </div>
  </div>
  <div style="width:1px;height:36px;background:rgba(255,255,255,0.25);margin:0 8px;"></div>
  <div>
    <h1>Private Banking &amp; Investments — Executive Dashboard</h1>
    <div class="subtitle">Forward'28 Strategy Tracker &nbsp;·&nbsp; {latest_q} &nbsp;·&nbsp; Confidential</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_overview, tab_aum, tab_markets, tab_commercial, tab_actions = st.tabs([
    "Forward'28 Overview",
    "AUM & Net New Money",
    "Nordic Markets",
    "Commercial Momentum",
    "Action Log",
])


# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — FORWARD'28 OVERVIEW
# ════════════════════════════════════════════════════════════════════════════════
with tab_overview:
    st.markdown('<div class="section-header">Forward\'28 Group KPIs — Progress to Target</div>',
                unsafe_allow_html=True)

    # KPI card data
    kpis = [
        {
            "label":     "Return on Equity",
            "value":     kpi_latest["roe"],
            "prev":      kpi_prev["roe"],
            "target":    TARGETS_2028["roe"],
            "unit":      "%",
            "direction": "higher_better",
            "baseline":  ACTUALS_Q1_2026["roe"],
        },
        {
            "label":     "Cost / Income Ratio",
            "value":     kpi_latest["cost_income"],
            "prev":      kpi_prev["cost_income"],
            "target":    TARGETS_2028["cost_income"],
            "unit":      "%",
            "direction": "lower_better",
            "baseline":  ACTUALS_Q1_2026["cost_income"],
        },
        {
            "label":     "Total Income",
            "value":     kpi_latest["total_income"],
            "prev":      kpi_prev["total_income"],
            "target":    TARGETS_2028["total_income"],
            "unit":      " DKK bn",
            "direction": "higher_better",
            "baseline":  ACTUALS_Q1_2026["total_income"],
        },
        {
            "label":     "CET1 Capital Ratio",
            "value":     kpi_latest["cet1"],
            "prev":      kpi_prev["cet1"],
            "target":    TARGETS_2028["cet1"],
            "unit":      "%",
            "direction": "higher_better",
            "baseline":  ACTUALS_Q1_2026["cet1"],
        },
        {
            "label":     "Assets Under Management",
            "value":     total_aum_now,
            "prev":      total_aum_prev,
            "target":    TARGETS_2028["aum"],
            "unit":      " DKK bn",
            "direction": "higher_better",
            "baseline":  ACTUALS_Q1_2026["aum"],
        },
        {
            "label":     "Net New Money (Q)",
            "value":     round(total_nnm, 1),
            "prev":      aum_prev["nnm"].sum(),
            "target":    TARGETS_2028["nnm_annual"] / 4,
            "unit":      " DKK bn",
            "direction": "higher_better",
            "baseline":  ACTUALS_Q1_2026["nnm_q1"],
        },
    ]

    cols = st.columns(3)
    for i, k in enumerate(kpis):
        col = cols[i % 3]
        v, t, b = k["value"], k["target"], k["baseline"]
        d = k["direction"]

        if d == "higher_better":
            travel = t - b
            done   = v - b
            pct    = max(0, done / travel * 100) if travel else 0
        else:
            travel = b - t
            done   = b - v
            pct    = max(0, done / travel * 100) if travel else 0

        rag    = rag_from_progress(pct, d)
        p_cls  = "default" if rag == "On Track" else ("warn" if rag == "Watch" else "risk")
        delt   = delta_str(v, k["prev"], invert=(d == "lower_better"))
        fmt    = ",.0f" if abs(v) >= 100 else ".1f"

        col.markdown(f"""
        <div class="kpi-card">
          <div class="label">{k["label"]}</div>
          <div style="display:flex;align-items:baseline;gap:8px;">
            <div class="value">{v:{fmt}}{k["unit"]}</div>
            {delt}
          </div>
          <div class="target-line">
            Target 2028: <strong>{t:{fmt}}{k["unit"]}</strong> &nbsp;·&nbsp; {rag_badge(rag)}
          </div>
          {progress_bar(pct, p_cls)}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">KPI Trends — Quarterly</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        fig = go.Figure(layout=plotly_layout(
            title=dict(text="ROE vs Cost / Income Ratio (%)", font=dict(size=13, color=DB_TEXT)),
            yaxis=dict(gridcolor=DB_BORDER, linecolor=DB_BORDER, tickcolor=DB_BORDER),
            yaxis2=dict(overlaying="y", side="right", showgrid=False,
                        linecolor=DB_BORDER, tickcolor=DB_BORDER),
        ))
        fig.add_trace(go.Scatter(
            x=kpi_df["quarter"], y=kpi_df["roe"],
            name="ROE (%)", line=dict(color=DB_NAVY, width=2.5),
            mode="lines+markers", marker=dict(size=5),
        ))
        fig.add_trace(go.Scatter(
            x=kpi_df["quarter"], y=kpi_df["cost_income"],
            name="C/I Ratio (%)", line=dict(color=DB_AMBER, width=2.5, dash="dash"),
            mode="lines+markers", marker=dict(size=5), yaxis="y2",
        ))
        fig.add_hline(y=TARGETS_2028["roe"], line_dash="dot", line_color=DB_GREEN, line_width=1,
                      annotation_text="ROE target", annotation_position="right")
        fig.add_hline(y=TARGETS_2028["cost_income"], yref="y2", line_dash="dot",
                      line_color=DB_RED, line_width=1,
                      annotation_text="C/I target", annotation_position="right")
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        fig2 = go.Figure(layout=plotly_layout(
            title=dict(text="Total Income (DKK bn)", font=dict(size=13, color=DB_TEXT)),
        ))
        fig2.add_trace(go.Bar(
            x=kpi_df["quarter"], y=kpi_df["total_income"],
            marker_color=DB_NAVY, name="Income", opacity=0.85,
        ))
        fig2.add_hline(y=TARGETS_2028["total_income"], line_dash="dot", line_color=DB_GREEN,
                       line_width=1.5, annotation_text="2028 target",
                       annotation_position="top right")
        st.plotly_chart(fig2, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — AUM & NET NEW MONEY
# ════════════════════════════════════════════════════════════════════════════════
with tab_aum:
    st.markdown('<div class="section-header">Assets Under Management &amp; Net New Money</div>',
                unsafe_allow_html=True)

    aum_total = aum_df.groupby("quarter")[["aum", "nnm"]].sum().reset_index()

    top_left, top_right = st.columns([2, 1])

    with top_left:
        fig = go.Figure(layout=plotly_layout(
            title=dict(text="Total AUM by Market (DKK bn)", font=dict(size=13, color=DB_TEXT)),
            barmode="stack",
        ))
        for market, color in MARKET_COLORS.items():
            sub = aum_df[aum_df["market"] == market]
            fig.add_trace(go.Bar(
                x=sub["quarter"], y=sub["aum"],
                name=market, marker_color=color, opacity=0.9,
            ))
        fig.add_trace(go.Scatter(
            x=aum_total["quarter"], y=aum_total["aum"],
            mode="lines+markers", name="Total AUM",
            line=dict(color=DB_TEXT, width=1.5, dash="dot"),
            marker=dict(size=5, color=DB_TEXT), yaxis="y",
        ))
        st.plotly_chart(fig, use_container_width=True)

    with top_right:
        nnm_q = aum_total[["quarter", "nnm"]].copy()
        colors_nnm = [DB_GREEN if v >= 0 else DB_RED for v in nnm_q["nnm"]]
        fig_nnm = go.Figure(layout=plotly_layout(
            title=dict(text="Net New Money (DKK bn)", font=dict(size=13, color=DB_TEXT)),
        ))
        fig_nnm.add_trace(go.Bar(
            x=nnm_q["quarter"], y=nnm_q["nnm"],
            marker_color=colors_nnm, name="NNM",
        ))
        fig_nnm.add_hline(y=TARGETS_2028["nnm_annual"] / 4, line_dash="dot",
                           line_color=DB_NAVY, line_width=1.5,
                           annotation_text="Quarterly target", annotation_position="top right")
        st.plotly_chart(fig_nnm, use_container_width=True)

    st.markdown('<div class="section-header">Client Segment Distribution</div>',
                unsafe_allow_html=True)

    seg_left, seg_right = st.columns(2)

    with seg_left:
        fig_seg = go.Figure(go.Pie(
            labels=seg_df["segment"],
            values=seg_df["aum_share"],
            hole=0.52,
            marker=dict(colors=SEGMENT_COLORS, line=dict(color=DB_WHITE, width=2)),
            textinfo="label+percent",
            textfont=dict(size=11, color=DB_TEXT),
            hovertemplate="<b>%{label}</b><br>AUM share: %{percent}<extra></extra>",
        ))
        fig_seg.update_layout(
            **{k: v for k, v in PLOTLY_BASE.items() if k != "xaxis" and k != "yaxis"},
            title=dict(text="AUM Share by Client Segment", font=dict(size=13, color=DB_TEXT)),
            showlegend=False,
        )
        fig_seg.add_annotation(text=f"DKK<br><b>{total_aum_now:,.0f}bn</b>",
                               showarrow=False, font=dict(size=13, color=DB_TEXT))
        st.plotly_chart(fig_seg, use_container_width=True)

    with seg_right:
        fig_cli = go.Figure(go.Bar(
            x=seg_df["segment"],
            y=seg_df["clients"],
            marker_color=SEGMENT_COLORS,
            text=[f"{v:,}" for v in seg_df["clients"]],
            textposition="outside",
            textfont=dict(size=11),
        ))
        fig_cli.update_layout(
            **{k: v for k, v in PLOTLY_BASE.items()},
            title=dict(text="Client Count by Segment", font=dict(size=13, color=DB_TEXT)),
            showlegend=False,
            yaxis=dict(showgrid=True, gridcolor=DB_BORDER, linecolor=DB_BORDER),
        )
        st.plotly_chart(fig_cli, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — NORDIC MARKETS
# ════════════════════════════════════════════════════════════════════════════════
with tab_markets:
    st.markdown('<div class="section-header">Nordic Market Breakdown — {}</div>'.format(latest_q),
                unsafe_allow_html=True)

    market_cols = st.columns(4)
    for i, (market, color) in enumerate(MARKET_COLORS.items()):
        row  = aum_latest[aum_latest["market"] == market].iloc[0]
        prev = aum_prev[aum_prev["market"] == market].iloc[0]
        delta_aum = row["aum"] - prev["aum"]
        arrow = "▲" if delta_aum >= 0 else "▼"
        a_color = DB_GREEN if delta_aum >= 0 else DB_RED

        market_cols[i].markdown(f"""
        <div class="kpi-card" style="border-top: 3px solid {color};">
          <div class="label">{market}</div>
          <div class="value">{row['aum']:,.0f}</div>
          <div class="target-line">DKK bn AUM</div>
          <div class="delta" style="color:{a_color}">
            {arrow} {abs(delta_aum):.1f} vs {prev_q}
          </div>
          <div class="target-line" style="margin-top:6px">
            NNM: <strong>{row['nnm']:+.1f} DKK bn</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    fig_market = go.Figure(layout=plotly_layout(
        title=dict(text="AUM by Market — Quarterly Trend (DKK bn)", font=dict(size=13, color=DB_TEXT)),
    ))
    for market, color in MARKET_COLORS.items():
        sub = aum_df[aum_df["market"] == market]
        fig_market.add_trace(go.Scatter(
            x=sub["quarter"], y=sub["aum"],
            name=market, line=dict(color=color, width=2.5),
            mode="lines+markers", marker=dict(size=5),
        ))
    st.plotly_chart(fig_market, use_container_width=True)

    # NNM waterfall for latest quarter
    st.markdown('<div class="section-header">Net New Money Waterfall — {}</div>'.format(latest_q),
                unsafe_allow_html=True)

    markets_list = list(MARKET_COLORS.keys())
    nnm_values = [float(aum_latest[aum_latest["market"] == m]["nnm"].values[0])
                  for m in markets_list]
    total_nnm_q = sum(nnm_values)

    measure = ["relative"] * len(markets_list) + ["total"]
    x_labels = markets_list + ["Total NNM"]
    y_values = nnm_values + [total_nnm_q]
    bar_colors = [DB_GREEN if v >= 0 else DB_RED for v in nnm_values] + [DB_NAVY]

    fig_wf = go.Figure(go.Waterfall(
        measure=measure,
        x=x_labels,
        y=y_values,
        connector=dict(line=dict(color=DB_BORDER, width=1)),
        increasing=dict(marker=dict(color=DB_GREEN)),
        decreasing=dict(marker=dict(color=DB_RED)),
        totals=dict(marker=dict(color=DB_NAVY)),
        text=[f"{v:+.1f}" for v in y_values],
        textposition="outside",
    ))
    fig_wf.update_layout(
        **{k: v for k, v in PLOTLY_BASE.items()},
        title=dict(text=f"NNM Waterfall by Market — {latest_q} (DKK bn)",
                   font=dict(size=13, color=DB_TEXT)),
        showlegend=False,
    )
    st.plotly_chart(fig_wf, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — COMMERCIAL MOMENTUM
# ════════════════════════════════════════════════════════════════════════════════
with tab_commercial:
    st.markdown('<div class="section-header">Commercial Momentum — {} Snapshot</div>'.format(latest_q),
                unsafe_allow_html=True)

    # Radar chart across markets
    radar_metrics = ["advisory_pct", "insurance_pct", "lending_growth"]
    radar_labels  = ["Advisory Penetration", "Insurance Penetration", "Lending Growth"]

    fig_radar = go.Figure(layout=plotly_layout(
        title=dict(text="Commercial KPIs by Market — Radar View", font=dict(size=13, color=DB_TEXT)),
        polar=dict(
            bgcolor=DB_WHITE,
            radialaxis=dict(visible=True, linecolor=DB_BORDER, gridcolor=DB_BORDER,
                            tickfont=dict(size=9, color=DB_MUTED)),
            angularaxis=dict(linecolor=DB_BORDER, gridcolor=DB_BORDER,
                             tickfont=dict(size=10, color=DB_TEXT)),
        ),
    ))
    for market, color in MARKET_COLORS.items():
        row = comm_latest[comm_latest["market"] == market].iloc[0]
        vals = [row["advisory_pct"], row["insurance_pct"], row["lending_growth"] * 10]
        vals_closed = vals + [vals[0]]
        labels_closed = radar_labels + [radar_labels[0]]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_closed, theta=labels_closed,
            fill="toself", name=market,
            line=dict(color=color, width=2),
            fillcolor=color, opacity=0.15,
        ))
    st.plotly_chart(fig_radar, use_container_width=True)

    col_adv, col_ins = st.columns(2)

    with col_adv:
        fig_adv = go.Figure(layout=plotly_layout(
            title=dict(text="Advisory Penetration Rate (%) — Quarterly",
                       font=dict(size=13, color=DB_TEXT)),
        ))
        for market, color in MARKET_COLORS.items():
            sub = comm_df[comm_df["market"] == market]
            fig_adv.add_trace(go.Scatter(
                x=sub["quarter"], y=sub["advisory_pct"],
                name=market, line=dict(color=color, width=2.5),
                mode="lines+markers", marker=dict(size=5),
            ))
        fig_adv.add_hline(y=70, line_dash="dot", line_color=DB_GREEN, line_width=1,
                          annotation_text="Target 70%", annotation_position="right")
        st.plotly_chart(fig_adv, use_container_width=True)

    with col_ins:
        fig_ins = go.Figure(layout=plotly_layout(
            title=dict(text="Insurance Penetration Rate (%) — Quarterly",
                       font=dict(size=13, color=DB_TEXT)),
        ))
        for market, color in MARKET_COLORS.items():
            sub = comm_df[comm_df["market"] == market]
            fig_ins.add_trace(go.Scatter(
                x=sub["quarter"], y=sub["insurance_pct"],
                name=market, line=dict(color=color, width=2.5),
                mode="lines+markers", marker=dict(size=5),
            ))
        fig_ins.add_hline(y=40, line_dash="dot", line_color=DB_GREEN, line_width=1,
                          annotation_text="Target 40%", annotation_position="right")
        st.plotly_chart(fig_ins, use_container_width=True)

    st.markdown('<div class="section-header">Lending Growth by Market (%)</div>',
                unsafe_allow_html=True)
    fig_lend = go.Figure(layout=plotly_layout(
        title=dict(text="Lending Volume Growth YoY (%) — Quarterly",
                   font=dict(size=13, color=DB_TEXT)),
    ))
    for market, color in MARKET_COLORS.items():
        sub = comm_df[comm_df["market"] == market]
        fig_lend.add_trace(go.Bar(
            x=sub["quarter"], y=sub["lending_growth"],
            name=market, marker_color=color, opacity=0.85,
        ))
    fig_lend.add_hline(y=3.0, line_dash="dot", line_color=DB_GREEN, line_width=1.5,
                       annotation_text="Group target +3%", annotation_position="top right")
    fig_lend.update_layout(barmode="group")
    st.plotly_chart(fig_lend, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 5 — ACTION LOG
# ════════════════════════════════════════════════════════════════════════════════
with tab_actions:
    st.markdown('<div class="section-header">Leadership Forum — Open Actions</div>',
                unsafe_allow_html=True)

    # Summary pills
    total   = len(actions)
    done    = int((actions["status"] == "Completed").sum())
    in_prog = int((actions["status"] == "In progress").sum())
    not_st  = int((actions["status"] == "Not started").sum())

    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.markdown(f'<div class="kpi-card"><div class="label">Total Actions</div><div class="value">{total}</div></div>', unsafe_allow_html=True)
    sc2.markdown(f'<div class="kpi-card"><div class="label">Completed</div><div class="value" style="color:{DB_GREEN}">{done}</div></div>', unsafe_allow_html=True)
    sc3.markdown(f'<div class="kpi-card"><div class="label">In Progress</div><div class="value" style="color:{DB_AMBER}">{in_prog}</div></div>', unsafe_allow_html=True)
    sc4.markdown(f'<div class="kpi-card"><div class="label">Not Started</div><div class="value" style="color:{DB_MUTED}">{not_st}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Filters
    filter_col1, filter_col2, _ = st.columns([1, 1, 2])
    status_filter = filter_col1.multiselect(
        "Filter by status",
        ["Completed", "In progress", "Not started"],
        default=["In progress", "Not started"],
    )
    owner_filter = filter_col2.multiselect(
        "Filter by owner",
        sorted(actions["owner"].unique()),
    )

    filtered = actions.copy()
    if status_filter:
        filtered = filtered[filtered["status"].isin(status_filter)]
    if owner_filter:
        filtered = filtered[filtered["owner"].isin(owner_filter)]

    # Render table
    rows_html = ""
    for _, row in filtered.iterrows():
        due_dt = pd.Timestamp(row["due"])
        today  = pd.Timestamp("2026-05-16")
        overdue = due_dt < today and row["status"] != "Completed"
        due_str = f'<span style="color:{DB_RED};font-weight:600">{row["due"]} ⚠</span>' \
                  if overdue else row["due"]
        rows_html += f"""
        <tr>
          <td style="max-width:380px;font-weight:500">{row['action']}</td>
          <td>{row['owner']}</td>
          <td>{due_str}</td>
          <td>{status_pill(row['status'])}</td>
        </tr>"""

    st.markdown(f"""
    <table class="action-table">
      <thead>
        <tr>
          <th style="width:50%">Action</th>
          <th style="width:20%">Owner</th>
          <th style="width:15%">Due Date</th>
          <th style="width:15%">Status</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-size:0.72rem;color:{DB_MUTED};">'
        f'Private Banking &amp; Investments · Execution Office · Last updated: 2026-05-16 · Confidential'
        f'</div>',
        unsafe_allow_html=True,
    )
