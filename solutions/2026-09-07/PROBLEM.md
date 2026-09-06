# Problem: Mask out sensitive information in python log

**Date:** 2026-09-07

**Source:** Stack Overflow

**Category:** general

**Why Selected:** Trending problem in general category

## Description

Consider the following code try: r = requests.get('https://sensitive:passw0rd@what.ever/') r.raise_for_status() except requests.HTTPError: logging.exception("Failed to what.ever") Here, if the endpoint returns non-successful http status code, the following will be logged Traceback (most recent call last): File "a.py", line 5, in <module> r.raise_for_status() File "venv/lib/python3.5/site-packages/requests/models.py", line 928, in raise_for_status raise HTTPError(http_error_msg, response=self) re

## Original URL

https://stackoverflow.com/questions/48380452/mask-out-sensitive-information-in-python-log
