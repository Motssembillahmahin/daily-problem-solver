#!/usr/bin/env python3
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
    
    print(f"\nHealth Metrics for {date}:")
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
    
    print("\nWeekly Statistics:")
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
        f.write("date,time,type,value\n")
        for m in data["metrics"]:
            f.write(f"{m['date']},{m['time']},{m['type']},{m['value']}\n")
    
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
