# 🏎️ Formula 1 Analytics

An end-to-end Formula 1 data engineering and analytics project built on Databricks, covering race history, championship standings, teammate head-to-head battles, and 2026 season predictions.

---

## 📊 Live Dashboard

**[Formula1 Analytics Dashboard](https://adb-7405609850307083.3.azuredatabricks.net/dashboardsv3/01f18a0d63bf19b7aa0f837790ecc8b4/published?o=7405609850307083)**

> No login required — publicly accessible.

---

## 🗂️ Project Structure

```
F1-Analytics/
├── 00-common/                  # Shared environment config
│   └── 01.environment-config   # Sets catalog, silver, gold schema vars
├── 01-setup/                   # Initial catalog & schema setup
├── 02-bronze/                  # Raw data ingestion (Ergast API / CSV)
├── 03-silver/                  # Cleaned & standardised tables
├── 04-gold/                    # Aggregated analytical tables & views
├── 05-analytics/               # View-building notebooks
│   ├── 01. Build Driver Standings View
│   ├── 02. Build Constructor Standings View
│   ├── 03. Build 2026 Predictions View
│   └── 04. Build Teammate H2H View
├── 06-ml-predictions/          # 2026 season predictions
│   └── 01. Season 2026 Predictions
└── Formula1 Analytics Dashboard.lvdash.json
```

---

## 🏗️ Data Architecture

```
Bronze (raw)  →  Silver (cleaned)  →  Gold (views & predictions)
```

**Catalog:** `formula1`  
**Schemas:** `bronze`, `silver`, `gold`

### Key Gold Tables & Views

| Asset | Description |
|---|---|
| `gold.v_driver_standing` | Driver championship standings by season |
| `gold.v_constructor_standing` | Constructor championship standings by season |
| `gold.v_teammate_h2h` | Teammate head-to-head stats per season (wide) |
| `gold.v_teammate_h2h_long` | Teammate H2H unpivoted (one row per driver) |
| `gold.v_2026_wdc_predictions` | 2026 WDC predicted standings |
| `gold.v_2026_wcc_predictions` | 2026 WCC predicted standings |
| `gold.pred_2026_drivers` | Raw 2026 driver prediction scores |
| `gold.pred_2026_constructors` | Raw 2026 constructor prediction scores |

---

## 📈 Dashboard Pages

| Page | Description |
|---|---|
| **Driver Championship Standings** | Points, wins by driver per season |
| **Constructor Championship Standings** | Team points per season |
| **Dominant Drivers** | Most successful drivers across all seasons |
| **Dominant Teams** | Most successful constructors across all seasons |
| **Teammate Head-to-Head** | Points gap, finishing position advantage, wins & podiums comparison per team |
| **Season 2026 Predictions** | Predicted WDC & WCC standings using composite scoring model |

---

## 🤖 2026 Predictions Model

A weighted composite scoring model combining:
- **Driver historical performance** (last 5 seasons, exponential decay weighting)
- **Constructor performance** (team's historical scoring)
- **Rookie adjustment factor** (0.70× for drivers/teams new to F1)
- **Weights:** Driver score 55% · Constructor score 45%

New teams with no history (Cadillac F1 Team) receive the median constructor score as a baseline.

---

## 🛠️ Tech Stack

- **Platform:** Databricks (Unity Catalog, Lakeflow Jobs, AI/BI Dashboards)
- **Language:** Python (PySpark), SQL
- **Storage:** Delta Lake
- **Version Control:** Git
