# Problem: Is there a way to export huge amount of data (more than a million rows) from SQL Server to csv?

**Date:** 2026-10-11

**Source:** Stack Overflow

**Category:** data

**Why Selected:** Trending problem in data category

## Description

I have no trouble exporting to csv files using ssis when the number of rows is less than 500k. I get the following error when the size gets bigger DT_TEXT, which is not supported with Unicode files. Use DT_NTEXT instead and convert the data to DT_TEXT using the data conversion component.

## Original URL

https://stackoverflow.com/questions/30731670/is-there-a-way-to-export-huge-amount-of-data-more-than-a-million-rows-from-sql
