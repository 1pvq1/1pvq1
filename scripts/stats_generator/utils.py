"""
Helper functions for date parsing, streak calculations, and geometry math.
"""

from datetime import datetime


def parse_iso_date(date_string):
    """Parse ISO date string into python datetime object."""
    if date_string.endswith('Z'):
        date_string = date_string[:-1] + '+00:00'
    return datetime.fromisoformat(date_string)


def compute_streaks(contrib_calendar):
    """Compute current streak and longest record streak from GitHub contribution calendar."""
    days = []
    for week in contrib_calendar.get('weeks', []):
        for d in week.get('contributionDays', []):
            days.append({'date': d['date'], 'count': d['contributionCount']})
    days.sort(key=lambda x: x['date'])

    longest = 0
    streak = 0
    prev_date = None
    for day in days:
        c = day['count']
        date = parse_iso_date(day['date'])
        if c > 0:
            if prev_date and (date.date() - prev_date.date()).days == 1:
                streak += 1
            else:
                streak = 1
            if streak > longest:
                longest = streak
        else:
            streak = 0
        prev_date = date

    cs = 0
    for day in reversed(days):
        if day['count'] > 0:
            cs += 1
        else:
            break
    return {'longest': max(longest, cs), 'current': cs}
