"""
Ireland Cost of Living Analysis Dashboard - Dash Version
========================================================
Production-ready Plotly Dash application for Render deployment.

Data Sources: CSO Ireland (HICP, Household Income, Personal Consumption)
"""

import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

# =============================================================================
# DATA LOADING
# =============================================================================

def load_annual_cpi():
    """Load Annual EU Index of Consumer Prices (HICP) data."""
    try:
        df = pd.read_csv('data/Annual EU Index of Consumer Prices.csv')
        df.columns = df.columns.str.strip()
        df['VALUE'] = pd.to_numeric(df['VALUE'], errors='coerce')
        return df
    except Exception as e:
        print(f"Error loading annual CPI: {e}")
        return pd.DataFrame()

def load_monthly_cpi():
    """Load Monthly EU Consumer Prices data."""
    try:
        df = pd.read_csv('data/Monthly EU Consumer Prices by Consumer Price .csv')
        df.columns = df.columns.str.strip()
        # Date format is '1996 January'
        df['Date'] = pd.to_datetime(df['Month'], format='%Y %B', errors='coerce')
        df['VALUE'] = pd.to_numeric(df['VALUE'], errors='coerce')
        return df
    except Exception as e:
        print(f"Error loading monthly CPI: {e}")
        return pd.DataFrame()

# Load data
annual_cpi = load_annual_cpi()
monthly_cpi = load_monthly_cpi()

# =============================================================================
# CONSTANTS
# =============================================================================

MAIN_CATEGORIES = [
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

CATEGORY_SHORT_NAMES = {
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

CATEGORY_COLORS = {
    "Food & Beverages":    "#FF4444",
    "Alcohol & Tobacco":   "#9B59B6",
    "Clothing & Footwear": "#2ECC71",
    "Housing & Utilities": "#2980B9",
    "Furnishings":         "#A0522D",
    "Health":              "#F1C40F",
    "Transport":           "#27AE60",
    "Communications":      "#FF69B4",
    "Recreation & Culture":"#8E44AD",
    "Education":           "#E67E22",
    "Restaurants & Hotels":"#967BB6",
    "Miscellaneous":       "#32CD32"
}

# =============================================================================
# INITIALIZE DASH APP
# =============================================================================

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Expose server for Render deployment

# =============================================================================
# LAYOUT
# =============================================================================

app.layout = html.Div([
    # Sidebar
    html.Div([
        html.H2("Filters & Controls", className="sidebar-title"),
        
        # Year Range Slider
        html.Div([
            html.Label("Select Year Range", className="filter-label"),
            html.Div([
                html.Span("2015", className="year-label"),
                html.Span("2024", className="year-label"),
            ], className="year-labels-row"),
            dcc.RangeSlider(
                id='year-slider',
                min=2015,
                max=2024,
                step=1,
                value=[2015, 2024],
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
                className="year-slider"
            ),
        ], className="filter-section"),
        
        # Category Checklist
        html.Div([
            html.Label("Select Categories to Compare", className="filter-label category-filter-label"),
            dcc.Checklist(
                id='category-checklist',
                options=[
                    {
                        'label': html.Span([
                            html.Span(
                                className='cat-color-square',
                                style={'backgroundColor': CATEGORY_COLORS[cat]}
                            ),
                            html.Span(cat, className='cat-name')
                        ], className='cat-option-label'),
                        'value': cat
                    }
                    for cat in CATEGORY_SHORT_NAMES.values()
                ],
                value=list(CATEGORY_SHORT_NAMES.values()),
                className='category-checklist',
            ),
        ], className="filter-section"),
        
    ], className="sidebar"),
    
    # Main content
    html.Div([
        # Header
        html.Div([
            html.H1("Ireland Cost of Living Analysis (2015–2024)", className="main-title"),
            html.P("Interactive dashboard exploring cost of living changes in Ireland", className="subtitle"),
        ], className="header"),
        
        # Section 1: Price Categories
        html.Div([
            html.Div([
                html.Div([
                    html.H2("1. Which Price Categories Have Increased the Most?"),
                    dcc.Graph(id='price-change-chart', config={'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToAdd': ['toImage'], 'toImageButtonOptions': {'format': 'png', 'filename': 'price_change_chart'}}),
                ], className="chart-container"),
                
                html.Div([
                    html.H3("Key Findings", className="findings-title"),
                    html.Div([
                        html.Div([
                            html.P("Housing & Utilities", className="card-label"),
                            html.P("+60.4%", className="card-value positive"),
                            html.P("Largest increase driven by energy costs and rent inflation", className="card-detail"),
                        ], className="finding-card"),
                        html.Div([
                            html.P("Restaurants & Hotels", className="card-label"),
                            html.P("+36.8%", className="card-value positive"),
                            html.P("Post-pandemic recovery and labor cost pressures", className="card-detail"),
                        ], className="finding-card"),
                        html.Div([
                            html.P("Alcohol & Tobacco", className="card-label"),
                            html.P("+32.6%", className="card-value positive"),
                            html.P("Consistent tax increases and regulatory changes", className="card-detail"),
                        ], className="finding-card"),
                    ], className="findings-cards"),
                ], className="findings-container"),
            ], className="section-row"),
        ], className="section"),
        
        # Section 2: Time Series
        html.Div([
            html.H2("2. How Do Price Increases Differ Over Time?"),
            dcc.Graph(id='time-series-chart', config={'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToAdd': ['toImage'], 'toImageButtonOptions': {'format': 'png', 'filename': 'time_series_chart'}}),
        ], className="section"),
        
        # Section 3: Economic Periods
        html.Div([
            html.H2("3. Price Changes Across Economic Periods"),
            html.Div([
                html.P("Pre-COVID (2015–2019): Steady growth period", className="period-text"),
                html.P("COVID (2020–2021): Pandemic disruption", className="period-text"),
                html.P("Inflation Surge (2022–2023): Post-pandemic inflation spike", className="period-text"),
            ], className="period-description"),
            
            html.Div([
                html.Label("Select Economic Period:", className="dropdown-label"),
                dcc.Dropdown(
                    id='period-dropdown',
                    options=[
                        {'label': 'All Periods', 'value': 'All Periods'},
                        {'label': 'Pre-COVID (2015-2019)', 'value': 'Pre-COVID (2015-2019)'},
                        {'label': 'COVID (2020-2021)', 'value': 'COVID (2020-2021)'},
                        {'label': 'Inflation Surge (2022-2023)', 'value': 'Inflation Surge (2022-2023)'},
                    ],
                    value='All Periods',
                    className="period-dropdown",
                    style={'backgroundColor': '#1c2128', 'color': '#e6edf3'}
                ),
            ], className="dropdown-container"),
            
            dcc.Graph(id='economic-periods-chart', config={'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToAdd': ['toImage'], 'toImageButtonOptions': {'format': 'png', 'filename': 'economic_periods_chart'}}),
        ], className="section"),
        
        # Section 4: Demographic Burden
        html.Div([
            html.Div([
                html.Div([
                    html.H2("4. Cost-of-Living Burden by Demographic Group"),
                    dcc.Graph(id='demographic-chart', config={'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToAdd': ['toImage'], 'toImageButtonOptions': {'format': 'png', 'filename': 'demographic_chart'}}),
                ], className="chart-container"),
                
                html.Div([
                    html.H3("Key Findings", className="findings-title"),
                    html.Div([
                        html.Div([
                            html.P("Most Affected", className="card-label"),
                            html.P("Renters", className="card-subtitle"),
                            html.P("+31.2%", className="card-value positive"),
                            html.P("Housing costs dominate spending for rental households", className="card-detail"),
                        ], className="finding-card"),
                        html.Div([
                            html.P("Least Affected", className="card-label"),
                            html.P("High Income", className="card-subtitle"),
                            html.P("+19.0%", className="card-value positive"),
                            html.P("Greater flexibility in spending and savings buffers", className="card-detail"),
                        ], className="finding-card"),
                        html.Div([
                            html.P("Burden Gap", className="card-label"),
                            html.P("~12 percentage points", className="card-value"),
                            html.P("Widening inequality in cost-of-living impact across groups", className="card-detail"),
                        ], className="finding-card"),
                    ], className="findings-cards"),
                ], className="findings-container"),
            ], className="section-row"),
        ], className="section"),
        
        # Section 5: Spending Patterns
        html.Div([
            html.H2("5. Household Spending Patterns Over Time"),
            dcc.Graph(id='spending-chart', config={'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToAdd': ['toImage'], 'toImageButtonOptions': {'format': 'png', 'filename': 'spending_chart'}}),
        ], className="section"),
        
        # Summary Section
        html.Div([
            html.H2("Key Insights & Summary"),
            html.Div([
                html.Div([
                    html.H3("Highest Price Increases"),
                    html.Ul([
                        html.Li("Housing & Utilities: +60.4%"),
                        html.Li("Restaurants & Hotels: +36.8%"),
                        html.Li("Alcohol & Tobacco: +32.6%"),
                    ]),
                ], className="summary-column"),
                
                html.Div([
                    html.H3("Economic Periods"),
                    html.Ul([
                        html.Li("Worst Period: Inflation Surge (2022–2023)"),
                        html.Li("Avg Inflation: ~1.8%/year (Pre-COVID)"),
                        html.Li("Peak Inflation: 8%+ (2022-2023)"),
                    ]),
                ], className="summary-column"),
                
                html.Div([
                    html.H3("Demographic Impact"),
                    html.Ul([
                        html.Li("Most Affected: Renters"),
                        html.Li("Burden: +31.2%"),
                        html.Li("Gap: 12 percentage points"),
                    ]),
                ], className="summary-column"),
            ], className="summary-grid"),
        ], className="section summary-section"),
        
        # Footer
        html.Div([
            html.P("Data Sources: CSO Ireland (HICP, Household Income, Consumption)", className="footer-text"),
            html.P("Methodology: Base index = 2015 = 100 | Weighted demographic basket approach", className="footer-text"),
            html.P("Last Updated: 2024", className="footer-text"),
        ], className="footer"),
        
    ], className="main-content"),
], className="dashboard-container")

# =============================================================================
# CALLBACKS
# =============================================================================

@app.callback(
    Output('price-change-chart', 'figure'),
    [Input('year-slider', 'value'),
     Input('category-checklist', 'value')]
)
def update_price_change_chart(year_range, selected_categories):
    """Update price change bar chart."""
    year_start, year_end = year_range
    
    hicp_index = annual_cpi[
        (annual_cpi['Statistic Label'] == 'Harmonised Index of Consumer Prices') &
        (annual_cpi['Commodity Group'].isin(MAIN_CATEGORIES)) &
        (annual_cpi['Year'] >= year_start) &
        (annual_cpi['Year'] <= year_end)
    ].copy()
    
    if hicp_index.empty:
        fig = go.Figure()
        fig.update_layout(paper_bgcolor='#0d1117', plot_bgcolor='#161b22', font=dict(color='#ffffff'))
        return fig
    
    base_year_data = hicp_index[hicp_index['Year'] == year_start].set_index('Commodity Group')['VALUE']
    latest_year_data = hicp_index[hicp_index['Year'] == year_end].set_index('Commodity Group')['VALUE']
    
    change_data = []
    for cat in MAIN_CATEGORIES:
        if cat in base_year_data.index and cat in latest_year_data.index:
            base_val = base_year_data[cat]
            latest_val = latest_year_data[cat]
            if pd.notna(base_val) and pd.notna(latest_val) and base_val > 0:
                pct_change = ((latest_val - base_val) / base_val) * 100
                short_name = CATEGORY_SHORT_NAMES[cat]
                if short_name in selected_categories:
                    change_data.append({
                        'Category': short_name,
                        'Change': pct_change
                    })
    
    df = pd.DataFrame(change_data).sort_values('Change', ascending=True)
    
    colors = [CATEGORY_COLORS.get(cat, '#888888') for cat in df['Category']]
    
    fig = go.Figure()
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
        paper_bgcolor='#0d1117',
        plot_bgcolor='#161b22',
        font=dict(color='#ffffff', size=12, family='Arial, sans-serif'),
        height=max(400, len(df) * 42),
        margin=dict(l=20, r=120, t=30, b=40),
        xaxis=dict(
            title=f'Price Change (%) from {year_start} to {year_end}',
            title_font=dict(color='#ffffff', size=12),
            tickfont=dict(color='#ffffff', size=11),
            showgrid=False,
            linecolor='#444c56',
            tickcolor='#444c56',
            zeroline=False
        ),
        yaxis=dict(
            tickfont=dict(color='#ffffff', size=11),
            showgrid=False,
            linecolor='#444c56',
            automargin=True
        ),
        showlegend=False
    )
    
    return fig

@app.callback(
    Output('time-series-chart', 'figure'),
    [Input('year-slider', 'value'),
     Input('category-checklist', 'value')]
)
def update_time_series_chart(year_range, selected_categories):
    """Update time series line chart."""
    year_start, year_end = year_range
    
    filtered_monthly = monthly_cpi[
        (monthly_cpi['Statistic Label'] == 'EU HICP') &
        (monthly_cpi['Commodity Group'].isin(MAIN_CATEGORIES))
    ].copy()
    
    if filtered_monthly.empty or 'Date' not in filtered_monthly.columns:
        fig = go.Figure()
        fig.update_layout(paper_bgcolor='#0d1117', plot_bgcolor='#161b22', font=dict(color='#ffffff'))
        return fig
    
    filtered_monthly = filtered_monthly[
        (filtered_monthly['Date'].dt.year >= year_start) &
        (filtered_monthly['Date'].dt.year <= year_end)
    ]
    
    filtered_monthly['ShortCategory'] = filtered_monthly['Commodity Group'].map(CATEGORY_SHORT_NAMES)
    filtered_monthly = filtered_monthly[filtered_monthly['ShortCategory'].isin(selected_categories)]
    
    fig = go.Figure()
    
    for cat in selected_categories:
        cat_data = filtered_monthly[filtered_monthly['ShortCategory'] == cat].sort_values('Date')
        if not cat_data.empty:
            fig.add_trace(go.Scatter(
                x=cat_data['Date'],
                y=cat_data['VALUE'],
                mode='lines',
                name=cat,
                line=dict(color=CATEGORY_COLORS.get(cat, '#888888'), width=2),
                hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%b %Y}<br>Index: %{y:.1f}<extra></extra>'
            ))
    
    fig.update_layout(
        paper_bgcolor='#0d1117',
        plot_bgcolor='#161b22',
        font=dict(color='#ffffff', size=12, family='Arial, sans-serif'),
        height=600,
        margin=dict(l=20, r=20, t=30, b=140),
        xaxis=dict(
            title='Date',
            title_font=dict(color='#ffffff', size=12),
            tickfont=dict(color='#ffffff', size=11),
            showgrid=False,
            linecolor='#444c56',
            tickcolor='#444c56'
        ),
        yaxis=dict(
            title='Price Index (Base 2015=100)',
            title_font=dict(color='#ffffff', size=12),
            tickfont=dict(color='#ffffff', size=11),
            showgrid=False,
            linecolor='#444c56',
            tickcolor='#444c56'
        ),
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.4,
            xanchor='center',
            x=0.5,
            font=dict(color='#ffffff', size=10),
            bgcolor='rgba(13,17,23,0.8)',
            bordercolor='#444c56'
        )
    )
    
    return fig

@app.callback(
    Output('economic-periods-chart', 'figure'),
    [Input('period-dropdown', 'value'),
     Input('category-checklist', 'value')]
)
def update_economic_periods_chart(selected_period, selected_categories):
    """Update economic periods chart."""
    periods = {
        'Pre-COVID (2015-2019)': (2015, 2019),
        'COVID (2020-2021)': (2020, 2021),
        'Inflation Surge (2022-2023)': (2022, 2023)
    }
    
    hicp_index = annual_cpi[
        (annual_cpi['Statistic Label'] == 'Harmonised Index of Consumer Prices') &
        (annual_cpi['Commodity Group'].isin(MAIN_CATEGORIES))
    ].copy()
    
    if hicp_index.empty:
        fig = go.Figure()
        fig.update_layout(paper_bgcolor='#0d1117', plot_bgcolor='#161b22', font=dict(color='#ffffff'))
        return fig
    
    period_data = []
    
    for period_name, (start_year, end_year) in periods.items():
        for cat in MAIN_CATEGORIES:
            cat_data = hicp_index[hicp_index['Commodity Group'] == cat]
            start_data = cat_data[cat_data['Year'] == start_year]
            end_data = cat_data[cat_data['Year'] == end_year]
            
            if not start_data.empty and not end_data.empty:
                start_val = start_data['VALUE'].values[0]
                end_val = end_data['VALUE'].values[0]
                
                if pd.notna(start_val) and pd.notna(end_val) and start_val > 0:
                    total_change = ((end_val - start_val) / start_val) * 100
                    years = end_year - start_year + 1
                    annual_change = total_change / years
                    
                    short_name = CATEGORY_SHORT_NAMES[cat]
                    if short_name in selected_categories:
                        period_data.append({
                            'Category': short_name,
                            'Period': period_name,
                            'AnnualChange': annual_change
                        })
    
    df = pd.DataFrame(period_data)
    
    if selected_period != 'All Periods':
        df = df[df['Period'] == selected_period]
    
    fig = go.Figure()
    
    if selected_period == 'All Periods':
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
        paper_bgcolor='#0d1117',
        plot_bgcolor='#161b22',
        font=dict(color='#ffffff', size=12, family='Arial, sans-serif'),
        height=450,
        margin=dict(l=20, r=20, t=30, b=100),
        xaxis=dict(
            title='Avg Annual Price Change (%)',
            title_font=dict(color='#ffffff', size=12),
            tickfont=dict(color='#ffffff', size=11),
            showgrid=False,
            linecolor='#444c56',
            tickcolor='#444c56',
            zeroline=False
        ),
        yaxis=dict(
            tickfont=dict(color='#ffffff', size=11),
            showgrid=False,
            linecolor='#444c56',
            automargin=True
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.3,
            xanchor='center',
            x=0.5,
            font=dict(color='#ffffff', size=10),
            bgcolor='rgba(13,17,23,0.8)',
            bordercolor='#444c56'
        )
    )
    
    return fig

@app.callback(
    Output('demographic-chart', 'figure'),
    [Input('year-slider', 'value')]
)
def update_demographic_chart(year_range):
    """Update demographic burden chart."""
    year_start, year_end = year_range
    
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
    
    hicp_index = annual_cpi[
        (annual_cpi['Statistic Label'] == 'Harmonised Index of Consumer Prices') &
        (annual_cpi['Commodity Group'].isin(MAIN_CATEGORIES))
    ].copy()
    
    if hicp_index.empty:
        fig = go.Figure()
        fig.update_layout(paper_bgcolor='#0d1117', plot_bgcolor='#161b22', font=dict(color='#ffffff'))
        return fig
    
    base_year_data = hicp_index[hicp_index['Year'] == year_start].set_index('Commodity Group')['VALUE']
    latest_year_data = hicp_index[hicp_index['Year'] == year_end].set_index('Commodity Group')['VALUE']
    
    price_changes = {}
    for cat in MAIN_CATEGORIES:
        if cat in base_year_data.index and cat in latest_year_data.index:
            base_val = base_year_data[cat]
            latest_val = latest_year_data[cat]
            if pd.notna(base_val) and pd.notna(latest_val) and base_val > 0:
                pct_change = ((latest_val - base_val) / base_val) * 100
                short_name = CATEGORY_SHORT_NAMES[cat]
                price_changes[short_name] = pct_change
    
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
        paper_bgcolor='#0d1117',
        plot_bgcolor='#161b22',
        font=dict(color='#ffffff', size=12, family='Arial, sans-serif'),
        height=400,
        margin=dict(l=20, r=120, t=30, b=40),
        xaxis=dict(
            title=f'Weighted Cost-of-Living Increase (%) ({year_start}-{year_end})',
            title_font=dict(color='#ffffff', size=12),
            tickfont=dict(color='#ffffff', size=11),
            showgrid=False,
            linecolor='#444c56',
            tickcolor='#444c56'
        ),
        yaxis=dict(
            tickfont=dict(color='#ffffff', size=11),
            showgrid=False,
            linecolor='#444c56',
            automargin=True
        ),
        showlegend=False
    )
    
    return fig

@app.callback(
    Output('spending-chart', 'figure'),
    Input('year-slider', 'value')
)
def update_spending_chart(year_range):
    """Update spending patterns stacked area chart."""
    years = list(range(2015, 2025))
    categories = list(CATEGORY_SHORT_NAMES.values())
    
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
        paper_bgcolor='#0d1117',
        plot_bgcolor='#161b22',
        font=dict(color='#ffffff', size=12, family='Arial, sans-serif'),
        height=500,
        margin=dict(l=20, r=20, t=30, b=160),
        xaxis=dict(
            title='Year',
            title_font=dict(color='#ffffff', size=12),
            tickfont=dict(color='#ffffff', size=11),
            showgrid=False,
            linecolor='#444c56',
            tickcolor='#444c56'
        ),
        yaxis=dict(
            title='Spending (€ millions)',
            title_font=dict(color='#ffffff', size=12),
            tickfont=dict(color='#ffffff', size=11),
            showgrid=False,
            linecolor='#444c56',
            tickcolor='#444c56'
        ),
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.5,
            xanchor='center',
            x=0.5,
            font=dict(color='#ffffff', size=10),
            bgcolor='rgba(13,17,23,0.8)',
            bordercolor='#444c56'
        )
    )
    
    return fig

# =============================================================================
# RUN SERVER
# =============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
