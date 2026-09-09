# Problem: Pandas Generate Multiple xlsx file from CSV

**Date:** 2026-09-10

**Source:** Stack Overflow

**Category:** data

**Why Selected:** Trending problem in data category

## Description

I'm trying to generate multiple excel files from a single CSV file, but after generating few files getting below error: UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 8: ordinal not in range(128) the error is coming after generating few files, I'm not sure if any specific with file or any issue in code, kindly help the code is as below: #!/usr/bin/env python # coding: utf-8 import pandas as pd import pandas.io.formats.excel pandas.io.formats.excel.header_style = None class 

## Original URL

https://stackoverflow.com/questions/52980181/pandas-generate-multiple-xlsx-file-from-csv
