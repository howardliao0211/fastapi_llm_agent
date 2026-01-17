from openai import AsyncOpenAI
from typing import List, Dict
from core.config import settings

class LLM_Service:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=settings.VLLM_BASE_URL,
            api_key="none"
        )
        self.model = settings.VLLM_MODEL
    
    async def call_chat_completion(self, messages: List[Dict[str, str]]) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content

llm_service = LLM_Service()
