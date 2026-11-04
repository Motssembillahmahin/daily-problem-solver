# Problem: How to fix Fortify Path Manipulation ( Input Validation and Representation , Data Flow ) vulnerability

**Date:** 2026-11-05

**Source:** Stack Overflow

**Category:** security

**Why Selected:** Trending problem in security category

## Description

I am getting fortify path manipulation vulnerability for creating a file with new keyword I have tried to sanitize the path before passing it to File object, but the problem persists. Tried this link also: https://www.securecoding.cert.org/confluence/display/java/FIO00-J.+Do+not+operate+on+files+in+shared+directories public static String sanitizePath(String sUnsanitized) throws URISyntaxException, EncodingException { String sSanitized = SAPI.encoder().canonicalize(sUnsanitized); return sSanitize

## Original URL

https://stackoverflow.com/questions/55823435/how-to-fix-fortify-path-manipulation-input-validation-and-representation-dat
