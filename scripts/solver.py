"""
AI-powered solution generator.
Uses HuggingFace free API (no key needed) or Ollama (local).
Generates full-stack solutions with React/Next.js frontend and Python backend.
"""

import os
import json
import requests
from typing import Dict, Any
from datetime import datetime


HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"


def determine_solution_type(problem: Dict) -> str:
    """Determine what type of solution to generate."""
    category = problem.get("category", "general")
    description = problem.get("description", "").lower()

    if any(w in description for w in ["website", "web app", "frontend", "ui", "dashboard"]):
        return "fullstack"
    if any(w in description for w in ["api", "backend", "server", "database"]):
        return "backend"
    if any(w in description for w in ["script", "automate", "cli", "tool", "process"]):
        return "script"
    if any(w in description for w in ["analyze", "data", "visualize", "chart", "report"]):
        return "data_analysis"

    return "fullstack"


def generate_with_huggingface(problem: Dict) -> Dict[str, Any]:
    """Generate solution using HuggingFace free inference API."""
    try:
        solution_type = determine_solution_type(problem)

        prompt = f"""Generate a complete {solution_type} solution for this problem:

PROBLEM: {problem['title']}
DESCRIPTION: {problem.get('description', 'N/A')}

Generate these files with complete, working code:
1. frontend/app/page.tsx (Next.js)
2. frontend/package.json
3. backend/main.py (FastAPI)
4. backend/requirements.txt

Return ONLY valid JSON:
{{"files": {{"path": "content"}}, "type": "{solution_type}"}}"""

        response = requests.post(
            HUGGINGFACE_API_URL,
            json={"inputs": prompt},
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            content = result[0].get("generated_text", "")

            # Extract JSON from response
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end != -1:
                return json.loads(content[start:end])

    except Exception as e:
        print(f"   HuggingFace API error: {e}")

    # Fallback to template
    return generate_template_solution(problem, solution_type)


def generate_with_ollama(problem: Dict) -> Dict[str, Any]:
    """Generate solution using local Ollama model."""
    try:
        import ollama

        solution_type = determine_solution_type(problem)

        prompt = f"""Generate a complete {solution_type} solution:

PROBLEM: {problem['title']}
DESCRIPTION: {problem.get('description', 'N/A')}

Return ONLY valid JSON:
{{"files": {{"path": "content"}}, "type": "{solution_type}"}}"""

        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response["message"]["content"]
        start = content.find("{")
        end = content.rfind("}") + 1
        if start != -1 and end != -1:
            return json.loads(content[start:end])

    except Exception as e:
        print(f"   Ollama error: {e}")

    return generate_template_solution(problem, determine_solution_type(problem))


def generate_template_solution(problem: Dict, solution_type: str) -> Dict[str, Any]:
    """Generate template-based solution as fallback."""
    files = {}

    if solution_type == "fullstack":
        files = generate_fullstack_template(problem)
    elif solution_type == "backend":
        files = generate_backend_template(problem)
    elif solution_type == "script":
        files = generate_script_template(problem)
    elif solution_type == "data_analysis":
        files = generate_data_template(problem)
    else:
        files = generate_fullstack_template(problem)

    return {"files": files, "type": solution_type}


def generate_fullstack_template(problem: Dict) -> Dict[str, str]:
    """Generate full-stack template files."""
    title = problem["title"].replace(" ", "_").lower()
    safe_title = problem["title"].replace("'", "\\'")

    return {
        "frontend/package.json": json.dumps({
            "name": f"{title}-frontend",
            "version": "1.0.0",
            "scripts": {"dev": "next dev", "build": "next build", "start": "next start"},
            "dependencies": {"next": "14.0.0", "react": "^18.2.0", "react-dom": "^18.2.0"}
        }, indent=2),

        "frontend/app/layout.tsx": f'''import type {{ Metadata }} from 'next'
import './globals.css'

export const metadata: Metadata = {{
    title: "{safe_title}",
    description: "AI-powered solution",
}}

export default function RootLayout({{ children }}: {{ children: React.ReactNode }}) {{
    return (
        <html lang="en">
            <body>{{children}}</body>
        </html>
    )
}}''',

        "frontend/app/page.tsx": f'''"use client"
import {{ useState, useEffect }} from 'react'

export default function Home() {{
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {{
        fetch('/api/solve')
            .then(res => res.json())
            .then(data => {{ setData(data); setLoading(false) }})
    }}, [])

    if (loading) return <div className="p-8">Loading solution...</div>

    return (
        <main className="p-8 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-4">{safe_title}</h1>
            <p className="text-gray-600 mb-8">{problem.get('description', '')[:200]}</p>
            <div className="bg-gray-50 p-6 rounded-lg">
                <h2 className="text-xl font-semibold mb-2">AI-Generated Solution</h2>
                <pre className="bg-white p-4 rounded overflow-auto text-sm">
                    {{JSON.stringify(data, null, 2)}}
                </pre>
            </div>
        </main>
    )
}}''',

        "frontend/app/globals.css": '''@tailwind base;
@tailwind components;
@tailwind utilities;

body { font-family: system-ui, -apple-system, sans-serif; }''',

        "backend/requirements.txt": '''fastapi==0.104.0
uvicorn==0.24.0
pydantic==2.5.0
requests==2.31.0
huggingface_hub==0.20.0''',

        "backend/main.py": f'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(title="{safe_title}")

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
    response = requests.post(HF_URL, json={{"inputs": "Solve: {safe_title}"}}, timeout=60)
    result = response.json() if response.status_code == 200 else {{"generated_text": "API limit reached"}}
    return {{"problem": "{safe_title}", "solution": result[0].get("generated_text", "")}}

@app.get("/api/health")
async def health_check():
    return {{"status": "healthy"}}''',

        "backend/agents/__init__.py": " ",

        "backend/agents/agent.py": f'''import requests
from typing import Dict, Any

HF_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

class ProblemSolverAgent:
    def __init__(self):
        pass

    def analyze(self, problem: Dict[str, Any]) -> str:
        prompt = f"Analyze this problem: {{problem.get('title', '')}}"
        response = requests.post(HF_URL, json={{"inputs": prompt}}, timeout=60)
        if response.status_code == 200:
            return response.json()[0].get("generated_text", "")
        return "Analysis unavailable"

    def generate_code(self, problem: Dict[str, Any]) -> str:
        prompt = f"Generate code for: {{problem.get('title', '')}}"
        response = requests.post(HF_URL, json={{"inputs": prompt}}, timeout=60)
        if response.status_code == 200:
            return response.json()[0].get("generated_text", "")
        return "# Code generation unavailable"
'''
    }


def generate_backend_template(problem: Dict) -> Dict[str, str]:
    """Generate backend-only template files."""
    safe_title = problem["title"].replace("'", "\\'")
    return {
        "requirements.txt": 'fastapi==0.104.0\nuvicorn==0.24.0\nrequests==2.31.0',
        "main.py": f'''from fastapi import FastAPI
import requests

app = FastAPI(title="{safe_title}")

@app.get("/api/solve")
async def solve():
    return {{"problem": "{safe_title}", "solution": "Template solution - enhance with AI"}}
'''
    }


def generate_script_template(problem: Dict) -> Dict[str, str]:
    """Generate script template files."""
    safe_title = problem["title"].replace("'", "\\'")
    return {
        "solution.py": f'''"""
Solution for: {safe_title}
Generated on: {datetime.now().strftime('%Y-%m-%d')}
"""
import requests

def solve():
    print("Solving: {safe_title}")
    # Add your solution logic here

if __name__ == "__main__":
    solve()
''',
        "requirements.txt": "requests==2.31.0"
    }


def generate_data_template(problem: Dict) -> Dict[str, str]:
    """Generate data analysis template files."""
    safe_title = problem["title"].replace("'", "\\'")
    return {
        "requirements.txt": 'pandas==2.1.0\nmatplotlib==3.8.0',
        "solution.py": f'''"""
Data Analysis: {safe_title}
"""
import pandas as pd
import matplotlib.pyplot as plt

def analyze():
    print("Analyzing: {safe_title}")

if __name__ == "__main__":
    analyze()
'''
    }


def generate_solution(problem: Dict) -> Dict[str, Any]:
    """Main entry point for solution generation."""
    solution_type = determine_solution_type(problem)
    print(f"   Generating {solution_type} solution...")

    # Try HuggingFace first (free, no key)
    solution = generate_with_huggingface(problem)

    # Ensure we have files
    if not solution.get("files"):
        solution = generate_template_solution(problem, solution_type)

    return solution
