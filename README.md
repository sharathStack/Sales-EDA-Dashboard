# Sales EDA Dashboard
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Matplotlib](https://img.shields.io/badge/Viz-Matplotlib%20%2B%20Seaborn-orange)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
> Reproduce a Power BI–style multi-KPI sales dashboard in pure Python: 4 KPI cards, monthly revenue trend, region breakdown, channel mix, category profit, margin heatmap, and year-over-year comparison — all in one chart.
Project Structure
```
DS8_SalesDashboard__config.py      ← Regions, categories, targets
DS8_SalesDashboard__data_gen.py    ← 2-year multi-dim synthetic sales data
DS8_SalesDashboard__kpi.py         ← All KPI aggregations
DS8_SalesDashboard__dashboard.py   ← 8-panel Power BI-style dashboard
DS8_SalesDashboard__main.py        ← Entry point
DS8_SalesDashboard__requirements.txt
```
Run
```bash
pip install -r DS8_SalesDashboard__requirements.txt
python DS8_SalesDashboard__main.py
```
## Dashboard Panels

### Panel	Content

KPI Cards (×4)	Total Revenue · Total Profit · Avg Margin · Units Sold

Monthly Trend	Revenue line chart with target line overlay

Region Bar	Revenue by North/South/East/West

Channel Pie	Online / Retail / Wholesale mix

Category Profit	Profit by Electronics / Apparel / Home / Beauty / Sports

Margin Heatmap	Avg margin % — Region × Category grid

YoY Comparison	2023 vs 2024 revenue per category (grouped bar)

