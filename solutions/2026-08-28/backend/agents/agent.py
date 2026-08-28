import requests
from typing import Dict, Any

HF_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

class ProblemSolverAgent:
    def __init__(self):
        pass

    def analyze(self, problem: Dict[str, Any]) -> str:
        prompt = f"Analyze this problem: {problem.get('title', '')}"
        response = requests.post(HF_URL, json={"inputs": prompt}, timeout=60)
        if response.status_code == 200:
            return response.json()[0].get("generated_text", "")
        return "Analysis unavailable"

    def generate_code(self, problem: Dict[str, Any]) -> str:
        prompt = f"Generate code for: {problem.get('title', '')}"
        response = requests.post(HF_URL, json={"inputs": prompt}, timeout=60)
        if response.status_code == 200:
            return response.json()[0].get("generated_text", "")
        return "# Code generation unavailable"
