"""Tests for the pipeline's date handling (solution folders must match the BDT commit date)."""

from datetime import datetime, timezone

from scripts.dates import today_str


def test_uses_dhaka_date_not_utc_date_at_cron_time():
    """Cron fires at 18:00 UTC, which is already the next day in Dhaka (UTC+6)."""
    cron_fire = datetime(2026, 9, 2, 18, 0, tzinfo=timezone.utc)

    assert today_str(now=cron_fire) == "2026-09-03"


def test_uses_dhaka_date_when_utc_and_dhaka_agree():
    midday = datetime(2026, 9, 2, 6, 0, tzinfo=timezone.utc)

    assert today_str(now=midday) == "2026-09-02"


def test_defaults_to_current_time():
    assert len(today_str()) == len("YYYY-MM-DD")
