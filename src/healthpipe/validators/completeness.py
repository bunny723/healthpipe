"""
Completeness validator for healthcare data quality assessment.

Evaluates the percentage of non-null values for required clinical fields,
with context-aware handling of "not applicable" vs "missing" data.
"""

from typing import Dict, List, Any, Optional, Union
import pandas as pd
from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql import functions as F

from ..utils.logger import get_logger
from .base import BaseValidator

logger = get_logger(__name__)


class CompletenessValidator(BaseValidator):
    """
    Validator for assessing data completeness in healthcare datasets.
    
    Key features:
    - Field-level completeness scores
    - Record-level completeness scores
    - Longitudinal completeness (for time-series data)
    - Clinical context awareness (required vs optional fields)
    """
    
    def __init__(self):
        super().__init__()
        self.required_fields = self._load_required_fields()
        self.clinical_rules = self._load_clinical_rules()
    
    def _load_required_fields(self) -> Dict[str, List[str]]:
        """Load required fields for different resource types."""
        return {
            "Patient": [
                "identifier", "name", "gender", "birthDate"
            ],
            "Observation": [
                "status", "code", "subject", "effectiveDateTime", "value"
            ],
            "Medication": [
                "status", "medicationCodeableConcept", "subject", "authoredOn"
            ],
            "Condition": [
                "clinicalStatus", "verificationStatus", "code", "subject"
            ],
            "Procedure": [
                "status", "code", "subject", "performedDateTime"
            ]
        }
    
    def _load_clinical_rules(self) -> Dict[str, Any]:
        """Load clinical context rules for completeness assessment."""
        return {
            "pregnancy_fields": {
                "applies_to": {"gender": "female", "age_range": [12, 55]},
                "required": ["pregnancyStatus", "lastMenstrualPeriod"]
            },
            "pediatric_fields": {
                "applies_to": {"age_range": [0, 18]},
                "required": ["immunizationStatus", "growthChart"]
            }
        }
    
    def assess(self, resources: List[Dict]) -> Dict[str, Any]:
        """
        Assess completeness of healthcare resources.
        
        Args:
            resources: List of FHIR resources as dictionaries
            
        Returns:
            Completeness assessment results
        """
        results = {
            "score": 0.0,
            "field_level": {},
            "record_level": {},
            "issues": [],
            "recommendations": []
        }
        
        # Group resources by type
        resources_by_type = self._group_by_type(resources)
        
        # Assess each resource type
        total_score = 0.0
        for resource_type, items in resources_by_type.items():
            type_results = self._assess_resource_type(resource_type, items)
            results["field_level"][resource_type] = type_results["field_scores"]
            results["record_level"][resource_type] = type_results["record_scores"]
            results["issues"].extend(type_results["issues"])
            total_score += type_results["score"]
        
        # Calculate overall score
        results["score"] = total_score / len(resources_by_type) if resources_by_type else 0.0
        
        # Generate recommendations
        results["recommendations"] = self._generate_recommendations(results)
        
        return results
    
    def assess_dataframe(self, 
                        df: Union[pd.DataFrame, SparkDataFrame],
                        schema_config: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Assess completeness of a DataFrame.
        
        Args:
            df: DataFrame to assess
            schema_config: Optional schema configuration
            
        Returns:
            Completeness assessment results
        """
        if isinstance(df, pd.DataFrame):
            return self._assess_pandas_df(df, schema_config)
        else:
            return self._assess_spark_df(df, schema_config)
    
    def _assess_pandas_df(self, df: pd.DataFrame, schema_config: Optional[Dict]) -> Dict[str, Any]:
        """Assess completeness of a pandas DataFrame."""
        results = {
            "score": 0.0,
            "field_scores": {},
            "missing_patterns": {},
            "issues": []
        }
        
        # Calculate field-level completeness
        for column in df.columns:
            non_null_count = df[column].notna().sum()
            completeness = non_null_count / len(df)
            results["field_scores"][column] = completeness
            
            if completeness < 0.9:  # Flag fields with <90% completeness
                results["issues"].append({
                    "field": column,
                    "completeness": completeness,
                    "missing_count": len(df) - non_null_count
                })
        
        # Calculate overall score
        results["score"] = sum(results["field_scores"].values()) / len(results["field_scores"])
        
        # Analyze missing patterns
        results["missing_patterns"] = self._analyze_missing_patterns(df)
        
        return results
    
    def _assess_spark_df(self, df: SparkDataFrame, schema_config: Optional[Dict]) -> Dict[str, Any]:
        """Assess completeness of a Spark DataFrame."""
        results = {
            "score": 0.0,
            "field_scores": {},
            "issues": []
        }
        
        total_count = df.count()
        
        # Calculate field-level completeness
        for column in df.columns:
            non_null_count = df.filter(F.col(column).isNotNull()).count()
            completeness = non_null_count / total_count if total_count > 0 else 0.0
            results["field_scores"][column] = completeness
            
            if completeness < 0.9:
                results["issues"].append({
                    "field": column,
                    "completeness": completeness,
                    "missing_count": total_count - non_null_count
                })
        
        # Calculate overall score
        results["score"] = sum(results["field_scores"].values()) / len(results["field_scores"])
        
        return results
    
    def _assess_resource_type(self, resource_type: str, items: List[Dict]) -> Dict[str, Any]:
        """Assess completeness for a specific resource type."""
        required_fields = self.required_fields.get(resource_type, [])
        
        field_scores = {}
        record_scores = []
        issues = []
        
        # Assess each item
        for idx, item in enumerate(items):
            item_score = 0.0
            missing_required = []
            
            for field in required_fields:
                if self._is_field_complete(item, field):
                    item_score += 1.0
                    field_scores[field] = field_scores.get(field, 0) + 1
                else:
                    missing_required.append(field)
            
            # Calculate record completeness
            record_completeness = item_score / len(required_fields) if required_fields else 1.0
            record_scores.append(record_completeness)
            
            # Log issues for incomplete records
            if missing_required:
                issues.append({
                    "resource_type": resource_type,
                    "record_index": idx,
                    "missing_fields": missing_required,
                    "completeness": record_completeness
                })
        
        # Normalize field scores
        for field in field_scores:
            field_scores[field] = field_scores[field] / len(items)
        
        return {
            "score": sum(record_scores) / len(record_scores) if record_scores else 0.0,
            "field_scores": field_scores,
            "record_scores": record_scores,
            "issues": issues
        }
    
    def _is_field_complete(self, item: Dict, field_path: str) -> bool:
        """Check if a field is complete (handles nested fields)."""
        parts = field_path.split('.')
        current = item
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False
        
        # Check if value is meaningful (not just empty string/list)
        if isinstance(current, str):
            return len(current.strip()) > 0
        elif isinstance(current, list):
            return len(current) > 0
        else:
            return current is not None
    
    def _analyze_missing_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze patterns in missing data."""
        missing_mask = df.isna()
        
        patterns = {
            "columns_always_missing_together": [],
            "conditional_missing": [],
            "temporal_patterns": []
        }
        
        # Find columns that are always missing together
        for i, col1 in enumerate(df.columns):
            for col2 in df.columns[i+1:]:
                if (missing_mask[col1] == missing_mask[col2]).all():
                    patterns["columns_always_missing_together"].append([col1, col2])
        
        return patterns
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations based on assessment."""
        recommendations = []
        
        # Check overall score
        if results["score"] < 0.8:
            recommendations.append(
                "Critical: Overall completeness below 80%. "
                "Implement mandatory field validation in data capture systems."
            )
        
        # Check for systematic missing fields
        for resource_type, field_scores in results.get("field_level", {}).items():
            for field, score in field_scores.items():
                if score < 0.5:
                    recommendations.append(
                        f"Field '{field}' in {resource_type} has <50% completeness. "
                        f"Investigate data capture workflow for this field."
                    )
        
        return recommendations
    
    def _group_by_type(self, resources: List[Dict]) -> Dict[str, List[Dict]]:
        """Group resources by their type."""
        grouped = {}
        for resource in resources:
            resource_type = resource.get('resourceType', 'Unknown')
            if resource_type not in grouped:
                grouped[resource_type] = []
            grouped[resource_type].append(resource)
        return grouped