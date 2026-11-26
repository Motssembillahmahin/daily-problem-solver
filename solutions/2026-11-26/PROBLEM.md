# Problem: How can I set a permanent default indentation for Python files to X spaces?

**Date:** 2026-11-26

**Source:** Stack Overflow

**Category:** general

**Why Selected:** Trending problem in general category

## Description

I have searched to find a solution for (Astro)N(eo)vim, and it is commonly suggested to set a tab equivalent to a default number of blank characters. However, I have observed that even if I set these variables in a configuration file, vim.opt.tabstop = 2 vim.opt.softtabstop = 2 vim.opt.shiftwidth = 2 Unfortunately, for Python files a separate additional line is needed: vim.cmd [[autocmd FileType python set shiftwidth=2 tabstop=2 expandtab]] If this line is not provided, e.g the tabstop option is

## Original URL

https://stackoverflow.com/questions/80018249/how-can-i-set-a-permanent-default-indentation-for-python-files-to-x-spaces
