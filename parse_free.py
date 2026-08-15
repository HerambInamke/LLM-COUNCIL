import json

with open(r"C:\Users\vansh\.claude\projects\C--Projects-LLM-COUNCIL\27a8a5fb-0751-48bb-bc25-01180ac6ca7c\tool-results\bn3zp8ckw.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

free_models = [m["id"] for m in data.get("data", []) if m.get("pricing", {}).get("prompt") == "0"]
print(",".join(free_models))
