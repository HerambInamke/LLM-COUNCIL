import asyncio
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

async def test_model(model):
    key = os.getenv("OPENROUTER_API_KEY")
    if key and key.startswith('"') and key.endswith('"'):
        key = key[1:-1]
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": [{"role": "user", "content": "hi"}]}
    async with httpx.AsyncClient() as client:
        r = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        print(model, r.status_code, r.text[:100])

async def main():
    models = ["liquid/lfm-2.5-2.6b:free", "poolside/laguna-s-2.1:free", "google/gemma-4-26b-a4b-it:free"]
    await asyncio.gather(*(test_model(m) for m in models))

asyncio.run(main())
