"""
Working with Dates & Times
===========================

Almost every real application eventually needs to record, format, parse, or
compute with dates and times: log timestamps, expiry dates, schedules,
durations. Python's `datetime` module provides the core building blocks --
`date`, `time`, `datetime`, and `timedelta` -- for representing points in
time and the spans between them. The separate `time` module deals more with
low-level system time and sleeping. Getting comfortable with formatting
(`strftime`), parsing (`strptime`), arithmetic, and timezone-awareness will
save you from a huge number of subtle date-related bugs.

This file covers:
- The datetime module: date, time, datetime, timedelta
- Creating and formatting dates (strftime)
- Parsing strings into dates (strptime)
- Date arithmetic
- Timezones (brief intro with timezone.utc)
- The time module: time.time() and time.sleep (mentioned, not really slept)
"""

import time as time_module
from datetime import date, time, datetime, timedelta, timezone

# ---------------------------------------------------------------------------
# 1. The datetime module: date, time, datetime, timedelta
# ---------------------------------------------------------------------------
# date       -> a calendar date (year, month, day), no time-of-day.
# time       -> a time-of-day (hour, minute, second, microsecond), no date.
# datetime   -> a combination of date + time.
# timedelta  -> a duration/difference between two dates or datetimes.

today = date.today()
now_time = datetime.now().time()
now = datetime.now()

print("date.today()         ->", today)
print("current time-of-day   ->", now_time)
print("datetime.now()        ->", now)
print("type(today)            :", type(today).__name__)
print("type(now_time)         :", type(now_time).__name__)
print("type(now)              :", type(now).__name__)

# ---------------------------------------------------------------------------
# 2. Creating dates and datetimes explicitly
# ---------------------------------------------------------------------------
independence_day = date(1776, 7, 4)
meeting = datetime(2026, 8, 24, 14, 30, 0)  # year, month, day, hour, minute, second
just_time = time(9, 15)  # 9:15 AM, no date attached

print("\nExplicit date:", independence_day)
print("Explicit datetime:", meeting)
print("Explicit time-of-day:", just_time)
print("Year/month/day access:", meeting.year, meeting.month, meeting.day)
print("Hour/minute access:", meeting.hour, meeting.minute)

# ---------------------------------------------------------------------------
# 3. Formatting dates with strftime
# ---------------------------------------------------------------------------
# strftime() turns a date/datetime object into a formatted string, using
# format codes like %Y (4-digit year), %m (month), %d (day), %H (24h hour),
# %M (minute), %S (second), %A (full weekday name), %B (full month name).

print("\nFormatting with strftime:")
print(" ", meeting.strftime("%Y-%m-%d"))
print(" ", meeting.strftime("%d/%m/%Y"))
print(" ", meeting.strftime("%A, %B %d, %Y"))
print(" ", meeting.strftime("%H:%M:%S"))
print(" ", meeting.strftime("%I:%M %p"))  # 12-hour clock with AM/PM

# str() and isoformat() give quick default representations too.
print("str(meeting):        ", str(meeting))
print("meeting.isoformat():  ", meeting.isoformat())

# ---------------------------------------------------------------------------
# 4. Parsing strings into dates with strptime
# ---------------------------------------------------------------------------
# strptime() is the inverse of strftime(): it parses a string into a
# datetime object, given a matching format string.

date_string = "2026-01-15 08:45:00"
parsed = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
print("\nParsed", repr(date_string), "->", parsed)

date_only_string = "15/01/2026"
parsed_date_only = datetime.strptime(date_only_string, "%d/%m/%Y")
print("Parsed", repr(date_only_string), "->", parsed_date_only)

# A mismatched format raises ValueError -- worth knowing when validating input.
try:
    datetime.strptime("not-a-date", "%Y-%m-%d")
except ValueError as exc:
    print("Parsing an invalid string raises ValueError:", exc)

# ---------------------------------------------------------------------------
# 5. Date arithmetic with timedelta
# ---------------------------------------------------------------------------
# Adding/subtracting a timedelta shifts a date or datetime; subtracting two
# dates/datetimes gives you a timedelta back.

one_week = timedelta(weeks=1)
ninety_minutes = timedelta(hours=1, minutes=30)

print("\nOne week from today:", today + one_week)
print("90 minutes from now: ", (datetime.now() + ninety_minutes).strftime("%H:%M:%S"))

start = datetime(2026, 8, 24, 9, 0, 0)
end = datetime(2026, 8, 24, 17, 30, 0)
work_duration = end - start
print("Duration between start and end:", work_duration)
print("  total seconds:", work_duration.total_seconds())
print("  as hours:", work_duration.total_seconds() / 3600)

birthday = date(2026, 12, 25)
days_until = (birthday - today).days
print(f"Days from today until {birthday}: {days_until}")

# ---------------------------------------------------------------------------
# 6. Timezones (brief intro)
# ---------------------------------------------------------------------------
# A "naive" datetime has no timezone attached -- it's just numbers, with no
# notion of UTC offset. An "aware" datetime knows its UTC offset via
# tzinfo, which avoids a whole class of "which timezone did we mean" bugs.

naive_dt = datetime(2026, 8, 24, 12, 0, 0)
aware_utc_dt = datetime(2026, 8, 24, 12, 0, 0, tzinfo=timezone.utc)

print("\nNaive datetime (no tzinfo):", naive_dt, "| tzinfo =", naive_dt.tzinfo)
print("Aware datetime (UTC):       ", aware_utc_dt, "| tzinfo =", aware_utc_dt.tzinfo)

utc_now = datetime.now(timezone.utc)
print("Current UTC time via datetime.now(timezone.utc):", utc_now)

# A fixed-offset timezone, e.g. UTC+6, can be built directly:
plus_six = timezone(timedelta(hours=6))
local_equivalent = utc_now.astimezone(plus_six)
print("Same instant converted to UTC+6:", local_equivalent)

# Comparing naive and aware datetimes directly raises TypeError -- another
# good reason to be consistent about using aware datetimes throughout a
# program once you start dealing with timezones at all.
try:
    naive_dt < aware_utc_dt
except TypeError as exc:
    print("Comparing naive vs aware datetimes raises TypeError:", exc)

# ---------------------------------------------------------------------------
# 7. The time module: time.time() and time.sleep()
# ---------------------------------------------------------------------------
# time.time() returns seconds since the Unix epoch (1970-01-01 UTC) as a
# float -- handy for simple elapsed-time measurements or timestamps.
# time.sleep(seconds) pauses execution; here we call it with 0 seconds so
# the tutorial doesn't actually pause, just to show the API exists.

epoch_seconds = time_module.time()
print("\ntime.time() (seconds since epoch):", epoch_seconds)
print("As a readable datetime:", datetime.fromtimestamp(epoch_seconds))

start_marker = time_module.time()
time_module.sleep(0)  # sleep for 0 seconds -- just demonstrating the API
elapsed = time_module.time() - start_marker
print(f"time.sleep(0) called; elapsed measured as {elapsed:.6f} seconds")
print("In real code, time.sleep(2) would pause execution for 2 seconds.")

# Key takeaways:
# - date, time, datetime, and timedelta are the four core building blocks:
#   calendar date, time-of-day, the combination of both, and a duration.
# - strftime() formats a date/datetime into a string; strptime() parses a
#   matching string back into a date/datetime -- they are inverses.
# - Subtracting two dates or datetimes gives a timedelta; adding/subtracting
#   a timedelta shifts a date or datetime forward or backward.
# - A "naive" datetime has no timezone info; an "aware" one carries a
#   tzinfo (e.g. timezone.utc), and mixing naive with aware raises TypeError.
# - The time module works at a lower level: time.time() gives epoch seconds,
#   and time.sleep() pauses execution for a given number of seconds.
