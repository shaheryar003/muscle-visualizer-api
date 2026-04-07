import httpx
import logging
from fastapi import HTTPException
from app.config import RAPID_API_KEY, RAPID_API_HOST

logger = logging.getLogger(__name__)


async def call_rapid_api(endpoint: str, params: dict = None, host: str = None, key: str = None):
    """
    Generic function to call a RapidAPI endpoint.

    Returns: The httpx.Response object (JSON or binary content).
    Raises:
        HTTPException(502) — upstream returned a non-2xx response.
        HTTPException(503) — network / timeout error reaching upstream.
    """
    if params is None:
        params = {}

    current_host = host if host else RAPID_API_HOST
    headers = {
        "X-RapidAPI-Key": key if key else RAPID_API_KEY,
        "X-RapidAPI-Host": current_host,
    }

    base_url = f"https://{current_host}"
    url = f"{base_url}{endpoint}"

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers, params=params)

        if response.status_code != 200:
            logger.error(
                "RapidAPI Error: %s - %s | URL: %s",
                response.status_code,
                response.text,
                response.url,
            )

        # Raise so we can inspect and re-map the error
        response.raise_for_status()
        return response

    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code

        # Try to surface the upstream error message to the caller
        try:
            upstream_detail = exc.response.json()
        except Exception:
            upstream_detail = exc.response.text or "Upstream API error"

        logger.error(
            "Upstream HTTP %s from %s: %s",
            status,
            exc.request.url,
            upstream_detail,
        )

        # 4xx → bad request from our side (invalid params, quota, auth, …)
        # Pass those back verbatim so callers see a meaningful message.
        if 400 <= status < 500:
            raise HTTPException(status_code=status, detail=upstream_detail)

        # 5xx → upstream problem
        raise HTTPException(
            status_code=502,
            detail={
                "error": "Upstream API returned an error",
                "upstream_status": status,
                "upstream_detail": upstream_detail,
            },
        )

    except httpx.TimeoutException as exc:
        logger.error("Request to %s timed out: %s", url, exc)
        raise HTTPException(
            status_code=503,
            detail={"error": "Upstream API request timed out. Please try again later."},
        )

    except httpx.RequestError as exc:
        logger.error("Network error calling %s: %s", url, exc)
        raise HTTPException(
            status_code=503,
            detail={"error": "Could not reach the upstream API. Please try again later."},
        )


async def get_muscles_list():
    """
    Fetch the list of available muscles.
    """
    response = await call_rapid_api("/api/v1/muscles")
    return response.json()


async def get_visualization(endpoint: str, params: dict):
    """
    Fetch the visualization image from the specified endpoint.
    endpoints: /v1/visualize/muscles, /v1/visualize/heatmap, /v1/visualize/workout
    Returns: The raw image bytes and content type.
    """
    response = await call_rapid_api(endpoint, params)
    return response.content, response.headers.get("content-type")
