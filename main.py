"""
Daily Problem Solver - Main Orchestrator
AI-powered system that scrapes real-world problems and generates full-stack solutions.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict

from scripts.dates import today_str
from scripts.scraper import scrape_all_sources
from scripts.extractor import extract_problems
from scripts.dedup import check_uniqueness
from scripts.smart_solver import generate_solution
from scripts.doc_generator import generate_documentation

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SOLUTIONS_DIR = BASE_DIR / "solutions"
HISTORY_FILE = DATA_DIR / "solved_problems.json"


def load_history():
    """Load previously solved problems."""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"problems": []}


def save_history(history):
    """Save solved problems history."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def write_solution_files(
    problem_dir: Path, date_str: str, problem: Dict, solution: Dict
) -> None:
    """Write metadata, the problem statement, and the generated solution files."""
    with open(problem_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump({
            "date": date_str,
            "problem": problem,
            "solution_type": solution["type"],
            "source": problem.get("source", "unknown"),
            "category": problem.get("category", "general")
        }, f, indent=2, ensure_ascii=False)

    with open(problem_dir / "PROBLEM.md", "w", encoding="utf-8") as f:
        f.write(f"# Problem: {problem['title']}\n\n")
        f.write(f"**Date:** {date_str}\n\n")
        f.write(f"**Source:** {problem.get('source', 'N/A')}\n\n")
        f.write(f"**Category:** {problem.get('category', 'N/A')}\n\n")
        f.write(f"**Why Selected:** {problem.get('reason', 'Unique and relevant')}\n\n")
        f.write(f"## Description\n\n{problem.get('description', 'N/A')}\n\n")
        f.write(f"## Original URL\n\n{problem.get('url', 'N/A')}\n")

    for filename, content in solution.get("files", {}).items():
        file_path = problem_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)


def run():
    """Main pipeline."""
    print("=" * 60)
    print("DAILY PROBLEM SOLVER - Starting Pipeline")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Step 1: Scrape all sources
    print("\n[1/5] Scraping problem sources...")
    raw_content = scrape_all_sources()
    print(f"   Scraped {len(raw_content)} items from sources")

    # Step 2: Extract problems
    print("\n[2/5] Extracting problems...")
    problems = extract_problems(raw_content)
    print(f"   Found {len(problems)} potential problems")

    # Step 3: Dedup check
    print("\n[3/5] Checking uniqueness...")
    history = load_history()
    unique_problems = check_uniqueness(problems, history)
    print(f"   {len(unique_problems)} unique problems found")

    if not unique_problems:
        print("\nNo unique problems found today. Skipping.")
        return False

    # Pick the best problem
    selected_problem = unique_problems[0]
    print(f"\n   Selected: {selected_problem['title']}")

    # Step 4: Generate solution
    print("\n[4/5] Generating AI solution...")
    solution = generate_solution(selected_problem)
    print(f"   Solution type: {solution['type']}")

    # Step 5: Save and create files
    print("\n[5/5] Saving solution and generating docs...")
    date_str = today_str()
    problem_dir = SOLUTIONS_DIR / date_str
    problem_dir.mkdir(parents=True, exist_ok=True)

    write_solution_files(problem_dir, date_str, selected_problem, solution)
    generate_documentation(problem_dir, selected_problem, solution)

    # Update history
    history["problems"].append({
        "date": date_str,
        "title": selected_problem["title"],
        "keywords": selected_problem.get("keywords", []),
        "type": solution["type"]
    })
    save_history(history)

    print(f"\nSolution saved to: {problem_dir}")
    print("=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)

    return True


if __name__ == "__main__":
    run()
    # exit 0 even when no unique problem -> workflow should succeed (no update today is not a failure)
    exit(0)
