# Getting Started with HealthPipe

Welcome to HealthPipe! This guide will help you get up and running with healthcare data quality assessment in minutes.

## 📋 Prerequisites

- Python 3.8 or higher
- 8GB RAM (16GB recommended for large datasets)
- Apache Spark 3.5+ (optional, for distributed processing)

## 🚀 Installation

### Quick Install

```bash
pip install healthpipe
```

### Development Install

```bash
git clone https://github.com/praveenpolisetty/healthpipe.git
cd healthpipe
pip install -e ".[dev]"
```

## 🏃 Quick Start

### 1. Basic Quality Assessment

```python
from healthpipe import QualityAssessor

# Initialize the assessor
assessor = QualityAssessor()

# Assess a FHIR bundle
results = assessor.assess_fhir_bundle("path/to/fhir_bundle.json")

# View the summary
print(f"Overall Quality Score: {results['composite_score']:.2%}")
```

### 2. Assess CSV Data

```python
import pandas as pd
from healthpipe import QualityAssessor

# Load your healthcare data
df = pd.read_csv("patient_data.csv")

# Run assessment
assessor = QualityAssessor()
results = assessor.assess_dataframe(df)

# Check specific dimensions
print(f"Completeness: {results['completeness']['score']:.2%}")
print(f"Consistency: {results['consistency']['score']:.2%}")
```

### 3. Real-time Monitoring

```python
from healthpipe import StreamingMonitor

# Monitor a Kafka stream
monitor = StreamingMonitor(alert_threshold=0.75)
monitor.watch_kafka_topic("patient-admissions")
```

## 🏥 Understanding Quality Dimensions

HealthPipe assesses six key dimensions:

### Completeness (20% weight)
- Are all required fields populated?
- Do we have enough data for analysis?

### Consistency (20% weight)
- Do related fields agree with each other?
- Is the data internally consistent?

### Accuracy (15% weight)
- Are values within clinical ranges?
- Do codes match standard terminologies?

### Timeliness (15% weight)
- Is the data current?
- Are timestamps in logical order?

### Validity (20% weight)
- Does data conform to schema?
- Are values clinically plausible?

### Uniqueness (10% weight)
- Are patient records properly deduplicated?
- Are there duplicate measurements?

## 📊 Working with Different Data Sources

### FHIR Resources

```python
# Single resource
patient_data = {
    "resourceType": "Patient",
    "id": "123",
    "name": [{"given": ["John"], "family": "Doe"}],
    "gender": "male",
    "birthDate": "1980-01-01"
}

# Assess quality
results = assessor.assess([patient_data])
```

### HL7 Messages

```python
# Coming soon in v0.2.0
from healthpipe.parsers import HL7Parser

parser = HL7Parser()
messages = parser.parse_file("hl7_messages.txt")
results = assessor.assess_hl7(messages)
```

### Direct Database Connection

```python
from healthpipe import MultiSystemAssessor

assessor = MultiSystemAssessor()

# Add Epic connection
assessor.add_source("epic", {
    "type": "postgresql",
    "host": "epic-db.hospital.org",
    "database": "ehr_prod"
})

# Add Cerner connection
assessor.add_source("cerner", {
    "type": "oracle",
    "host": "cerner-db.hospital.org",
    "service": "CERNER_PRD"
})

# Run cross-system assessment
results = assessor.run_assessment()
```

## 🎯 Common Use Cases

### Pre-AI Model Training

```python
from healthpipe import AIReadinessChecker

checker = AIReadinessChecker()
score = checker.assess_dataset("training_data.parquet")

if score < 0.8:
    print("⚠️ Data quality too low for reliable model training")
    print("Run data cleaning pipeline before proceeding")
else:
    print("✅ Data ready for AI model training")
```

### Regulatory Compliance Check

```python
# Check for required fields for meaningful use
compliance_config = {
    "required_fields": [
        "patient.identifier",
        "patient.name",
        "patient.gender",
        "patient.birthDate",
        "encounter.period",
        "diagnosis.code"
    ]
}

results = assessor.assess_dataframe(df, schema_config=compliance_config)
```

## 🛠️ Configuration

### Custom Validation Rules

```python
# Add custom clinical rules
custom_rules = {
    "blood_pressure": {
        "systolic": {"min": 70, "max": 190},
        "diastolic": {"min": 40, "max": 120}
    },
    "heart_rate": {"min": 40, "max": 200}
}

assessor = QualityAssessor(clinical_rules=custom_rules)
```

### Spark Configuration

```python
from pyspark.sql import SparkSession

# Custom Spark session
spark = SparkSession.builder \
    .appName("HealthPipe-Hospital") \
    .config("spark.executor.memory", "4g") \
    .config("spark.executor.cores", "4") \
    .getOrCreate()

assessor = QualityAssessor(spark_session=spark)
```

## 📈 Next Steps

1. **Explore Examples**: Check out the `/examples` directory
2. **Read API Docs**: Detailed [API Reference](api_reference.md)
3. **Clinical Rules**: Learn about [Clinical Validation](clinical_rules.md)
4. **Architecture**: Understand the [System Architecture](architecture.md)

## 🆘 Need Help?

- 📖 [Full Documentation](https://github.com/praveenpolisetty/healthpipe/docs)
- 💬 [Discussions](https://github.com/praveenpolisetty/healthpipe/discussions)
- 🐛 [Report Issues](https://github.com/praveenpolisetty/healthpipe/issues)

Happy assessing! 🏥✨