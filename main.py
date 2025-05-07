from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from schemas import Input, Output

# a descriptive title and description are helpful for the navigator
app = FastAPI(
    title="Heart Rate Calculator",
    description=(
        "Calculate maximum heart rate and target heart rate zones based on age and activity level. "
        "Supports different activity profiles including sedentary, active, and athlete. "
        "Returns personalized heart rate recommendations."
    ),
    version="1.0.0",
)

# This is so that other services can make requests to this service
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Calculate maximum heart rate based on age and activity level
@app.post(
    "/call/",
    response_model=Output,
)
async def call(data: Input) -> Output | JSONResponse:
    """Calculate maximum heart rate based on age and activity level.

    Args:
        data: Input containing:
            - age: Age in years (int)
            - activity_level: Activity level ('sedentary', 'active', or 'athlete')

    Returns:
        Maximum heart rate calculation and target heart rate zones
    """
    try:
        age = data.data.get('age')
        activity_level = data.data.get('activity_level', 'active')

        # Validate inputs
        if not isinstance(age, int) or age < 0 or age > 120:
            return JSONResponse(
                {"error": "Age must be a number between 0 and 120"}, 
                status_code=400
            )
            
        if activity_level not in ['sedentary', 'active', 'athlete']:
            return JSONResponse(
                {"error": "Activity level must be 'sedentary', 'active', or 'athlete'"}, 
                status_code=400
            )

        # Calculate max heart rate using common formula
        max_hr = 220 - age
        
        # Adjust based on activity level
        if activity_level == 'athlete':
            max_hr += 5
        elif activity_level == 'sedentary':
            max_hr -= 5
            
        # Calculate target zones
        zones = {
            'low_intensity': f"{int(max_hr * 0.5)}-{int(max_hr * 0.6)}",
            'fat_burn': f"{int(max_hr * 0.6)}-{int(max_hr * 0.7)}",
            'cardio': f"{int(max_hr * 0.7)}-{int(max_hr * 0.85)}",
            'peak': f"{int(max_hr * 0.85)}-{max_hr}"
        }
        
        return Output(data={
            'max_heart_rate': max_hr,
            'target_zones': zones
        })
        
    except Exception as e:
        return JSONResponse(
            {"error": f"Calculation failed: {str(e)}"}, 
            status_code=500
        )

# include a health check endpoint to help determine if the tool is healthy
@app.get("/health", response_class=JSONResponse)
async def health_check():
    """Health check endpoint."""
    return {"status": "Application is running."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
