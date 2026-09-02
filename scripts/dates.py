"""Date helpers for the pipeline.

The daily workflow is scheduled at 18:00 UTC, which is 00:00 the *next* day in
Bangladesh. Solution folders are named for the BDT date so they match the commit
message produced by the workflow (which uses TZ='Asia/Dhaka').
"""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

PIPELINE_TZ = ZoneInfo("Asia/Dhaka")


def today_str(now: datetime | None = None) -> str:
    """Return the current date in the pipeline's timezone as YYYY-MM-DD."""
    now = now or datetime.now(timezone.utc)
    return now.astimezone(PIPELINE_TZ).strftime("%Y-%m-%d")
