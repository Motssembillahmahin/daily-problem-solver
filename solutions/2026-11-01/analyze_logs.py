#!/usr/bin/env python3
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
        r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(\w+)\s+(.*)',
        r'\[(.*?)\]\s+\[(.*?)\]\s+(.*)',
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
        
        print(f"\nLog Analysis: {file_path}")
        print("=" * 60)
        print(f"Total lines: {len(lines)}")
        
        # Count log levels
        level_patterns = {
            "ERROR": r'\bERROR\b',
            "WARNING": r'\bWARN(ING)?\b',
            "INFO": r'\bINFO\b',
            "DEBUG": r'\bDEBUG\b',
        }
        
        level_counts = Counter()
        error_lines = []
        
        for line in lines:
            for level, pattern in level_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    level_counts[level] += 1
                    if level == "ERROR":
                        error_lines.append(line.strip())
        
        print(f"\nLog Levels:")
        for level, count in level_counts.most_common():
            print(f"  {level}: {count}")
        
        # Show recent errors
        if error_lines:
            print(f"\nRecent Errors (last 5):")
            for line in error_lines[-5:]:
                print(f"  {line[:100]}...")
        
        print("\n" + "=" * 60)
    
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_logs.py <logfile.log>")
        sys.exit(1)
    
    analyze_logs(sys.argv[1])
