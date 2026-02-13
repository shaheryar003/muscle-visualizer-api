
import httpx
import asyncio
import os

API_KEY = "0ff91de6e1mshefd47e741cb9c07p199ca7jsn69d67ba79eda"
HOST = "muscle-visualizer-api.p.rapidapi.com"

async def test():
    url = f"https://{HOST}/v1/muscles"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": HOST
    }
    
    print(f"Requesting: {url}")
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        print(f"Status: {resp.status_code}")
        print(f"Body: {resp.text}")

if __name__ == "__main__":
    asyncio.run(test())
