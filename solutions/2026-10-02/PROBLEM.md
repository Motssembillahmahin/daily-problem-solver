# Problem: No such file or directory @ rb_sysopen

**Date:** 2026-10-02

**Source:** Stack Overflow

**Category:** data

**Why Selected:** Trending problem in data category

## Description

I'm using Ruby 2.1.1 When I run this code: <CSV.foreach("public/data/original/example_data.csv",headers: true, converters: :numeric) do |info| I get an error: No such file or directory @ rb_sysopen It works if I place example_data.csv in the same directory as shown below, but my boss said it can't be that way he wants all *.csv files in a different directory: <CSV.foreach("example_data.csv",headers: true, converters: :numeric) do |info|

## Original URL

https://stackoverflow.com/questions/22818611/no-such-file-or-directory-rb-sysopen
