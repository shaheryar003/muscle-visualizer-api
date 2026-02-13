import httpx
from app.config import RAPID_API_KEY, RAPID_API_HOST

# BASE_URL = f"https://{RAPID_API_HOST}" # Dynamic per call now

async def call_rapid_api(endpoint: str, params: dict = None, host: str = None, key: str = None):
    """
    Generic function to call RapidAPI endpoint.
    Returns: The response object (can be JSON or binary content).
    """
    if params is None:
        params = {}
    
    headers = {
        "X-RapidAPI-Key": key if key else RAPID_API_KEY,
        "X-RapidAPI-Host": host if host else RAPID_API_HOST
    }
    
    # If host is provided, we might need to change the base URL or just use the host in the header?
    # Usually the Base URL depends on the host. 
    # The existing BASE_URL is f"https://{RAPID_API_HOST}"
    # So we should construct the url dynamically if host is provided.
    
    current_host = host if host else RAPID_API_HOST
    base_url = f"https://{current_host}"
    url = f"{base_url}{endpoint}"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"RapidAPI Error: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response

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
