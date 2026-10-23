# Problem: How can I use different output templates for different log levels with Serilog when using appsettings for configuration?

**Date:** 2026-10-24

**Source:** Stack Overflow

**Category:** general

**Why Selected:** Trending problem in general category

## Description

When using Serilog with .NET, I want to use a different output template for error level logs, since I want the error logs to contain additional information. I'm using the appsettings.json to configure how Serilog behaves, so I need a solution which uses JSON instead of C#. I am able to use "restrictiedToMinimumLevel" : "Error" to produce error logs with the additional information I want, but this results in the logs appearing twice (once with the extra information, and once without). I've also f

## Original URL

https://stackoverflow.com/questions/80011341/how-can-i-use-different-output-templates-for-different-log-levels-with-serilog-w
