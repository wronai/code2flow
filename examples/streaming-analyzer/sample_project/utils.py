"""Utility functions for the sample project."""

import json
from typing import Any, Dict, List


def validate_input(data: Dict) -> bool:
    """Validate input data."""
    if not isinstance(data, dict):
        return False
    
    # Check required fields
    if "test" not in data:
        return False
    
    # Validate data types
    if not isinstance(data["test"], str):
        return False
    
    return True


def format_output(data: Any) -> str:
    """Format output data."""
    if isinstance(data, dict):
        return json.dumps(data, indent=2)
    elif isinstance(data, list):
        return json.dumps(data, indent=2)
    else:
        return str(data)


def calculate_metrics(data: List[Dict]) -> Dict[str, float]:
    """Calculate metrics from data list."""
    if not data:
        return {"count": 0, "avg": 0.0}
    
    count = len(data)
    total = sum(len(str(item)) for item in data)
    avg = total / count if count > 0 else 0.0
    
    return {
        "count": count,
        "total_size": total,
        "avg_size": avg
    }


def filter_data(data: List[Dict], criteria: Dict) -> List[Dict]:
    """Filter data based on criteria."""
    filtered = []
    
    for item in data:
        match = True
        for key, value in criteria.items():
            if item.get(key) != value:
                match = False
                break
        
        if match:
            filtered.append(item)
    
    return filtered


def transform_data(data: List[Dict], transformations: Dict[str, str]) -> List[Dict]:
    """Transform data fields."""
    transformed = []
    
    for item in data:
        new_item = item.copy()
        
        for field, operation in transformations.items():
            if field in new_item:
                if operation == "upper":
                    new_item[field] = str(new_item[field]).upper()
                elif operation == "lower":
                    new_item[field] = str(new_item[field]).lower()
                elif operation == "reverse":
                    new_item[field] = str(new_item[field])[::-1]
        
        transformed.append(new_item)
    
    return transformed
