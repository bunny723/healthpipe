"""Base validator class for all quality dimension validators."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
import pandas as pd
from pyspark.sql import DataFrame as SparkDataFrame


class BaseValidator(ABC):
    """Abstract base class for quality validators."""
    
    @abstractmethod
    def assess(self, resources: List[Dict]) -> Dict[str, Any]:
        """
        Assess quality for a list of resources.
        
        Args:
            resources: List of resources to assess
            
        Returns:
            Assessment results with score and details
        """
        pass
    
    @abstractmethod
    def assess_dataframe(self, 
                        df: Union[pd.DataFrame, SparkDataFrame],
                        schema_config: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Assess quality for a DataFrame.
        
        Args:
            df: DataFrame to assess
            schema_config: Optional schema configuration
            
        Returns:
            Assessment results with score and details
        """
        pass