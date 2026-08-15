import asyncio
import os
import time
from dotenv import load_dotenv
import httpx

load_dotenv()

async def test_model(client, model):
    key = os.getenv("OPENROUTER_API_KEY")
    if key and key.startswith('"') and key.endswith('"'):
        key = key[1:-1]
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": [{"role": "user", "content": "What is 2+2?"}]}
    
    start = time.time()
    try:
        r = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=15.0)
        elapsed = time.time() - start
        print(f"{model}: {r.status_code} in {elapsed:.2f}s")
    except Exception as e:
        print(f"{model}: Failed - {str(e)}")

async def main():
    models = [
        "openrouter/free",
        "nvidia/nemotron-nano-9b-v2:free",
        "openai/gpt-oss-20b:free",
        "poolside/laguna-xs-2.1:free"
    ]
    async with httpx.AsyncClient() as client:
        tasks = [test_model(client, m) for m in models]
        await asyncio.gather(*tasks)

asyncio.run(main())
