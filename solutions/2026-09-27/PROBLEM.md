# Problem: log4j writing to console but not to file (Liferay + Tomcat)

**Date:** 2026-09-27

**Source:** Stack Overflow

**Category:** health

**Why Selected:** Trending problem in health category

## Description

I've recently had issues with my Liferay/Tomcat logs getting clogged up from several portlets logging to the same files, which makes it tough to track down issues sometimes. Decided I'd like to have a log file for each portlet so it is easier to track down issues and I've found some helpful articles, but no matter what I try I cannot get the custom log file to be created (and by extension written to). As per this article , I've added the following lines to liferay-plugin-package.properties: port

## Original URL

https://stackoverflow.com/questions/18640215/log4j-writing-to-console-but-not-to-file-liferay-tomcat
