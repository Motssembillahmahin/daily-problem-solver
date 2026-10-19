# Problem: Python can't find function from imported module - first time creating an __init__.py file

**Date:** 2026-10-20

**Source:** Stack Overflow

**Category:** productivity

**Why Selected:** Trending problem in productivity category

## Description

In main.py I have this line: from core import * . There is a subfolder called core and in that folder I created a bunch of modules to organize my functions. One is called fileManagement.py . It has a couple functions in it including importInputs() . I also created an __init__.py file in the core folder with __all__ = ["fileManagement"] . Main.py includes this line: df=importInputs() . All of this worked when everything was in one .py file, but now I get NameError: name 'importInputs' is not defi

## Original URL

https://stackoverflow.com/questions/80010672/python-cant-find-function-from-imported-module-first-time-creating-an-init
