# Ireland Cost of Living Visualization: Design Document
**CS7DS4 Information Visualization | Author: Monish | February 2026**

## Overview
This dashboard explores how the cost of living has changed in Ireland since 2015, addressing: (1) Which price categories increased most? (2) How do increases differ over time? (3) How have changes evolved across economic periods? (4) Which demographic groups face the greatest burden? **Data:** CSO Ireland HICP, Household Income, Personal Consumption (2015-2024).

## Design Process

### Iterative Refinement
The dashboard evolved through multiple iterations based on usability testing and design principles:

1. **Initial Prototype:** Basic bar and line charts exploring price data
2. **Research Question Refinement:** Shifted from regional income analysis to economic periods (Pre-COVID, COVID, Inflation Surge) for more actionable insights
3. **Demographic Focus:** Replaced essential vs non-essential goods with demographic burden analysis showing real-world impact on different household types
4. **Color Consistency:** Implemented unified color scheme—each category has one fixed color across all charts, making it easy to track categories visually
5. **Interactive Filtering:** Added color-coded checkboxes in sidebar matching chart colors; all charts filter to selected categories
6. **Reduced Clutter:** Removed redundant visualizations (e.g., duplicate line chart) following "less is more" principle

### Key Design Decisions
- **Horizontal bars** over vertical: Category labels are easier to read
- **Grouped bars by category** in "All Periods" view: Enables comparing how each category changed across periods
- **Dropdown for period selection:** Reduces cognitive load vs showing all periods simultaneously
- **Linked views:** All charts respond to sidebar selection, enabling coordinated exploration

## Visualization Design & Encodings

### Chart 1: Price Change by Category (Horizontal Bar Chart) — Q1
| Channel | Encoding | Rationale |
|---------|----------|-----------|
| Position (X) | % change | Most accurate channel for magnitude comparison |
| Position (Y) | Category (sorted) | Rapid identification of highest/lowest |
| Color | Consistent category color | Visual continuity across dashboard |

**Interaction:** Filters to show only selected categories. **Alternatives:** Lollipop (less familiar), treemap (poor for comparison). **Pros:** Clear ranking, interactive filtering. **Cons:** No temporal view.

### Chart 2: Monthly Price Trends (Multi-line with Hover Highlight) — Q2
| Channel | Encoding | Rationale |
|---------|----------|-----------|
| Position (X/Y) | Time / Index | Natural temporal mapping |
| Color | Consistent category color | Visual continuity |
| Opacity | Hover highlight | Focus+context reduces clutter |

**Alternatives:** Small multiples (loses comparison), stacked area (obscures trends). **Pros:** Direct comparison, hover isolation. **Cons:** Cluttered with many categories (mitigated by filtering).

### Chart 3: Economic Periods Analysis (Grouped Bar with Dropdown) — Q3
| Channel | Encoding | Rationale |
|---------|----------|-----------|
| Position (X) | Annual % change | Quantitative comparison |
| Position (Y) | Category | Categorical grouping |
| Color | Consistent category color | Visual continuity |
| yOffset | Period (in All Periods view) | Grouped comparison |

**Periods:** Pre-COVID (2015-19), COVID (2020-21), Inflation Surge (2022-23). **Interaction:** Dropdown selects period or "All Periods" view. **Pros:** Clear period comparison, reduced clutter via dropdown. **Cons:** Aggregates within-period variation.

### Chart 4: Demographic Burden Analysis (Bar + Stacked Bar) — Q4
| Channel | Encoding | Rationale |
|---------|----------|-----------|
| Position (X) | Weighted cost increase | Quantitative burden measure |
| Position (Y) | Demographic group | Categorical grouping |
| Color | Consistent category color | Visual continuity in spending profile |

**Groups:** Low/Middle/High income, Renters, Homeowners, Families. **Key Metric:** Weighted cost = sum(spending weight x price change). **Pros:** Shows real-world impact by group.

### Chart 5: Household Spending (Interactive Stacked Area)
| Channel | Encoding | Rationale |
|---------|----------|-----------|
| Position (X/Y) | Year / Spending (euros M) | Temporal spending trends |
| Color | Consistent category color | Visual continuity |
| Opacity | Legend selection | Focus+context via click |

**Interaction:** Connected to sidebar filters; legend click highlights. **Pros:** Shows compositional shifts interactively.

## Interaction Design
| Interaction | Purpose |
|-------------|---------|
| Year range slider | Filter all charts to specific period |
| Color-coded checkboxes | Select categories with visual color matching |
| Period dropdown | Focus on specific economic period |
| Hover tooltips | Details on demand |
| Linked views | All charts respond to sidebar selection |

**Rationale:** Follows Shneiderman's mantra: "Overview first, zoom and filter, details on demand." Color-coded checkboxes provide immediate visual feedback connecting sidebar to charts.

## Key Insights
1. **Housing & Utilities:** Highest increase (~45%), driven by 2022 energy crisis
2. **Inflation Surge (2022-23):** Worst period with highest annual price increases across categories
3. **Renters & Low Income:** Face greatest cost-of-living burden due to high housing cost share
4. **Clothing & Footwear:** Only category with price *decrease* (fast fashion/imports)
5. **Families with Children:** High burden due to education and food costs

## Technical Stack & Limitations
**Stack:** Python, Streamlit, Altair (Vega-Lite), Pandas. **Limitations:** Demographic spending weights are estimates based on CSO patterns; actual individual burden varies.

*CS7DS4 Information Visualization Assignment*
