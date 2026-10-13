# Problem: How to parse json-file with spring batch?

**Date:** 2026-10-14

**Source:** Stack Overflow

**Category:** general

**Why Selected:** Trending problem in general category

## Description

I have a list of serialized entities written to a file in json format. I need to read them from the file using spring batch (then process them and write to DB). I found only Flat file, DB and Xml readers provided with spring batch. What's the right way to parse json? The approach I'm going to implement is: 1. read the whole file with FlatFile reader 2. parse it with Jaxson in `read` method I'm completely newbie in spring batch, so I need a piece of advice here. Is this approach correct? Doesn't 

## Original URL

https://stackoverflow.com/questions/15204491/how-to-parse-json-file-with-spring-batch
