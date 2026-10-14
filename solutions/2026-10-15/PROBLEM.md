# Problem: How to randomly sample very large pyArrow dataset

**Date:** 2026-10-15

**Source:** Stack Overflow

**Category:** data

**Why Selected:** Trending problem in data category

## Description

I have a very large arrow dataset (181GB, 30m rows) from the huggingface framework I've been using. I want to randomly sample with replacement 100 rows (20 times), but after looking around, I cannot find a clear way to do this. I've tried converting to a pd.DataFrame so that I can use df.sample(), but Python crashes everytime (assuming due to the large dataset). So, I'm looking for something built-in within pyarrow. df = Dataset.from_file("embeddings_job/combined_embeddings_small/data-00000-of-0

## Original URL

https://stackoverflow.com/questions/78005435/how-to-randomly-sample-very-large-pyarrow-dataset
