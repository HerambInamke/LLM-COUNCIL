import asyncio
import os
import json
from dotenv import load_dotenv
import httpx

load_dotenv(override=True)

async def main():
    key = os.getenv("OPENROUTER_API_KEY")
    if key and key.startswith('"') and key.endswith('"'):
        key = key[1:-1]
        
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": "google/gemini-2.5-flash", 
        "messages": [{"role": "user", "content": "hello"}]
    }
    
    async with httpx.AsyncClient() as client:
        r = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=10.0)
        print(f"gemini-2.5-flash: {r.status_code}")
        
    payload["model"] = "anthropic/claude-3-haiku"
    async with httpx.AsyncClient() as client:
        r = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=10.0)
        print(f"claude-3-haiku: {r.status_code}")

asyncio.run(main())
