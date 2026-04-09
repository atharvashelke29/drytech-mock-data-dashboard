# Drytech Processes — Executive Dashboard

A real-time, interactive executive dashboard for **Drytech Processes (India) Pvt. Ltd.**, a B2B food ingredient manufacturer.

## 🚀 Live Demo
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 📊 Features
- **4 reactive KPI cards** — Revenue, Export Share, Gross Profit, Target Achievement
- **Revenue Trend** area chart — Domestic vs Export (monthly/quarterly/yearly)
- **Industry Segment** donut chart — 5 verticals
- **Product Revenue** bar chart — 6 SKUs, updates live on price change
- **Supply Chain** line chart — Production vs Inventory vs Capacity
- **4 Gauge charts** — Fulfillment, Delivery, Utilization, Target %
- **Smart Alerts** — auto-generated from your inputs
- **CSV Upload & Download** — bring your own data or export results

## 🛠 Tech Stack
- Python 3 + Streamlit
- Plotly
- Pandas / NumPy

## ▶️ Run Locally
```bash
pip install -r requirements.txt
streamlit run streamlit_dashboard.py
```

## 🔄 Connect Real Data
Search `# 🔄 REPLACE` in `streamlit_dashboard.py` to swap mock data with your production database, API, or CSV.

## 📁 Project Structure
```
drytech/
├── streamlit_dashboard.py   # Main app (Streamlit)
├── dashboard.html           # Static HTML dashboard (Chart.js)
├── requirements.txt         # Python dependencies
├── .streamlit/
│   └── config.toml          # Theme & server config
└── README.md
```
