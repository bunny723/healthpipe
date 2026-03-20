"""
Basic usage example for HealthPipe.

This example demonstrates how to assess the quality of a synthetic
healthcare dataset using the HealthPipe framework.
"""

import json
from pathlib import Path
from healthpipe import QualityAssessor

# Create sample FHIR bundle data
sample_bundle = {
    "resourceType": "Bundle",
    "type": "collection",
    "entry": [
        {
            "resource": {
                "resourceType": "Patient",
                "id": "patient-1",
                "identifier": [{"system": "http://hospital.org", "value": "12345"}],
                "name": [{"family": "Smith", "given": ["John"]}],
                "gender": "male",
                "birthDate": "1970-01-01"
            }
        },
        {
            "resource": {
                "resourceType": "Patient",
                "id": "patient-2",
                "identifier": [{"system": "http://hospital.org", "value": "67890"}],
                "name": [{"family": "Johnson", "given": ["Jane"]}],
                "gender": "female",
                # Missing birthDate - will affect completeness score
            }
        },
        {
            "resource": {
                "resourceType": "Observation",
                "id": "obs-1",
                "status": "final",
                "code": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": "29463-7",
                        "display": "Body weight"
                    }]
                },
                "subject": {"reference": "Patient/patient-1"},
                "effectiveDateTime": "2024-01-15T10:30:00Z",
                "valueQuantity": {
                    "value": 70.5,
                    "unit": "kg",
                    "system": "http://unitsofmeasure.org"
                }
            }
        }
    ]
}

def main():
    """Run basic quality assessment example."""
    
    # Save sample bundle to file
    bundle_path = Path("sample_bundle.json")
    with open(bundle_path, 'w') as f:
        json.dump(sample_bundle, f, indent=2)
    
    print("HealthPipe - Basic Usage Example")
    print("=" * 50)
    
    # Initialize assessor
    print("\n1. Initializing Quality Assessor...")
    assessor = QualityAssessor()
    
    # Run assessment
    print("\n2. Running quality assessment on FHIR bundle...")
    results = assessor.assess_fhir_bundle(str(bundle_path))
    
    # Display results
    print("\n3. Assessment Results:")
    print("-" * 50)
    
    print(f"\nComposite Quality Score: {results['composite_score']:.2%}")
    
    print("\nDimension Scores:")
    for dimension, score in results['dimension_scores'].items():
        print(f"  - {dimension.capitalize()}: {score:.2%}")
    
    # Display detailed results for completeness
    print("\n4. Detailed Completeness Analysis:")
    print("-" * 50)
    
    detailed_results = assessor.assess_fhir_bundle(str(bundle_path), output_format="detailed")
    completeness_issues = detailed_results.get('completeness', {}).get('issues', [])
    
    if completeness_issues:
        print("\nCompleteness Issues Found:")
        for issue in completeness_issues[:5]:  # Show first 5 issues
            print(f"  - Resource Type: {issue.get('resource_type')}")
            print(f"    Missing Fields: {', '.join(issue.get('missing_fields', []))}")
            print(f"    Completeness: {issue.get('completeness', 0):.2%}")
    
    # Show recommendations
    print("\n5. Recommendations:")
    print("-" * 50)
    recommendations = detailed_results.get('completeness', {}).get('recommendations', [])
    for rec in recommendations[:3]:  # Show first 3 recommendations
        print(f"  • {rec}")
    
    # Clean up
    bundle_path.unlink()
    
    print("\n" + "=" * 50)
    print("Assessment complete!")
    
    # Note about production usage
    print("\n💡 For production use:")
    print("  - Connect to your FHIR server or data warehouse")
    print("  - Use Spark for processing large datasets")
    print("  - Set up continuous monitoring with StreamingMonitor")
    print("  - Configure clinical validation rules for your use case")


if __name__ == "__main__":
    main()