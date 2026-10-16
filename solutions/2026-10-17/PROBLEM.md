# Problem: How to get the expansions from a glob pattern to use in another path

**Date:** 2026-10-17

**Source:** Stack Overflow

**Category:** general

**Why Selected:** Trending problem in general category

## Description

The Problem I want to create a function in Python for finding and moving files where I can specify a glob-style pattern to find source files, and then a second pattern to describe where to move them to. Essentially I want regex match groups for glob patterns. Example For example, I would like to be able to do something like: move('./a/**/foo/**/*.json', r'./new/\2/\1/\3.txt') Then, assuming it found the file ./a/b/c/foo/bar/bat/test.json it would match \1 , \2 , etc with the corresponding expans

## Original URL

https://stackoverflow.com/questions/79867224/how-to-get-the-expansions-from-a-glob-pattern-to-use-in-another-path
