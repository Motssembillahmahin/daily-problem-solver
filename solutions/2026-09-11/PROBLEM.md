# Problem: getting pyarrow.lib.ArrowInvalid: CSV parse error: Expected 9 columns, got 1

**Date:** 2026-09-11

**Source:** Stack Overflow

**Category:** productivity

**Why Selected:** Trending problem in productivity category

## Description

so I am trying apache arrow for the first time and want to read an entire directory of txt files into a pyarrow datastructure. I am getting pyarrow.lib.ArrowInvalid: CSV parse error: Expected 9 columns, got 1 when I run the code below? no clue how to debug this. any help appreciated. ALSO if there's a book that covers python and pyarrow happy to read it. import pyarrow.csv as csv import pyarrow as pa l_all_files = ['x08.txt', 'x21.txt', 'x108.txt'] read_options = csv.ReadOptions( column_names= (

## Original URL

https://stackoverflow.com/questions/63908360/getting-pyarrow-lib-arrowinvalid-csv-parse-error-expected-9-columns-got-1
