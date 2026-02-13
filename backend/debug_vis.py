
import httpx
import asyncio

API_KEY = "0ff91de6e1mshefd47e741cb9c07p199ca7jsn69d67ba79eda"
HOST = "muscle-visualizer-api.p.rapidapi.com"

async def check(endpoint):
    url = f"https://{HOST}{endpoint}"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": HOST
    }
    
    print(f"Checking: {endpoint}")
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        print(f"Status: {resp.status_code}")
        if resp.status_code != 200:
            print(f"Body: {resp.text}")
        else:
            print("Success (200)")

async def main():
    e = "/api/v1/visualize/muscles?muscles=biceps"
    await check(e)

if __name__ == "__main__":
    asyncio.run(main())
