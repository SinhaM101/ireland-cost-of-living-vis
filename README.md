# 🇮🇪 Ireland Cost of Living Visualization

An interactive information visualization exploring how the cost of living in Ireland has changed since 2015, examining price trends across categories, regional income disparities, and the impact on essential goods.

**Course:** CS7DS4 Information Visualization  
**Author:** Monish  
**Date:** February 2026

---

## Primary Research Question

> **How has the cost of living changed in Ireland since ~2015, and who is most affected by these changes?**

### Sub-questions Addressed

1. **Which price categories have increased the most?**
2. **How do these increases differ over time?**
3. **Are regions with lower household income experiencing higher pressure?**
4. **Are price increases concentrated in essential goods?**

---

## Key Findings

| Finding | Insight |
|---------|---------|
| 🏠 **Housing & Utilities** | Highest increase (~45% since 2015), driven by 2022 energy crisis |
| 📚 **Education** | Consistently outpaces inflation (~40% increase) |
| 👕 **Clothing & Footwear** | Only category showing price *decrease* (fast fashion/imports) |
| ⚠️ **Essential Goods** | Average higher increases than non-essentials |
| 🗺️ **Northern & Western Region** | Lowest real income growth, highest cost pressure |
| 📈 **2022-2023** | Clear inflation spike visible across most categories |

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

### 1. Price Change by Category (Bar Chart)
- **Encoding:** Position (sorted), color (essential vs non-essential)
- **Purpose:** Identify which categories increased most

### 2. Monthly Price Trends (Multi-line Chart)
- **Encoding:** Position (time/value), color (category), hover highlight
- **Interaction:** Hover to isolate individual category trends
- **Purpose:** Show temporal evolution of prices

### 3. Year-over-Year Heatmap
- **Encoding:** Position (year/category), color saturation (% change)
- **Purpose:** Identify inflation patterns across time and categories

### 4. Regional Income Comparison (Grouped Bars)
- **Encoding:** Position, color (region)
- **Derived metric:** Real Income Change = Income Growth - CPI Growth
- **Purpose:** Analyze regional disparities in purchasing power

### 5. Essential vs Non-Essential (Violin Plot)
- **Encoding:** Density distribution + individual points
- **Purpose:** Compare price pressure on essential goods

### 6. Spending Distribution (Stacked Area)
- **Encoding:** Part-to-whole over time
- **Purpose:** Show shifts in household spending allocation

---

## Interactive Features

| Feature | Description |
|---------|-------------|
| **Year Range Slider** | Filter all charts to specific time period (2015-2024) |
| **Category Multi-select** | Focus on specific categories for comparison |
| **Hover Tooltips** | Detailed values on demand |
| **Highlight on Hover** | Focus+context in line charts |
| **Linked Views** | All charts respond to sidebar filters |

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
2. **Design Document:** `DESIGN_DOCUMENT.md` (2-page rationale)
3. **Video:** Screen recording of dashboard interactions
4. **Data:** All CSV files in `data/` folder

---

## Design Rationale

See `DESIGN_DOCUMENT.md` for detailed discussion of:
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
