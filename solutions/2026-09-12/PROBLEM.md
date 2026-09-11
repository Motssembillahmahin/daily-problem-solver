# Problem: Why does my Py-Shiny web app download an empty file?

**Date:** 2026-09-12

**Source:** Stack Overflow

**Category:** data

**Why Selected:** Trending problem in data category

## Description

I'm working on a web app that searches a database and returns the relevant information as CSV files in a Zip archive (company security policy prevents me from returning the information as tabs in an XLSX file). When I run the get_data() function on its own, I get a CSV file with the expected information in it. But when I use the app, I get a CSV file that is empty except for the header row. from shiny import render, ui, reactive from shiny.express import input from pandas import DataFrame import

## Original URL

https://stackoverflow.com/questions/80002466/why-does-my-py-shiny-web-app-download-an-empty-file
