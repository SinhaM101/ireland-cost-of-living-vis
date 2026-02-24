"""
Ireland Cost of Living Analysis Dashboard
==========================================
An interactive Streamlit dashboard exploring how the cost of living has changed 
in Ireland since 2015, addressing four key research questions:
1. Which price categories have increased the most?
2. How do these increases differ over time?
3. How have price changes evolved across major economic periods?
4. Which demographic groups face the greatest cost-of-living burden?

Data Sources: CSO Ireland (HICP, Household Income, Personal Consumption)
"""

import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
# Set up the Streamlit page with title, icon, and wide layout
st.set_page_config(
    page_title="Ireland Cost of Living Analysis",
    page_icon="🇮🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Disable Altair's default 5000 row limit for large datasets
alt.data_transformers.disable_max_rows()

# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================
# Using @st.cache_data decorator to cache data and avoid reloading on each interaction

@st.cache_data
def load_annual_cpi():
    """
    Load Annual EU Index of Consumer Prices (HICP) data.
    Contains yearly price indices by COICOP category (2012-2025).
    """
    df = pd.read_csv("data/Annual EU Index of Consumer Prices.csv")
    df.columns = ['Statistic', 'Year', 'Category', 'Unit', 'Value']
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    return df

@st.cache_data
def load_monthly_cpi():
    """
    Load Monthly EU Consumer Prices data.
    Contains detailed monthly HICP data (1996-2025) for trend analysis.
    """
    df = pd.read_csv("data/Monthly EU Consumer Prices by Consumer Price .csv")
    df.columns = ['Statistic', 'Month', 'Category', 'Unit', 'Value']
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    # Parse month strings like "2015 January" into datetime objects
    df['Date'] = pd.to_datetime(df['Month'], format='%Y %B', errors='coerce')
    df['Year'] = df['Date'].dt.year
    df['MonthNum'] = df['Date'].dt.month
    return df

@st.cache_data
def load_consumption():
    """
    Load Annual Consumption of Personal Income data.
    Contains household spending by category in Euro Million (1995-2024).
    """
    df = pd.read_csv("data/Annual consumption of persional income by item.csv")
    df.columns = ['Statistic', 'Year', 'Item', 'Unit', 'Value']
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    return df

@st.cache_data
def load_household_income():
    """
    Load Annual Estimates of Household Income data.
    Contains regional income data by NUTS 2 regions (2000-2024).
    """
    df = pd.read_csv("data/Annual estimates of household income.csv")
    df.columns = ['Statistic', 'Year', 'Region', 'Unit', 'Value']
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    return df

# Load all datasets into memory (cached after first load)
annual_cpi = load_annual_cpi()
monthly_cpi = load_monthly_cpi()
consumption = load_consumption()
household_income = load_household_income()

# =============================================================================
# CATEGORY DEFINITIONS
# =============================================================================
# COICOP (Classification of Individual Consumption According to Purpose) categories
# These are the 12 main spending categories used in EU consumer price statistics

MAIN_CATEGORIES = [
    "All-items HICP (COICOP 00)",
    "Food and non-alcoholic beverages (COICOP 01)",
    "Alcoholic beverages, tobacco and narcotics (COICOP 02)",
    "Clothing and footwear (COICOP 03)",
    "Housing, water, electricity, gas and other fuels (COICOP 04)",
    "Furnishings, household equipment and routine household maintenance (COICOP 05)",
    "Health (COICOP 06)",
    "Transport (COICOP 07)",
    "Communications (COICOP 08)",
    "Recreation and culture (COICOP 09)",
    "Education (COICOP 10)",
    "Restaurants and hotels (COICOP 11)",
    "Miscellaneous goods and services (COICOP 12)"
]

# Essential categories: goods/services that households cannot easily reduce spending on
# Used to analyze whether basic necessities face higher price pressure
ESSENTIAL_CATEGORIES = [
    "Food and non-alcoholic beverages (COICOP 01)",
    "Housing, water, electricity, gas and other fuels (COICOP 04)",
    "Health (COICOP 06)",
    "Transport (COICOP 07)",
    "Education (COICOP 10)"
]

# Non-essential categories: discretionary spending that can be reduced if needed
NON_ESSENTIAL_CATEGORIES = [
    "Alcoholic beverages, tobacco and narcotics (COICOP 02)",
    "Clothing and footwear (COICOP 03)",
    "Furnishings, household equipment and routine household maintenance (COICOP 05)",
    "Communications (COICOP 08)",
    "Recreation and culture (COICOP 09)",
    "Restaurants and hotels (COICOP 11)",
    "Miscellaneous goods and services (COICOP 12)"
]

# Mapping from full COICOP names to shorter display names for charts
CATEGORY_SHORT_NAMES = {
    "All-items HICP (COICOP 00)": "All Items",
    "Food and non-alcoholic beverages (COICOP 01)": "Food & Beverages",
    "Alcoholic beverages, tobacco and narcotics (COICOP 02)": "Alcohol & Tobacco",
    "Clothing and footwear (COICOP 03)": "Clothing & Footwear",
    "Housing, water, electricity, gas and other fuels (COICOP 04)": "Housing & Utilities",
    "Furnishings, household equipment and routine household maintenance (COICOP 05)": "Furnishings",
    "Health (COICOP 06)": "Health",
    "Transport (COICOP 07)": "Transport",
    "Communications (COICOP 08)": "Communications",
    "Recreation and culture (COICOP 09)": "Recreation & Culture",
    "Education (COICOP 10)": "Education",
    "Restaurants and hotels (COICOP 11)": "Restaurants & Hotels",
    "Miscellaneous goods and services (COICOP 12)": "Miscellaneous"
}

# =============================================================================
# CONSISTENT COLOR SCHEME FOR CATEGORIES
# =============================================================================
# Define a fixed color for each category to ensure consistency across all visualizations
# Base palette: #BDD9BF, #929084, #FFC857, #A997DF, #E5323B, #2E4052
# Extended with variations to ensure each category has a unique color
CATEGORY_COLORS = {
    "All Items": "#929084",
    "Food & Beverages": "#E5323B",
    "Alcohol & Tobacco": "#A997DF",
    "Clothing & Footwear": "#BDD9BF",
    "Housing & Utilities": "#2E4052",
    "Furnishings": "#8B7355",
    "Health": "#FFC857",
    "Transport": "#5B8A72",
    "Communications": "#D4A5A5",
    "Recreation & Culture": "#7B68EE",
    "Education": "#FF8C42",
    "Restaurants & Hotels": "#6B5B95",
    "Miscellaneous": "#88B04B"
}

# Create Altair scale for consistent category colors
CATEGORY_COLOR_SCALE = alt.Scale(
    domain=list(CATEGORY_COLORS.keys()),
    range=list(CATEGORY_COLORS.values())
)

# =============================================================================
# DASHBOARD HEADER
# =============================================================================
st.title("Ireland Cost of Living Analysis (2015-2024)")
st.markdown("""
This interactive dashboard explores how the cost of living has changed in Ireland since 2015, 
examining which price categories have increased the most, how changes evolved across economic periods 
(pre-COVID, COVID, inflation surge, stabilization), and which demographic groups face the greatest burden.
""")

# =============================================================================
# SIDEBAR CONTROLS
# =============================================================================
# Interactive filters that affect all visualizations in the dashboard
with st.sidebar:
    st.header("Filters & Controls")
    
    # Year range slider: filters data across all charts
    year_range = st.slider(
        "Select Year Range",
        min_value=2015,
        max_value=2024,
        value=(2015, 2024),
        step=1
    )
    
    # Category multi-select: allows users to focus on specific categories
    st.subheader("Select Categories to Compare")
    
    # Create checkboxes with color indicators for each category
    selected_categories = []
    all_categories = [c for c in CATEGORY_SHORT_NAMES.values() if c != "All Items"]
    
    # Default selections - all categories selected by default
    default_selected = all_categories
    
    for cat in all_categories:
        color = CATEGORY_COLORS.get(cat, "#666666")
        # Create a colored box indicator next to each checkbox
        col1, col2 = st.columns([0.15, 0.85])
        with col1:
            st.markdown(f'<div style="background-color:{color}; width:20px; height:20px; border-radius:3px; margin-top:5px;"></div>', unsafe_allow_html=True)
        with col2:
            if st.checkbox(cat, value=(cat in default_selected), key=f"cat_{cat}"):
                selected_categories.append(cat)
    
    # Convert short names back to full COICOP names for data filtering
    reverse_short_names = {v: k for k, v in CATEGORY_SHORT_NAMES.items()}
    selected_full_categories = [reverse_short_names[c] for c in selected_categories]

# =============================================================================
# SECTION 1: PRICE CHANGE BY CATEGORY (Bar Chart)
# =============================================================================
# Answers Q1: Which price categories have increased the most?
# Encoding: Horizontal bar chart with position (sorted) and color (essential vs non-essential)
st.header("1. Which Price Categories Have Increased the Most?")

# Filter HICP data for main categories within selected year range
hicp_index = annual_cpi[
    (annual_cpi['Statistic'] == 'Harmonised Index of Consumer Prices') &
    (annual_cpi['Category'].isin(MAIN_CATEGORIES)) &
    (annual_cpi['Year'] >= year_range[0]) &
    (annual_cpi['Year'] <= year_range[1])
].copy()

# Add short category names for display
hicp_index['ShortCategory'] = hicp_index['Category'].map(CATEGORY_SHORT_NAMES)

if not hicp_index.empty:
    # Get index values for base year and latest year to calculate percentage change
    base_year_data = hicp_index[hicp_index['Year'] == year_range[0]].set_index('Category')['Value']
    latest_year_data = hicp_index[hicp_index['Year'] == year_range[1]].set_index('Category')['Value']
    
    # Calculate percentage change for each category
    change_data = []
    for cat in MAIN_CATEGORIES:
        if cat in base_year_data.index and cat in latest_year_data.index:
            base_val = base_year_data[cat]
            latest_val = latest_year_data[cat]
            if pd.notna(base_val) and pd.notna(latest_val) and base_val > 0:
                # Percentage change formula: ((new - old) / old) * 100
                pct_change = ((latest_val - base_val) / base_val) * 100
                change_data.append({
                    'Category': CATEGORY_SHORT_NAMES[cat],
                    'FullCategory': cat,
                    'Change': pct_change,
                    'BaseValue': base_val,
                    'LatestValue': latest_val,
                    'IsEssential': cat in ESSENTIAL_CATEGORIES  # Flag for color encoding
                })
    
    change_df = pd.DataFrame(change_data)
    change_df = change_df.sort_values('Change', ascending=False)  # Sort by highest change
    
    # Filter to only show selected categories from sidebar
    if selected_categories:
        filtered_change_df = change_df[change_df['Category'].isin(selected_categories)]
    else:
        filtered_change_df = change_df
    
    # Create two-column layout: chart on left, metrics on right
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Horizontal bar chart with consistent category colors
        bar_chart = alt.Chart(filtered_change_df).mark_bar().encode(
            x=alt.X('Change:Q', 
                    title=f'Price Change (%) from {year_range[0]} to {year_range[1]}',
                    axis=alt.Axis(format='.1f')),
            y=alt.Y('Category:N', 
                    sort='-x',  # Sort by x-value (highest change at top)
                    title=''),
            color=alt.Color('Category:N',
                           scale=CATEGORY_COLOR_SCALE,
                           legend=None),
            tooltip=[
                alt.Tooltip('Category:N', title='Category'),
                alt.Tooltip('Change:Q', title='Change (%)', format='.1f'),
                alt.Tooltip('BaseValue:Q', title=f'{year_range[0]} Index', format='.1f'),
                alt.Tooltip('LatestValue:Q', title=f'{year_range[1]} Index', format='.1f')
            ]
        ).properties(
            width=500,
            height=max(200, len(filtered_change_df) * 35),
            title=f'Price Index Change by Category ({year_range[0]}-{year_range[1]})'
        )
        
        st.altair_chart(bar_chart, use_container_width=True)
    
    with col2:
        # Display top 3 categories as metric cards
        st.subheader("Key Findings")
        top_3 = change_df.head(3)
        for _, row in top_3.iterrows():
            st.metric(
                label=row['Category'],
                value=f"+{row['Change']:.1f}%",
                delta=f"Index: {row['LatestValue']:.1f}"
            )

st.divider()

# =============================================================================
# SECTION 2: PRICE TRENDS OVER TIME (Line Chart + Heatmap)
# =============================================================================
# Answers Q2: How do these increases differ over time?
# Encoding: Multi-line chart with hover highlight + Year-over-Year heatmap
st.header("2. How Do Price Increases Differ Over Time?")

# Filter monthly HICP data for selected categories and year range
monthly_hicp = monthly_cpi[
    (monthly_cpi['Statistic'] == 'EU HICP') &
    (monthly_cpi['Category'].isin(MAIN_CATEGORIES)) &
    (monthly_cpi['Year'] >= year_range[0]) &
    (monthly_cpi['Year'] <= year_range[1])
].copy()

monthly_hicp['ShortCategory'] = monthly_hicp['Category'].map(CATEGORY_SHORT_NAMES)

if not monthly_hicp.empty and selected_full_categories:
    # Filter to only user-selected categories
    filtered_monthly = monthly_hicp[monthly_hicp['Category'].isin(selected_full_categories)]
    
    # Create hover highlight interaction - highlights one line at a time
    # This implements focus+context technique to reduce visual clutter
    highlight = alt.selection_point(on='pointerover', fields=['ShortCategory'], nearest=True)
    
    # Base encoding shared by lines and points - using consistent color scheme
    base = alt.Chart(filtered_monthly).encode(
        x=alt.X('Date:T', title='Date', axis=alt.Axis(format='%Y')),
        y=alt.Y('Value:Q', title='Price Index (Base 2015=100)'),
        color=alt.Color('ShortCategory:N', 
                       title='Category',
                       scale=CATEGORY_COLOR_SCALE,
                       legend=alt.Legend(orient='bottom', columns=3))
    )
    
    # Line marks with opacity tied to hover state
    lines = base.mark_line(strokeWidth=2).encode(
        opacity=alt.condition(highlight, alt.value(1), alt.value(0.3)),
        tooltip=[
            alt.Tooltip('ShortCategory:N', title='Category'),
            alt.Tooltip('Date:T', title='Date', format='%B %Y'),
            alt.Tooltip('Value:Q', title='Index Value', format='.1f')
        ]
    ).add_params(highlight)
    
    # Line chart without dots - increased height for better readability
    line_chart = lines.properties(
        width=800,
        height=600,
        title='Monthly Price Index Trends by Category'
    ).interactive()  # Enable pan/zoom
    
    st.altair_chart(line_chart, use_container_width=True)

st.divider()

# =============================================================================
# SECTION 3: ECONOMIC PERIODS ANALYSIS
# =============================================================================
# Answers Q3: How have price changes evolved across major economic periods?
# Economic periods: Pre-COVID (2015-2019), COVID (2020-2021), Inflation Surge (2022-2023), Stabilization (2024)
st.header("3. Price Changes Across Economic Periods")

# Define economic periods (removed Stabilization 2024 - no data available)
ECONOMIC_PERIODS = {
    'Pre-COVID (2015-2019)': (2015, 2019),
    'COVID (2020-2021)': (2020, 2021),
    'Inflation Surge (2022-2023)': (2022, 2023)
}

st.markdown("""
Analyzing how price changes evolved across three distinct economic periods:
- **Pre-COVID (2015-2019):** Stable growth period
- **COVID (2020-2021):** Pandemic disruptions, supply chain issues
- **Inflation Surge (2022-2023):** Energy crisis, post-pandemic inflation
""")

# Calculate average annual price change for each period and category
period_data = []
for period_name, (start_year, end_year) in ECONOMIC_PERIODS.items():
    period_cpi = annual_cpi[
        (annual_cpi['Statistic'] == 'Harmonised Index of Consumer Prices') &
        (annual_cpi['Category'].isin(MAIN_CATEGORIES)) &
        (annual_cpi['Year'] >= start_year) &
        (annual_cpi['Year'] <= end_year)
    ].copy()
    
    if not period_cpi.empty:
        for cat in MAIN_CATEGORIES:
            if cat == "All-items HICP (COICOP 00)":
                continue
            cat_data = period_cpi[period_cpi['Category'] == cat]
            if len(cat_data) >= 1:
                start_val = cat_data[cat_data['Year'] == start_year]['Value'].values
                end_val = cat_data[cat_data['Year'] == end_year]['Value'].values
                if len(start_val) > 0 and len(end_val) > 0 and start_val[0] > 0:
                    # Calculate total change over period
                    total_change = ((end_val[0] - start_val[0]) / start_val[0]) * 100
                    # Annualized change
                    years = end_year - start_year + 1
                    annual_change = total_change / years if years > 0 else total_change
                    period_data.append({
                        'Period': period_name,
                        'Category': CATEGORY_SHORT_NAMES[cat],
                        'TotalChange': total_change,
                        'AnnualChange': annual_change,
                        'IsEssential': cat in ESSENTIAL_CATEGORIES
                    })

if period_data:
    period_df = pd.DataFrame(period_data)
    
    # Period selector - dropdown to filter by economic period
    col1, col2 = st.columns([3, 1])
    
    with col2:
        # Dropdown to select economic period
        period_options = ['All Periods', 'Pre-COVID (2015-2019)', 'COVID (2020-2021)', 
                         'Inflation Surge (2022-2023)']
        selected_period = st.selectbox(
            "Select Economic Period",
            options=period_options,
            index=0
        )
    
    with col1:
        # Filter to selected categories if any
        if selected_categories:
            filtered_period_df = period_df[period_df['Category'].isin(selected_categories)]
        else:
            filtered_period_df = period_df
        
        # Filter by selected period if not "All Periods"
        if selected_period != 'All Periods':
            filtered_period_df = filtered_period_df[filtered_period_df['Period'] == selected_period]
        
        if selected_period == 'All Periods':
            # Show horizontal grouped bar chart - categories as rows, periods as grouped bars
            # Using consistent category colors
            period_chart = alt.Chart(filtered_period_df).mark_bar().encode(
                x=alt.X('AnnualChange:Q', title='Avg Annual Price Change (%)'),
                y=alt.Y('Category:N', title=''),
                color=alt.Color('Category:N', 
                               title='Category',
                               scale=CATEGORY_COLOR_SCALE,
                               legend=alt.Legend(orient='bottom', columns=4)),
                yOffset=alt.YOffset('Period:N', sort=['Pre-COVID (2015-2019)', 'COVID (2020-2021)', 'Inflation Surge (2022-2023)']),
                tooltip=[
                    alt.Tooltip('Category:N', title='Category'),
                    alt.Tooltip('Period:N', title='Period'),
                    alt.Tooltip('AnnualChange:Q', title='Avg Annual Change (%)', format='.1f'),
                    alt.Tooltip('TotalChange:Q', title='Total Change (%)', format='.1f')
                ]
            ).properties(
                width=700,
                height=450,
                title='Average Annual Price Change by Category Across Economic Periods'
            )
        else:
            # Show horizontal bar chart for single period comparison
            # Using consistent category colors
            filtered_period_df = filtered_period_df.sort_values('AnnualChange', ascending=False)
            period_chart = alt.Chart(filtered_period_df).mark_bar().encode(
                x=alt.X('AnnualChange:Q', title='Avg Annual Price Change (%)'),
                y=alt.Y('Category:N', 
                        title='',
                        sort='-x'),
                color=alt.Color('Category:N',
                               scale=CATEGORY_COLOR_SCALE,
                               legend=None),
                tooltip=[
                    alt.Tooltip('Category:N', title='Category'),
                    alt.Tooltip('AnnualChange:Q', title='Avg Annual Change (%)', format='.1f'),
                    alt.Tooltip('TotalChange:Q', title='Total Change (%)', format='.1f')
                ]
            ).properties(
                width=700,
                height=400,
                title=f'Price Changes During {selected_period}'
            )
        
        st.altair_chart(period_chart, use_container_width=True)

st.divider()

# =============================================================================
# SECTION 4: DEMOGRAPHIC BURDEN ANALYSIS
# =============================================================================
# Answers Q4: Which demographic groups face the greatest cost-of-living burden?
# Analysis based on spending patterns and price changes
st.header("4. Cost-of-Living Burden by Demographic Group")

# Define demographic groups with their typical spending weights
# Based on CSO Household Budget Survey patterns
DEMOGRAPHIC_PROFILES = {
    'Low Income Household': {
        'Food & Beverages': 0.20,
        'Housing & Utilities': 0.35,
        'Transport': 0.10,
        'Health': 0.05,
        'Education': 0.03,
        'Clothing & Footwear': 0.05,
        'Communications': 0.04,
        'Recreation & Culture': 0.05,
        'Restaurants & Hotels': 0.03,
        'Alcohol & Tobacco': 0.04,
        'Furnishings': 0.03,
        'Miscellaneous': 0.03
    },
    'Middle Income Household': {
        'Food & Beverages': 0.15,
        'Housing & Utilities': 0.25,
        'Transport': 0.15,
        'Health': 0.05,
        'Education': 0.05,
        'Clothing & Footwear': 0.06,
        'Communications': 0.03,
        'Recreation & Culture': 0.10,
        'Restaurants & Hotels': 0.08,
        'Alcohol & Tobacco': 0.03,
        'Furnishings': 0.03,
        'Miscellaneous': 0.02
    },
    'High Income Household': {
        'Food & Beverages': 0.10,
        'Housing & Utilities': 0.15,
        'Transport': 0.12,
        'Health': 0.06,
        'Education': 0.08,
        'Clothing & Footwear': 0.08,
        'Communications': 0.02,
        'Recreation & Culture': 0.15,
        'Restaurants & Hotels': 0.12,
        'Alcohol & Tobacco': 0.02,
        'Furnishings': 0.05,
        'Miscellaneous': 0.05
    },
    'Renters': {
        'Food & Beverages': 0.15,
        'Housing & Utilities': 0.40,
        'Transport': 0.10,
        'Health': 0.04,
        'Education': 0.04,
        'Clothing & Footwear': 0.05,
        'Communications': 0.03,
        'Recreation & Culture': 0.07,
        'Restaurants & Hotels': 0.05,
        'Alcohol & Tobacco': 0.03,
        'Furnishings': 0.02,
        'Miscellaneous': 0.02
    },
    'Homeowners': {
        'Food & Beverages': 0.14,
        'Housing & Utilities': 0.18,
        'Transport': 0.15,
        'Health': 0.06,
        'Education': 0.06,
        'Clothing & Footwear': 0.06,
        'Communications': 0.03,
        'Recreation & Culture': 0.12,
        'Restaurants & Hotels': 0.10,
        'Alcohol & Tobacco': 0.03,
        'Furnishings': 0.04,
        'Miscellaneous': 0.03
    },
    'Family with Children': {
        'Food & Beverages': 0.18,
        'Housing & Utilities': 0.22,
        'Transport': 0.14,
        'Health': 0.05,
        'Education': 0.12,
        'Clothing & Footwear': 0.08,
        'Communications': 0.03,
        'Recreation & Culture': 0.08,
        'Restaurants & Hotels': 0.04,
        'Alcohol & Tobacco': 0.01,
        'Furnishings': 0.03,
        'Miscellaneous': 0.02
    }
}

st.markdown("""
Different demographic groups experience cost-of-living changes differently based on their spending patterns.
This analysis calculates a **weighted cost-of-living index** for each group based on typical spending allocations.
""")

# Calculate price changes for each category
category_changes = {}
for cat in MAIN_CATEGORIES:
    if cat == "All-items HICP (COICOP 00)":
        continue
    cat_data = hicp_index[hicp_index['Category'] == cat]
    if not cat_data.empty:
        start_data = cat_data[cat_data['Year'] == year_range[0]]['Value'].values
        end_data = cat_data[cat_data['Year'] == year_range[1]]['Value'].values
        if len(start_data) > 0 and len(end_data) > 0 and start_data[0] > 0:
            change = ((end_data[0] - start_data[0]) / start_data[0]) * 100
            category_changes[CATEGORY_SHORT_NAMES[cat]] = change

# Calculate weighted cost-of-living burden for each demographic group
if category_changes:
    burden_data = []
    for group_name, weights in DEMOGRAPHIC_PROFILES.items():
        weighted_change = 0
        for category, weight in weights.items():
            if category in category_changes:
                weighted_change += weight * category_changes[category]
        burden_data.append({
            'Demographic Group': group_name,
            'Weighted Cost Increase (%)': weighted_change
        })
    
    burden_df = pd.DataFrame(burden_data)
    burden_df = burden_df.sort_values('Weighted Cost Increase (%)', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Bar chart showing burden by demographic group
        burden_chart = alt.Chart(burden_df).mark_bar().encode(
            x=alt.X('Weighted Cost Increase (%):Q', 
                    title=f'Weighted Cost-of-Living Increase (%) ({year_range[0]}-{year_range[1]})'),
            y=alt.Y('Demographic Group:N', 
                    sort='-x',
                    title=''),
            color=alt.Color('Weighted Cost Increase (%):Q',
                           scale=alt.Scale(scheme='reds'),
                           legend=None),
            tooltip=[
                alt.Tooltip('Demographic Group:N', title='Group'),
                alt.Tooltip('Weighted Cost Increase (%):Q', title='Burden (%)', format='.1f')
            ]
        ).properties(
            width=500,
            height=350,
            title='Cost-of-Living Burden by Demographic Group'
        )
        
        st.altair_chart(burden_chart, use_container_width=True)
    
    with col2:
        st.subheader("Key Findings")
        most_affected = burden_df.iloc[0]
        least_affected = burden_df.iloc[-1]
        
        st.metric(
            label="Most Affected",
            value=most_affected['Demographic Group'],
            delta=f"+{most_affected['Weighted Cost Increase (%)']:.1f}%"
        )
        st.metric(
            label="Least Affected",
            value=least_affected['Demographic Group'],
            delta=f"+{least_affected['Weighted Cost Increase (%)']:.1f}%"
        )
        
        gap = most_affected['Weighted Cost Increase (%)'] - least_affected['Weighted Cost Increase (%)']
        st.markdown(f"**Burden Gap:** {gap:.1f} percentage points")
    
    # Show spending breakdown for selected group
    st.subheader("Spending Profile Comparison")
    
    # Create data for spending profile visualization
    profile_data = []
    for group_name, weights in DEMOGRAPHIC_PROFILES.items():
        for category, weight in weights.items():
            profile_data.append({
                'Group': group_name,
                'Category': category,
                'Weight': weight * 100,
                'Price Change': category_changes.get(category, 0)
            })
    
    profile_df = pd.DataFrame(profile_data)
    
    # Filter to only selected categories from sidebar
    if selected_categories:
        profile_df = profile_df[profile_df['Category'].isin(selected_categories)]
    
    # Stacked bar showing spending allocation by group
    # Using consistent category colors
    profile_chart = alt.Chart(profile_df).mark_bar().encode(
        x=alt.X('Weight:Q', title='Share of Spending (%)', stack='normalize'),
        y=alt.Y('Group:N', title=''),
        color=alt.Color('Category:N', 
                       title='Category',
                       scale=CATEGORY_COLOR_SCALE,
                       legend=alt.Legend(orient='bottom', columns=4)),
        tooltip=[
            alt.Tooltip('Group:N', title='Group'),
            alt.Tooltip('Category:N', title='Category'),
            alt.Tooltip('Weight:Q', title='Spending Share (%)', format='.1f'),
            alt.Tooltip('Price Change:Q', title='Price Change (%)', format='.1f')
        ]
    ).properties(
        width=700,
        height=300,
        title='Spending Allocation by Demographic Group'
    )
    
    st.altair_chart(profile_chart, use_container_width=True)

st.divider()

# =============================================================================
# SECTION 5: HOUSEHOLD SPENDING PATTERNS (INTERACTIVE)
# =============================================================================
# Shows how household spending allocation has shifted over time
# Now connected to sidebar filters for year range and categories
st.header("5. Household Spending Patterns Over Time")

# Main consumption categories from personal income data
main_consumption_items = [
    "CP01 - Food and non-alcoholic beverages",
    "CP02 - Alcoholic beverages, tobacco and narcotics",
    "CP03 - Clothing and footwear",
    "CP04 - Housing, water, electricity, gas and other fuels",
    "CP05 - Furnishings, household equipment and routine household maintenance",
    "CP06 - Health",
    "CP07 - Transport",
    "CP08 - Communications",
    "CP09 - Recreation and culture",
    "CP10 - Education",
    "CP11 - Restaurants and hotels",
    "CP12 - Miscellaneous goods and services"
]

# Mapping from consumption item names to short category names (to match sidebar filter)
CONSUMPTION_TO_SHORT = {
    "CP01 - Food and non-alcoholic beverages": "Food & Beverages",
    "CP02 - Alcoholic beverages, tobacco and narcotics": "Alcohol & Tobacco",
    "CP03 - Clothing and footwear": "Clothing & Footwear",
    "CP04 - Housing, water, electricity, gas and other fuels": "Housing & Utilities",
    "CP05 - Furnishings, household equipment and routine household maintenance": "Furnishings",
    "CP06 - Health": "Health",
    "CP07 - Transport": "Transport",
    "CP08 - Communications": "Communications",
    "CP09 - Recreation and culture": "Recreation & Culture",
    "CP10 - Education": "Education",
    "CP11 - Restaurants and hotels": "Restaurants & Hotels",
    "CP12 - Miscellaneous goods and services": "Miscellaneous"
}

# Filter consumption data for main categories and year range from sidebar
consumption_filtered = consumption[
    (consumption['Item'].isin(main_consumption_items)) &
    (consumption['Year'] >= year_range[0]) &
    (consumption['Year'] <= year_range[1])
].copy()

# Extract short item names (remove "CP01 - " prefix)
consumption_filtered['ShortItem'] = consumption_filtered['Item'].map(CONSUMPTION_TO_SHORT)

# Filter to selected categories from sidebar if any are selected
if selected_categories:
    consumption_filtered = consumption_filtered[consumption_filtered['ShortItem'].isin(selected_categories)]

st.markdown(f"""
**Filters Applied:** Year range {year_range[0]}-{year_range[1]} | 
Categories: {', '.join(selected_categories) if selected_categories else 'All categories'}
""")

if not consumption_filtered.empty:
    # Calculate yearly totals for percentage calculation
    yearly_total = consumption_filtered.groupby('Year')['Value'].sum().reset_index()
    yearly_total.columns = ['Year', 'Total']
    
    # Merge to calculate each category's share of total spending
    consumption_merged = consumption_filtered.merge(yearly_total, on='Year')
    consumption_merged['Percentage'] = (consumption_merged['Value'] / consumption_merged['Total']) * 100
    
    # Create selection for interactivity
    selection = alt.selection_point(fields=['ShortItem'], bind='legend')
    
    # Stacked area chart showing spending composition over time
    # Using consistent category colors
    area_chart = alt.Chart(consumption_merged).mark_area().encode(
        x=alt.X('Year:O', title='Year'),
        y=alt.Y('Value:Q', title='Spending (€ Million)', stack='zero'),
        color=alt.Color('ShortItem:N', 
                       title='Category',
                       scale=CATEGORY_COLOR_SCALE,
                       legend=alt.Legend(orient='right')),
        opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        tooltip=[
            alt.Tooltip('ShortItem:N', title='Category'),
            alt.Tooltip('Year:O', title='Year'),
            alt.Tooltip('Value:Q', title='€ Million', format=',.0f'),
            alt.Tooltip('Percentage:Q', title='Share (%)', format='.1f')
        ]
    ).properties(
        width=700,
        height=400,
        title=f'Household Spending by Category ({year_range[0]}-{year_range[1]})'
    ).add_params(selection).interactive()
    
    st.altair_chart(area_chart, use_container_width=True)
    st.caption("Click on legend items to highlight specific categories")
else:
    st.warning("No data available for the selected filters. Please adjust the year range or categories.")

st.divider()

# =============================================================================
# SECTION 6: KEY INSIGHTS SUMMARY
# =============================================================================
# Aggregates key findings from all visualizations
st.header("Key Insights & Summary")

# Three-column layout for key insights
col1, col2, col3 = st.columns(3)

with col1:
    # Summary of highest price increases from Section 1
    st.markdown("### Highest Price Increases")
    if 'change_df' in dir() and not change_df.empty:
        top_increases = change_df.head(3)
        for _, row in top_increases.iterrows():
            st.markdown(f"- **{row['Category']}**: +{row['Change']:.1f}%")

with col2:
    # Summary of economic periods from Section 3
    st.markdown("### Economic Periods")
    if 'period_df' in dir() and not period_df.empty:
        period_avg = period_df.groupby('Period')['AnnualChange'].mean()
        worst_period = period_avg.idxmax()
        st.markdown(f"- Worst period: **{worst_period}**")
        st.markdown(f"- Avg inflation: **+{period_avg[worst_period]:.1f}%/year**")

with col3:
    # Summary of demographic burden from Section 4
    st.markdown("### Demographic Impact")
    if 'burden_df' in dir() and not burden_df.empty:
        most_affected = burden_df.iloc[0]
        st.markdown(f"- Most affected: **{most_affected['Demographic Group']}**")
        st.markdown(f"- Burden: **+{most_affected['Weighted Cost Increase (%)']:.1f}%**")

st.divider()

# =============================================================================
# FOOTER: DATA SOURCES AND METHODOLOGY
# =============================================================================
st.markdown("""
---
**Data Sources:** Central Statistics Office (CSO) Ireland - Harmonised Index of Consumer Prices (HICP), 
Household Income Statistics, Personal Consumption Expenditure

**Methodology:** Price indices are based on 2015=100. Economic periods defined as Pre-COVID (2015-2019), 
COVID (2020-2021), Inflation Surge (2022-2023), and Stabilization (2024). Demographic burden calculated 
using weighted spending profiles based on CSO Household Budget Survey patterns.
""")
