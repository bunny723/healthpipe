# HealthPipe Dashboard Guide

## Overview

The HealthPipe Dashboard provides real-time visualization of healthcare data quality metrics across six key dimensions.

## Running the Dashboard

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (if not already installed)
pip install dash plotly

# Run the dashboard
python src/healthpipe/dashboard/app.py

# Open your browser to http://localhost:8050
```

## Dashboard Features

### 1. **Summary Metrics Cards**
- **Overall Quality Score**: Composite score across all dimensions
- **Records Processed**: Total records analyzed in last 24 hours
- **Quality Alerts**: Active data quality issues requiring attention
- **AI Ready Score**: Assessment of data readiness for AI/ML models

### 2. **Quality Metrics Over Time**
Real-time line chart showing trends for:
- Completeness
- Consistency
- Accuracy
- Timeliness
- Validity
- Uniqueness

### 3. **Current Quality Radar Chart**
Visual representation of current quality scores across all six dimensions, making it easy to identify weak areas.

### 4. **Quality by Data Source**
Bar chart showing quality scores broken down by data source (Epic, Cerner, Custom Systems, etc.)

### 5. **Recent Quality Issues**
Live feed of detected quality issues with:
- Timestamp
- Issue description
- Source system
- Severity level (High/Medium/Low)

## Configuration

The dashboard refreshes every 5 seconds by default. To change this, modify the `interval` parameter in `app.py`:

```python
dcc.Interval(
    id='interval-component',
    interval=5*1000,  # milliseconds
    n_intervals=0
)
```

## Customization

To connect to your real data sources, modify the `generate_sample_metrics()` function to query your actual quality assessment results.

## Performance

The dashboard is designed to handle:
- Updates every second without performance degradation
- Up to 100 concurrent users
- Datasets with millions of quality metrics

## Troubleshooting

**Dashboard not loading?**
- Ensure port 8050 is not in use
- Check that all dependencies are installed
- Verify Python 3.8+ is being used

**Data not updating?**
- Check the browser console for errors
- Ensure the interval component is enabled
- Verify data source connections

## Future Enhancements

- Export functionality for reports
- Historical data comparison
- Drill-down capabilities
- Email alerts integration
- Mobile app support