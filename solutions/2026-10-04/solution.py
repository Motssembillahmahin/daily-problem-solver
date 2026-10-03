#!/usr/bin/env python3
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

    print(f"\nSummary: Organized {sum(stats.values())} files")
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
        print("DRY RUN - No files will be moved\n")
    
    organize_files(folder, dry_run)
