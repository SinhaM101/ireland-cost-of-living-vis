# Ireland Cost of Living Visualization

An interactive information visualization exploring how the cost of living in Ireland has changed since 2015, examining price trends across categories, economic periods, and demographic impact.

**Interactive Dashboard:** [https://sinham101-ireland-cost-of-living-vis-app-hkhoa0.streamlit.app/](https://sinham101-ireland-cost-of-living-vis-app-hkhoa0.streamlit.app/)

**Course:** CS7DS4 Information Visualization  
**Author:** Monish  
**Date:** February 2026

---

## Primary Research Question

> **How has the cost of living changed in Ireland since ~2015, and who is most affected by these changes?**

### Sub-questions Addressed

1. **Which price categories have increased the most?**
2. **How do these increases differ over time?**
3. **How have price changes evolved across major economic periods?** (Pre-COVID, COVID, Inflation Surge)
4. **Which demographic groups face the greatest cost-of-living burden?** (Income levels, renters vs homeowners, household types)

---

## Key Findings

| Finding | Insight |
|---------|---------|
| 🏠 **Housing & Utilities** | Highest increase (~45% since 2015), driven by 2022 energy crisis |
| 📚 **Education** | Consistently outpaces inflation (~40% increase) |
| 👕 **Clothing & Footwear** | Only category showing price *decrease* (fast fashion/imports) |
| 📊 **Inflation Surge (2022-2023)** | Worst economic period with highest annual price increases |
| 🏘️ **Renters & Low Income** | Face greatest cost-of-living burden due to housing costs |
| 📈 **2022-2023** | Clear inflation spike visible across most categories |

---

## Design Process

### Iterative Development
The dashboard was developed through an iterative design process, with multiple refinements based on usability and clarity:

1. **Initial Design:** Started with basic bar charts and line charts to explore the data
2. **Added Economic Periods:** Replaced regional income analysis with economic period comparison (Pre-COVID, COVID, Inflation Surge) for more meaningful temporal insights
3. **Demographic Focus:** Replaced essential vs non-essential goods analysis with demographic burden analysis to show real-world impact
4. **Color Consistency:** Implemented a unified color scheme across all visualizations so each category maintains the same color throughout the dashboard
5. **Interactive Category Selection:** Added color-coded checkboxes in the sidebar that visually match chart colors, making it intuitive to track categories across views
6. **Removed Redundancy:** Eliminated duplicate visualizations (e.g., removed redundant line chart from spending section) to reduce clutter

### Design Decisions
- **Horizontal bar charts** for category comparisons (easier to read category labels)
- **Grouped bars by category** in the "All Periods" view (allows comparing how each category changed across periods)
- **Stacked area chart** for spending patterns (shows composition and total simultaneously)
- **Linked views** via sidebar filters (all charts respond to the same category selection)

---

## Installation & Running

### Prerequisites
- Python 3.8+
- pip

### Quick Start

```bash
# Clone the repository
git clone https://github.com/monish/ireland-cost-of-living-vis.git
cd ireland-cost-of-living-vis

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## Project Structure

```
ireland-cost-of-living-vis/
├── app.py                    # Main Streamlit dashboard (Python)
├── requirements.txt          # Python dependencies
├── DESIGN_DOCUMENT.md        # 2-page design rationale document
├── DESIGN_DOCUMENT.pdf       # PDF version of design document
├── README.md                 # This file
└── data/
    ├── Annual EU Index of Consumer Prices.csv
    ├── Monthly EU Consumer Prices by Consumer Price .csv
    ├── Annual consumption of persional income by item.csv
    └── Annual estimates of household income.csv
```

---

## Data Sources

All data sourced from the **Central Statistics Office (CSO) Ireland**:

| Dataset | Description | Time Range |
|---------|-------------|------------|
| Harmonised Index of Consumer Prices (HICP) | Price indices by COICOP category | 2012-2025 |
| Monthly EU Consumer Prices | Detailed monthly HICP data | 1996-2025 |
| Household Income Statistics | Regional income by NUTS 2 | 2000-2024 |
| Personal Consumption Expenditure | Spending by category (€ Million) | 1995-2024 |

---

## Visualizations

### 1. Price Change by Category (Horizontal Bar Chart)
- **Encoding:** Position (sorted by change), consistent category colors
- **Interaction:** Filters to show only selected categories from sidebar
- **Purpose:** Identify which categories increased most

### 2. Monthly Price Trends (Multi-line Chart)
- **Encoding:** Position (time/value), consistent category colors, hover highlight
- **Interaction:** Hover to isolate individual category trends; filters by selected categories
- **Purpose:** Show temporal evolution of prices

### 3. Economic Periods Analysis (Grouped Bar Chart)
- **Encoding:** Position (category/period), consistent category colors
- **Interaction:** Dropdown to select period (All Periods, Pre-COVID, COVID, Inflation Surge)
- **Periods:** Pre-COVID (2015-2019), COVID (2020-2021), Inflation Surge (2022-2023)
- **Purpose:** Compare price changes across major economic periods

### 4. Demographic Burden Analysis (Bar Chart + Stacked Bar)
- **Encoding:** Position (demographic group), consistent category colors
- **Groups:** Low/Middle/High income, Renters, Homeowners, Families with Children
- **Purpose:** Identify which demographic groups face greatest cost pressure

### 5. Household Spending Patterns (Interactive Stacked Area)
- **Encoding:** Area (spending amount), consistent category colors
- **Interaction:** Connected to sidebar filters, legend click to highlight
- **Purpose:** Show shifts in household spending allocation over time

---

## Interactive Features

| Feature | Description |
|---------|-------------|
| **Year Range Slider** | Filter all charts to specific time period (2015-2024) |
| **Color-coded Category Checkboxes** | Select categories with visual color indicators matching chart colors |
| **Period Dropdown** | Select economic period for focused analysis |
| **Hover Tooltips** | Detailed values on demand |
| **Highlight on Hover** | Focus+context in line charts |
| **Linked Views** | All charts respond to sidebar category selection |

---

## Consistent Color Scheme

Each category has a fixed color used across all visualizations:

| Category | Color |
|----------|-------|
| Food & Beverages | Red (#E5323B) |
| Housing & Utilities | Dark Blue (#2E4052) |
| Health | Yellow (#FFC857) |
| Alcohol & Tobacco | Purple (#A997DF) |
| Clothing & Footwear | Mint (#BDD9BF) |
| Transport | Teal (#5B8A72) |
| Education | Orange (#FF8C42) |
| Recreation & Culture | Medium Purple (#7B68EE) |
| Restaurants & Hotels | Violet (#6B5B95) |
| Communications | Rose (#D4A5A5) |
| Furnishings | Brown (#8B7355) |
| Miscellaneous | Green (#88B04B) |

---

## Technology Stack

- **Python 3.9+**
- **Streamlit** - Dashboard framework
- **Altair** - Declarative visualization (Vega-Lite based)
- **Pandas** - Data manipulation
- **NumPy** - Numerical operations

---

## Submission Contents

For CS7DS4 assignment submission:

1. **Code:** `app.py` (Python/Streamlit implementation)
2. **Design Document:** `DESIGN_DOCUMENT.md` and `DESIGN_DOCUMENT.pdf` (2-page rationale)
3. **Video:** Screen recording of dashboard interactions
4. **Data:** All CSV files in `data/` folder

---

## Design Rationale

See `DESIGN_DOCUMENT.md` for detailed discussion of:
- Design process and iterative refinements
- Encoding choices and alternatives considered
- Interaction design rationale
- Pros and cons of each visualization approach
- Insights supported by the visualizations

---

## License

This project is for educational purposes as part of CS7DS4 Information Visualization coursework.

---

## Acknowledgments

- Data provided by the Central Statistics Office (CSO) Ireland
- Built with Streamlit and Altair
