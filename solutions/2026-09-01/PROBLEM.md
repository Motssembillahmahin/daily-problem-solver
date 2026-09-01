# Problem: Show HN: Running 104GB Qwen3.8-Flash-Next on 48GB Mac with at ~12 tok/s

**Date:** 2026-09-01

**Source:** Hacker News

**Category:** ai_ml

**Why Selected:** Trending problem in ai_ml category

## Description

I built slotstream, a way to run Qwen3.8-Flash-Next 4-bit on a low-memory mac starting from 16GB, a 125B parameter model that would need 100GB+ memory&#x2F;RAM, thanks to expert-offloading&#x2F;ssd-streaming. Easy to install&#x2F;update, and mac-native using MLX and Swift.<p>It ships with auto-mode, which makes a good tradeoff between memory usage and speed. I&#x27;ll be implementing and porting the MTP module for speculative decoding next

## Original URL

https://github.com/carloslfu/slotstream
