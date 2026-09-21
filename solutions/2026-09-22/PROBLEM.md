# Problem: Warning: simplexml_load_string(): Memory allocation failed : growing buffer

**Date:** 2026-09-22

**Source:** Stack Overflow

**Category:** data

**Why Selected:** Trending problem in data category

## Description

Following code is used to convert an XLSX file to CSV using PHPExcel: <?php require_once 'PHPExcel/PHPExcel/IOFactory.php'; $excel = PHPExcel_IOFactory::load("test123.xlsx"); $writer = PHPExcel_IOFactory::createWriter($excel, 'CSV'); $writer->setDelimiter(";"); $writer->setEnclosure(""); $writer->save("test123.csv"); ?> I am trying to convert large excel file, 70MB in size, to CSV. I am getting this error: Warning: simplexml_load_string(): Memory allocation failed : growing buffer I have increas

## Original URL

https://stackoverflow.com/questions/20138597/warning-simplexml-load-string-memory-allocation-failed-growing-buffer
