# Problem: Deleting all files in a folder older than X days

**Date:** 2026-10-25

**Source:** Stack Overflow

**Category:** productivity

**Why Selected:** Trending problem in productivity category

## Description

I'm trying to write a Python script to delete all files in a folder older than X days. This is what I have so far: import os, time, sys path = r"c:\users\%myusername%\downloads" now = time.time() for f in os.listdir(path): if os.stat(f).st_mtime < now - 7 * 86400: if os.path.isfile(f): os.remove(os.path.join(path, f)) When I run the script, I get: Error2 - system cannot find the file specified , and it gives the filename. What am I doing wrong?

## Original URL

https://stackoverflow.com/questions/12485666/deleting-all-files-in-a-folder-older-than-x-days
