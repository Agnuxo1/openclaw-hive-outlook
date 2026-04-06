import os
import httpx
import logging
import asyncio

logger = logging.getLogger(__name__)

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    async def chat_completion(self, messages, temperature=0.7, max_tokens=1000):
        if not self.api_key:
            return "Error: GROQ_API_KEY not set."
            
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
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"Groq API Error: {e}")
                return f"Error in Groq inference: {str(e)}"
