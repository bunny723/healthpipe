"""
HealthPipe: Automated Data Quality Assessment Framework for AI-Ready Clinical Datasets

A comprehensive framework for assessing and ensuring data quality in healthcare datasets,
specifically designed for preparing clinical data for AI/ML applications.
"""

__version__ = "0.1.0"
__author__ = "Praveen Kumar Polisetty"
__email__ = "praveen.polisetty2123@gmail.com"

from .core.assessor import QualityAssessor
from .core.monitor import StreamingMonitor
from .core.readiness import AIReadinessChecker
from .core.multi_system import MultiSystemAssessor

__all__ = [
    "QualityAssessor",
    "StreamingMonitor", 
    "AIReadinessChecker",
    "MultiSystemAssessor",
]