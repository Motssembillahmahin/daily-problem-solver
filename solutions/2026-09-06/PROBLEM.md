# Problem: CSV with too few values in one row does not cause an error in pandas

**Date:** 2026-09-06

**Source:** Stack Overflow

**Category:** data

**Why Selected:** Trending problem in data category

## Description

This example CSV has three columns, but the second row has a missing value: A;B;C D;E F;G;H When I run: import pandas import io csv = io.StringIO('A;B;C\nD;E\nF;G;H') df = pandas.read_csv(csv, encoding='utf-8', sep=';', header=None, error_bad_lines=True, warn_bad_lines=True) print(df) I get NaN in the last column with no warning or error: 0 1 2 0 A B C 1 D E NaN 2 F G H Based on the pandas documentation, I believe that I should get a warning if there are too few values in a row. How can I catch 

## Original URL

https://stackoverflow.com/questions/67775180/csv-with-too-few-values-in-one-row-does-not-cause-an-error-in-pandas
