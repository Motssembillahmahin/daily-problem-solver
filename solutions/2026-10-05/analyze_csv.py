#!/usr/bin/env python3
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
        
        print(f"\nCSV Analysis: {file_path}")
        print("=" * 50)
        print(f"Total rows: {len(rows)}")
        print(f"Columns: {len(columns)}")
        print(f"Column names: {', '.join(columns)}")
        
        # Analyze each column
        for col in columns:
            values = [row[col] for row in rows if row[col]]
            
            print(f"\nColumn: {col}")
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
        
        print("\n" + "=" * 50)
    
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_csv.py <file.csv>")
        sys.exit(1)
    
    analyze_csv(sys.argv[1])
