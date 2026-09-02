"""
Smart Solution Generator - Creates REAL working solutions.
Not templates - actual code that solves the problem.
"""

import os
import json
import re
from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path

from scripts.matching import mentions


class SolutionGenerator:
    """Generates actual working solutions based on problem analysis."""

    # A problem must score at least this many keyword hits for a template to be
    # considered a fit. Below it, the library has nothing relevant and the
    # pipeline should move on rather than ship an unrelated tool.
    MIN_FIT = 2

    # Only templates that are actually implemented appear here.
    TEMPLATE_KEYWORDS = {
        "health_tracker": ["health", "fitness", "workout", "exercise", "calorie",
                            "steps", "sleep", "weight", "medical", "wellness"],
        "file_organizer": ["file", "files", "organize", "organise", "sort",
                            "folder", "directory", "rename", "duplicate"],
        "url_shortener": ["url", "shorten", "shortener", "link", "redirect", "slug"],
        "todo_api": ["todo", "task", "tasks", "checklist", "kanban", "backlog"],
        "weather_app": ["weather", "forecast", "temperature", "rain", "climate"],
        "json_formatter": ["json", "format", "beautify", "pretty print", "lint",
                            "minify", "validate", "unreadable"],
        "csv_analyzer": ["csv", "spreadsheet", "excel", "column", "rows",
                          "tabular", "dataset"],
        "password_generator": ["password", "passphrase", "credential", "random",
                                "secure", "generator"],
        "note_taker": ["note", "notes", "journal", "diary", "scratchpad"],
        "pomodoro_timer": ["pomodoro", "timer", "focus", "concentrate",
                            "distraction", "break"],
        "budget_tracker": ["budget", "expense", "expenses", "spending", "money",
                            "income", "finance", "cost"],
        "bookmark_manager": ["bookmark", "bookmarks", "read later", "saved links",
                              "tabs", "favourites", "favorites"],
        "text_summarizer": ["summarize", "summarise", "summary", "tldr",
                             "article", "long text", "condense"],
        "log_analyzer": ["log", "logs", "logfile", "stacktrace", "traceback",
                          "error rate", "monitor"],
        "backup_tool": ["backup", "backups", "restore", "snapshot", "archive",
                         "sync"],
        "email_validator": ["email", "e-mail", "mailbox", "smtp", "bounce",
                             "verify address"],
    }

    def __init__(self):
        self.solution_templates = {
            "file_organizer": self._file_organizer,
            "url_shortener": self._url_shortener,
            "todo_api": self._todo_api,
            "weather_app": self._weather_app,
            "json_formatter": self._json_formatter,
            "csv_analyzer": self._csv_analyzer,
            "password_generator": self._password_generator,
            "health_tracker": self._health_tracker,
            "note_taker": self._note_taker,
            "pomodoro_timer": self._pomodoro_timer,
            "budget_tracker": self._budget_tracker,
            "bookmark_manager": self._bookmark_manager,
            "text_summarizer": self._text_summarizer,
            "log_analyzer": self._log_analyzer,
            "backup_tool": self._backup_tool,
            "email_validator": self._email_validator,
        }

    def score_templates(self, problem: Dict) -> Dict[str, int]:
        """Score every template by how many of its keywords the problem mentions."""
        combined = " ".join([
            problem.get("title", ""),
            problem.get("description", ""),
            " ".join(problem.get("keywords", [])),
        ]).lower()

        return {
            name: sum(1 for kw in keywords if mentions(kw, combined))
            for name, keywords in self.TEMPLATE_KEYWORDS.items()
        }

    def analyze_problem(self, problem: Dict) -> str | None:
        """Return the best-fitting template, or None when the library has none."""
        scores = self.score_templates(problem)
        best = max(scores, key=scores.get)
        return best if scores[best] >= self.MIN_FIT else None

    def generate_solution(self, problem: Dict) -> Dict[str, Any] | None:
        """Generate a solution, or None when no template fits the problem."""
        solution_type = self.analyze_problem(problem)
        if solution_type is None:
            print(f"   No template fits: {problem.get('title', '')[:60]}")
            return None

        print(f"   Analyzed as: {solution_type}")
        files = self.solution_templates[solution_type](problem)

        return {
            "type": solution_type,
            "files": files,
            "description": f"Working solution for: {problem['title']}",
        }

    def _file_organizer(self, problem: Dict) -> Dict[str, str]:
        """Generate a file organizer script."""
        return {
            "solution.py": '''#!/usr/bin/env python3
"""
File Organizer - Automatically organizes files by type
Usage: python solution.py /path/to/folder
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

# File type mappings
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Code": [".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Data": [".json", ".csv", ".xml", ".sql", ".db"],
}

def organize_files(source_dir: str, dry_run: bool = False):
    """Organize files into folders by type."""
    source = Path(source_dir)
    if not source.exists():
        print(f"Error: {source} does not exist")
        return

    stats = defaultdict(int)
    
    for file_path in source.iterdir():
        if file_path.is_file():
            suffix = file_path.suffix.lower()
            
            # Find category
            category = "Other"
            for cat, extensions in FILE_TYPES.items():
                if suffix in extensions:
                    category = cat
                    break
            
            # Create target folder
            target_dir = source / category
            
            if not dry_run:
                target_dir.mkdir(exist_ok=True)
                target_file = target_dir / file_path.name
                
                # Handle duplicate names
                counter = 1
                while target_file.exists():
                    target_file = target_dir / f"{file_path.stem}_{counter}{suffix}"
                    counter += 1
                
                shutil.move(str(file_path), str(target_file))
            
            stats[category] += 1
            action = "Would move" if dry_run else "Moved"
            print(f"  {action}: {file_path.name} -> {category}/")

    print(f"\\nSummary: Organized {sum(stats.values())} files")
    for category, count in sorted(stats.items()):
        print(f"  {category}: {count} files")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python solution.py <folder_path> [--dry-run]")
        sys.exit(1)
    
    folder = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    
    if dry_run:
        print("DRY RUN - No files will be moved\\n")
    
    organize_files(folder, dry_run)
''',
            "requirements.txt": "# No external dependencies - uses Python standard library",
            "README.md": '''# File Organizer

Automatically organizes files in a folder by their type.

## Usage

```bash
# Preview changes (dry run)
python solution.py /path/to/folder --dry-run

# Actually organize files
python solution.py /path/to/folder
```

## Categories

- Images (jpg, png, gif, etc.)
- Documents (pdf, doc, txt, etc.)
- Videos (mp4, avi, mkv, etc.)
- Audio (mp3, wav, flac, etc.)
- Code (py, js, ts, etc.)
- Archives (zip, tar, etc.)
- Data (json, csv, etc.)
'''
        }

    def _url_shortener(self, problem: Dict) -> Dict[str, str]:
        """Generate a URL shortener."""
        return {
            "main.py": '''#!/usr/bin/env python3
"""
URL Shortener - Simple in-memory URL shortener
Usage: python main.py
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import hashlib
import string
import random

app = FastAPI(title="URL Shortener")

# In-memory storage
url_database = {}

class URLRequest(BaseModel):
    url: str
    custom_code: str = None

def generate_short_code(url: str) -> str:
    """Generate a short code from URL hash."""
    hash_obj = hashlib.md5(url.encode())
    return hash_obj.hexdigest()[:6]

@app.post("/shorten")
async def shorten_url(request: URLRequest):
    """Shorten a URL."""
    # Use custom code or generate one
    if request.custom_code:
        code = request.custom_code
    else:
        code = generate_short_code(request.url)
    
    # Store mapping
    url_database[code] = request.url
    
    return {
        "original": request.url,
        "shortened": f"http://localhost:8000/{code}",
        "code": code
    }

@app.get("/{code}")
async def redirect_to_url(code: str):
    """Redirect to original URL."""
    if code not in url_database:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return RedirectResponse(url=url_database[code])

@app.get("/stats/{code}")
async def get_stats(code: str):
    """Get URL statistics."""
    if code not in url_database:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return {
        "code": code,
        "original": url_database[code],
        "access_count": url_database.get(f"{code}_count", 0)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''',
            "requirements.txt": '''fastapi==0.104.0
uvicorn==0.24.0
pydantic==2.5.0''',
            "README.md": '''# URL Shortener

A simple URL shortener API built with FastAPI.

## Run

```bash
pip install -r requirements.txt
python main.py
```

## API Endpoints

- `POST /shorten` - Shorten a URL
- `GET /{code}` - Redirect to original URL
- `GET /stats/{code}` - Get URL statistics
'''
        }

    def _todo_api(self, problem: Dict) -> Dict[str, str]:
        """Generate a Todo API."""
        return {
            "main.py": '''#!/usr/bin/env python3
"""
Todo API - Full CRUD API for task management
Usage: python main.py
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
from pathlib import Path

app = FastAPI(title="Todo API")

# Simple file-based storage
TODO_FILE = "todos.json"

class Todo(BaseModel):
    title: str
    description: str = ""
    completed: bool = False
    priority: str = "medium"  # low, medium, high

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None

def load_todos() -> dict:
    if Path(TODO_FILE).exists():
        with open(TODO_FILE) as f:
            return json.load(f)
    return {"todos": [], "next_id": 1}

def save_todos(data: dict):
    with open(TODO_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.get("/todos")
async def get_todos():
    """Get all todos."""
    data = load_todos()
    return {"todos": data["todos"], "count": len(data["todos"])}

@app.post("/todos")
async def create_todo(todo: Todo):
    """Create a new todo."""
    data = load_todos()
    new_todo = {
        "id": data["next_id"],
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "priority": todo.priority,
        "created_at": "2026-01-01"
    }
    data["todos"].append(new_todo)
    data["next_id"] += 1
    save_todos(data)
    return new_todo

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    """Get a specific todo."""
    data = load_todos()
    for todo in data["todos"]:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, update: TodoUpdate):
    """Update a todo."""
    data = load_todos()
    for todo in data["todos"]:
        if todo["id"] == todo_id:
            if update.title is not None:
                todo["title"] = update.title
            if update.description is not None:
                todo["description"] = update.description
            if update.completed is not None:
                todo["completed"] = update.completed
            if update.priority is not None:
                todo["priority"] = update.priority
            save_todos(data)
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    """Delete a todo."""
    data = load_todos()
    data["todos"] = [t for t in data["todos"] if t["id"] != todo_id]
    save_todos(data)
    return {"message": "Todo deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
''',
            "requirements.txt": '''fastapi==0.104.0
uvicorn==0.24.0
pydantic==2.5.0''',
            "README.md": '''# Todo API

A full CRUD API for task management.

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Endpoints

- `GET /todos` - List all todos
- `POST /todos` - Create a todo
- `GET /todos/{id}` - Get a todo
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo
'''
        }

    def _weather_app(self, problem: Dict) -> Dict[str, str]:
        """Generate a weather app."""
        return {
            "app.py": '''#!/usr/bin/env python3
"""
Weather App - CLI tool to check weather
Usage: python app.py <city>
"""

import requests
import sys

def get_weather(city: str) -> dict:
    """Get weather for a city using Open-Meteo (free, no API key)."""
    # First, geocode the city
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_response = requests.get(geo_url)
    geo_data = geo_response.json()
    
    if not geo_data.get("results"):
        return {"error": f"City '{city}' not found"}
    
    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]
    name = geo_data["results"][0]["name"]
    
    # Get weather
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
    )
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    
    current = weather_data.get("current", {})
    
    # Weather codes to descriptions
    weather_codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
    }
    
    return {
        "city": name,
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "wind_speed": current.get("wind_speed_10m"),
        "weather": weather_codes.get(current.get("weather_code"), "Unknown")
    }

def display_weather(data: dict):
    """Display weather information."""
    if "error" in data:
        print(f"Error: {data['error']}")
        return
    
    print(f"\\nWeather for {data['city']}:")
    print(f"  Temperature: {data['temperature']}°C")
    print(f"  Weather: {data['weather']}")
    print(f"  Humidity: {data['humidity']}%")
    print(f"  Wind Speed: {data['wind_speed']} km/h\\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py <city>")
        sys.exit(1)
    
    city = sys.argv[1]
    weather = get_weather(city)
    display_weather(weather)
''',
            "requirements.txt": "requests>=2.31.0",
            "README.md": '''# Weather App

CLI tool to check weather for any city.

## Usage

```bash
pip install -r requirements.txt
python app.py London
python app.py "New York"
```

Uses Open-Meteo API - free, no API key required.
'''
        }

    def _json_formatter(self, problem: Dict) -> Dict[str, str]:
        """Generate a JSON formatter."""
        return {
            "format_json.py": '''#!/usr/bin/env python3
"""
JSON Formatter - Format and validate JSON files
Usage: python format_json.py <file.json> [--indent 2] [--sort]
"""

import json
import sys
from pathlib import Path

def format_json(file_path: str, indent: int = 2, sort_keys: bool = False) -> str:
    """Format a JSON file."""
    try:
        with open(file_path) as f:
            data = json.load(f)
        
        formatted = json.dumps(data, indent=indent, sort_keys=sort_keys)
        
        # Write back to file
        with open(file_path, "w") as f:
            f.write(formatted)
        
        return f"Formatted {file_path} ({len(formatted)} bytes)"
    
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {e}"
    except FileNotFoundError:
        return f"File not found: {file_path}"

def validate_json(file_path: str) -> dict:
    """Validate a JSON file."""
    try:
        with open(file_path) as f:
            data = json.load(f)
        
        return {
            "valid": True,
            "type": type(data).__name__,
            "size": len(json.dumps(data))
        }
    except json.JSONDecodeError as e:
        return {
            "valid": False,
            "error": str(e)
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python format_json.py <file.json> [--indent N] [--sort]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    indent = 2
    sort_keys = False
    
    if "--indent" in sys.argv:
        idx = sys.argv.index("--indent")
        indent = int(sys.argv[idx + 1])
    
    if "--sort" in sys.argv:
        sort_keys = True
    
    result = format_json(file_path, indent, sort_keys)
    print(result)
''',
            "requirements.txt": "# No external dependencies",
            "README.md": '''# JSON Formatter

CLI tool to format and validate JSON files.

## Usage

```bash
# Format JSON file
python format_json.py data.json

# Format with custom indent
python format_json.py data.json --indent 4

# Format with sorted keys
python format_json.py data.json --sort

# Validate JSON
python format_json.py data.json
```
'''
        }

    def _csv_analyzer(self, problem: Dict) -> Dict[str, str]:
        """Generate a CSV analyzer."""
        return {
            "analyze_csv.py": '''#!/usr/bin/env python3
"""
CSV Analyzer - Analyze CSV files and generate reports
Usage: python analyze_csv.py <file.csv>
"""

import csv
import sys
from collections import Counter

def analyze_csv(file_path: str):
    """Analyze a CSV file."""
    try:
        with open(file_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            columns = reader.fieldnames
        
        if not rows:
            print("CSV file is empty")
            return
        
        print(f"\\nCSV Analysis: {file_path}")
        print("=" * 50)
        print(f"Total rows: {len(rows)}")
        print(f"Columns: {len(columns)}")
        print(f"Column names: {', '.join(columns)}")
        
        # Analyze each column
        for col in columns:
            values = [row[col] for row in rows if row[col]]
            
            print(f"\\nColumn: {col}")
            print(f"  Non-empty values: {len(values)}")
            print(f"  Empty values: {len(rows) - len(values)}")
            
            # Check if numeric
            try:
                nums = [float(v) for v in values]
                print(f"  Type: Numeric")
                print(f"  Min: {min(nums)}")
                print(f"  Max: {max(nums)}")
                print(f"  Avg: {sum(nums)/len(nums):.2f}")
            except ValueError:
                # Categorical
                unique = set(values)
                print(f"  Type: Categorical")
                print(f"  Unique values: {len(unique)}")
                if len(unique) <= 10:
                    counts = Counter(values)
                    for val, count in counts.most_common(5):
                        print(f"    {val}: {count}")
        
        print("\\n" + "=" * 50)
    
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_csv.py <file.csv>")
        sys.exit(1)
    
    analyze_csv(sys.argv[1])
''',
            "requirements.txt": "# No external dependencies",
            "README.md": '''# CSV Analyzer

CLI tool to analyze CSV files and generate reports.

## Usage

```bash
python analyze_csv.py data.csv
```

## Features

- Row and column counts
- Data types per column
- Numeric statistics (min, max, avg)
- Categorical value counts
- Missing value detection
'''
        }

    def _password_generator(self, problem: Dict) -> Dict[str, str]:
        """Generate a password generator."""
        return {
            "generate_password.py": '''#!/usr/bin/env python3
"""
Password Generator - Generate secure passwords
Usage: python generate_password.py [--length 16] [--count 5]
"""

import secrets
import string
import argparse

def generate_password(length: int = 16, use_special: bool = True) -> str:
    """Generate a secure password."""
    characters = string.ascii_letters + string.digits
    if use_special:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one of each type
    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
    ]
    
    if use_special:
        password.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
    
    # Fill the rest
    password.extend(secrets.choice(characters) for _ in range(length - len(password)))
    
    # Shuffle
    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    
    return "".join(password_list)

def check_password_strength(password: str) -> dict:
    """Check password strength."""
    checks = {
        "length": len(password) >= 12,
        "uppercase": any(c.isupper() for c in password),
        "lowercase": any(c.islower() for c in password),
        "digits": any(c.isdigit() for c in password),
        "special": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
    }
    
    score = sum(checks.values())
    
    return {
        "password": password,
        "score": score,
        "max_score": 5,
        "strength": ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"][score - 1],
        "checks": checks
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate secure passwords")
    parser.add_argument("--length", type=int, default=16, help="Password length")
    parser.add_argument("--count", type=int, default=1, help="Number of passwords")
    parser.add_argument("--no-special", action="store_true", help="Exclude special characters")
    
    args = parser.parse_args()
    
    print(f"\\nGenerating {args.count} password(s) (length: {args.length}):\\n")
    
    for i in range(args.count):
        password = generate_password(args.length, not args.no_special)
        strength = check_password_strength(password)
        
        print(f"{i+1}. {password}")
        print(f"   Strength: {strength['strength']} ({strength['score']}/{strength['max_score']})")
        print()
''',
            "requirements.txt": "# No external dependencies",
            "README.md": '''# Password Generator

Generate secure passwords with strength checking.

## Usage

```bash
# Generate single password
python generate_password.py

# Generate 5 passwords
python generate_password.py --count 5

# Generate 32-char password
python generate_password.py --length 32

# Without special characters
python generate_password.py --no-special
```
'''
        }

    def _text_summarizer(self, problem: Dict) -> Dict[str, str]:
        """Generate a text summarizer."""
        return {
            "summarize.py": '''#!/usr/bin/env python3
"""
Text Summarizer - Summarize text using extractive method
Usage: python summarize.py <file.txt> [--sentences 3]
"""

import re
import sys
from collections import Counter

def split_sentences(text: str) -> list:
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if len(s) > 10]

def score_sentences(sentences: list, word_frequencies: dict) -> list:
    """Score sentences based on word frequency."""
    scores = []
    for sentence in sentences:
        words = re.findall(r'\\w+', sentence.lower())
        score = sum(word_frequencies.get(word, 0) for word in words)
        scores.append((score, sentence))
    return scores

def summarize(text: str, num_sentences: int = 3) -> str:
    """Summarize text using extractive method."""
    sentences = split_sentences(text)
    
    if len(sentences) <= num_sentences:
        return text
    
    # Calculate word frequencies
    words = re.findall(r'\\w+', text.lower())
    word_freq = Counter(words)
    
    # Normalize frequencies
    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] /= max_freq
    
    # Score and rank sentences
    scored = score_sentences(sentences, word_freq)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Get top sentences
    top_sentences = [s[1] for s in scored[:num_sentences]]
    
    # Maintain original order
    ordered = []
    for sentence in sentences:
        if sentence in top_sentences:
            ordered.append(sentence)
    
    return " ".join(ordered)

def summarize_file(file_path: str, num_sentences: int = 3):
    """Summarize a text file."""
    try:
        with open(file_path) as f:
            text = f.read()
        
        summary = summarize(text, num_sentences)
        
        print(f"\\nOriginal: {len(text)} characters, {len(split_sentences(text))} sentences")
        print(f"Summary: {len(summary)} characters, {len(split_sentences(summary))} sentences")
        print(f"\\nSummary:\\n{'='*50}\\n{summary}\\n{'='*50}")
    
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python summarize.py <file.txt> [--sentences N]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    num_sentences = 3
    
    if "--sentences" in sys.argv:
        idx = sys.argv.index("--sentences")
        num_sentences = int(sys.argv[idx + 1])
    
    summarize_file(file_path, num_sentences)
''',
            "requirements.txt": "# No external dependencies",
            "README.md": '''# Text Summarizer

Summarize text files using extractive summarization.

## Usage

```bash
python summarize.py article.txt
python summarize.py article.txt --sentences 5
```
'''
        }

    def _log_analyzer(self, problem: Dict) -> Dict[str, str]:
        """Generate a log analyzer."""
        return {
            "analyze_logs.py": '''#!/usr/bin/env python3
"""
Log Analyzer - Analyze log files for patterns and errors
Usage: python analyze_logs.py <logfile.log>
"""

import re
import sys
from collections import Counter, defaultdict
from datetime import datetime

def parse_log_line(line: str) -> dict:
    """Parse a log line."""
    patterns = [
        r'(\\d{4}-\\d{2}-\\d{2})\\s+(\\d{2}:\\d{2}:\\d{2})\\s+(\\w+)\\s+(.*)',
        r'\\[(.*?)\\]\\s+\\[(.*?)\\]\\s+(.*)',
    ]
    
    for pattern in patterns:
        match = re.match(pattern, line)
        if match:
            return {"raw": line, "parts": match.groups()}
    
    return {"raw": line, "parts": ()}

def analyze_logs(file_path: str):
    """Analyze a log file."""
    try:
        with open(file_path) as f:
            lines = f.readlines()
        
        print(f"\\nLog Analysis: {file_path}")
        print("=" * 60)
        print(f"Total lines: {len(lines)}")
        
        # Count log levels
        level_patterns = {
            "ERROR": r'\\bERROR\\b',
            "WARNING": r'\\bWARN(ING)?\\b',
            "INFO": r'\\bINFO\\b',
            "DEBUG": r'\\bDEBUG\\b',
        }
        
        level_counts = Counter()
        error_lines = []
        
        for line in lines:
            for level, pattern in level_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    level_counts[level] += 1
                    if level == "ERROR":
                        error_lines.append(line.strip())
        
        print(f"\\nLog Levels:")
        for level, count in level_counts.most_common():
            print(f"  {level}: {count}")
        
        # Show recent errors
        if error_lines:
            print(f"\\nRecent Errors (last 5):")
            for line in error_lines[-5:]:
                print(f"  {line[:100]}...")
        
        print("\\n" + "=" * 60)
    
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_logs.py <logfile.log>")
        sys.exit(1)
    
    analyze_logs(sys.argv[1])
''',
            "requirements.txt": "# No external dependencies",
            "README.md": '''# Log Analyzer

Analyze log files for patterns, errors, and statistics.

## Usage

```bash
python analyze_logs.py app.log
```

## Features

- Total line count
- Log level distribution
- Error message extraction
- Pattern detection
'''
        }

    def _backup_tool(self, problem: Dict) -> Dict[str, str]:
        """Generate a backup tool."""
        return {
            "backup.py": '''#!/usr/bin/env python3
"""
Backup Tool - Backup files and directories
Usage: python backup.py <source> <destination>
"""

import shutil
import sys
from pathlib import Path
from datetime import datetime

def create_backup(source: str, destination: str):
    """Create a backup of source to destination."""
    source_path = Path(source)
    dest_path = Path(destination)
    
    if not source_path.exists():
        print(f"Error: Source does not exist - {source}")
        return False
    
    # Create timestamped backup folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"
    backup_path = dest_path / backup_name
    
    try:
        print(f"Backing up: {source_path}")
        print(f"To: {backup_path}")
        
        if source_path.is_dir():
            shutil.copytree(source_path, backup_path)
        else:
            backup_path.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, backup_path / source_path.name)
        
        print(f"Backup completed successfully!")
        print(f"Size: {sum(f.stat().st_size for f in backup_path.rglob('*') if f.is_file())} bytes")
        return True
    
    except Exception as e:
        print(f"Backup failed: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python backup.py <source> <destination>")
        sys.exit(1)
    
    source = sys.argv[1]
    destination = sys.argv[2]
    
    create_backup(source, destination)
''',
            "requirements.txt": "# No external dependencies",
            "README.md": '''# Backup Tool

Simple backup utility for files and directories.

## Usage

```bash
python backup.py /path/to/source /path/to/backup
```

Creates timestamped backups with size reporting.
'''
        }

    def _email_validator(self, problem: Dict) -> Dict[str, str]:
        """Generate an email validator."""
        return {
            "validate_email.py": '''#!/usr/bin/env python3
"""
Email Validator - Validate email addresses
Usage: python validate_email.py <email>
"""

import re
import sys

def validate_email(email: str) -> dict:
    """Validate an email address."""
    # Basic regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    is_valid = bool(re.match(pattern, email))
    
    # Additional checks
    checks = {
        "format": is_valid,
        "has_at": "@" in email,
        "has_domain": "." in email.split("@")[-1] if "@" in email else False,
        "no_spaces": " " not in email,
        "length": len(email) <= 254,
    }
    
    return {
        "email": email,
        "valid": all(checks.values()),
        "checks": checks
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_email.py <email>")
        sys.exit(1)
    
    email = sys.argv[1]
    result = validate_email(email)
    
    print(f"\\nEmail: {result['email']}")
    print(f"Valid: {result['valid']}")
    print(f"\\nChecks:")
    for check, passed in result['checks'].items():
        print(f"  {check}: {'\\u2713' if passed else '\\u2717'}")
''',
            "requirements.txt": "# No external dependencies",
            "README.md": '''# Email Validator

Validate email addresses with detailed checks.

## Usage

```bash
python validate_email.py user@example.com
```
'''
        }

    def _health_tracker(self, problem: Dict) -> Dict[str, str]:
        """Generate a health tracking app."""
        return {
            "health_tracker.py": '''#!/usr/bin/env python3
"""
Health Tracker - Track daily health metrics
Usage: python health_tracker.py [command] [args]
Commands:
  log <type> <value>  - Log a metric (water, steps, sleep, weight)
  show [date]         - Show metrics for date (default: today)
  stats               - Show weekly statistics
  export              - Export to CSV
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

DATA_FILE = "health_data.json"

def load_data():
    if Path(DATA_FILE).exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"metrics": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def log_metric(metric_type: str, value: float):
    """Log a health metric."""
    data = load_data()
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "type": metric_type.lower(),
        "value": value
    }
    data["metrics"].append(entry)
    save_data(data)
    print(f"Logged: {metric_type} = {value}")

def show_metrics(date: str = None):
    """Show metrics for a specific date."""
    data = load_data()
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    metrics = [m for m in data["metrics"] if m["date"] == date]
    
    if not metrics:
        print(f"No metrics found for {date}")
        return
    
    print(f"\\nHealth Metrics for {date}:")
    print("=" * 40)
    
    grouped = defaultdict(list)
    for m in metrics:
        grouped[m["type"]].append(m["value"])
    
    for metric_type, values in grouped.items():
        total = sum(values)
        avg = total / len(values)
        print(f"  {metric_type.title()}: {total:.1f} (avg: {avg:.1f})")

def show_stats():
    """Show weekly statistics."""
    data = load_data()
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    
    week_metrics = [
        m for m in data["metrics"]
        if datetime.strptime(m["date"], "%Y-%m-%d") >= week_ago
    ]
    
    if not week_metrics:
        print("No data for the past week")
        return
    
    print("\\nWeekly Statistics:")
    print("=" * 40)
    
    grouped = defaultdict(list)
    for m in week_metrics:
        grouped[m["type"]].append(m["value"])
    
    for metric_type, values in grouped.items():
        total = sum(values)
        avg = total / len(values)
        print(f"  {metric_type.title()}:")
        print(f"    Total: {total:.1f}")
        print(f"    Average: {avg:.1f}")
        print(f"    Entries: {len(values)}")

def export_csv():
    """Export data to CSV."""
    data = load_data()
    
    if not data["metrics"]:
        print("No data to export")
        return
    
    filename = f"health_data_{datetime.now().strftime('%Y%m%d')}.csv"
    
    with open(filename, "w") as f:
        f.write("date,time,type,value\\n")
        for m in data["metrics"]:
            f.write(f"{m['date']},{m['time']},{m['type']},{m['value']}\\n")
    
    print(f"Exported to {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "log" and len(sys.argv) >= 4:
        log_metric(sys.argv[2], float(sys.argv[3]))
    elif command == "show":
        date = sys.argv[2] if len(sys.argv) > 2 else None
        show_metrics(date)
    elif command == "stats":
        show_stats()
    elif command == "export":
        export_csv()
    else:
        print(__doc__)
''',
            "requirements.txt": "# No external dependencies",
            "README.md": '''# Health Tracker

Track daily health metrics like water intake, steps, sleep, and weight.

## Usage

```bash
# Log metrics
python health_tracker.py log water 8
python health_tracker.py log steps 10000
python health_tracker.py log sleep 7.5
python health_tracker.py log weight 70

# View today's metrics
python health_tracker.py show

# View specific date
python health_tracker.py show 2026-08-28

# Weekly statistics
python health_tracker.py stats

# Export to CSV
python health_tracker.py export
```

## Metrics Tracked

- Water (glasses)
- Steps
- Sleep (hours)
- Weight (kg)
'''
        }

    def _note_taker(self, problem: Dict) -> Dict[str, str]:
        """Generate a note-taking app."""
        return {
            "notes.py": '''#!/usr/bin/env python3
"""
Note Taker - Simple CLI note-taking app
Usage: python notes.py [command] [args]
Commands:
  add <title> <content>  - Add a new note
  list                   - List all notes
  show <id>              - Show a specific note
  search <query>         - Search notes
  delete <id>            - Delete a note
"""

import json
import sys
from datetime import datetime
from pathlib import Path

NOTES_FILE = "notes.json"

def load_notes():
    if Path(NOTES_FILE).exists():
        with open(NOTES_FILE) as f:
            return json.load(f)
    return {"notes": [], "next_id": 1}

def save_notes(data):
    with open(NOTES_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_note(title: str, content: str):
    """Add a new note."""
    data = load_notes()
    note = {
        "id": data["next_id"],
        "title": title,
        "content": content,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat()
    }
    data["notes"].append(note)
    data["next_id"] += 1
    save_notes(data)
    print(f"Note {note['id']} added: {title}")

def list_notes():
    """List all notes."""
    data = load_notes()
    if not data["notes"]:
        print("No notes found")
        return
    
    print("\\nYour Notes:")
    print("=" * 50)
    for note in data["notes"]:
        print(f"  [{note['id']}] {note['title']}")
        print(f"      Created: {note['created'][:10]}")
        print()

def show_note(note_id: int):
    """Show a specific note."""
    data = load_notes()
    for note in data["notes"]:
        if note["id"] == note_id:
            print(f"\\nNote #{note['id']}: {note['title']}")
            print(f"Created: {note['created']}")
            print(f"Updated: {note['updated']}")
            print("\\n" + "-" * 50)
            print(note["content"])
            print("-" * 50)
            return
    print(f"Note {note_id} not found")

def search_notes(query: str):
    """Search notes by content."""
    data = load_notes()
    results = []
    
    for note in data["notes"]:
        if (query.lower() in note["title"].lower() or
            query.lower() in note["content"].lower()):
            results.append(note)
    
    if not results:
        print(f"No notes matching '{query}'")
        return
    
    print(f"\\nSearch results for '{query}':")
    print("=" * 50)
    for note in results:
        print(f"  [{note['id']}] {note['title']}")
        print()

def delete_note(note_id: int):
    """Delete a note."""
    data = load_notes()
    data["notes"] = [n for n in data["notes"] if n["id"] != note_id]
    save_notes(data)
    print(f"Note {note_id} deleted")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add" and len(sys.argv) >= 4:
        add_note(sys.argv[2], " ".join(sys.argv[3:]))
    elif command == "list":
        list_notes()
    elif command == "show" and len(sys.argv) >= 3:
        show_note(int(sys.argv[2]))
    elif command == "search" and len(sys.argv) >= 3:
        search_notes(" ".join(sys.argv[2:]))
    elif command == "delete" and len(sys.argv) >= 3:
        delete_note(int(sys.argv[2]))
    else:
        print(__doc__)
''',
            "requirements.txt": "# No external dependencies",
            "README.md": '''# Note Taker

Simple CLI note-taking app.

## Usage

```bash
python notes.py add "My Note" "This is the content"
python notes.py list
python notes.py show 1
python notes.py search "keyword"
python notes.py delete 1
```
'''
        }

    def _pomodoro_timer(self, problem: Dict) -> Dict[str, str]:
        """Generate a Pomodoro timer."""
        return {
            "pomodoro.py": '''#!/usr/bin/env python3
"""
Pomodoro Timer - Productivity timer
Usage: python pomodoro.py [work_min] [break_min]
"""

import time
import sys
from datetime import datetime

def countdown(minutes: int, label: str):
    """Display countdown timer."""
    total_seconds = minutes * 60
    
    print(f"\\n{label} - {minutes} minutes")
    print("Press Ctrl+C to stop\\n")
    
    try:
        for remaining in range(total_seconds, 0, -1):
            mins, secs = divmod(remaining, 60)
            print(f"\\r  {mins:02d}:{secs:02d} remaining", end="", flush=True)
            time.sleep(1)
        
        print(f"\\r  00:00 - {label} complete!    ")
        print("\\a")  # Bell sound
        return True
    
    except KeyboardInterrupt:
        print(f"\\n\\n  {label} stopped by user")
        return False

def run_pomodoro(work_min: int = 25, break_min: int = 5, sessions: int = 4):
    """Run Pomodoro sessions."""
    print("=" * 50)
    print("  POMODORO TIMER")
    print(f"  Work: {work_min} min | Break: {break_min} min | Sessions: {sessions}")
    print("=" * 50)
    
    for session in range(1, sessions + 1):
        print(f"\\n--- Session {session}/{sessions} ---")
        
        # Work phase
        if not countdown(work_min, "WORK"):
            break
        
        # Break phase (short break except after last session)
        if session < sessions:
            countdown(break_min, "BREAK")
        else:
            print("\\n  All sessions complete! Great work!")
    
    print("\\n" + "=" * 50)

if __name__ == "__main__":
    work = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    brk = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    try:
        run_pomodoro(work, brk)
    except KeyboardInterrupt:
        print("\\n\\nTimer stopped. Goodbye!")
''',
            "requirements.txt": "# No external dependencies",
            "README.md": '''# Pomodoro Timer

Productivity timer for focused work sessions.

## Usage

```bash
# Default: 25 min work, 5 min break
python pomodoro.py

# Custom: 45 min work, 10 min break
python pomodoro.py 45 10
```

## Features

- Visual countdown display
- Audio notification when complete
- 4 work sessions by default
- Ctrl+C to stop
'''
        }

    def _budget_tracker(self, problem: Dict) -> Dict[str, str]:
        """Generate a budget tracker."""
        return {
            "budget.py": '''#!/usr/bin/env python3
"""
Budget Tracker - Track income and expenses
Usage: python budget.py [command] [args]
Commands:
  add <income|expense> <category> <amount> [description]
  show                  - Show current month summary
  history [month]       - Show transaction history
  categories            - Show spending by category
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

BUDGET_FILE = "budget_data.json"

def load_data():
    if Path(BUDGET_FILE).exists():
        with open(BUDGET_FILE) as f:
            return json.load(f)
    return {"transactions": []}

def save_data(data):
    with open(BUDGET_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_transaction(txn_type: str, category: str, amount: float, description: str = ""):
    """Add a transaction."""
    data = load_data()
    transaction = {
        "date": datetime.now().isoformat(),
        "type": txn_type.lower(),
        "category": category,
        "amount": amount,
        "description": description
    }
    data["transactions"].append(transaction)
    save_data(data)
    print(f"Added: {txn_type} - {category}: ${amount:.2f}")

def show_summary():
    """Show current month summary."""
    data = load_data()
    current_month = datetime.now().strftime("%Y-%m")
    
    month_txns = [
        t for t in data["transactions"]
        if t["date"][:7] == current_month
    ]
    
    if not month_txns:
        print("No transactions this month")
        return
    
    income = sum(t["amount"] for t in month_txns if t["type"] == "income")
    expenses = sum(t["amount"] for t in month_txns if t["type"] == "expense")
    
    print(f"\\nBudget Summary - {current_month}")
    print("=" * 40)
    print(f"  Income:   ${income:>10.2f}")
    print(f"  Expenses: ${expenses:>10.2f}")
    print(f"  Balance:  ${income - expenses:>10.2f}")
    print()

def show_history(month: str = None):
    """Show transaction history."""
    data = load_data()
    
    if month is None:
        month = datetime.now().strftime("%Y-%m")
    
    txns = [t for t in data["transactions"] if t["date"][:7] == month]
    
    if not txns:
        print(f"No transactions for {month}")
        return
    
    print(f"\\nTransactions - {month}")
    print("=" * 60)
    
    for t in txns:
        icon = "+" if t["type"] == "income" else "-"
        print(f"  {t['date'][:10]} {icon} {t['category']:15} ${t['amount']:>8.2f}  {t.get('description', '')}")

def show_categories():
    """Show spending by category."""
    data = load_data()
    current_month = datetime.now().strftime("%Y-%m")
    
    expenses = [
        t for t in data["transactions"]
        if t["date"][:7] == current_month and t["type"] == "expense"
    ]
    
    if not expenses:
        print("No expenses this month")
        return
    
    by_category = defaultdict(float)
    for t in expenses:
        by_category[t["category"]] += t["amount"]
    
    print(f"\\nSpending by Category - {current_month}")
    print("=" * 40)
    
    for category, total in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category:15} ${total:>10.2f}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add" and len(sys.argv) >= 5:
        desc = " ".join(sys.argv[5:]) if len(sys.argv) > 5 else ""
        add_transaction(sys.argv[2], sys.argv[3], float(sys.argv[4]), desc)
    elif command == "show":
        show_summary()
    elif command == "history":
        month = sys.argv[2] if len(sys.argv) > 2 else None
        show_history(month)
    elif command == "categories":
        show_categories()
    else:
        print(__doc__)
''',
            "requirements.txt": "# No external dependencies",
            "README.md": '''# Budget Tracker

Track income and expenses by category.

## Usage

```bash
# Add income
python budget.py add income salary 5000 "Monthly salary"

# Add expense
python budget.py add expense food 45.50 "Groceries"

# Show monthly summary
python budget.py show

# View history
python budget.py history
python budget.py history 2026-08

# Spending by category
python budget.py categories
```
'''
        }

    def _bookmark_manager(self, problem: Dict) -> Dict[str, str]:
        """Generate a bookmark manager."""
        return {
            "bookmarks.py": '''#!/usr/bin/env python3
"""
Bookmark Manager - Save and organize bookmarks
Usage: python bookmarks.py [command] [args]
Commands:
  add <url> [title] [tags]  - Add a bookmark
  list [tag]                - List bookmarks (optionally filter by tag)
  search <query>            - Search bookmarks
  delete <id>               - Delete a bookmark
  tags                      - List all tags
"""

import json
import sys
from datetime import datetime
from pathlib import Path

BOOKMARKS_FILE = "bookmarks.json"

def load_data():
    if Path(BOOKMARKS_FILE).exists():
        with open(BOOKMARKS_FILE) as f:
            return json.load(f)
    return {"bookmarks": [], "next_id": 1}

def save_data(data):
    with open(BOOKMARKS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_bookmark(url: str, title: str = "", tags: str = ""):
    """Add a bookmark."""
    data = load_data()
    bookmark = {
        "id": data["next_id"],
        "url": url,
        "title": title or url,
        "tags": [t.strip() for t in tags.split(",") if t.strip()],
        "created": datetime.now().isoformat()
    }
    data["bookmarks"].append(bookmark)
    data["next_id"] += 1
    save_data(data)
    print(f"Bookmark {bookmark['id']} added: {bookmark['title']}")

def list_bookmarks(tag: str = None):
    """List bookmarks."""
    data = load_data()
    bookmarks = data["bookmarks"]
    
    if tag:
        bookmarks = [b for b in bookmarks if tag in b.get("tags", [])]
    
    if not bookmarks:
        print("No bookmarks found")
        return
    
    print("\\nYour Bookmarks:")
    print("=" * 60)
    for b in bookmarks:
        tags = ", ".join(b.get("tags", []))
        print(f"  [{b['id']}] {b['title']}")
        print(f"      URL: {b['url']}")
        if tags:
            print(f"      Tags: {tags}")
        print()

def search_bookmarks(query: str):
    """Search bookmarks."""
    data = load_data()
    results = []
    
    for b in data["bookmarks"]:
        if (query.lower() in b["url"].lower() or
            query.lower() in b["title"].lower() or
            query.lower() in " ".join(b.get("tags", []))):
            results.append(b)
    
    if not results:
        print(f"No bookmarks matching '{query}'")
        return
    
    print(f"\\nSearch results for '{query}':")
    print("=" * 60)
    for b in results:
        print(f"  [{b['id']}] {b['title']}")
        print(f"      {b['url']}")
        print()

def list_tags():
    """List all tags."""
    data = load_data()
    all_tags = set()
    for b in data["bookmarks"]:
        all_tags.update(b.get("tags", []))
    
    if not all_tags:
        print("No tags found")
        return
    
    print("\\nAll Tags:")
    print("=" * 40)
    for tag in sorted(all_tags):
        print(f"  - {tag}")

def delete_bookmark(bookmark_id: int):
    """Delete a bookmark."""
    data = load_data()
    data["bookmarks"] = [b for b in data["bookmarks"] if b["id"] != bookmark_id]
    save_data(data)
    print(f"Bookmark {bookmark_id} deleted")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "add" and len(sys.argv) >= 3:
        title = sys.argv[3] if len(sys.argv) > 3 else ""
        tags = sys.argv[4] if len(sys.argv) > 4 else ""
        add_bookmark(sys.argv[2], title, tags)
    elif command == "list":
        tag = sys.argv[2] if len(sys.argv) > 2 else None
        list_bookmarks(tag)
    elif command == "search" and len(sys.argv) >= 3:
        search_bookmarks(" ".join(sys.argv[2:]))
    elif command == "tags":
        list_tags()
    elif command == "delete" and len(sys.argv) >= 3:
        delete_bookmark(int(sys.argv[2]))
    else:
        print(__doc__)
''',
            "requirements.txt": "# No external dependencies",
            "README.md": '''# Bookmark Manager

Save and organize bookmarks with tags.

## Usage

```bash
# Add bookmark
python bookmarks.py add https://example.com "Example Site" "reference,tools"

# List all
python bookmarks.py list

# Filter by tag
python bookmarks.py list tools

# Search
python bookmarks.py search "example"

# List tags
python bookmarks.py tags

# Delete
python bookmarks.py delete 1
```
'''
        }


def generate_solution(problem: Dict) -> Dict[str, Any] | None:
    """Main entry point. Returns None when no template fits."""
    generator = SolutionGenerator()
    return generator.generate_solution(problem)
