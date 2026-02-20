# Ireland Cost of Living Visualization: Design Document
**CS7DS4 Information Visualization | Author: Monish | February 2026**

## Overview
This dashboard explores how the cost of living has changed in Ireland since 2015, addressing: (1) Which price categories increased most? (2) How do increases differ over time? (3) Are lower-income regions experiencing higher pressure? (4) Are price increases concentrated in essential goods? **Data:** CSO Ireland HICP, Household Income, Personal Consumption (2015-2024).

## Visualization Design & Encodings

### Chart 1: Price Change by Category (Horizontal Bar Chart) — Q1
| Channel | Encoding | Rationale |
|---------|----------|-----------|
| Position (X) | % change | Most accurate channel for magnitude comparison |
| Position (Y) | Category (sorted) | Rapid identification of highest/lowest |
| Color | Essential (red) / Non-essential (blue) | Highlights essential goods |

**Alternatives:** Lollipop (less familiar), treemap (poor for comparison). **Pros:** Clear ranking. **Cons:** No temporal view.

### Chart 2: Monthly Price Trends (Multi-line with Hover Highlight) — Q2
| Channel | Encoding | Rationale |
|---------|----------|-----------|
| Position (X/Y) | Time / Index | Natural temporal mapping |
| Color | Category | Nominal distinction |
| Opacity | Hover highlight | Focus+context reduces clutter |

**Alternatives:** Small multiples (loses comparison), stacked area (obscures trends). **Pros:** Direct comparison. **Cons:** Cluttered >7 categories.

### Chart 3: Year-over-Year Heatmap
| Channel | Encoding | Rationale |
|---------|----------|-----------|
| Position (X/Y) | Year / Category | 2D layout |
| Color saturation | YoY % change | Diverging blue-red shows inflation vs deflation |

**Pros:** Compact overview, pattern recognition (2022 crisis = red band). **Cons:** Less precise than position.

### Chart 4: Regional Income Comparison (Grouped Bars) — Q3
| Channel | Encoding | Rationale |
|---------|----------|-----------|
| Position | Year/Region | Categorical grouping |
| Color | Region (3 NUTS 2) | Categorical distinction |
| Grouped bars | Income vs CPI growth | Direct metric comparison |

**Key Metric:** Real Income Change = Income Growth - CPI Growth. **Alternatives:** Choropleth (ineffective for 3 regions).

### Chart 5: Essential vs Non-Essential (Violin Plot) — Q4
| Channel | Encoding | Rationale |
|---------|----------|-----------|
| Position (X/Y) | Type / Price change % | Binary grouping, quantitative |
| Density shape | Distribution | Shows spread and concentration |
| Overlaid points | Individual categories | Prevents aggregation loss |

**Alternatives:** Box plot (less informative), histogram (loses identity). **Pros:** Shows distribution + individual values.

### Chart 6: Spending Distribution (Stacked Area)
| Channel | Encoding | Rationale |
|---------|----------|-----------|
| Position (X/Y) | Year / % of total | Part-to-whole over time |
| Color | Category | Categorical |

**Pros:** Shows compositional shifts. **Cons:** Baseline shift for middle layers.

## Interaction Design
| Interaction | Purpose |
|-------------|---------|
| Year range slider | Filter all charts to specific period |
| Category multi-select | Focus on specific categories |
| Hover tooltips | Details on demand |
| Highlight on hover | Focus+context in line charts |
| Linked views | Sidebar filters affect all charts |

**Rationale:** Follows Shneiderman's mantra: "Overview first, zoom and filter, details on demand."

## Key Insights
1. **Housing & Utilities:** Highest increase (~45%), driven by 2022 energy crisis
2. **Education:** Consistently outpaces inflation (~40%)
3. **Clothing & Footwear:** Only category with price *decrease* (fast fashion/imports)
4. **Essential goods** average higher increases than non-essentials
5. **Northern & Western region:** Lowest real income growth, highest cost pressure
6. **2022-2023:** Clear inflation spike visible across categories

## Technical Stack & Limitations
**Stack:** Python, Streamlit, Altair (Vega-Lite), Pandas. **Limitations:** Regional data limited to 3 NUTS 2 regions; no income quintile data; basket-weighted indices would improve analysis.

*CS7DS4 Information Visualization Assignment*
