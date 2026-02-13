from fastapi import FastAPI, UploadFile, File, Response, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from app.services.rapid_api_service import call_rapid_api
from app.config import RAPID_API_KEY, RAPID_API_HOST, EDB_API_KEY, EDB_API_HOST
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Muscle Visualizer API",
    description="A simple wrapper around the Muscle Visualizer RapidAPI",
    version="1.0.0"
)

# CORS Middleware
origins = [
    "http://localhost:5173",  # React default port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/muscles")
async def get_muscles():
    """
    Get the list of available muscle groups.
    """
    response = await call_rapid_api("/api/v1/muscles")
    return response.json()

@app.get("/api/v1/visualize/muscles")
async def visualize_muscles(
    muscles: str = Query(..., description="Comma separated list of muscles"),
    color: str = Query(None, description="Hex color code")
):
    """
    Visualize specific muscles highlighted.
    """
    params = {
        "muscles": muscles,
        "color": color,
        "gender": "male",
        "background": "transparent",
        "size": "small",
        "format": "jpeg"
    }
    
    response = await call_rapid_api("/api/v1/visualize", params=params)
    return Response(content=response.content, media_type=response.headers.get("Content-Type"))

@app.get("/api/v1/visualize/heatmap")
async def visualize_heatmap(
    muscles: str = Query(..., description="Comma separated muscles"),
    colors: str = Query(None, description="Comma separated hex colors for each muscle or global color")
):
    params = {
        "muscles": muscles,
        "colors": colors,
        "gender": "male",
        "background": "transparent",
        "size": "small",
        "format": "jpeg"
    }
        
    response = await call_rapid_api("/api/v1/visualize/heatmap", params=params)
    return Response(content=response.content, media_type=response.headers.get("Content-Type"))

@app.get("/api/v1/visualize/workout")
async def visualize_workout(
    targetMuscles: str = Query(..., description="Target muscles"),
    targetMusclesColor: str = Query(..., description="Target muscles color"),
    secondaryMuscles: str = Query(None, description="Secondary muscles"),
    secondaryMusclesColor: str = Query(None, description="Secondary muscles color")
):
    """
    Visualize workout activation (primary/secondary).
    """
    logger.info(f"Received params: targetMuscles={targetMuscles}, targetMusclesColor={targetMusclesColor}, secondaryMuscles={secondaryMuscles}, secondaryMusclesColor={secondaryMusclesColor}")
    params = {
        "targetMuscles": targetMuscles,
        "targetMusclesColor": targetMusclesColor,
        "gender": "male",
        "background": "transparent",
        "size": "small",
        "format": "jpeg"
    }
    # API requires these fields and validates strict formats
    params["secondaryMuscles"] = secondaryMuscles if secondaryMuscles else "none"
    params["secondaryMusclesColor"] = secondaryMusclesColor if secondaryMusclesColor else "#000000"
        
    response = await call_rapid_api("/api/v1/visualize/workout", params=params)
    return Response(content=response.content, media_type=response.headers.get("Content-Type"))


# ExerciseDB Endpoints

@app.get("/api/v1/edb/muscles")
async def get_edb_muscles():
    """
    Get the list of available muscle groups from ExerciseDB.
    """
    response = await call_rapid_api("/api/v1/muscles", host=EDB_API_HOST, key=EDB_API_KEY)
    return response.json()

@app.get("/api/v1/edb/equipments")
async def get_equipments():
    """
    Get the list of available equipments from ExerciseDB.
    """
    response = await call_rapid_api("/api/v1/equipments", host=EDB_API_HOST, key=EDB_API_KEY)
    return response.json()

@app.get("/api/v1/edb/exercisetypes")
async def get_exercise_types():
    """
    Get the list of available exercise types.
    """
    response = await call_rapid_api("/api/v1/exercisetypes", host=EDB_API_HOST, key=EDB_API_KEY)
    return response.json()

@app.get("/api/v1/edb/exercises/search")
async def search_exercises(search: str = Query(..., description="Search term")):
    """
    Search exercises by keyword.
    """
    response = await call_rapid_api("/api/v1/exercises/search", params={"search": search}, host=EDB_API_HOST, key=EDB_API_KEY)
    return response.json()

@app.get("/api/v1/edb/exercises")
async def list_exercises(name: str = Query(None), keywords: str = Query(None)):
    """
    List exercises with optional filters.
    """
    params = {}
    if name: params["name"] = name
    if keywords: params["keywords"] = keywords
    response = await call_rapid_api("/api/v1/exercises", params=params, host=EDB_API_HOST, key=EDB_API_KEY)
    return response.json()

@app.get("/api/v1/edb/exercises/{exercise_id}")
async def get_exercise_details(exercise_id: str):
    """
    Get details for a specific exercise.
    """
    response = await call_rapid_api(f"/api/v1/exercises/{exercise_id}", host=EDB_API_HOST, key=EDB_API_KEY)
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
