# Problem: Mule - JSON to XML - Unbound prefix

**Date:** 2026-09-30

**Source:** Stack Overflow

**Category:** general

**Why Selected:** Trending problem in general category

## Description

With my mule flow I get a JSON message and I use a JSON to XML transformer to send the XML to a Web Service. HTTP => JSON to XML => WS Consumer The XML needs a prefix " int: " : <int:contact>Name</int:contact> And the JSON format is like this: { "Modify":{ "int:contact":"Name" } } The JSON to XML transformer return an error: javax.xml.stream.XMLStreamException: Unbound prefix: int How can I pass the prefix?

## Original URL

https://stackoverflow.com/questions/35222950/mule-json-to-xml-unbound-prefix
