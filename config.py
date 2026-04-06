"""
config.py — Sales EDA Power-BI-style Dashboard
"""

# ── Data ───────────────────────────────────────────────────────────────────────
N_ROWS    = 5_000
SEED      = 7
START_DATE= "2023-01-01"
N_MONTHS  = 24

REGIONS    = ["North", "South", "East", "West"]
CATEGORIES = ["Electronics", "Apparel", "Home", "Beauty", "Sports"]
CHANNELS   = ["Online", "Retail", "Wholesale"]

# ── KPI targets ────────────────────────────────────────────────────────────────
TARGET_MARGIN_PCT = 38.0   # company target gross margin %
TARGET_REVENUE_M  = 50.0   # monthly revenue target ($M)

# ── Output ─────────────────────────────────────────────────────────────────────
CHART_OUTPUT = "sales_dashboard.png"
CHART_DPI    = 150
