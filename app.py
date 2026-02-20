"""
Ireland Cost of Living Analysis Dashboard
==========================================
An interactive Streamlit dashboard exploring how the cost of living has changed 
in Ireland since 2015, addressing four key research questions:
1. Which price categories have increased the most?
2. How do these increases differ over time?
3. Are regions with lower household income experiencing higher pressure?
4. Are price increases concentrated in essential goods?

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
# DASHBOARD HEADER
# =============================================================================
st.title("🇮🇪 Ireland Cost of Living Analysis (2015-2024)")
st.markdown("""
This interactive dashboard explores how the cost of living has changed in Ireland since 2015, 
examining which price categories have increased the most, how changes differ over time, 
regional income disparities, and whether essential goods face higher price pressure.
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
    selected_categories = st.multiselect(
        "Select Categories to Compare",
        options=list(CATEGORY_SHORT_NAMES.values()),
        default=["Food & Beverages", "Housing & Utilities", "Transport", "Education", "Health"]
    )
    
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
    
    # Create two-column layout: chart on left, metrics on right
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Horizontal bar chart with conditional coloring
        # Red = essential categories, Blue = non-essential
        bar_chart = alt.Chart(change_df).mark_bar().encode(
            x=alt.X('Change:Q', 
                    title=f'Price Change (%) from {year_range[0]} to {year_range[1]}',
                    axis=alt.Axis(format='.1f')),
            y=alt.Y('Category:N', 
                    sort='-x',  # Sort by x-value (highest change at top)
                    title=''),
            color=alt.condition(
                alt.datum.IsEssential,
                alt.value('#e45756'),  # Red for essential
                alt.value('#4c78a8')   # Blue for non-essential
            ),
            tooltip=[
                alt.Tooltip('Category:N', title='Category'),
                alt.Tooltip('Change:Q', title='Change (%)', format='.1f'),
                alt.Tooltip('BaseValue:Q', title=f'{year_range[0]} Index', format='.1f'),
                alt.Tooltip('LatestValue:Q', title=f'{year_range[1]} Index', format='.1f')
            ]
        ).properties(
            width=500,
            height=400,
            title=f'Price Index Change by Category ({year_range[0]}-{year_range[1]})'
        )
        
        st.altair_chart(bar_chart, use_container_width=True)
        st.caption("🔴 Essential categories | 🔵 Non-essential categories")
    
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
    
    # Base encoding shared by lines and points
    base = alt.Chart(filtered_monthly).encode(
        x=alt.X('Date:T', title='Date', axis=alt.Axis(format='%Y')),
        y=alt.Y('Value:Q', title='Price Index (Base 2015=100)'),
        color=alt.Color('ShortCategory:N', 
                       title='Category',
                       legend=alt.Legend(orient='bottom', columns=3))
    )
    
    # Line marks with opacity tied to hover state
    lines = base.mark_line(strokeWidth=2).encode(
        opacity=alt.condition(highlight, alt.value(1), alt.value(0.3))
    ).add_params(highlight)
    
    # Circle marks appear on hover for precise value reading
    points = base.mark_circle(size=60).encode(
        opacity=alt.condition(highlight, alt.value(1), alt.value(0)),
        tooltip=[
            alt.Tooltip('ShortCategory:N', title='Category'),
            alt.Tooltip('Date:T', title='Date', format='%B %Y'),
            alt.Tooltip('Value:Q', title='Index Value', format='.1f')
        ]
    )
    
    # Combine lines and points into layered chart
    line_chart = (lines + points).properties(
        width=800,
        height=400,
        title='Monthly Price Index Trends by Category'
    ).interactive()  # Enable pan/zoom
    
    st.altair_chart(line_chart, use_container_width=True)
    
    # --- Year-over-Year Heatmap ---
    # Shows inflation intensity across categories and years simultaneously
    st.subheader("Year-over-Year Change Heatmap")
    
    # Calculate YoY change: compare each month to same month previous year
    yoy_data = []
    for cat in selected_full_categories:
        cat_data = monthly_hicp[monthly_hicp['Category'] == cat].copy()
        cat_data = cat_data.sort_values('Date')
        # pct_change with periods=12 compares to 12 months ago (same month last year)
        cat_data['YoY_Change'] = cat_data['Value'].pct_change(periods=12) * 100
        for _, row in cat_data.iterrows():
            if pd.notna(row['YoY_Change']) and pd.notna(row['Year']):
                yoy_data.append({
                    'Category': CATEGORY_SHORT_NAMES[cat],
                    'Year': int(row['Year']),
                    'Month': row['MonthNum'],
                    'YoY_Change': row['YoY_Change']
                })
    
    if yoy_data:
        yoy_df = pd.DataFrame(yoy_data)
        # Average YoY change per year (across all months in that year)
        yoy_annual = yoy_df.groupby(['Category', 'Year'])['YoY_Change'].mean().reset_index()
        
        # Heatmap: color saturation encodes inflation rate
        # Diverging color scale: blue (deflation) to red (high inflation)
        heatmap = alt.Chart(yoy_annual).mark_rect().encode(
            x=alt.X('Year:O', title='Year'),
            y=alt.Y('Category:N', title=''),
            color=alt.Color('YoY_Change:Q', 
                           title='Avg YoY Change (%)',
                           scale=alt.Scale(scheme='redblue', reverse=True, domain=[-5, 15])),
            tooltip=[
                alt.Tooltip('Category:N', title='Category'),
                alt.Tooltip('Year:O', title='Year'),
                alt.Tooltip('YoY_Change:Q', title='Avg YoY Change (%)', format='.1f')
            ]
        ).properties(
            width=600,
            height=300,
            title='Average Year-over-Year Price Change by Category and Year'
        )
        
        st.altair_chart(heatmap, use_container_width=True)

st.divider()

# =============================================================================
# SECTION 3: REGIONAL INCOME ANALYSIS
# =============================================================================
# Answers Q3: Are regions with lower household income experiencing higher pressure?
# Encoding: Line chart for income trends, grouped bars for income vs CPI comparison
st.header("3. Regional Income Disparities and Cost Pressure")

# Filter employee compensation data by region (excluding Ireland total)
# NUTS 2 regions: Northern & Western, Southern, Eastern & Midland
income_data = household_income[
    (household_income['Statistic'].str.contains('Compensation of Employees', na=False)) &
    (household_income['Year'] >= year_range[0]) &
    (household_income['Year'] <= year_range[1]) &
    (household_income['Region'] != 'Ireland')  # Exclude national total
].copy()

# Filter disposable income index data (State=100 baseline)
disposable_income = household_income[
    (household_income['Statistic'].str.contains('Disposable Income per Person', na=False)) &
    (household_income['Year'] >= year_range[0]) &
    (household_income['Year'] <= year_range[1]) &
    (household_income['Region'] != 'Ireland')
].copy()

# Two-column layout for regional charts
col1, col2 = st.columns(2)

with col1:
    if not income_data.empty:
        # Line chart showing employee compensation trends by region
        income_chart = alt.Chart(income_data).mark_line(point=True, strokeWidth=2).encode(
            x=alt.X('Year:O', title='Year'),
            y=alt.Y('Value:Q', title='Compensation (€ Million)'),
            color=alt.Color('Region:N', 
                           title='Region',
                           scale=alt.Scale(scheme='category10')),
            tooltip=[
                alt.Tooltip('Region:N', title='Region'),
                alt.Tooltip('Year:O', title='Year'),
                alt.Tooltip('Value:Q', title='€ Million', format=',.0f')
            ]
        ).properties(
            width=400,
            height=350,
            title='Regional Employee Compensation Over Time'
        ).interactive()
        
        st.altair_chart(income_chart, use_container_width=True)

with col2:
    if not disposable_income.empty:
        # Grouped bar chart showing disposable income index by region
        # Values relative to State=100 (national average)
        disp_chart = alt.Chart(disposable_income).mark_bar().encode(
            x=alt.X('Year:O', title='Year'),
            y=alt.Y('Value:Q', title='Index (State=100)'),
            color=alt.Color('Region:N', title='Region'),
            xOffset='Region:N',  # Group bars by region within each year
            tooltip=[
                alt.Tooltip('Region:N', title='Region'),
                alt.Tooltip('Year:O', title='Year'),
                alt.Tooltip('Value:Q', title='Index', format='.1f')
            ]
        ).properties(
            width=400,
            height=350,
            title='Disposable Income Index by Region (State=100)'
        )
        
        st.altair_chart(disp_chart, use_container_width=True)

# Get overall CPI for comparison with income growth
all_items_cpi = annual_cpi[
    (annual_cpi['Statistic'] == 'Harmonised Index of Consumer Prices') &
    (annual_cpi['Category'] == 'All-items HICP (COICOP 00)') &
    (annual_cpi['Year'] >= year_range[0]) &
    (annual_cpi['Year'] <= year_range[1])
].copy()

# --- Income Growth vs CPI Growth Comparison ---
# Key insight: Real income change = Income Growth - CPI Growth
# Positive = purchasing power increased, Negative = purchasing power decreased
if not income_data.empty and not all_items_cpi.empty:
    st.subheader("Income Growth vs Price Inflation by Region")
    
    # Calculate income growth for each region
    regional_growth = []
    for region in income_data['Region'].unique():
        region_data = income_data[income_data['Region'] == region].sort_values('Year')
        if len(region_data) >= 2:
            start_val = region_data[region_data['Year'] == year_range[0]]['Value'].values
            end_val = region_data[region_data['Year'] == year_range[1]]['Value'].values
            if len(start_val) > 0 and len(end_val) > 0 and start_val[0] > 0:
                income_growth = ((end_val[0] - start_val[0]) / start_val[0]) * 100
                regional_growth.append({
                    'Region': region,
                    'Income Growth (%)': income_growth
                })
    
    # Calculate CPI growth (same for all regions - national figure)
    cpi_start = all_items_cpi[all_items_cpi['Year'] == year_range[0]]['Value'].values
    cpi_end = all_items_cpi[all_items_cpi['Year'] == year_range[1]]['Value'].values
    
    if len(cpi_start) > 0 and len(cpi_end) > 0 and cpi_start[0] > 0:
        cpi_growth = ((cpi_end[0] - cpi_start[0]) / cpi_start[0]) * 100
        
        if regional_growth:
            growth_df = pd.DataFrame(regional_growth)
            growth_df['CPI Growth (%)'] = cpi_growth
            # Real income change: how much purchasing power changed
            growth_df['Real Income Change (%)'] = growth_df['Income Growth (%)'] - growth_df['CPI Growth (%)']
            
            # Reshape data for grouped bar chart
            growth_melted = growth_df.melt(
                id_vars=['Region'],
                value_vars=['Income Growth (%)', 'CPI Growth (%)'],
                var_name='Metric',
                value_name='Growth'
            )
            
            # Grouped bar chart comparing income growth vs CPI growth
            comparison_chart = alt.Chart(growth_melted).mark_bar().encode(
                x=alt.X('Region:N', title=''),
                y=alt.Y('Growth:Q', title='Growth (%)'),
                color=alt.Color('Metric:N', 
                               title='',
                               scale=alt.Scale(range=['#4c78a8', '#e45756'])),
                xOffset='Metric:N',
                tooltip=[
                    alt.Tooltip('Region:N', title='Region'),
                    alt.Tooltip('Metric:N', title='Metric'),
                    alt.Tooltip('Growth:Q', title='Growth (%)', format='.1f')
                ]
            ).properties(
                width=600,
                height=300,
                title=f'Income Growth vs CPI Growth ({year_range[0]}-{year_range[1]})'
            )
            
            st.altair_chart(comparison_chart, use_container_width=True)
            
            # Display real income change as metric cards
            st.markdown("**Real Income Change (Income Growth - CPI Growth):**")
            cols = st.columns(len(growth_df))
            for i, (_, row) in enumerate(growth_df.iterrows()):
                with cols[i]:
                    delta_color = "normal" if row['Real Income Change (%)'] >= 0 else "inverse"
                    st.metric(
                        label=row['Region'],
                        value=f"{row['Real Income Change (%)']:.1f}%",
                        delta="Real purchasing power change"
                    )

st.divider()

# =============================================================================
# SECTION 4: ESSENTIAL VS NON-ESSENTIAL GOODS
# =============================================================================
# Answers Q4: Are price increases concentrated in essential goods?
# Encoding: Violin plot for distribution comparison
st.header("4. Are Price Increases Concentrated in Essential Goods?")

# Calculate price change for each category and classify as essential/non-essential
essential_vs_non = []
for cat in MAIN_CATEGORIES:
    if cat == "All-items HICP (COICOP 00)":
        continue  # Skip the "All Items" aggregate
    cat_data = hicp_index[hicp_index['Category'] == cat]
    if not cat_data.empty:
        start_data = cat_data[cat_data['Year'] == year_range[0]]['Value'].values
        end_data = cat_data[cat_data['Year'] == year_range[1]]['Value'].values
        if len(start_data) > 0 and len(end_data) > 0 and start_data[0] > 0:
            change = ((end_data[0] - start_data[0]) / start_data[0]) * 100
            essential_vs_non.append({
                'Category': CATEGORY_SHORT_NAMES[cat],
                'Type': 'Essential' if cat in ESSENTIAL_CATEGORIES else 'Non-Essential',
                'Change': change
            })

if essential_vs_non:
    essential_df = pd.DataFrame(essential_vs_non)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Violin plot showing distribution of price changes for each type
        # Uses density transform to create the violin shape
        violin = alt.Chart(essential_df).transform_density(
            'Change',
            as_=['Change', 'density'],
            extent=[-10, 50],  # Range of price changes
            groupby=['Type']
        ).mark_area(orient='horizontal').encode(
            y=alt.Y('Change:Q', title='Price Change (%)'),
            x=alt.X('density:Q', 
                    stack='center',  # Center the violin
                    impute=None,
                    title=None,
                    axis=alt.Axis(labels=False, values=[0], grid=False, ticks=True)),
            color=alt.Color('Type:N', 
                           scale=alt.Scale(range=['#e45756', '#4c78a8']),
                           legend=alt.Legend(title='Category Type')),
            column=alt.Column('Type:N', 
                             header=alt.Header(titleOrient='bottom', labelOrient='bottom', labelPadding=0),
                             title='')
        ).properties(
            width=150,
            height=350,
            title='Distribution of Price Changes: Essential vs Non-Essential'
        )
        
        # Overlay individual points on the violin
        points = alt.Chart(essential_df).mark_circle(size=100, opacity=0.8).encode(
            y=alt.Y('Change:Q'),
            x=alt.value(75),  # Center points in the violin
            color=alt.Color('Type:N', scale=alt.Scale(range=['#e45756', '#4c78a8'])),
            tooltip=[
                alt.Tooltip('Category:N', title='Category'),
                alt.Tooltip('Change:Q', title='Change (%)', format='.1f')
            ],
            column=alt.Column('Type:N', header=alt.Header(labelFontSize=0, title=''))
        ).properties(
            width=150,
            height=350
        )
        
        st.altair_chart(violin, use_container_width=False)
        
        # Show individual data points separately for clarity
        st.markdown("**Individual Category Values:**")
        strip_plot = alt.Chart(essential_df).mark_circle(size=120).encode(
            x=alt.X('Type:N', title=''),
            y=alt.Y('Change:Q', title='Price Change (%)'),
            color=alt.Color('Type:N', 
                           scale=alt.Scale(range=['#e45756', '#4c78a8']),
                           legend=None),
            tooltip=[
                alt.Tooltip('Category:N', title='Category'),
                alt.Tooltip('Change:Q', title='Change (%)', format='.1f')
            ]
        ).properties(
            width=300,
            height=250
        )
        st.altair_chart(strip_plot, use_container_width=True)
    
    with col2:
        # Summary statistics for each type
        summary = essential_df.groupby('Type')['Change'].agg(['mean', 'median', 'std']).reset_index()
        summary.columns = ['Type', 'Mean', 'Median', 'Std Dev']
        
        st.subheader("Summary Statistics")
        for _, row in summary.iterrows():
            st.markdown(f"**{row['Type']}**")
            st.write(f"- Mean: {row['Mean']:.1f}%")
            st.write(f"- Median: {row['Median']:.1f}%")
            st.write(f"- Std Dev: {row['Std Dev']:.1f}%")
    
    # Detailed scatter plot showing all categories
    st.subheader("Detailed Category Comparison")
    
    scatter = alt.Chart(essential_df).mark_circle(size=150).encode(
        x=alt.X('Category:N', title='', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('Change:Q', title='Price Change (%)'),
        color=alt.Color('Type:N', 
                       title='Category Type',
                       scale=alt.Scale(range=['#e45756', '#4c78a8'])),
        tooltip=[
            alt.Tooltip('Category:N', title='Category'),
            alt.Tooltip('Type:N', title='Type'),
            alt.Tooltip('Change:Q', title='Change (%)', format='.1f')
        ]
    ).properties(
        width=700,
        height=350,
        title='Price Change by Category (Essential vs Non-Essential)'
    )
    
    # Add horizontal reference line at y=0 (no change)
    rule = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(strokeDash=[5, 5], color='gray').encode(y='y:Q')
    
    st.altair_chart(scatter + rule, use_container_width=True)

st.divider()

# =============================================================================
# SECTION 5: HOUSEHOLD SPENDING PATTERNS
# =============================================================================
# Shows how household spending allocation has shifted over time
# Encoding: Stacked area chart (part-to-whole over time)
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

# Filter consumption data for main categories
consumption_filtered = consumption[
    (consumption['Item'].isin(main_consumption_items)) &
    (consumption['Year'] >= year_range[0]) &
    (consumption['Year'] <= year_range[1])
].copy()

# Extract short item names (remove "CP01 - " prefix)
consumption_filtered['ShortItem'] = consumption_filtered['Item'].str.extract(r'CP\d+ - (.+)')[0]

if not consumption_filtered.empty:
    # Calculate yearly totals for percentage calculation
    yearly_total = consumption_filtered.groupby('Year')['Value'].sum().reset_index()
    yearly_total.columns = ['Year', 'Total']
    
    # Merge to calculate each category's share of total spending
    consumption_merged = consumption_filtered.merge(yearly_total, on='Year')
    consumption_merged['Percentage'] = (consumption_merged['Value'] / consumption_merged['Total']) * 100
    
    # Stacked area chart showing spending composition over time
    # stack='normalize' ensures all years sum to 100%
    area_chart = alt.Chart(consumption_merged).mark_area().encode(
        x=alt.X('Year:O', title='Year'),
        y=alt.Y('Percentage:Q', title='Share of Total Spending (%)', stack='normalize'),
        color=alt.Color('ShortItem:N', 
                       title='Category',
                       legend=alt.Legend(orient='right')),
        tooltip=[
            alt.Tooltip('ShortItem:N', title='Category'),
            alt.Tooltip('Year:O', title='Year'),
            alt.Tooltip('Value:Q', title='€ Million', format=',.0f'),
            alt.Tooltip('Percentage:Q', title='Share (%)', format='.1f')
        ]
    ).properties(
        width=700,
        height=400,
        title='Household Spending Distribution by Category'
    ).interactive()
    
    st.altair_chart(area_chart, use_container_width=True)

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
    st.markdown("### 📈 Highest Price Increases")
    if not change_df.empty:
        top_increases = change_df.head(3)
        for _, row in top_increases.iterrows():
            st.markdown(f"- **{row['Category']}**: +{row['Change']:.1f}%")

with col2:
    # Summary of essential vs non-essential comparison from Section 4
    st.markdown("### 🏠 Essential Goods Impact")
    if essential_vs_non:
        essential_avg = essential_df[essential_df['Type'] == 'Essential']['Change'].mean()
        non_essential_avg = essential_df[essential_df['Type'] == 'Non-Essential']['Change'].mean()
        st.markdown(f"- Essential goods avg: **+{essential_avg:.1f}%**")
        st.markdown(f"- Non-essential avg: **+{non_essential_avg:.1f}%**")
        if essential_avg > non_essential_avg:
            st.markdown("- ⚠️ Essential goods rising faster")

with col3:
    # Summary of regional disparities from Section 3
    st.markdown("### 🗺️ Regional Disparities")
    if 'growth_df' in dir() and growth_df is not None:
        lowest_region = growth_df.loc[growth_df['Real Income Change (%)'].idxmin()]
        highest_region = growth_df.loc[growth_df['Real Income Change (%)'].idxmax()]
        st.markdown(f"- Most affected: **{lowest_region['Region']}**")
        st.markdown(f"- Least affected: **{highest_region['Region']}**")

st.divider()

# =============================================================================
# FOOTER: DATA SOURCES AND METHODOLOGY
# =============================================================================
st.markdown("""
---
**Data Sources:** Central Statistics Office (CSO) Ireland - Harmonised Index of Consumer Prices (HICP), 
Household Income Statistics, Personal Consumption Expenditure

**Methodology:** Price indices are based on 2015=100. Essential categories include Food, Housing, Health, 
Transport, and Education. Regional analysis uses NUTS 2 regions.
""")
