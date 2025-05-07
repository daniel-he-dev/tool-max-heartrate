from typing import Any, Dict, Union

from pydantic import BaseModel, Field


class Input(BaseModel):
    """
    Form-based input schema for heart rate calculation.
    """
    data: Dict[str, Union[int, str]] = Field(
        ...,
        title="Heart Rate Calculator Input",
        examples=[{
            "age": 35,
            "activity_level": "active"
        }],
        description="Input data containing age (0-120) and activity level (sedentary, active, or athlete)"
    )

class Output(BaseModel):
    """
    Form-based output schema for heart rate calculation results.
    """
    data: Dict[str, Union[int, Dict[str, str]]] = Field(
        ...,
        title="Heart Rate Calculator Results",
        examples=[{
            "max_heart_rate": 185,
            "target_zones": {
                "low_intensity": "92-111",
                "fat_burn": "111-129",
                "cardio": "129-157",
                "peak": "157-185"
            }
        }],
        description="Maximum heart rate and target heart rate zones based on age and activity level"
    )
