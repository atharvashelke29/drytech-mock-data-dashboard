"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  DRYTECH PROCESSES (INDIA) — REAL-TIME EXECUTIVE DASHBOARD                  ║
║  Tech Stack : Python 3 + Streamlit + Plotly                                 ║
║  Run        : streamlit run streamlit_dashboard.py                          ║
║  Author     : Generated for Drytech Processes (India) Pvt. Ltd.             ║
╚══════════════════════════════════════════════════════════════════════════════╝

HOW TO RUN LOCALLY
──────────────────
1. Open Terminal / Anaconda Prompt
2. pip install streamlit plotly pandas numpy
3. cd /Users/atharvashelke/drytech
4. streamlit run streamlit_dashboard.py
5. Browser opens automatically at http://localhost:8501

TO SWAP IN REAL DATA
────────────────────
Search for "# 🔄 REPLACE" comments throughout the file.
Each one marks exactly where mock data should be swapped with
your production data source (CSV, database query, API call, etc.).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG  (must be first Streamlit call)
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Drytech Executive Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL STYLES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #f1f5f9; }

    /* Hide default Streamlit header/footer */
    #MainMenu { visibility: hidden; }
    footer    { visibility: hidden; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f766e 0%, #065f55 100%);
    }
    [data-testid="stSidebar"] * { color: #e2fffb !important; }
    [data-testid="stSidebar"] .stSlider > label,
    [data-testid="stSidebar"] .stSelectbox > label,
    [data-testid="stSidebar"] .stNumberInput > label { color: #ccf7f1 !important; font-size:0.78rem !important; }

    /* KPI card style */
    .kpi-box {
        background: white;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        border-left: 4px solid #0f766e;
        margin-bottom: 4px;
    }
    .kpi-label { font-size: 0.72rem; font-weight: 600; color: #64748b;
                 text-transform: uppercase; letter-spacing: 0.06em; }
    .kpi-value { font-size: 1.85rem; font-weight: 800; color: #1e293b; margin: 2px 0; }
    .kpi-delta { font-size: 0.75rem; font-weight: 600; }
    .kpi-up   { color: #16a34a; }
    .kpi-down { color: #dc2626; }

    /* Section header */
    .section-hdr {
        font-size: 0.88rem; font-weight: 700; color: #334155;
        border-bottom: 2px solid #e2e8f0; padding-bottom: 6px;
        margin-bottom: 14px; margin-top: 8px;
    }

    /* Alert box */
    .alert-warn {
        background:#fef3c7; border-left:4px solid #d97706;
        border-radius:8px; padding:10px 14px; font-size:0.8rem; color:#92400e;
    }
    .alert-good {
        background:#dcfce7; border-left:4px solid #16a34a;
        border-radius:8px; padding:10px 14px; font-size:0.8rem; color:#166534;
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# COLOUR PALETTE
# ══════════════════════════════════════════════════════════════════════════════
C_TEAL   = "#0f766e"
C_GREEN  = "#65a30d"
C_AMBER  = "#d97706"
C_BLUE   = "#3b82f6"
C_ROSE   = "#e11d48"
C_SLATE  = "#64748b"
PALETTE  = [C_TEAL, C_GREEN, C_AMBER, C_BLUE, "#8b5cf6", C_ROSE]

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — ALL INPUT WIDGETS
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🏭 Drytech Controls")
    st.markdown("---")

    # ── Data Source ──────────────────────────────────────────────────────────
    st.markdown("### 📂 Data Source")
    data_mode = st.radio(
        "Input Method",
        ["Use Mock Data", "Upload CSV", "Manual Entry"],
        index=0,
        help="Switch between demo data, your own CSV, or manual inputs"
    )

    uploaded_file = None
    if data_mode == "Upload CSV":
        uploaded_file = st.file_uploader(
            "Upload Revenue CSV",
            type=["csv"],
            help="Expected columns: month, domestic, export"
            # 🔄 REPLACE: point this at your actual data pipeline or S3 bucket
        )

    st.markdown("---")

    # ── Business Parameters ───────────────────────────────────────────────────
    st.markdown("### 🎯 Business Parameters")

    annual_target = st.slider(
        "Annual Revenue Target (₹ Cr)",
        min_value=100, max_value=500, value=260, step=5,
        help="Total revenue goal for FY 2024-25"
        # 🔄 REPLACE: pull from your ERP / finance system
    )

    export_target_pct = st.slider(
        "Export Revenue Target (%)",
        min_value=10, max_value=60, value=40, step=1
    )

    production_cap = st.slider(
        "Monthly Production Capacity (MT)",
        min_value=200, max_value=800, value=500, step=10,
        help="Factory nameplate capacity per month"
    )

    st.markdown("---")

    # ── Product Pricing (Manual Entry) ────────────────────────────────────────
    st.markdown("### 💰 Avg. Price per MT (₹ L)")
    price_gum       = st.number_input("Gum Arabic",          value=12.2, step=0.1, format="%.1f")
    price_fruit     = st.number_input("Fruit & Veg Powders", value=10.3, step=0.1, format="%.1f")
    price_creamer   = st.number_input("Non-Dairy Creamers",  value=10.2, step=0.1, format="%.1f")
    price_casein    = st.number_input("Caseinates",          value=10.6, step=0.1, format="%.1f")
    price_seasoning = st.number_input("Seasonings",          value= 9.1, step=0.1, format="%.1f")
    price_color     = st.number_input("Natural Colors",      value=11.0, step=0.1, format="%.1f")

    st.markdown("---")

    # ── Operational Parameters ────────────────────────────────────────────────
    st.markdown("### ⚙️ Operations")
    gross_margin_pct = st.slider("Gross Margin (%)", 10, 50, 28, 1)
    fulfillment_rate = st.slider("Order Fulfillment Rate (%)", 85.0, 100.0, 98.4, 0.1)
    otd_rate         = st.slider("On-Time Delivery (%)",       85.0, 100.0, 97.8, 0.1)
    active_clients   = st.number_input("Active B2B Clients", value=148, step=1)

    st.markdown("---")
    st.markdown("### 📅 Period Filter")
    fy_months = ["Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar"]
    month_range = st.select_slider(
        "Month Range",
        options=fy_months,
        value=("Apr", "Mar")
    )

# ══════════════════════════════════════════════════════════════════════════════
# DATA LAYER — Mock / Upload / Manual
# ══════════════════════════════════════════════════════════════════════════════

# 🔄 REPLACE this entire block with your real database query, API call, or
#    data warehouse connection. The only contract downstream code needs is a
#    DataFrame with columns: month, domestic, export, production, inventory.

MOCK_DOMESTIC = [8.2, 9.1, 8.7, 10.3, 11.2, 10.8, 12.5, 13.1, 14.2, 11.6, 12.9, 14.8]
MOCK_EXPORT   = [5.1, 5.8, 6.2,  6.9,  7.4,  7.1,  8.3,  9.0,  9.8,  8.2,  8.9, 10.4]
MOCK_PROD     = [280,310,295,340,368,352,405,428,465,381,412,480]
MOCK_INV      = [145,162,138,175,188,171,195,208,222,198,207,225]

@st.cache_data(show_spinner=False)
def load_mock_data():
    return pd.DataFrame({
        "month":      ["Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar"],
        "domestic":   MOCK_DOMESTIC,
        "export":     MOCK_EXPORT,
        "production": MOCK_PROD,
        "inventory":  MOCK_INV,
    })

def load_uploaded_data(f):
    try:
        df = pd.read_csv(f)
        # Normalise column names
        df.columns = [c.strip().lower() for c in df.columns]
        required = {"month","domestic","export"}
        if not required.issubset(set(df.columns)):
            st.error(f"CSV must have columns: {required}. Found: {set(df.columns)}")
            return load_mock_data()
        if "production" not in df.columns: df["production"] = 400
        if "inventory"  not in df.columns: df["inventory"]  = 180
        return df
    except Exception as e:
        st.error(f"Could not parse CSV: {e}")
        return load_mock_data()

# Select data source
if data_mode == "Upload CSV" and uploaded_file:
    raw_df = load_uploaded_data(uploaded_file)
elif data_mode == "Manual Entry":
    st.info("Manual entry mode: edit the sliders in the sidebar. Trend data uses mock baseline.", icon="ℹ️")
    raw_df = load_mock_data()
else:
    raw_df = load_mock_data()

# ── Apply month range filter ──────────────────────────────────────────────────
month_order = ["Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec","Jan","Feb","Mar"]
start_idx   = month_order.index(month_range[0])
end_idx     = month_order.index(month_range[1])
if end_idx >= start_idx:
    selected_months = month_order[start_idx : end_idx + 1]
else:
    selected_months = month_order[start_idx:] + month_order[:end_idx + 1]

df = raw_df[raw_df["month"].isin(selected_months)].copy()
df["month"] = pd.Categorical(df["month"], categories=selected_months, ordered=True)
df = df.sort_values("month")

# ══════════════════════════════════════════════════════════════════════════════
# REACTIVE CALCULATIONS  ← everything here re-runs on every widget change
# ══════════════════════════════════════════════════════════════════════════════

total_domestic = df["domestic"].sum()
total_export   = df["export"].sum()
total_revenue  = total_domestic + total_export
export_pct     = (total_export / total_revenue * 100) if total_revenue > 0 else 0
gross_profit   = total_revenue * (gross_margin_pct / 100)
target_gap     = annual_target - total_revenue          # negative = over target
target_achiev  = (total_revenue / annual_target * 100)  if annual_target > 0 else 0

avg_monthly_rev = total_revenue / len(df) if len(df) > 0 else 0
run_rate_annual = avg_monthly_rev * 12

# MoM growth (last month vs second-last)
if len(df) >= 2:
    last_total       = df.iloc[-1]["domestic"] + df.iloc[-1]["export"]
    prev_total       = df.iloc[-2]["domestic"] + df.iloc[-2]["export"]
    mom_growth       = ((last_total - prev_total) / prev_total * 100) if prev_total else 0
else:
    mom_growth = 0.0

# Product revenue estimate (volume × price)
PRODUCT_VOLUMES = {  # MT — 🔄 REPLACE with actual shipment volumes
    "Gum Arabic":         312,
    "Fruit & Veg Powders":287,
    "Non-Dairy Creamers": 241,
    "Caseinates":         178,
    "Seasonings":         156,
    "Natural Colors":      98,
}
prices = {
    "Gum Arabic":         price_gum,
    "Fruit & Veg Powders":price_fruit,
    "Non-Dairy Creamers": price_creamer,
    "Caseinates":         price_casein,
    "Seasonings":         price_seasoning,
    "Natural Colors":     price_color,
}
product_df = pd.DataFrame({
    "Product": list(PRODUCT_VOLUMES.keys()),
    "Volume (MT)": list(PRODUCT_VOLUMES.values()),
    "Price (₹L/MT)": [prices[p] for p in PRODUCT_VOLUMES],
})
product_df["Revenue (₹ Cr)"] = (
    product_df["Volume (MT)"] * product_df["Price (₹L/MT)"] / 100
).round(2)

# Industry segments (proportional)  — 🔄 REPLACE with actual segment data
SEGMENT_SHARES = {"Beverages":0.284,"Bakery":0.221,"Nutraceuticals":0.187,"Dairy":0.163,"Confectionery":0.145}
segment_df = pd.DataFrame({
    "Segment": list(SEGMENT_SHARES.keys()),
    "Revenue (₹ Cr)": [total_revenue * s for s in SEGMENT_SHARES.values()],
})

# Supply chain derived
avg_production    = df["production"].mean() if len(df) > 0 else 0
avg_inventory     = df["inventory"].mean()  if len(df) > 0 else 0
capacity_util_pct = (avg_production / production_cap * 100) if production_cap > 0 else 0

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
col_logo, col_title, col_ts = st.columns([0.08, 0.72, 0.20])
with col_logo:
    st.markdown(
        '<div style="background:linear-gradient(135deg,#0f766e,#0d9488);'
        'width:52px;height:52px;border-radius:12px;display:flex;align-items:center;'
        'justify-content:center;font-size:1.6rem;">🏭</div>',
        unsafe_allow_html=True
    )
with col_title:
    st.markdown(
        '<h2 style="margin:0;padding:0;color:#1e293b;font-size:1.35rem;font-weight:800;">'
        'Drytech Processes (India) Pvt. Ltd.</h2>'
        '<p style="margin:0;color:#64748b;font-size:0.8rem;">Executive Overview Dashboard · FY 2024–25 · Real-Time Reactive</p>',
        unsafe_allow_html=True
    )
with col_ts:
    st.markdown(
        f'<div style="text-align:right;padding-top:6px;">'
        f'<span style="background:#dcfce7;color:#166534;font-size:0.72rem;font-weight:600;'
        f'padding:4px 10px;border-radius:20px;">● Live</span><br>'
        f'<span style="color:#94a3b8;font-size:0.72rem;">'
        f'{datetime.now().strftime("%d %b %Y, %H:%M")}</span></div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# ROW 1 — KPI CARDS  (all reactive)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-hdr">Key Performance Indicators</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)

def kpi(col, label, value, delta_text, delta_up=True, accent=C_TEAL):
    arrow = "▲" if delta_up else "▼"
    cls   = "kpi-up" if delta_up else "kpi-down"
    col.markdown(
        f'<div class="kpi-box" style="border-left-color:{accent};">'
        f'  <div class="kpi-label">{label}</div>'
        f'  <div class="kpi-value">{value}</div>'
        f'  <div class="kpi-delta {cls}">{arrow} {delta_text}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

kpi(k1, "Total Revenue YTD",      f"₹{total_revenue:.1f} Cr",   f"14.2% vs FY24",          True,  C_TEAL)
kpi(k2, "Export Share",            f"{export_pct:.1f}%",          f"{export_pct - 36:.1f}pp vs target", export_pct >= export_target_pct, C_GREEN)
kpi(k3, "Gross Profit",            f"₹{gross_profit:.1f} Cr",    f"{gross_margin_pct}% margin",True,  C_AMBER)
kpi(k4, "Target Achievement",      f"{target_achiev:.1f}%",       f"₹{abs(target_gap):.1f} Cr {'ahead' if target_gap<=0 else 'short'}", target_gap<=0, C_BLUE)
kpi(k5, "Active B2B Clients",      f"{int(active_clients)}",      f"MoM Rev Growth {mom_growth:+.1f}%", mom_growth>=0, C_ROSE)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 2 — REVENUE TREND  +  INDUSTRY SEGMENT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-hdr">Revenue Analytics</div>', unsafe_allow_html=True)
chart_col1, chart_col2 = st.columns([3, 2])

# ── Revenue Trend (Area Chart) ────────────────────────────────────────────────
with chart_col1:
    st.markdown("**Revenue Trend — Domestic vs Export (₹ Cr)**")
    fig_rev = go.Figure()
    fig_rev.add_trace(go.Scatter(
        x=df["month"], y=df["domestic"],
        name="Domestic", fill="tozeroy",
        line=dict(color=C_TEAL, width=2.5),
        fillcolor="rgba(15,118,110,0.12)",
        mode="lines+markers",
        marker=dict(size=5, color=C_TEAL),
        hovertemplate="<b>%{x}</b><br>Domestic: ₹%{y:.1f} Cr<extra></extra>"
    ))
    fig_rev.add_trace(go.Scatter(
        x=df["month"], y=df["export"],
        name="Export", fill="tozeroy",
        line=dict(color=C_GREEN, width=2.5),
        fillcolor="rgba(101,163,13,0.12)",
        mode="lines+markers",
        marker=dict(size=5, color=C_GREEN),
        hovertemplate="<b>%{x}</b><br>Export: ₹%{y:.1f} Cr<extra></extra>"
    ))
    # Annotate last point
    if len(df) > 0:
        fig_rev.add_annotation(
            x=df["month"].iloc[-1],
            y=df["domestic"].iloc[-1] + df["export"].iloc[-1],
            text=f"₹{df['domestic'].iloc[-1]+df['export'].iloc[-1]:.1f}Cr",
            showarrow=False, font=dict(size=10, color=C_TEAL),
            yshift=12
        )
    fig_rev.update_layout(
        height=280, margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor="white", plot_bgcolor="white",
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                    font=dict(size=11)),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=10, color=C_SLATE)),
        yaxis=dict(gridcolor="#f1f5f9", zeroline=False, tickprefix="₹",
                   tickfont=dict(size=10, color=C_SLATE)),
        hovermode="x unified"
    )
    st.plotly_chart(fig_rev, use_container_width=True, config={"displayModeBar": False})

# ── Industry Segment Pie ──────────────────────────────────────────────────────
with chart_col2:
    st.markdown("**Revenue by Industry Segment**")
    fig_seg = go.Figure(go.Pie(
        labels=segment_df["Segment"],
        values=segment_df["Revenue (₹ Cr)"],
        hole=0.55,
        marker=dict(colors=PALETTE, line=dict(color="white", width=2)),
        textinfo="label+percent",
        textfont=dict(size=10),
        hovertemplate="<b>%{label}</b><br>₹%{value:.1f} Cr<br>%{percent}<extra></extra>"
    ))
    fig_seg.add_annotation(
        text=f"₹{total_revenue:.1f}<br><span style='font-size:10px'>Crore</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=14, color="#1e293b", family="Inter"),
        align="center"
    )
    fig_seg.update_layout(
        height=280, margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor="white",
        showlegend=True,
        legend=dict(orientation="v", font=dict(size=10), x=1.0, y=0.5)
    )
    st.plotly_chart(fig_seg, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════════════════════════════════════
# ROW 3 — PRODUCTS  +  SUPPLY CHAIN
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-hdr">Products & Operations</div>', unsafe_allow_html=True)
p_col, s_col = st.columns(2)

# ── Top Products Bar ──────────────────────────────────────────────────────────
with p_col:
    st.markdown("**Product Revenue (₹ Cr) — Reactive to Price Inputs**")
    fig_prod = go.Figure(go.Bar(
        x=product_df["Revenue (₹ Cr)"],
        y=product_df["Product"],
        orientation="h",
        marker=dict(
            color=product_df["Revenue (₹ Cr)"],
            colorscale=[[0,"#b2f5ea"],[0.5,"#0d9488"],[1,"#0f766e"]],
            showscale=False
        ),
        text=product_df["Revenue (₹ Cr)"].apply(lambda v: f"₹{v:.1f}Cr"),
        textposition="outside",
        textfont=dict(size=10, color=C_SLATE),
        hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:.1f} Cr<extra></extra>"
    ))
    fig_prod.update_layout(
        height=270, margin=dict(l=0,r=60,t=10,b=0),
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#f1f5f9", tickprefix="₹",
                   tickfont=dict(size=10)),
        yaxis=dict(showgrid=False, tickfont=dict(size=10, color="#334155")),
    )
    st.plotly_chart(fig_prod, use_container_width=True, config={"displayModeBar": False})

# ── Supply Chain Line ──────────────────────────────────────────────────────────
with s_col:
    st.markdown("**Production vs Inventory (MT)**")
    fig_sc = go.Figure()
    fig_sc.add_trace(go.Scatter(
        x=df["month"], y=df["production"],
        name="Production (MT)",
        line=dict(color=C_TEAL, width=2.5),
        fill="tozeroy", fillcolor="rgba(15,118,110,0.08)",
        mode="lines+markers", marker=dict(size=4),
        hovertemplate="%{x}: %{y} MT<extra>Production</extra>"
    ))
    fig_sc.add_trace(go.Scatter(
        x=df["month"], y=df["inventory"],
        name="Inventory (MT)",
        line=dict(color=C_AMBER, width=2, dash="dot"),
        mode="lines+markers", marker=dict(size=4, color=C_AMBER),
        hovertemplate="%{x}: %{y} MT<extra>Inventory</extra>"
    ))
    # Capacity reference line
    fig_sc.add_hline(
        y=production_cap,
        line_dash="dash", line_color=C_ROSE, line_width=1.2,
        annotation_text=f"Capacity ({production_cap} MT)",
        annotation_position="top right",
        annotation_font=dict(size=9, color=C_ROSE)
    )
    fig_sc.update_layout(
        height=270, margin=dict(l=0,r=0,t=10,b=0),
        paper_bgcolor="white", plot_bgcolor="white",
        legend=dict(orientation="h", y=-0.22, x=0.5, xanchor="center", font=dict(size=10)),
        xaxis=dict(showgrid=False, tickfont=dict(size=10, color=C_SLATE)),
        yaxis=dict(gridcolor="#f1f5f9", tickfont=dict(size=10, color=C_SLATE)),
        hovermode="x unified"
    )
    st.plotly_chart(fig_sc, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════════════════════════════════════
# ROW 4 — GAUGES  +  ALERTS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-hdr">Operational Health Gauges</div>', unsafe_allow_html=True)
g1, g2, g3, g4 = st.columns(4)

def gauge(col, title, value, min_val=0, max_val=100, suffix="%",
          threshold_warn=90, threshold_good=96, color=C_TEAL):
    bar_color = C_ROSE if value < threshold_warn else (C_AMBER if value < threshold_good else color)
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        number={"suffix": suffix, "font": {"size": 22, "color": "#1e293b"}},
        delta={"reference": threshold_good, "relative": False,
               "font": {"size": 11}, "valueformat": ".1f"},
        title={"text": title, "font": {"size": 11, "color": C_SLATE}},
        gauge={
            "axis": {"range": [min_val, max_val], "tickfont": {"size": 9}},
            "bar":  {"color": bar_color, "thickness": 0.28},
            "bgcolor": "white",
            "steps": [
                {"range": [min_val, threshold_warn], "color": "#fee2e2"},
                {"range": [threshold_warn, threshold_good], "color": "#fef3c7"},
                {"range": [threshold_good, max_val], "color": "#dcfce7"},
            ],
            "threshold": {
                "line": {"color": "#1e293b", "width": 2},
                "thickness": 0.75,
                "value": threshold_good
            }
        }
    ))
    fig.update_layout(
        height=190, margin=dict(l=10,r=10,t=30,b=10),
        paper_bgcolor="white"
    )
    col.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

gauge(g1, "Order Fulfillment",    fulfillment_rate,  min_val=80, threshold_warn=92, threshold_good=97)
gauge(g2, "On-Time Delivery",     otd_rate,          min_val=80, threshold_warn=91, threshold_good=96)
gauge(g3, "Capacity Utilization", capacity_util_pct, min_val=0,  threshold_warn=60, threshold_good=80)
gauge(g4, "Target Achievement",   target_achiev,     min_val=0,  max_val=120, threshold_warn=70, threshold_good=90)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 5 — SMART ALERTS  (reactive)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-hdr">Smart Alerts</div>', unsafe_allow_html=True)
al1, al2 = st.columns(2)

alerts_warn = []
alerts_good = []

if export_pct < export_target_pct:
    alerts_warn.append(f"Export share ({export_pct:.1f}%) is below target ({export_target_pct}%). "
                       f"Need ₹{(annual_target*export_target_pct/100 - total_export):.1f} Cr more in exports.")
if capacity_util_pct > 90:
    alerts_warn.append(f"Factory utilization at {capacity_util_pct:.1f}% — approaching capacity ceiling ({production_cap} MT). Consider capacity expansion.")
if target_gap > 0:
    months_left = 12 - len(df)
    monthly_needed = target_gap / months_left if months_left > 0 else target_gap
    alerts_warn.append(f"Revenue gap of ₹{target_gap:.1f} Cr to annual target. Need ₹{monthly_needed:.1f} Cr/month for remaining {months_left} months.")
if mom_growth < 0:
    alerts_warn.append(f"Month-on-month revenue declined {mom_growth:.1f}%. Review last-month performance.")

if target_achiev >= 100: alerts_good.append(f"Annual target achieved! ₹{abs(target_gap):.1f} Cr ahead of plan.")
if export_pct >= export_target_pct: alerts_good.append(f"Export target met at {export_pct:.1f}% (target {export_target_pct}%).")
if fulfillment_rate >= 98: alerts_good.append(f"Excellent order fulfillment at {fulfillment_rate:.1f}%.")
if mom_growth > 0: alerts_good.append(f"Positive MoM revenue growth of {mom_growth:+.1f}%.")

with al1:
    if alerts_warn:
        for a in alerts_warn:
            st.markdown(f'<div class="alert-warn">⚠️ {a}</div><br>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-good">✅ No warnings. All metrics within targets.</div>', unsafe_allow_html=True)

with al2:
    if alerts_good:
        for a in alerts_good:
            st.markdown(f'<div class="alert-good">✅ {a}</div><br>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-warn">No targets achieved yet this period.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 6 — DATA TABLE  +  DOWNLOAD
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-hdr">Monthly Revenue Detail</div>', unsafe_allow_html=True)

display_df = df.copy()
display_df["Total (₹ Cr)"] = (display_df["domestic"] + display_df["export"]).round(2)
display_df["Export Mix (%)"] = (display_df["export"] / display_df["Total (₹ Cr)"] * 100).round(1)
display_df.columns = ["Month","Domestic (₹ Cr)","Export (₹ Cr)","Production (MT)","Inventory (MT)","Total (₹ Cr)","Export Mix (%)"]

st.dataframe(
    display_df.set_index("Month"),
    use_container_width=True,
    height=240,
)

# Download button
csv_buf = io.StringIO()
display_df.to_csv(csv_buf, index=False)
st.download_button(
    label="⬇️ Download as CSV",
    data=csv_buf.getvalue(),
    file_name=f"drytech_dashboard_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv"
)

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#94a3b8;font-size:0.75rem;">'
    'Drytech Processes (India) Pvt. Ltd. · Executive Dashboard · '
    'Prototype with representative mock data · '
    'Built with Streamlit + Plotly</p>',
    unsafe_allow_html=True
)
