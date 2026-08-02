#!/usr/bin/env python3
"""
Generate SVG assets for README using GitHub API (GraphQL + REST where needed).
Writes these files into assets/:
 - profile-overview.svg
 - top-langs.svg
 - streak.svg
 - profile-details.svg
 - productive-time.svg

Requires env GITHUB_TOKEN and USERNAME (optional, defaults to repo owner '1pvq1').
"""
import os
import sys
import time
import math
import requests
from collections import defaultdict
from datetime import datetime

GITHUB_API = "https://api.github.com/graphql"
REST_API = "https://api.github.com"

USERNAME = os.environ.get('USERNAME', '1pvq1')
TOKEN = os.environ.get('GITHUB_TOKEN')
if not TOKEN:
    print('Error: GITHUB_TOKEN environment variable is required', file=sys.stderr)
    sys.exit(2)

HEADERS = {
    'Authorization': f'bearer {TOKEN}',
    'Accept': 'application/vnd.github.v4+json',
}

os.makedirs('assets', exist_ok=True)

# GraphQL helper
def graphql(query, variables=None):
    r = requests.post(GITHUB_API, json={'query': query, 'variables': variables or {}}, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()
    if 'errors' in data:
        raise RuntimeError(data['errors'])
    return data['data']

# Fetch user basic info, contributions calendar, and repositories (with language byte sizes)

def fetch_all_repo_language_sizes(login):
    # Use GraphQL to page through repos and languages (languages has size)
    after = None
    languages = defaultdict(int)
    total_repos = 0
    while True:
        query = '''
        query($login:String!, $after:String) {
          user(login:$login) {
            repositories(first:100, after:$after, privacy:PUBLIC, ownerAffiliations:OWNER, isFork:false) {
              totalCount
              pageInfo { hasNextPage, endCursor }
              nodes {
                name
                languages(first: 20, orderBy: {field: SIZE, direction: DESC}) {
                  edges { size, node { name } }
                }
              }
            }
          }
        }
        '''
        variables = {'login': login, 'after': after}
        data = graphql(query, variables)
        repos = data['user']['repositories']
        total_repos = repos['totalCount']
        for node in repos['nodes']:
            langs = node.get('languages') or {}
            for edge in langs.get('edges', []):
                name = edge['node']['name']
                size = edge.get('size') or 0
                languages[name] += size
        if repos['pageInfo']['hasNextPage']:
            after = repos['pageInfo']['endCursor']
            time.sleep(0.1)
        else:
            break
    return total_repos, languages


def fetch_contributions_and_user(login, from_date='2022-03-19T00:00:00Z'):
    # Query contributions calendar and user basic info
    query = '''
    query($login:String!, $from:DateTime!) {
      user(login:$login) {
        name
        login
        bio
        location
        followers { totalCount }
        following { totalCount }
        contributionsCollection(from: $from) {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays { date, contributionCount }
            }
          }
        }
        repositories(privacy:PUBLIC) { totalCount }
      }
    }
    '''
    variables = {'login': login, 'from': from_date}
    data = graphql(query, variables)
    return data['user']


def compute_streaks(contrib_calendar):
    days = []
    for week in contrib_calendar['weeks']:
        for d in week['contributionDays']:
            days.append({'date': d['date'], 'count': d['contributionCount']})
    # Sort by date
    days.sort(key=lambda x: x['date'])
    # Compute longest and current streak
    longest = 0
    current = 0
    max_end_date = None

    streak = 0
    prev_date = None
    for day in days:
        c = day['count']
        date = datetime.fromisoformat(day['date'])
        if c > 0:
            if prev_date and (date.date() - prev_date.date()).days == 1:
                streak += 1
            else:
                streak = 1
            if streak > longest:
                longest = streak
                max_end_date = date
        else:
            streak = 0
        prev_date = date
    # current streak: count backwards from last day
    cs = 0
    for day in reversed(days):
        if day['count'] > 0:
            cs += 1
        else:
            break
    return {'longest': longest, 'current': cs, 'longest_end': max_end_date}


def write_profile_overview(user, total_contribs, total_repos, out='assets/profile-overview.svg'):
    followers = user.get('followers', {}).get('totalCount', 0)
    name = user.get('name') or user.get('login')
    # Simple SVG card
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="240">
  <rect width="100%" height="100%" rx="8" fill="#0f1720" />
  <text x="40" y="60" font-size="28" fill="#8ab4ff">{name}</text>
  <text x="40" y="110" font-size="42" font-weight="700" fill="#82aaff">{total_contribs}</text>
  <text x="40" y="150" font-size="14" fill="#9ad1c7">Total Contributions since Mar 19, 2022</text>
  <text x="300" y="110" font-size="42" font-weight="700" fill="#82aaff">{total_repos}</text>
  <text x="300" y="150" font-size="14" fill="#9ad1c7">Public Repos</text>
  <text x="520" y="110" font-size="42" font-weight="700" fill="#82aaff">{followers}</text>
  <text x="520" y="150" font-size="14" fill="#9ad1c7">Followers</text>
</svg>'''
    with open(out, 'w', encoding='utf-8') as f:
        f.write(svg)
    print('Wrote', out)


def write_top_langs(langs, out='assets/top-langs.svg', max_items=6):
    # Sort and pick top
    items = sorted(langs.items(), key=lambda kv: kv[1], reverse=True)
    total = sum(v for _, v in items) or 1
    items = items[:max_items]
    width = 760
    height = 120 + 30*len(items)
    bar_x = 220
    bar_w = 480
    svg_lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">', f'<rect width="100%" height="100%" rx="8" fill="#0f1720" />']
    y = 40
    for name, size in items:
        pct = size/total
        bar_len = int(pct * bar_w)
        svg_lines.append(f'<text x="40" y="{y}" font-size="16" fill="#cfe7ff">{name}</text>')
        svg_lines.append(f'<rect x="{bar_x}" y="{y-14}" width="{bar_len}" height="16" fill="#5dd9c1" rx="4" />')
        svg_lines.append(f'<text x="{bar_x+bar_len+8}" y="{y}" font-size="12" fill="#9ad1c7">{pct*100:.1f}%</text>')
        y += 30
    svg_lines.append('</svg>')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_lines))
    print('Wrote', out)


def write_streaks(streak_info, out='assets/streak.svg'):
    current = streak_info['current']
    longest = streak_info['longest']
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="140">
  <rect width="100%" height="100%" rx="8" fill="#0f1720" />
  <text x="40" y="60" font-size="28" fill="#caa6ff">Current Streak</text>
  <text x="40" y="100" font-size="42" font-weight="700" fill="#82aaff">{current}</text>
  <text x="300" y="60" font-size="28" fill="#8ab4ff">Longest Streak</text>
  <text x="300" y="100" font-size="42" font-weight="700" fill="#82aaff">{longest}</text>
</svg>'''
    with open(out, 'w', encoding='utf-8') as f:
        f.write(svg)
    print('Wrote', out)


def write_profile_details(user, out='assets/profile-details.svg'):
    name = user.get('name') or user.get('login')
    login = user.get('login')
    bio = user.get('bio') or ''
    loc = user.get('location') or ''
    followers = user.get('followers', {}).get('totalCount', 0)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="380" height="120">
  <rect width="100%" height="100%" rx="8" fill="#0f1720" />
  <text x="20" y="40" font-size="18" fill="#cfe7ff">{name} ({login})</text>
  <text x="20" y="68" font-size="12" fill="#9ad1c7">{bio}</text>
  <text x="20" y="92" font-size="12" fill="#82aaff">Location: {loc} • Followers: {followers}</text>
</svg>'''
    with open(out, 'w', encoding='utf-8') as f:
        f.write(svg)
    print('Wrote', out)


def write_productive_time(days, out='assets/productive-time.svg'):
    # days: list of {'date': 'YYYY-MM-DD', 'count': N}
    # aggregate by weekday
    bywd = [0]*7
    for d in days:
        dt = datetime.fromisoformat(d['date'])
        wd = dt.weekday() # Mon=0
        bywd[wd] += d['count']
    labels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    maxv = max(bywd) or 1
    width = 760
    height = 180
    left = 60
    bar_w = 40
    gap = 20
    start_x = left
    svg_lines = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">', f'<rect width="100%" height="100%" rx="8" fill="#0f1720" />']
    y_base = 140
    for i, val in enumerate(bywd):
        h = int((val/maxv)*(y_base-40))
        x = start_x + i*(bar_w+gap)
        svg_lines.append(f'<rect x="{x}" y="{y_base-h}" width="{bar_w}" height="{h}" fill="#5dd9c1" rx="4" />')
        svg_lines.append(f'<text x="{x}" y="{y_base+18}" font-size="12" fill="#cfe7ff">{labels[i]}</text>')
    svg_lines.append('</svg>')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg_lines))
    print('Wrote', out)


def main():
    print('Fetching contributions and user info for', USERNAME)
    user = fetch_contributions_and_user(USERNAME)
    total_contribs = user['contributionsCollection']['contributionCalendar']['totalContributions']
    contrib_calendar = user['contributionsCollection']['contributionCalendar']
    streak_info = compute_streaks(contrib_calendar)

    print('Fetching repository language sizes (may take a few seconds)')
    total_repos, languages = fetch_all_repo_language_sizes(USERNAME)

    # Write SVGs
    write_profile_overview(user, total_contribs, total_repos)
    write_top_langs(languages)
    write_streaks(streak_info)
    write_profile_details(user)
    # Flatten days for productive time
    days = []
    for w in contrib_calendar['weeks']:
        for d in w['contributionDays']:
            days.append(d)
    write_productive_time(days)

if __name__ == '__main__':
    main()
