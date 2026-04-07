from fastapi import FastAPI, Response, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.services.rapid_api_service import call_rapid_api
from app.config import RAPID_API_KEY, RAPID_API_HOST, EDB_API_KEY, EDB_API_HOST
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Muscle Visualizer API",
    description="A simple wrapper around the Muscle Visualizer RapidAPI",
    version="1.0.0"
)

# CORS Middleware — allow all origins for public API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Global exception handler — catches any unhandled exception and returns JSON
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    logger.exception("Unhandled exception on %s %s", request.method, request.url)
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected internal server error occurred."},
    )


# ---------------------------------------------------------------------------
# Muscle Visualizer endpoints
# ---------------------------------------------------------------------------

@app.get("/api/v1/muscles")
async def get_muscles():
    """Get the list of available muscle groups."""
    try:
        response = await call_rapid_api("/api/v1/muscles")
        return response.json()
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected error in get_muscles")
        raise HTTPException(status_code=500, detail={"error": "Failed to fetch muscles list."})


@app.get("/api/v1/visualize/muscles")
async def visualize_muscles(
    muscles: str = Query(..., description="Comma separated list of muscles"),
    color: str = Query(None, description="Hex color code"),
):
    """Visualize specific muscles highlighted."""
    if not muscles.strip():
        raise HTTPException(status_code=422, detail={"error": "muscles parameter must not be empty."})

    params = {
        "muscles": muscles,
        "color": color,
        "gender": "male",
        "background": "transparent",
        "size": "small",
        "format": "jpeg",
    }

    try:
        response = await call_rapid_api("/api/v1/visualize", params=params)
        return Response(
            content=response.content,
            media_type=response.headers.get("Content-Type", "image/jpeg"),
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected error in visualize_muscles")
        raise HTTPException(status_code=500, detail={"error": "Failed to generate muscle visualization."})


@app.get("/api/v1/visualize/heatmap")
async def visualize_heatmap(
    muscles: str = Query(..., description="Comma separated muscles"),
    colors: str = Query(None, description="Comma separated hex colors — one per muscle or a single global color"),
):
    """
    Visualize muscle heatmap.

    The upstream API requires either:
      - A single color applied to all muscles, OR
      - Exactly one color per muscle (colors count == muscles count).

    This endpoint validates that constraint before forwarding the request so
    callers receive a clear 422 instead of a cryptic 400 from upstream.
    """
    muscle_list = [m.strip() for m in muscles.split(",") if m.strip()]
    if not muscle_list:
        raise HTTPException(status_code=422, detail={"error": "muscles parameter must not be empty."})

    if colors:
        color_list = [c.strip() for c in colors.split(",") if c.strip()]
        if len(color_list) > 1 and len(color_list) != len(muscle_list):
            raise HTTPException(
                status_code=422,
                detail={
                    "error": (
                        f"Number of colors ({len(color_list)}) must be 1 (global) "
                        f"or match the number of muscles ({len(muscle_list)})."
                    )
                },
            )

    params = {
        "muscles": muscles,
        "colors": colors,
        "gender": "male",
        "background": "transparent",
        "size": "small",
        "format": "jpeg",
    }

    try:
        response = await call_rapid_api("/api/v1/visualize/heatmap", params=params)
        return Response(
            content=response.content,
            media_type=response.headers.get("Content-Type", "image/jpeg"),
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected error in visualize_heatmap")
        raise HTTPException(status_code=500, detail={"error": "Failed to generate heatmap visualization."})


@app.get("/api/v1/visualize/workout")
async def visualize_workout(
    targetMuscles: str = Query(..., description="Target muscles"),
    targetMusclesColor: str = Query(..., description="Target muscles color"),
    secondaryMuscles: str = Query(None, description="Secondary muscles"),
    secondaryMusclesColor: str = Query(None, description="Secondary muscles color"),
):
    """Visualize workout activation (primary/secondary)."""
    if not targetMuscles.strip():
        raise HTTPException(status_code=422, detail={"error": "targetMuscles parameter must not be empty."})
    if not targetMusclesColor.strip():
        raise HTTPException(status_code=422, detail={"error": "targetMusclesColor parameter must not be empty."})

    logger.info(
        "Received params: targetMuscles=%s, targetMusclesColor=%s, secondaryMuscles=%s, secondaryMusclesColor=%s",
        targetMuscles, targetMusclesColor, secondaryMuscles, secondaryMusclesColor,
    )

    params = {
        "targetMuscles": targetMuscles,
        "targetMusclesColor": targetMusclesColor,
        "gender": "male",
        "background": "transparent",
        "size": "small",
        "format": "jpeg",
        # API requires these fields even if empty
        "secondaryMuscles": secondaryMuscles if secondaryMuscles else "none",
        "secondaryMusclesColor": secondaryMusclesColor if secondaryMusclesColor else "#000000",
    }

    try:
        response = await call_rapid_api("/api/v1/visualize/workout", params=params)
        return Response(
            content=response.content,
            media_type=response.headers.get("Content-Type", "image/jpeg"),
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected error in visualize_workout")
        raise HTTPException(status_code=500, detail={"error": "Failed to generate workout visualization."})


# ---------------------------------------------------------------------------
# ExerciseDB endpoints
# ---------------------------------------------------------------------------

@app.get("/api/v1/edb/muscles")
async def get_edb_muscles():
    """Get the list of available muscle groups from ExerciseDB."""
    try:
        response = await call_rapid_api("/api/v1/muscles", host=EDB_API_HOST, key=EDB_API_KEY)
        return response.json()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error in get_edb_muscles")
        raise HTTPException(status_code=500, detail={"error": "Failed to fetch ExerciseDB muscles list."})


@app.get("/api/v1/edb/equipments")
async def get_equipments():
    """Get the list of available equipments from ExerciseDB."""
    try:
        response = await call_rapid_api("/api/v1/equipments", host=EDB_API_HOST, key=EDB_API_KEY)
        return response.json()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error in get_equipments")
        raise HTTPException(status_code=500, detail={"error": "Failed to fetch equipment list."})


@app.get("/api/v1/edb/exercisetypes")
async def get_exercise_types():
    """Get the list of available exercise types."""
    try:
        response = await call_rapid_api("/api/v1/exercisetypes", host=EDB_API_HOST, key=EDB_API_KEY)
        return response.json()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error in get_exercise_types")
        raise HTTPException(status_code=500, detail={"error": "Failed to fetch exercise types."})


@app.get("/api/v1/edb/exercises/search")
async def search_exercises(search: str = Query(..., description="Search term")):
    """Search exercises by keyword."""
    if not search.strip():
        raise HTTPException(status_code=422, detail={"error": "search parameter must not be empty."})

    try:
        response = await call_rapid_api(
            "/api/v1/exercises/search",
            params={"search": search},
            host=EDB_API_HOST,
            key=EDB_API_KEY,
        )
        return response.json()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error in search_exercises")
        raise HTTPException(status_code=500, detail={"error": "Failed to search exercises."})


@app.get("/api/v1/edb/exercises")
async def list_exercises(
    name: str = Query(None),
    keywords: str = Query(None),
):
    """List exercises with optional filters."""
    params = {}
    if name:
        params["name"] = name
    if keywords:
        params["keywords"] = keywords

    try:
        response = await call_rapid_api("/api/v1/exercises", params=params, host=EDB_API_HOST, key=EDB_API_KEY)
        return response.json()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error in list_exercises")
        raise HTTPException(status_code=500, detail={"error": "Failed to list exercises."})


@app.get("/api/v1/edb/exercises/{exercise_id}")
async def get_exercise_details(exercise_id: str):
    """Get details for a specific exercise."""
    if not exercise_id.strip():
        raise HTTPException(status_code=422, detail={"error": "exercise_id must not be empty."})

    try:
        response = await call_rapid_api(
            f"/api/v1/exercises/{exercise_id}",
            host=EDB_API_HOST,
            key=EDB_API_KEY,
        )
        return response.json()
    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error in get_exercise_details for %s", exercise_id)
        raise HTTPException(status_code=500, detail={"error": f"Failed to fetch details for exercise '{exercise_id}'."})


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
