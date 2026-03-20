"""
Comprehensive demo of HealthPipe capabilities for healthcare data quality assessment.

This demo shows real-world scenarios for using HealthPipe to prepare
clinical data for AI/ML applications.
"""

import json
import pandas as pd
from datetime import datetime, timedelta
import random
from healthpipe import QualityAssessor, AIReadinessChecker

# Generate synthetic patient data that mimics real healthcare data challenges
def generate_synthetic_ehr_data(num_patients=100):
    """Generate synthetic EHR data with realistic quality issues."""
    
    patients = []
    observations = []
    
    for i in range(num_patients):
        # Create patient with some missing data (mimics real-world incompleteness)
        patient = {
            "resourceType": "Patient",
            "id": f"patient-{i}",
            "identifier": [{"system": "http://hospital.org", "value": f"MRN{i:06d}"}],
            "name": [{"family": f"Test{i}", "given": [f"Patient{i}"]}],
            "gender": random.choice(["male", "female", "other"]),
        }
        
        # Simulate missing birthDate in 15% of records
        if random.random() > 0.15:
            patient["birthDate"] = f"{random.randint(1940, 2020)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        
        patients.append(patient)
        
        # Generate observations with various quality issues
        num_obs = random.randint(0, 10)
        for j in range(num_obs):
            obs_date = datetime.now() - timedelta(days=random.randint(0, 365))
            
            observation = {
                "resourceType": "Observation",
                "id": f"obs-{i}-{j}",
                "status": "final",
                "code": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": random.choice(["29463-7", "8302-2", "8867-4", "2708-6"]),
                        "display": random.choice(["Body weight", "Body height", "Heart rate", "Oxygen saturation"])
                    }]
                },
                "subject": {"reference": f"Patient/patient-{i}"},
                "effectiveDateTime": obs_date.isoformat()
            }
            
            # Simulate missing values in 10% of observations
            if random.random() > 0.10:
                observation["valueQuantity"] = {
                    "value": round(random.uniform(50, 200), 1),
                    "unit": random.choice(["kg", "cm", "/min", "%"])
                }
            
            observations.append(observation)
    
    return {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": [{"resource": p} for p in patients] + [{"resource": o} for o in observations]
    }


def demonstrate_quality_assessment():
    """Demonstrate comprehensive quality assessment workflow."""
    
    print("=" * 80)
    print("HealthPipe - Healthcare Data Quality Assessment Demo")
    print("=" * 80)
    
    # Generate synthetic data
    print("\n1. Generating synthetic EHR data with realistic quality issues...")
    ehr_data = generate_synthetic_ehr_data(num_patients=50)
    print(f"   ✓ Generated {len(ehr_data['entry'])} resources")
    
    # Save to file
    with open("synthetic_ehr_bundle.json", "w") as f:
        json.dump(ehr_data, f, indent=2)
    
    # Initialize assessor
    print("\n2. Initializing HealthPipe Quality Assessor...")
    assessor = QualityAssessor()
    print("   ✓ Assessor ready")
    
    # Run comprehensive assessment
    print("\n3. Running comprehensive quality assessment...")
    results = assessor.assess_fhir_bundle("synthetic_ehr_bundle.json", output_format="detailed")
    
    # Display overall results
    print("\n4. Quality Assessment Results:")
    print("-" * 80)
    print(f"\n   📊 Composite Quality Score: {results['composite_score']:.1%}")
    
    # Display dimension scores
    print("\n   Dimension Scores:")
    dimensions = ["completeness", "consistency", "accuracy", "timeliness", "validity", "uniqueness"]
    for dim in dimensions:
        score = results.get(dim, {}).get('score', 0)
        print(f"   • {dim.capitalize():<15} {score:.1%}")
    
    # Show specific issues
    print("\n5. Identified Quality Issues:")
    print("-" * 80)
    
    # Completeness issues
    completeness_issues = results.get('completeness', {}).get('issues', [])[:3]
    if completeness_issues:
        print("\n   Completeness Issues:")
        for issue in completeness_issues:
            print(f"   - {issue['resource_type']} #{issue['record_index']}: "
                  f"Missing {', '.join(issue['missing_fields'])}")
    
    # AI Readiness Check
    print("\n6. AI Readiness Assessment:")
    print("-" * 80)
    ai_checker = AIReadinessChecker()
    readiness = ai_checker.assess_dataset("synthetic_ehr_bundle.json")
    
    if readiness >= 0.8:
        print(f"   ✅ Dataset is AI-ready (score: {readiness:.1%})")
    else:
        print(f"   ⚠️  Dataset needs improvement for AI (score: {readiness:.1%})")
        print("   Recommendations:")
        print("   • Improve completeness of patient demographics")
        print("   • Standardize observation value units")
        print("   • Add missing temporal data")
    
    # Demonstrate pandas DataFrame assessment
    print("\n7. Assessing Tabular Data (CSV/DataFrame):")
    print("-" * 80)
    
    # Create sample patient DataFrame
    patient_df = pd.DataFrame({
        'patient_id': [f'P{i:04d}' for i in range(20)],
        'age': [random.randint(18, 90) if random.random() > 0.1 else None for _ in range(20)],
        'gender': [random.choice(['M', 'F', None]) for _ in range(20)],
        'diagnosis_code': [f'I{random.randint(10,99)}.{random.randint(0,9)}' for _ in range(20)],
        'lab_result': [random.uniform(0, 100) if random.random() > 0.2 else None for _ in range(20)]
    })
    
    df_results = assessor.assess_dataframe(patient_df)
    print(f"   📊 DataFrame Quality Score: {df_results['score']:.1%}")
    
    # Show field-level completeness
    print("\n   Field Completeness:")
    for field, score in df_results.get('completeness', {}).get('field_scores', {}).items():
        print(f"   • {field:<15} {score:.1%}")
    
    # Cleanup
    import os
    os.remove("synthetic_ehr_bundle.json")
    
    print("\n" + "=" * 80)
    print("Demo complete! 🎉")
    print("\nNext steps:")
    print("• Install HealthPipe: pip install healthpipe")
    print("• Read the docs: https://github.com/bunny723/healthpipe")
    print("• Try it on your data!")


if __name__ == "__main__":
    demonstrate_quality_assessment()