
from config import settings
from openai import AsyncOpenAI

class LLMClient:

    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    async def complete(self, prompt):

        response = await self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        return response.output_text