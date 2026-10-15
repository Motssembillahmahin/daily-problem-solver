# Problem: How to do code generation with modern Python packaging?

**Date:** 2026-10-16

**Source:** Stack Overflow

**Category:** productivity

**Why Selected:** Trending problem in productivity category

## Description

I've been trying to wrap my head around modern Python packaging, and one of the things I still can't find anything clear about is how to do build-time codegen (so e.g. in-source data files get compiled to code file during build, and those code files get packaged in the sdist or wheel). From what PEP517 seems to imply , I feel like it requires implementing a custom build backend: [build-system] build-backend = "local_backend" backend-path = ["backend"] and then that's supposed to do some things a

## Original URL

https://stackoverflow.com/questions/73437687/how-to-do-code-generation-with-modern-python-packaging
