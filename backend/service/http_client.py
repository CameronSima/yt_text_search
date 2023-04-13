import httpx


async def get(url: str) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response


async def post(url: str, data: dict, headers: dict) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data, headers=headers)
        return response
