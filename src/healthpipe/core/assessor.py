"""
Main Quality Assessor module for healthcare data quality assessment.
"""

import json
import pandas as pd
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from pyspark.sql import SparkSession, DataFrame as SparkDataFrame
import great_expectations as gx
from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient

from ..validators import (
    CompletenessValidator,
    ConsistencyValidator,
    AccuracyValidator,
    TimelinessValidator,
    ValidityValidator,
    UniquenessValidator
)
from ..utils.logger import get_logger
from ..utils.metrics import QualityMetrics

logger = get_logger(__name__)


class QualityAssessor:
    """
    Main class for assessing healthcare data quality across six dimensions.
    
    Implements the comprehensive quality assessment framework described in the paper:
    - Completeness: Percentage of non-null values for required fields
    - Consistency: Adherence to expected patterns and relationships
    - Accuracy: Correctness compared to authoritative sources
    - Timeliness: Currency and temporal ordering of events
    - Validity: Conformance to clinical and technical constraints
    - Uniqueness: Absence of duplicate records
    """
    
    def __init__(self, spark_session: Optional[SparkSession] = None):
        """
        Initialize the Quality Assessor.
        
        Args:
            spark_session: Optional Spark session for distributed processing
        """
        self.spark = spark_session or self._create_spark_session()
        self.validators = self._initialize_validators()
        self.metrics = QualityMetrics()
        
    def _create_spark_session(self) -> SparkSession:
        """Create a Spark session with healthcare-optimized settings."""
        return SparkSession.builder \
            .appName("HealthPipe-QualityAssessment") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .getOrCreate()
    
    def _initialize_validators(self) -> Dict[str, Any]:
        """Initialize all quality dimension validators."""
        return {
            "completeness": CompletenessValidator(),
            "consistency": ConsistencyValidator(),
            "accuracy": AccuracyValidator(),
            "timeliness": TimelinessValidator(),
            "validity": ValidityValidator(),
            "uniqueness": UniquenessValidator()
        }
    
    def assess_fhir_bundle(self, 
                          bundle_path: str,
                          output_format: str = "summary") -> Dict[str, Any]:
        """
        Assess quality of a FHIR bundle.
        
        Args:
            bundle_path: Path to FHIR bundle JSON file
            output_format: Output format ('summary', 'detailed', 'json')
            
        Returns:
            Quality assessment results
        """
        logger.info(f"Starting assessment of FHIR bundle: {bundle_path}")
        
        # Load and parse FHIR bundle
        try:
            with open(bundle_path, 'r') as f:
                bundle_data = json.load(f)
            bundle = Bundle(**bundle_data)
        except Exception as e:
            logger.error(f"Failed to load FHIR bundle: {e}")
            raise
        
        # Extract resources for assessment
        resources = self._extract_resources(bundle)
        
        # Run quality assessments
        results = {}
        for dimension, validator in self.validators.items():
            logger.info(f"Running {dimension} assessment...")
            results[dimension] = validator.assess(resources)
        
        # Calculate composite score
        results['composite_score'] = self._calculate_composite_score(results)
        
        # Add metadata
        results['metadata'] = {
            'assessment_timestamp': datetime.utcnow().isoformat(),
            'bundle_path': bundle_path,
            'resource_count': len(resources),
            'healthpipe_version': '0.1.0'
        }
        
        return self._format_results(results, output_format)
    
    def assess_dataframe(self, 
                        df: Union[pd.DataFrame, SparkDataFrame],
                        schema_config: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Assess quality of a pandas or Spark DataFrame.
        
        Args:
            df: DataFrame to assess
            schema_config: Optional schema configuration
            
        Returns:
            Quality assessment results
        """
        logger.info(f"Starting assessment of DataFrame with shape: {df.shape if hasattr(df, 'shape') else 'Spark DataFrame'}")
        
        # Convert pandas to Spark if needed
        if isinstance(df, pd.DataFrame):
            df = self.spark.createDataFrame(df)
        
        results = {}
        for dimension, validator in self.validators.items():
            logger.info(f"Running {dimension} assessment...")
            results[dimension] = validator.assess_dataframe(df, schema_config)
        
        results['composite_score'] = self._calculate_composite_score(results)
        return results
    
    def _extract_resources(self, bundle: Bundle) -> List[Dict]:
        """Extract and flatten resources from FHIR bundle."""
        resources = []
        for entry in bundle.entry or []:
            if entry.resource:
                resources.append(entry.resource.dict())
        return resources
    
    def _calculate_composite_score(self, results: Dict[str, Any]) -> float:
        """
        Calculate weighted composite quality score.
        
        Uses weights from the research paper:
        - Completeness: 0.20
        - Consistency: 0.20
        - Accuracy: 0.15
        - Timeliness: 0.15
        - Validity: 0.20
        - Uniqueness: 0.10
        """
        weights = {
            'completeness': 0.20,
            'consistency': 0.20,
            'accuracy': 0.15,
            'timeliness': 0.15,
            'validity': 0.20,
            'uniqueness': 0.10
        }
        
        composite_score = 0.0
        for dimension, weight in weights.items():
            if dimension in results and 'score' in results[dimension]:
                composite_score += results[dimension]['score'] * weight
        
        return round(composite_score, 3)
    
    def _format_results(self, results: Dict, output_format: str) -> Union[Dict, str]:
        """Format results based on requested output format."""
        if output_format == "json":
            return json.dumps(results, indent=2)
        elif output_format == "detailed":
            return results
        else:  # summary
            summary = {
                'composite_score': results['composite_score'],
                'dimension_scores': {
                    dim: res.get('score', 0) for dim, res in results.items() 
                    if dim not in ['composite_score', 'metadata']
                },
                'metadata': results['metadata']
            }
            return summary
    
    def get_summary(self) -> str:
        """Get a human-readable summary of the last assessment."""
        if not hasattr(self, 'last_results'):
            return "No assessment has been run yet."
        
        summary = f"""
Healthcare Data Quality Assessment Summary
==========================================
Composite Score: {self.last_results['composite_score']:.1%}

Dimension Scores:
- Completeness: {self.last_results.get('completeness', {}).get('score', 0):.1%}
- Consistency: {self.last_results.get('consistency', {}).get('score', 0):.1%}
- Accuracy: {self.last_results.get('accuracy', {}).get('score', 0):.1%}
- Timeliness: {self.last_results.get('timeliness', {}).get('score', 0):.1%}
- Validity: {self.last_results.get('validity', {}).get('score', 0):.1%}
- Uniqueness: {self.last_results.get('uniqueness', {}).get('score', 0):.1%}

Assessment completed at: {self.last_results.get('metadata', {}).get('assessment_timestamp', 'Unknown')}
        """
        return summary.strip()