"""
Real-time Data Quality Dashboard for HealthPipe.

This module provides a web-based dashboard for monitoring healthcare
data quality metrics in real-time using Plotly Dash.
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__, title="HealthPipe Dashboard")

# Sample data generator (replace with real data connection)
def generate_sample_metrics():
    """Generate sample quality metrics for demonstration."""
    timestamps = pd.date_range(
        start=datetime.now() - timedelta(hours=24),
        end=datetime.now(),
        freq='H'
    )
    
    data = {
        'timestamp': timestamps,
        'completeness': np.random.normal(0.85, 0.05, len(timestamps)),
        'consistency': np.random.normal(0.82, 0.06, len(timestamps)),
        'accuracy': np.random.normal(0.88, 0.04, len(timestamps)),
        'timeliness': np.random.normal(0.84, 0.05, len(timestamps)),
        'validity': np.random.normal(0.86, 0.03, len(timestamps)),
        'uniqueness': np.random.normal(0.92, 0.02, len(timestamps))
    }
    
    df = pd.DataFrame(data)
    # Ensure scores are between 0 and 1
    for col in ['completeness', 'consistency', 'accuracy', 'timeliness', 'validity', 'uniqueness']:
        df[col] = df[col].clip(0, 1)
    
    return df

# Define the layout
app.layout = html.Div([
    html.Div([
        html.H1("HealthPipe Data Quality Dashboard", className="header-title"),
        html.P("Real-time monitoring of healthcare data quality metrics", className="header-subtitle")
    ], className="header"),
    
    # Summary Cards
    html.Div([
        html.Div([
            html.H3("Overall Quality Score"),
            html.H1(id="overall-score", children="--"),
            html.P("Last 24 hours average")
        ], className="metric-card"),
        
        html.Div([
            html.H3("Records Processed"),
            html.H1(id="records-processed", children="--"),
            html.P("Last 24 hours")
        ], className="metric-card"),
        
        html.Div([
            html.H3("Quality Alerts"),
            html.H1(id="quality-alerts", children="--"),
            html.P("Active issues")
        ], className="metric-card"),
        
        html.Div([
            html.H3("AI Ready Score"),
            html.H1(id="ai-ready-score", children="--"),
            html.P("Current assessment")
        ], className="metric-card"),
    ], className="metrics-container"),
    
    # Main Charts
    html.Div([
        # Time series chart
        html.Div([
            html.H3("Quality Metrics Over Time"),
            dcc.Graph(id="time-series-chart")
        ], className="chart-container"),
        
        # Radar chart for current scores
        html.Div([
            html.H3("Current Quality Dimensions"),
            dcc.Graph(id="radar-chart")
        ], className="chart-container"),
    ], className="charts-row"),
    
    # Data source breakdown
    html.Div([
        html.Div([
            html.H3("Quality by Data Source"),
            dcc.Graph(id="source-breakdown-chart")
        ], className="chart-container"),
        
        html.Div([
            html.H3("Recent Quality Issues"),
            html.Div(id="issues-table", className="issues-list")
        ], className="chart-container"),
    ], className="charts-row"),
    
    # Auto-refresh
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # Update every 5 seconds
        n_intervals=0
    )
])

# Callbacks for updating charts
@app.callback(
    Output('overall-score', 'children'),
    Output('records-processed', 'children'),
    Output('quality-alerts', 'children'),
    Output('ai-ready-score', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_metrics(n):
    """Update summary metrics."""
    df = generate_sample_metrics()
    
    # Calculate overall score
    quality_cols = ['completeness', 'consistency', 'accuracy', 'timeliness', 'validity', 'uniqueness']
    overall_score = df[quality_cols].mean().mean()
    
    # Simulate other metrics
    records = np.random.randint(80000, 120000)
    alerts = np.random.randint(0, 5)
    ai_ready = 0.85 if overall_score > 0.8 else 0.65
    
    return (
        f"{overall_score:.1%}",
        f"{records:,}",
        str(alerts),
        f"{ai_ready:.1%}"
    )

@app.callback(
    Output('time-series-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_time_series(n):
    """Update time series chart."""
    df = generate_sample_metrics()
    
    fig = go.Figure()
    
    quality_cols = ['completeness', 'consistency', 'accuracy', 'timeliness', 'validity', 'uniqueness']
    colors = px.colors.qualitative.Set2
    
    for i, col in enumerate(quality_cols):
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df[col],
            mode='lines',
            name=col.capitalize(),
            line=dict(color=colors[i], width=2)
        ))
    
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Quality Score",
        yaxis=dict(tickformat='.0%', range=[0, 1]),
        hovermode='x unified',
        showlegend=True,
        height=400
    )
    
    return fig

@app.callback(
    Output('radar-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_radar_chart(n):
    """Update radar chart with current quality dimensions."""
    df = generate_sample_metrics()
    
    # Get latest scores
    latest_scores = df.iloc[-1]
    
    categories = ['Completeness', 'Consistency', 'Accuracy', 
                  'Timeliness', 'Validity', 'Uniqueness']
    values = [
        latest_scores['completeness'],
        latest_scores['consistency'],
        latest_scores['accuracy'],
        latest_scores['timeliness'],
        latest_scores['validity'],
        latest_scores['uniqueness']
    ]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current Quality'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickformat='.0%'
            )),
        showlegend=False,
        height=400
    )
    
    return fig

@app.callback(
    Output('source-breakdown-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_source_breakdown(n):
    """Update data source quality breakdown."""
    sources = ['Epic EHR', 'Cerner', 'Custom System', 'HL7 Feed', 'FHIR API']
    scores = [0.88, 0.82, 0.75, 0.91, 0.94]
    
    fig = go.Figure(data=[
        go.Bar(x=sources, y=scores, marker_color='lightblue')
    ])
    
    fig.update_layout(
        xaxis_title="Data Source",
        yaxis_title="Quality Score",
        yaxis=dict(tickformat='.0%', range=[0, 1]),
        height=400
    )
    
    return fig

@app.callback(
    Output('issues-table', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_issues_table(n):
    """Update recent issues list."""
    issues = [
        {"time": "2 min ago", "issue": "Missing patient birthdate", "source": "Epic", "severity": "Medium"},
        {"time": "5 min ago", "issue": "Duplicate records detected", "source": "Cerner", "severity": "Low"},
        {"time": "12 min ago", "issue": "Invalid diagnosis code", "source": "HL7", "severity": "High"},
        {"time": "18 min ago", "issue": "Temporal inconsistency", "source": "Custom", "severity": "Medium"},
    ]
    
    issue_elements = []
    for issue in issues[:4]:  # Show only recent 4
        severity_class = f"severity-{issue['severity'].lower()}"
        issue_elements.append(
            html.Div([
                html.Span(issue['time'], className="issue-time"),
                html.Span(issue['issue'], className="issue-text"),
                html.Span(issue['source'], className="issue-source"),
                html.Span(issue['severity'], className=f"issue-severity {severity_class}")
            ], className="issue-row")
        )
    
    return issue_elements

# Add CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f7fa;
            }
            .header {
                background-color: #2c3e50;
                color: white;
                padding: 20px;
                text-align: center;
            }
            .header-title {
                margin: 0;
                font-size: 2.5em;
            }
            .header-subtitle {
                margin: 5px 0 0 0;
                font-size: 1.2em;
                opacity: 0.8;
            }
            .metrics-container {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                padding: 20px;
            }
            .metric-card {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }
            .metric-card h3 {
                margin: 0;
                color: #666;
                font-size: 0.9em;
            }
            .metric-card h1 {
                margin: 10px 0;
                color: #2c3e50;
                font-size: 2.5em;
            }
            .metric-card p {
                margin: 0;
                color: #999;
                font-size: 0.8em;
            }
            .charts-row {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                padding: 0 20px 20px;
            }
            .chart-container {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .chart-container h3 {
                margin: 0 0 20px 0;
                color: #2c3e50;
            }
            .issue-row {
                display: grid;
                grid-template-columns: 80px 1fr 100px 80px;
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            .issue-time {
                color: #999;
                font-size: 0.9em;
            }
            .issue-severity {
                text-align: center;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 0.8em;
            }
            .severity-high {
                background: #fee;
                color: #c00;
            }
            .severity-medium {
                background: #fff4e6;
                color: #f57c00;
            }
            .severity-low {
                background: #e8f5e9;
                color: #4caf50;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, port=8050)