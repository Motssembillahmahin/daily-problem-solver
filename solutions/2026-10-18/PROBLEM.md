# Problem: Pipreqs: SyntaxError: invalid non-printable character U+FEFF

**Date:** 2026-10-18

**Source:** Stack Overflow

**Category:** general

**Why Selected:** Trending problem in general category

## Description

When I try to run pipreqs /path/to/project it comes back with File "<unknown>", line 1 # !/usr/bin/env python3 ^ SyntaxError: invalid non-printable character U+FEFF my project contains a number of files and all of them contain their own imports. I read somewhere that it could be an issue to create a requirements.txt for a number of files so I tried to move the main file into a new dir and run pipreqs on there but again no success. my imports look like so: #!/usr/bin/env python3 # -*- coding: utf

## Original URL

https://stackoverflow.com/questions/71565071/pipreqs-syntaxerror-invalid-non-printable-character-ufeff
