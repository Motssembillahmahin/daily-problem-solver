# Problem: Load Data Infile OPTIONALLY ENCLOSED BY not working as expected

**Date:** 2026-10-28

**Source:** Stack Overflow

**Category:** data

**Why Selected:** Trending problem in data category

## Description

Many related tickets and tut sites but unfortunately no solutions have worked for me so far, couple hours stuck on this. I have many csv files I need to insert into a mysql db, using 'load in file' does it very quickly and easily. However, it stumbles on one section: Sample csv line: ABSOLUTE,Glenn,Anakie,"Cool Synd, Super Cool" Code I'm using is: $q = "load data infile '$file' into table $table FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\n';"; mysql_query($q, $db)

## Original URL

https://stackoverflow.com/questions/35478520/load-data-infile-optionally-enclosed-by-not-working-as-expected
