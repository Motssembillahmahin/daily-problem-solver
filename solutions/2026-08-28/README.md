# JSON Formatter CLI

A working Python CLI tool to format and validate JSON files.

## Problem

People frequently need to format messy JSON files for readability or validation. Manual formatting is tedious and error-prone.

## Solution

A simple, working Python script that:
- Formats JSON files with proper indentation
- Validates JSON syntax
- Sorts keys alphabetically (optional)
- Reports file size after formatting

## Usage

```bash
# Format a JSON file
python format_json.py data.json

# Format with custom indent
python format_json.py data.json --indent 4

# Format with sorted keys
python format_json.py data.json --sort
```

## How It Works

1. Reads JSON file
2. Parses and validates JSON
3. Formats with specified indentation
4. Writes formatted output back to file

## Files

| File | Description |
|------|-------------|
| `format_json.py` | Main script - fully working |
| `requirements.txt` | No dependencies needed |
| `README.md` | This file |

## Example

Input (`messy.json`):
```json
{"name":"John","age":30,"city":"New York"}
```

After running `python format_json.py messy.json`:
```json
{
  "age": 30,
  "city": "New York",
  "name": "John"
}
```

## Source

Problem identified from: Google Trends - AI automation tools category
Date: 2026-08-28
