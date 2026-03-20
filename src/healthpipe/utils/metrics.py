"""Metrics tracking for quality assessments."""

from typing import Dict, Any, List
from datetime import datetime
import json


class QualityMetrics:
    """Track and aggregate quality metrics over time."""
    
    def __init__(self):
        self.assessments: List[Dict[str, Any]] = []
        
    def add_assessment(self, results: Dict[str, Any]) -> None:
        """Add an assessment result to metrics tracking."""
        self.assessments.append({
            "timestamp": datetime.utcnow().isoformat(),
            "results": results
        })
    
    def get_trends(self) -> Dict[str, List[float]]:
        """Get quality score trends over time."""
        trends = {
            "composite": [],
            "completeness": [],
            "consistency": [],
            "accuracy": [],
            "timeliness": [],
            "validity": [],
            "uniqueness": []
        }
        
        for assessment in self.assessments:
            results = assessment["results"]
            trends["composite"].append(results.get("composite_score", 0))
            
            for dimension in ["completeness", "consistency", "accuracy", 
                            "timeliness", "validity", "uniqueness"]:
                score = results.get(dimension, {}).get("score", 0)
                trends[dimension].append(score)
        
        return trends
    
    def export_metrics(self, filepath: str) -> None:
        """Export metrics to JSON file."""
        with open(filepath, 'w') as f:
            json.dump({
                "assessments": self.assessments,
                "trends": self.get_trends()
            }, f, indent=2)