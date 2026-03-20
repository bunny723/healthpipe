"""Tests for the Quality Assessor module."""

import pytest
from healthpipe import QualityAssessor


def test_assessor_initialization():
    """Test that QualityAssessor initializes correctly."""
    assessor = QualityAssessor()
    assert assessor is not None
    assert hasattr(assessor, 'validators')
    assert len(assessor.validators) == 6  # Six quality dimensions


def test_composite_score_calculation():
    """Test composite score calculation."""
    assessor = QualityAssessor()
    
    # Mock results
    mock_results = {
        'completeness': {'score': 0.8},
        'consistency': {'score': 0.85},
        'accuracy': {'score': 0.9},
        'timeliness': {'score': 0.88},
        'validity': {'score': 0.92},
        'uniqueness': {'score': 0.95}
    }
    
    composite = assessor._calculate_composite_score(mock_results)
    
    # Expected: (0.8*0.2 + 0.85*0.2 + 0.9*0.15 + 0.88*0.15 + 0.92*0.2 + 0.95*0.1)
    expected = 0.876
    assert abs(composite - expected) < 0.001