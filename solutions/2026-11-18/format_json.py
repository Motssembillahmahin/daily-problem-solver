#!/usr/bin/env python3
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
