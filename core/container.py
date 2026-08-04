
from infrastructure.clients.http_client import HttpClient
from infrastructure.clients.serapi_client import SerpApiClient
from infrastructure.clients.llm_client import LLMClient

openai_client = LLMClient()

http_client = HttpClient()

serp_api_client = SerpApiClient(
    http_client=http_client
)