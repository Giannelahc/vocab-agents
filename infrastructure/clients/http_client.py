import httpx


class HttpClient:

    def __init__(self):

        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=10.0,
                read=30.0,
                write=10.0,
                pool=10.0
            )
        )


    async def close(self):
        await self.client.aclose()