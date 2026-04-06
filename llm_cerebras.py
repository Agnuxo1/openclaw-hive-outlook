import os
import httpx
import logging
import asyncio

logger = logging.getLogger(__name__)

class CerebrasClient:
    def __init__(self):
        # Rotating between the two keys provided
        self.api_keys = [
            os.getenv("CEREBRAS_API_KEY_1", ""),
            os.getenv("CEREBRAS_API_KEY_2", "")
        ]
        self.api_key = os.getenv("CEREBRAS_API_KEY", self.api_keys[0])
        self.base_url = "https://api.cerebras.ai/v1"
        self.model = os.getenv("CEREBRAS_MODEL", "llama3.1-70b") # or llama3.1-8b

    async def chat_completion(self, messages, temperature=0.7, max_tokens=1000):
        if not self.api_key:
            return "Error: CEREBRAS_API_KEY not set."
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"Cerebras API Error: {e}")
                # Optional: try the second key if first fails
                if self.api_key == self.api_keys[0]:
                    logger.info("Retrying with secondary Cerebras key...")
                    self.api_key = self.api_keys[1]
                    return await self.chat_completion(messages, temperature, max_tokens)
                return f"Error in Cerebras inference: {str(e)}"
