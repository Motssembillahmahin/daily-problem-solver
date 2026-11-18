# Problem: How to solve `npm i package` and Vscode Default Formatter conflict

**Date:** 2026-11-18

**Source:** Stack Overflow

**Category:** general

**Why Selected:** Trending problem in general category

## Description

When I run npm i a-package package.json contains a new line at the end, but when I format that file with Json Language Feature the default json formatter of vscode, that line is removed. This causes unnecessary conflicts within our environment because we also formatOnSave config. If the last developer saved the package.json, the line gets removed, if they installed a package, the line comes back. There is an issue related to it: https://github.com/npm/npm/issues/18545 but it isn't solved and npm

## Original URL

https://stackoverflow.com/questions/79975142/how-to-solve-npm-i-package-and-vscode-default-formatter-conflict
