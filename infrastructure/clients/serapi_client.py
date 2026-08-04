
##from serpapi import GoogleSearch
import asyncio

from core.config import settings

import httpx

from infrastructure.clients.http_client import HttpClient

class SerpApiClient:

    def __init__(self,http_client: HttpClient):
        self.semaphore = asyncio.Semaphore(3)

        self.http_client = http_client

    async def search(self, query):

        params = {
            "engine": "google",
            "q": query,
            "api_key": settings.SERP_API_KEY
        }

        async with self.semaphore:

            for attempt in range(3):
                try:
                    response = await self.http_client.client.get(
                        "https://serpapi.com/search",
                        params=params
                    )

                    response.raise_for_status()

                    return response.json()

                except httpx.ReadTimeout:

                    if attempt == 2:
                        raise

                    await asyncio.sleep(2 ** attempt)

    async def close(self):
        await self.http_client.close()