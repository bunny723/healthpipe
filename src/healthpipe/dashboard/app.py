"""
Simple working dashboard for HealthPipe data quality monitoring.
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Generate sample data
def get_current_metrics():
    """Get current quality metrics."""
    return {
        'completeness': np.random.uniform(0.8, 0.95),
        'consistency': np.random.uniform(0.75, 0.9),
        'accuracy': np.random.uniform(0.85, 0.95),
        'timeliness': np.random.uniform(0.8, 0.92),
        'validity': np.random.uniform(0.82, 0.94),
        'uniqueness': np.random.uniform(0.9, 0.98)
    }

def generate_time_series():
    """Generate time series data."""
    hours = 24
    timestamps = pd.date_range(end=datetime.now(), periods=hours, freq='H')
    
    data = {
        'timestamp': timestamps,
        'completeness': np.random.normal(0.85, 0.03, hours).clip(0, 1),
        'consistency': np.random.normal(0.82, 0.04, hours).clip(0, 1),
        'accuracy': np.random.normal(0.88, 0.02, hours).clip(0, 1),
        'timeliness': np.random.normal(0.84, 0.03, hours).clip(0, 1),
        'validity': np.random.normal(0.86, 0.02, hours).clip(0, 1),
        'uniqueness': np.random.normal(0.92, 0.01, hours).clip(0, 1)
    }
    
    return pd.DataFrame(data)

# Layout
app.layout = html.Div([
    html.Div([
        html.H1("HealthPipe Data Quality Dashboard", style={'textAlign': 'center', 'color': '#2c3e50'}),
        html.Hr()
    ]),
    
    # Summary section
    html.Div([
        html.Div([
            html.H3("Overall Quality Score", style={'textAlign': 'center'}),
            html.H1(id='overall-score', style={'textAlign': 'center', 'color': '#27ae60'})
        ], style={'width': '24%', 'display': 'inline-block', 'backgroundColor': '#ecf0f1', 'margin': '0.5%', 'padding': '20px', 'borderRadius': '5px'}),
        
        html.Div([
            html.H3("Records Processed", style={'textAlign': 'center'}),
            html.H1(id='records-count', style={'textAlign': 'center', 'color': '#3498db'})
        ], style={'width': '24%', 'display': 'inline-block', 'backgroundColor': '#ecf0f1', 'margin': '0.5%', 'padding': '20px', 'borderRadius': '5px'}),
        
        html.Div([
            html.H3("Quality Alerts", style={'textAlign': 'center'}),
            html.H1(id='alerts-count', style={'textAlign': 'center', 'color': '#e74c3c'})
        ], style={'width': '24%', 'display': 'inline-block', 'backgroundColor': '#ecf0f1', 'margin': '0.5%', 'padding': '20px', 'borderRadius': '5px'}),
        
        html.Div([
            html.H3("AI Ready Score", style={'textAlign': 'center'}),
            html.H1(id='ai-score', style={'textAlign': 'center', 'color': '#9b59b6'})
        ], style={'width': '24%', 'display': 'inline-block', 'backgroundColor': '#ecf0f1', 'margin': '0.5%', 'padding': '20px', 'borderRadius': '5px'})
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    # Charts section
    html.Div([
        html.Div([
            dcc.Graph(id='time-series-chart')
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            dcc.Graph(id='radar-chart')
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    html.Div([
        html.Div([
            dcc.Graph(id='bar-chart')
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '10px'}),
        
        html.Div([
            html.H3("Recent Quality Issues", style={'textAlign': 'center'}),
            html.Div(id='issues-list', style={'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '5px', 'height': '300px', 'overflowY': 'scroll'})
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '10px'})
    ]),
    
    # Auto-refresh every 5 seconds
    dcc.Interval(
        id='interval-component',
        interval=5*1000,
        n_intervals=0
    )
])

# Callbacks
@app.callback(
    Output('overall-score', 'children'),
    Output('records-count', 'children'),
    Output('alerts-count', 'children'),
    Output('ai-score', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_summary_metrics(n):
    """Update summary metrics."""
    metrics = get_current_metrics()
    overall = np.mean(list(metrics.values()))
    records = np.random.randint(90000, 110000)
    alerts = np.random.randint(0, 5)
    ai_ready = 0.92 if overall > 0.85 else 0.73
    
    return f"{overall:.1%}", f"{records:,}", str(alerts), f"{ai_ready:.1%}"

@app.callback(
    Output('time-series-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_time_series(n):
    """Update time series chart."""
    df = generate_time_series()
    
    fig = go.Figure()
    
    for col in ['completeness', 'consistency', 'accuracy', 'timeliness', 'validity', 'uniqueness']:
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df[col],
            mode='lines',
            name=col.capitalize()
        ))
    
    fig.update_layout(
        title="Quality Metrics Over Time (24 Hours)",
        xaxis_title="Time",
        yaxis_title="Quality Score",
        yaxis=dict(tickformat='.0%', range=[0.6, 1]),
        hovermode='x unified'
    )
    
    return fig

@app.callback(
    Output('radar-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_radar(n):
    """Update radar chart."""
    metrics = get_current_metrics()
    
    fig = go.Figure(data=go.Scatterpolar(
        r=list(metrics.values()),
        theta=[k.capitalize() for k in metrics.keys()],
        fill='toself',
        name='Current Quality'
    ))
    
    fig.update_layout(
        title="Current Quality Dimensions",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickformat='.0%'
            )
        ),
        showlegend=False
    )
    
    return fig

@app.callback(
    Output('bar-chart', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_bar(n):
    """Update bar chart."""
    sources = ['Epic EHR', 'Cerner', 'HL7 Feed', 'FHIR API', 'Custom']
    scores = [
        np.random.uniform(0.8, 0.95),
        np.random.uniform(0.75, 0.9),
        np.random.uniform(0.85, 0.95),
        np.random.uniform(0.9, 0.98),
        np.random.uniform(0.7, 0.85)
    ]
    
    fig = go.Figure(data=[go.Bar(x=sources, y=scores)])
    
    fig.update_layout(
        title="Quality by Data Source",
        xaxis_title="Data Source",
        yaxis_title="Quality Score",
        yaxis=dict(tickformat='.0%', range=[0, 1])
    )
    
    for i, (source, score) in enumerate(zip(sources, scores)):
        color = '#27ae60' if score > 0.85 else '#e74c3c' if score < 0.75 else '#f39c12'
        fig.data[0].marker.color = [color if j == i else '#3498db' for j in range(len(sources))]
    
    return fig

@app.callback(
    Output('issues-list', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_issues(n):
    """Update issues list."""
    issues = [
        {"time": "2 min ago", "issue": "Missing patient birthdate in Epic", "severity": "Medium"},
        {"time": "5 min ago", "issue": "Duplicate records detected in Cerner", "severity": "Low"},
        {"time": "8 min ago", "issue": "Invalid diagnosis code format", "severity": "High"},
        {"time": "12 min ago", "issue": "Temporal inconsistency in lab results", "severity": "Medium"},
        {"time": "18 min ago", "issue": "Incomplete medication records", "severity": "Low"}
    ]
    
    issue_elements = []
    for issue in issues:
        color = '#e74c3c' if issue['severity'] == 'High' else '#f39c12' if issue['severity'] == 'Medium' else '#27ae60'
        issue_elements.append(
            html.Div([
                html.Span(issue['time'], style={'color': '#7f8c8d', 'marginRight': '10px'}),
                html.Span(issue['issue'], style={'marginRight': '10px'}),
                html.Span(issue['severity'], style={
                    'backgroundColor': color, 
                    'color': 'white', 
                    'padding': '2px 8px', 
                    'borderRadius': '3px',
                    'fontSize': '12px'
                })
            ], style={'marginBottom': '10px', 'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '5px'})
        )
    
    return issue_elements

if __name__ == '__main__':
    print("Starting HealthPipe Dashboard on http://localhost:8050")
    app.run(debug=True, port=8050)