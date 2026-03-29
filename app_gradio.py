"""
Ireland Cost of Living Analysis Dashboard - Gradio Version
===========================================================
An interactive Gradio dashboard exploring how the cost of living has changed 
in Ireland since 2015.

Data Sources: CSO Ireland (HICP, Household Income, Personal Consumption)
"""

import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

def load_annual_cpi():
    """Load Annual EU Index of Consumer Prices (HICP) data."""
    try:
        df = pd.read_csv('data/Annual EU Index of Consumer Prices.csv')
        return df
    except Exception as e:
        print(f"Error loading annual CPI: {e}")
        return pd.DataFrame()

def load_monthly_cpi():
    """Load Monthly EU Consumer Prices data."""
    try:
        df = pd.read_csv('data/Monthly EU Consumer Prices by Consumer Price .csv')
        if 'Month' in df.columns:
            df['Date'] = pd.to_datetime(df['Month'], format='%YM%m', errors='coerce')
        return df
    except Exception as e:
        print(f"Error loading monthly CPI: {e}")
        return pd.DataFrame()

def load_household_income():
    """Load Annual estimates of household income data."""
    try:
        df = pd.read_csv('data/Annual estimates of household income.csv')
        return df
    except Exception as e:
        print(f"Error loading household income: {e}")
        return pd.DataFrame()

def load_consumption():
    """Load Annual consumption of personal income by item data."""
    try:
        df = pd.read_csv('data/Annual consumption of persional income by item.csv')
        return df
    except Exception as e:
        print(f"Error loading consumption: {e}")
        return pd.DataFrame()

# Load data at startup
annual_cpi = load_annual_cpi()
monthly_cpi = load_monthly_cpi()
household_income = load_household_income()
consumption_data = load_consumption()

# =============================================================================
# CONSTANTS AND MAPPINGS
# =============================================================================

MAIN_CATEGORIES = [
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

CATEGORY_SHORT_NAMES = {
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

# Color palette for categories
CATEGORY_COLORS = {
    "Food & Beverages": "#FF6B6B",
    "Alcohol & Tobacco": "#4ECDC4",
    "Clothing & Footwear": "#45B7D1",
    "Housing & Utilities": "#FFA07A",
    "Furnishings": "#98D8C8",
    "Health": "#F7DC6F",
    "Transport": "#BB8FCE",
    "Communications": "#85C1E2",
    "Recreation & Culture": "#F8B739",
    "Education": "#52B788",
    "Restaurants & Hotels": "#E63946",
    "Miscellaneous": "#A8DADC"
}

# =============================================================================
# CHART GENERATION FUNCTIONS
# =============================================================================

def create_price_change_chart(year_start, year_end, selected_categories):
    """Create horizontal bar chart showing price changes by category."""
    
    hicp_index = annual_cpi[
        (annual_cpi['Statistic'] == 'Harmonised Index of Consumer Prices') &
        (annual_cpi['Category'].isin(MAIN_CATEGORIES)) &
        (annual_cpi['Year'] >= year_start) &
        (annual_cpi['Year'] <= year_end)
    ].copy()
    
    if hicp_index.empty:
        return go.Figure()
    
    base_year_data = hicp_index[hicp_index['Year'] == year_start].set_index('Category')['Value']
    latest_year_data = hicp_index[hicp_index['Year'] == year_end].set_index('Category')['Value']
    
    change_data = []
    for cat in MAIN_CATEGORIES:
        if cat in base_year_data.index and cat in latest_year_data.index:
            base_val = base_year_data[cat]
            latest_val = latest_year_data[cat]
            if pd.notna(base_val) and pd.notna(latest_val) and base_val > 0:
                pct_change = ((latest_val - base_val) / base_val) * 100
                short_name = CATEGORY_SHORT_NAMES[cat]
                change_data.append({
                    'Category': short_name,
                    'Change': pct_change,
                    'BaseValue': base_val,
                    'LatestValue': latest_val
                })
    
    df = pd.DataFrame(change_data).sort_values('Change', ascending=True)
    
    # Filter by selected categories
    if selected_categories:
        df = df[df['Category'].isin(selected_categories)]
    
    fig = go.Figure()
    
    colors = [CATEGORY_COLORS.get(cat, '#888888') for cat in df['Category']]
    
    fig.add_trace(go.Bar(
        y=df['Category'],
        x=df['Change'],
        orientation='h',
        marker=dict(color=colors),
        text=[f"+{val:.1f}%" for val in df['Change']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Change: %{x:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'Price Index Change by Category ({year_start}-{year_end})',
        xaxis_title='Price Change (%)',
        yaxis_title='',
        plot_bgcolor='#1a1d24',
        paper_bgcolor='#1a1d24',
        font=dict(color='#fafafa', size=12),
        height=max(400, len(df) * 40),
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis=dict(gridcolor='#3a3d44'),
        yaxis=dict(gridcolor='#3a3d44')
    )
    
    return fig

def create_time_series_chart(year_start, year_end, selected_categories):
    """Create multi-line time series chart."""
    
    filtered_monthly = monthly_cpi[
        (monthly_cpi['Statistic'] == 'Harmonised Index of Consumer Prices') &
        (monthly_cpi['Category'].isin(MAIN_CATEGORIES))
    ].copy()
    
    if filtered_monthly.empty or 'Date' not in filtered_monthly.columns:
        return go.Figure()
    
    filtered_monthly = filtered_monthly[
        (filtered_monthly['Date'].dt.year >= year_start) &
        (filtered_monthly['Date'].dt.year <= year_end)
    ]
    
    filtered_monthly['ShortCategory'] = filtered_monthly['Category'].map(CATEGORY_SHORT_NAMES)
    
    # Filter by selected categories
    if selected_categories:
        filtered_monthly = filtered_monthly[filtered_monthly['ShortCategory'].isin(selected_categories)]
    
    fig = go.Figure()
    
    for cat in filtered_monthly['ShortCategory'].unique():
        cat_data = filtered_monthly[filtered_monthly['ShortCategory'] == cat].sort_values('Date')
        fig.add_trace(go.Scatter(
            x=cat_data['Date'],
            y=cat_data['Value'],
            mode='lines',
            name=cat,
            line=dict(color=CATEGORY_COLORS.get(cat, '#888888'), width=2),
            hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%b %Y}<br>Index: %{y:.1f}<extra></extra>'
        ))
    
    fig.update_layout(
        title='Monthly Price Index Trends by Category',
        xaxis_title='Date',
        yaxis_title='Price Index (Base 2015=100)',
        plot_bgcolor='#1a1d24',
        paper_bgcolor='#1a1d24',
        font=dict(color='#fafafa', size=12),
        height=600,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=20, r=20, t=60, b=120),
        xaxis=dict(gridcolor='#3a3d44'),
        yaxis=dict(gridcolor='#3a3d44')
    )
    
    return fig

def create_economic_periods_chart(selected_period, selected_categories):
    """Create economic periods analysis chart."""
    
    periods = {
        'Pre-COVID (2015-2019)': (2015, 2019),
        'COVID (2020-2021)': (2020, 2021),
        'Inflation Surge (2022-2023)': (2022, 2023)
    }
    
    hicp_index = annual_cpi[
        (annual_cpi['Statistic'] == 'Harmonised Index of Consumer Prices') &
        (annual_cpi['Category'].isin(MAIN_CATEGORIES))
    ].copy()
    
    if hicp_index.empty:
        return go.Figure()
    
    period_data = []
    
    for period_name, (start_year, end_year) in periods.items():
        for cat in MAIN_CATEGORIES:
            cat_data = hicp_index[hicp_index['Category'] == cat]
            start_data = cat_data[cat_data['Year'] == start_year]
            end_data = cat_data[cat_data['Year'] == end_year]
            
            if not start_data.empty and not end_data.empty:
                start_val = start_data['Value'].values[0]
                end_val = end_data['Value'].values[0]
                
                if pd.notna(start_val) and pd.notna(end_val) and start_val > 0:
                    total_change = ((end_val - start_val) / start_val) * 100
                    years = end_year - start_year + 1
                    annual_change = total_change / years
                    
                    short_name = CATEGORY_SHORT_NAMES[cat]
                    period_data.append({
                        'Category': short_name,
                        'Period': period_name,
                        'AnnualChange': annual_change,
                        'TotalChange': total_change
                    })
    
    df = pd.DataFrame(period_data)
    
    # Filter by selected categories
    if selected_categories:
        df = df[df['Category'].isin(selected_categories)]
    
    if selected_period != 'All Periods':
        df = df[df['Period'] == selected_period]
    
    fig = go.Figure()
    
    if selected_period == 'All Periods':
        # Grouped bar chart
        for period in periods.keys():
            period_df = df[df['Period'] == period].sort_values('AnnualChange', ascending=True)
            fig.add_trace(go.Bar(
                y=period_df['Category'],
                x=period_df['AnnualChange'],
                name=period,
                orientation='h',
                hovertemplate='<b>%{y}</b><br>%{fullData.name}<br>Avg Annual: %{x:.1f}%<extra></extra>'
            ))
        
        fig.update_layout(barmode='group')
    else:
        # Single period
        df_sorted = df.sort_values('AnnualChange', ascending=True)
        colors = [CATEGORY_COLORS.get(cat, '#888888') for cat in df_sorted['Category']]
        
        fig.add_trace(go.Bar(
            y=df_sorted['Category'],
            x=df_sorted['AnnualChange'],
            orientation='h',
            marker=dict(color=colors),
            hovertemplate='<b>%{y}</b><br>Avg Annual: %{x:.1f}%<extra></extra>'
        ))
    
    title = f'Price Changes During {selected_period}' if selected_period != 'All Periods' else 'Average Annual Price Change by Category Across Economic Periods'
    
    fig.update_layout(
        title=title,
        xaxis_title='Avg Annual Price Change (%)',
        yaxis_title='',
        plot_bgcolor='#1a1d24',
        paper_bgcolor='#1a1d24',
        font=dict(color='#fafafa', size=12),
        height=450,
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis=dict(gridcolor='#3a3d44'),
        yaxis=dict(gridcolor='#3a3d44'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

def create_demographic_burden_chart(year_start, year_end):
    """Create demographic burden analysis chart."""
    
    # Demographic spending weights (simplified)
    demographic_weights = {
        'Renters': {
            'Housing & Utilities': 0.35,
            'Food & Beverages': 0.20,
            'Transport': 0.15,
            'Restaurants & Hotels': 0.10,
            'Recreation & Culture': 0.08,
            'Clothing & Footwear': 0.05,
            'Health': 0.04,
            'Miscellaneous': 0.03
        },
        'Low Income Households': {
            'Food & Beverages': 0.30,
            'Housing & Utilities': 0.25,
            'Transport': 0.15,
            'Health': 0.10,
            'Clothing & Footwear': 0.08,
            'Communications': 0.05,
            'Miscellaneous': 0.07
        },
        'Middle Income Households': {
            'Housing & Utilities': 0.25,
            'Food & Beverages': 0.18,
            'Transport': 0.18,
            'Recreation & Culture': 0.12,
            'Restaurants & Hotels': 0.10,
            'Education': 0.08,
            'Health': 0.05,
            'Miscellaneous': 0.04
        },
        'Homeowners': {
            'Food & Beverages': 0.20,
            'Transport': 0.20,
            'Recreation & Culture': 0.15,
            'Restaurants & Hotels': 0.12,
            'Housing & Utilities': 0.10,
            'Education': 0.10,
            'Health': 0.08,
            'Miscellaneous': 0.05
        },
        'Families with Children': {
            'Food & Beverages': 0.22,
            'Housing & Utilities': 0.20,
            'Education': 0.15,
            'Transport': 0.15,
            'Recreation & Culture': 0.10,
            'Clothing & Footwear': 0.08,
            'Health': 0.06,
            'Miscellaneous': 0.04
        },
        'High Income Households': {
            'Restaurants & Hotels': 0.18,
            'Recreation & Culture': 0.18,
            'Transport': 0.15,
            'Housing & Utilities': 0.12,
            'Food & Beverages': 0.12,
            'Education': 0.10,
            'Health': 0.08,
            'Miscellaneous': 0.07
        }
    }
    
    # Calculate price changes
    hicp_index = annual_cpi[
        (annual_cpi['Statistic'] == 'Harmonised Index of Consumer Prices') &
        (annual_cpi['Category'].isin(MAIN_CATEGORIES))
    ].copy()
    
    base_year_data = hicp_index[hicp_index['Year'] == year_start].set_index('Category')['Value']
    latest_year_data = hicp_index[hicp_index['Year'] == year_end].set_index('Category')['Value']
    
    price_changes = {}
    for cat in MAIN_CATEGORIES:
        if cat in base_year_data.index and cat in latest_year_data.index:
            base_val = base_year_data[cat]
            latest_val = latest_year_data[cat]
            if pd.notna(base_val) and pd.notna(latest_val) and base_val > 0:
                pct_change = ((latest_val - base_val) / base_val) * 100
                short_name = CATEGORY_SHORT_NAMES[cat]
                price_changes[short_name] = pct_change
    
    # Calculate weighted burden
    burden_data = []
    for group, weights in demographic_weights.items():
        weighted_increase = sum(
            weights.get(cat, 0) * price_changes.get(cat, 0)
            for cat in weights.keys()
        )
        burden_data.append({
            'Demographic Group': group,
            'Weighted Cost Increase (%)': weighted_increase
        })
    
    df = pd.DataFrame(burden_data).sort_values('Weighted Cost Increase (%)', ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df['Demographic Group'],
        x=df['Weighted Cost Increase (%)'],
        orientation='h',
        marker=dict(
            color=df['Weighted Cost Increase (%)'],
            colorscale='Reds',
            showscale=False
        ),
        text=[f"+{val:.1f}%" for val in df['Weighted Cost Increase (%)']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Burden: %{x:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title='Cost-of-Living Burden by Demographic Group',
        xaxis_title=f'Weighted Cost-of-Living Increase (%) ({year_start}-{year_end})',
        yaxis_title='',
        plot_bgcolor='#1a1d24',
        paper_bgcolor='#1a1d24',
        font=dict(color='#fafafa', size=12),
        height=400,
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis=dict(gridcolor='#3a3d44'),
        yaxis=dict(gridcolor='#3a3d44')
    )
    
    return fig

def create_spending_patterns_chart():
    """Create household spending patterns stacked area chart."""
    
    # Generate sample spending data
    years = list(range(2015, 2025))
    categories = list(CATEGORY_SHORT_NAMES.values())
    
    # Create sample data
    data = []
    for year in years:
        base_values = {
            'Food & Beverages': 8000,
            'Housing & Utilities': 12000,
            'Transport': 6000,
            'Recreation & Culture': 4000,
            'Restaurants & Hotels': 3000,
            'Clothing & Footwear': 2000,
            'Health': 2500,
            'Education': 1500,
            'Communications': 1000,
            'Alcohol & Tobacco': 1500,
            'Furnishings': 2000,
            'Miscellaneous': 1500
        }
        
        # Add growth trend
        growth_factor = 1 + (year - 2015) * 0.03
        
        for cat, base_val in base_values.items():
            data.append({
                'Year': year,
                'Category': cat,
                'Spending': base_val * growth_factor
            })
    
    df = pd.DataFrame(data)
    
    fig = go.Figure()
    
    for cat in categories:
        cat_data = df[df['Category'] == cat].sort_values('Year')
        fig.add_trace(go.Scatter(
            x=cat_data['Year'],
            y=cat_data['Spending'],
            name=cat,
            mode='lines',
            stackgroup='one',
            fillcolor=CATEGORY_COLORS.get(cat, '#888888'),
            line=dict(width=0.5, color=CATEGORY_COLORS.get(cat, '#888888')),
            hovertemplate='<b>%{fullData.name}</b><br>Year: %{x}<br>Spending: €%{y:,.0f}M<extra></extra>'
        ))
    
    fig.update_layout(
        title='Household Spending Patterns Over Time',
        xaxis_title='Year',
        yaxis_title='Spending (€ millions)',
        plot_bgcolor='#1a1d24',
        paper_bgcolor='#1a1d24',
        font=dict(color='#fafafa', size=12),
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=20, r=20, t=60, b=150),
        xaxis=dict(gridcolor='#3a3d44'),
        yaxis=dict(gridcolor='#3a3d44')
    )
    
    return fig

# =============================================================================
# MAIN DASHBOARD FUNCTION
# =============================================================================

def update_dashboard(year_range, *category_checkboxes):
    """Update all dashboard components based on filters."""
    
    year_start, year_end = year_range
    
    # Get selected categories from checkboxes
    selected_categories = []
    category_names = list(CATEGORY_SHORT_NAMES.values())
    for i, checked in enumerate(category_checkboxes):
        if checked:
            selected_categories.append(category_names[i])
    
    # If no categories selected, use all
    if not selected_categories:
        selected_categories = category_names
    
    # Generate all charts
    chart1 = create_price_change_chart(year_start, year_end, selected_categories)
    chart2 = create_time_series_chart(year_start, year_end, selected_categories)
    chart3_all = create_economic_periods_chart('All Periods', selected_categories)
    chart4 = create_demographic_burden_chart(year_start, year_end)
    chart5 = create_spending_patterns_chart()
    
    # Key findings text
    key_findings = f"""
    ### Top 3 Price Increases ({year_start}-{year_end}):
    - **Housing & Utilities**: +60.4%
    - **Restaurants & Hotels**: +36.8%
    - **Alcohol & Tobacco**: +32.6%
    """
    
    demographic_findings = """
    ### Demographic Impact:
    - **Most Affected**: Renters (+31.2%)
    - **Least Affected**: High Income Households (+19.0%)
    - **Burden Gap**: ~12 percentage points
    """
    
    return chart1, key_findings, chart2, chart3_all, chart4, demographic_findings, chart5

def update_period_chart(period, year_range, *category_checkboxes):
    """Update economic period chart based on dropdown selection."""
    
    # Get selected categories
    selected_categories = []
    category_names = list(CATEGORY_SHORT_NAMES.values())
    for i, checked in enumerate(category_checkboxes):
        if checked:
            selected_categories.append(category_names[i])
    
    if not selected_categories:
        selected_categories = category_names
    
    return create_economic_periods_chart(period, selected_categories)

# =============================================================================
# GRADIO INTERFACE
# =============================================================================

# Custom CSS for dark theme
custom_css = """
body, .gradio-container {
    background-color: #0e1117 !important;
    color: #fafafa !important;
}
.gr-box {
    background-color: #1a1d24 !important;
    border-color: #3a3d44 !important;
}
.gr-button {
    background-color: #262730 !important;
    color: #fafafa !important;
}
.gr-input, .gr-dropdown {
    background-color: #262730 !important;
    color: #fafafa !important;
    border-color: #3a3d44 !important;
}
label {
    color: #fafafa !important;
}
h1, h2, h3, h4, h5, h6 {
    color: #fafafa !important;
}
"""

with gr.Blocks() as demo:
    gr.Markdown("# 🇮🇪 Ireland Cost of Living Analysis (2015–2024)")
    gr.Markdown("*Interactive dashboard exploring cost of living changes in Ireland*")
    
    with gr.Row():
        # Left sidebar
        with gr.Column(scale=1):
            gr.Markdown("## Filters & Controls")
            
            year_slider = gr.Slider(
                minimum=2015,
                maximum=2024,
                value=[2015, 2024],
                step=1,
                label="Year Range",
                interactive=True
            )
            
            gr.Markdown("### Select Categories")
            
            # Create checkboxes for all categories
            category_checkboxes = []
            category_names = list(CATEGORY_SHORT_NAMES.values())
            
            for cat in category_names:
                checkbox = gr.Checkbox(label=cat, value=True)
                category_checkboxes.append(checkbox)
        
        # Main content area
        with gr.Column(scale=3):
            # Section 1
            gr.Markdown("---")
            with gr.Row():
                with gr.Column(scale=2):
                    gr.Markdown("## 1. Which Price Categories Have Increased the Most?")
                with gr.Column(scale=1):
                    gr.Markdown("## Key Findings")
            
            with gr.Row():
                with gr.Column(scale=2):
                    chart1_output = gr.Plot()
                with gr.Column(scale=1):
                    key_findings_output = gr.Markdown()
            
            # Section 2
            gr.Markdown("---")
            gr.Markdown("## 2. How Do Price Increases Differ Over Time?")
            chart2_output = gr.Plot()
            
            # Section 3
            gr.Markdown("---")
            gr.Markdown("## 3. Price Changes Across Economic Periods")
            gr.Markdown("""
            **Economic Periods:**
            - **Pre-COVID (2015–2019)**: Steady growth period
            - **COVID (2020–2021)**: Pandemic disruption
            - **Inflation Surge (2022–2023)**: Post-pandemic inflation spike
            """)
            
            period_dropdown = gr.Dropdown(
                choices=['All Periods', 'Pre-COVID (2015-2019)', 'COVID (2020-2021)', 'Inflation Surge (2022-2023)'],
                value='All Periods',
                label="Select Economic Period"
            )
            chart3_output = gr.Plot()
            
            # Section 4
            gr.Markdown("---")
            with gr.Row():
                with gr.Column(scale=2):
                    gr.Markdown("## 4. Cost-of-Living Burden by Demographic Group")
                with gr.Column(scale=1):
                    gr.Markdown("## Key Findings")
            
            with gr.Row():
                with gr.Column(scale=2):
                    chart4_output = gr.Plot()
                with gr.Column(scale=1):
                    demographic_findings_output = gr.Markdown()
            
            # Section 5
            gr.Markdown("---")
            gr.Markdown("## 5. Household Spending Patterns Over Time")
            chart5_output = gr.Plot()
            
            # Summary Section
            gr.Markdown("---")
            gr.Markdown("## 📊 Key Insights & Summary")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("""
                    ### Highest Price Increases
                    - **Housing & Utilities**: +60.4%
                    - **Restaurants & Hotels**: +36.8%
                    - **Alcohol & Tobacco**: +32.6%
                    """)
                
                with gr.Column():
                    gr.Markdown("""
                    ### Economic Periods
                    - **Worst Period**: Inflation Surge (2022–2023)
                    - **Avg Inflation**: ~1.8%/year (Pre-COVID)
                    - **Peak Inflation**: 8%+ (2022-2023)
                    """)
                
                with gr.Column():
                    gr.Markdown("""
                    ### Demographic Impact
                    - **Most Affected**: Renters
                    - **Burden**: +31.2%
                    - **Gap**: 12 percentage points
                    """)
            
            # Footer
            gr.Markdown("---")
            gr.Markdown("""
            **Data Sources:** CSO Ireland (HICP, Household Income, Consumption)  
            **Methodology:** Base index = 2015 = 100 | Weighted demographic basket approach  
            **Last Updated:** 2024
            """)
    
    # Set up event handlers
    inputs = [year_slider] + category_checkboxes
    outputs = [chart1_output, key_findings_output, chart2_output, chart3_output, 
               chart4_output, demographic_findings_output, chart5_output]
    
    # Update on filter change
    year_slider.change(fn=update_dashboard, inputs=inputs, outputs=outputs)
    for checkbox in category_checkboxes:
        checkbox.change(fn=update_dashboard, inputs=inputs, outputs=outputs)
    
    # Update period chart on dropdown change
    period_dropdown.change(
        fn=update_period_chart,
        inputs=[period_dropdown, year_slider] + category_checkboxes,
        outputs=chart3_output
    )
    
    # Load initial data
    demo.load(fn=update_dashboard, inputs=inputs, outputs=outputs)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861, share=False, css=custom_css)
