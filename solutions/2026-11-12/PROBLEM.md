# Problem: How can I dynamically log as the program runs?

**Date:** 2026-11-12

**Source:** Stack Overflow

**Category:** general

**Why Selected:** Trending problem in general category

## Description

My logging creates a StreamWriter and FileStream : //Activate Logging try { streamer = new FileStream("filepath and name", FileMode.OpenOrCreate, FileAccess.Write); writer = new StreamWriter(streamer); } I use parameters to create the file name. If an error occurs before this file is created I create another file called "crashlog", which logs the error itself. However, this file is sometimes empty. If an unhandled error occurs, even if the original logfile is created, that file is empty. I belie

## Original URL

https://stackoverflow.com/questions/79810553/how-can-i-dynamically-log-as-the-program-runs
