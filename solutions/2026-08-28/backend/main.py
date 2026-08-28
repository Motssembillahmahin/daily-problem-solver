from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(title="Show HN: We built open OpenRouter that turns usage into a better model")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

@app.get("/api/solve")
async def solve_problem():
    response = requests.post(HF_URL, json={"inputs": "Solve: Show HN: We built open OpenRouter that turns usage into a better model"}, timeout=60)
    result = response.json() if response.status_code == 200 else {"generated_text": "API limit reached"}
    return {"problem": "Show HN: We built open OpenRouter that turns usage into a better model", "solution": result[0].get("generated_text", "")}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}