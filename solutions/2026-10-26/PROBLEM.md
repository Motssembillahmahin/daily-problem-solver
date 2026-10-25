# Problem: Is there a way to include a comment in an f-string?

**Date:** 2026-10-26

**Source:** Stack Overflow

**Category:** general

**Why Selected:** Trending problem in general category

## Description

It would be useful for mo to include a comment in an f-string. For instance, take this code: f""" <a href="{ escape(url) }" target="_blank" { # users expect link to open in new tab } >bla</a> """ It would be nice if this code was equivalent to: f""" <a href="{ escape(url) }" target="_blank" >bla</a> """ You can include full Python expressions in between the curly brackets, but it looks like you can't include comments. Am I correct? Is there a way to do this?

## Original URL

https://stackoverflow.com/questions/61972492/is-there-a-way-to-include-a-comment-in-an-f-string
