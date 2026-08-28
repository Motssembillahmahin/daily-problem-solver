"""
AI-powered solution generator.
Generates full-stack solutions with React/Next.js frontend and Python backend.
"""

import os
import json
from typing import Dict, Any
from datetime import datetime


def determine_solution_type(problem: Dict) -> str:
    """Determine what type of solution to generate."""
    category = problem.get("category", "general")
    description = problem.get("description", "").lower()

    # Check for specific solution needs
    if any(w in description for w in ["website", "web app", "frontend", "ui", "dashboard"]):
        return "fullstack"

    if any(w in description for w in ["api", "backend", "server", "database"]):
        return "backend"

    if any(w in description for w in ["script", "automate", "cli", "tool", "process"]):
        return "script"

    if any(w in description for w in ["analyze", "data", "visualize", "chart", "report"]):
        return "data_analysis"

    return "fullstack"  # Default to fullstack


def generate_with_ollama(problem: Dict) -> Dict[str, Any]:
    """Generate solution using local Ollama model."""
    try:
        import ollama

        solution_type = determine_solution_type(problem)

        prompt = f"""Generate a complete {solution_type} solution for this problem:

PROBLEM: {problem['title']}
DESCRIPTION: {problem.get('description', 'N/A')}
CATEGORY: {problem.get('category', 'general')}

Generate the following files with complete, working code:

1. For fullstack:
   - frontend/app/page.tsx (Next.js page)
   - frontend/app/layout.tsx (Layout)
   - frontend/package.json
   - backend/main.py (FastAPI)
   - backend/requirements.txt
   - backend/agents/agent.py (AI agent)

2. For script:
   - solution.py (Complete script)
   - requirements.txt
   - README.md

Return the files as JSON with this format:
{{
    "files": {{
        "path/to/file": "file content here"
    }},
    "type": "{solution_type}"
}}"""

        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response["message"]["content"]

        # Try to parse JSON from response
        try:
            # Find JSON in the response
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end != -1:
                return json.loads(content[start:end])
        except json.JSONDecodeError:
            pass

        # Fallback to template
        return generate_template_solution(problem, solution_type)

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

    return {
        "files": files,
        "type": solution_type
    }


def generate_fullstack_template(problem: Dict) -> Dict[str, str]:
    """Generate full-stack template files."""
    title = problem["title"].replace(" ", "_").lower()

    return {
        "frontend/package.json": json.dumps({
            "name": f"{title}-frontend",
            "version": "1.0.0",
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start"
            },
            "dependencies": {
                "next": "14.0.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            }
        }, indent=2),

        "frontend/app/layout.tsx": '''import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
    title: "''' + problem['title'] + '''",
    description: "AI-powered solution",
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    )
}''',

        "frontend/app/page.tsx": '''"use client"
import { useState, useEffect } from 'react'

export default function Home() {
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetch('/api/solve')
            .then(res => res.json())
            .then(data => {
                setData(data)
                setLoading(false)
            })
    }, [])

    if (loading) return <div className="p-8">Loading...</div>

    return (
        <main className="p-8">
            <h1 className="text-3xl font-bold mb-4">''' + problem['title'] + '''</h1>
            <p className="text-gray-600 mb-8">''' + problem.get('description', '')[:200] + '''</p>
            <div className="bg-gray-50 p-6 rounded-lg">
                <h2 className="text-xl font-semibold mb-2">Solution</h2>
                <pre className="bg-white p-4 rounded overflow-auto">
                    {JSON.stringify(data, null, 2)}
                </pre>
            </div>
        </main>
    )
}''',

        "frontend/app/globals.css": '''@tailwind base;
@tailwind components;
@tailwind utilities;

body {
    font-family: system-ui, -apple-system, sans-serif;
}''',

        "backend/requirements.txt": '''fastapi==0.104.0
uvicorn==0.24.0
pydantic==2.5.0
ollama==0.1.0
requests==2.31.0''',

        "backend/main.py": '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

app = FastAPI(title="''' + problem['title'] + '''")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SolutionResponse(BaseModel):
    problem: str
    solution: str
    code: str

@app.get("/api/solve")
async def solve_problem():
    """AI-powered solution endpoint"""
    response = ollama.chat(
        model="llama3.2",
        messages=[{
            "role": "user",
            "content": "Provide a solution for: ''' + problem['title'] + '''"
        }]
    )
    return {
        "problem": "''' + problem['title'] + '''",
        "solution": response["message"]["content"],
        "code": "# Generated code here"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}''',

        "backend/agents/__init__.py": " ",
        "backend/agents/agent.py": '''import ollama
from typing import Dict, Any

class ProblemSolverAgent:
    """AI Agent that solves problems using local LLM"""

    def __init__(self, model: str = "llama3.2"):
        self.model = model

    def analyze(self, problem: Dict[str, Any]) -> str:
        """Analyze problem and suggest approach"""
        prompt = f"""
        Analyze this problem and suggest the best approach:
        Problem: {problem.get('title', '')}
        Description: {problem.get('description', '')}
        """

        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]

    def generate_code(self, problem: Dict[str, Any], approach: str) -> str:
        """Generate code solution"""
        prompt = f"""
        Generate Python code for:
        Problem: {problem.get('title', '')}
        Approach: {approach}
        """

        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]
'''
    }

    return files


def generate_backend_template(problem: Dict) -> Dict[str, str]:
    """Generate backend-only template files."""
    return {
        "requirements.txt": '''fastapi==0.104.0
uvicorn==0.24.0
ollama==0.1.0''',

        "main.py": '''from fastapi import FastAPI
import ollama

app = FastAPI(title="''' + problem['title'] + '''")

@app.get("/api/solve")
async def solve():
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": "Solve: ''' + problem['title'] + '''"}]
    )
    return {"solution": response["message"]["content"]}
'''
    }


def generate_script_template(problem: Dict) -> Dict[str, str]:
    """Generate script template files."""
    return {
        "solution.py": '''"""
Solution for: ''' + problem['title'] + '''
Generated on: ''' + datetime.now().strftime('%Y-%m-%d') + '''
"""

import ollama

def solve():
    """AI-powered solution"""
    response = ollama.chat(
        model="llama3.2",
        messages=[{
            "role": "user",
            "content": "Solve this problem step by step: ''' + problem['title'] + '''"
        }]
    )
    print(response["message"]["content"])
    return response["message"]["content"]

if __name__ == "__main__":
    solve()
''',

        "requirements.txt": "ollama==0.1.0"
    }


def generate_data_template(problem: Dict) -> Dict[str, str]:
    """Generate data analysis template files."""
    return {
        "requirements.txt": '''pandas==2.1.0
matplotlib==3.8.0
seaborn==0.13.0
ollama==0.1.0''',

        "solution.py": '''"""
Data Analysis Solution for: ''' + problem['title'] + '''
"""

import pandas as pd
import matplotlib.pyplot as plt
import ollama

def analyze():
    """Analyze data and generate insights"""
    # AI analysis
    response = ollama.chat(
        model="llama3.2",
        messages=[{
            "role": "user",
            "content": "Provide data analysis approach for: ''' + problem['title'] + '''"
        }]
    )
    print(response["message"]["content"])

if __name__ == "__main__":
    analyze()
'''
    }


def generate_solution(problem: Dict) -> Dict[str, Any]:
    """Main entry point for solution generation."""
    print(f"   Generating {determine_solution_type(problem)} solution...")

    # Try Ollama first
    solution = generate_with_ollama(problem)

    # Ensure we have files
    if not solution.get("files"):
        solution = generate_template_solution(
            problem,
            determine_solution_type(problem)
        )

    return solution
