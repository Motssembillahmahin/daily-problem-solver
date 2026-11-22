# Problem: How to retrieve PID from windows event log?

**Date:** 2026-11-23

**Source:** Stack Overflow

**Category:** general

**Why Selected:** Trending problem in general category

## Description

I have a python code that uses WMI module of python to get windows event viewer logs. But I am unable to retrieve the PID of the process that generated the log. My code : wmi_obj = wmi.WMI('.') #Initialize WMI object and query. wmi_query = "SELECT * FROM Win32_NTLogEvent WHERE Logfile='System' AND EventType=1" query_result = wmi_obj.query(wmi_query) # Query WMI object query_result is a list of wmi objects. Each object in this list is a windows system log and I want PID of the process that genera

## Original URL

https://stackoverflow.com/questions/39997471/how-to-retrieve-pid-from-windows-event-log
