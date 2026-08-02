#!/usr/bin/env python3
"""
GitHub README Stats Generator - CLI Entry Point
Uses the stats_generator modular package to generate SVG assets for GitHub Profile.
"""

import sys
from stats_generator import (
    USERNAME,
    fetch_contributions_and_user,
    fetch_all_repo_language_sizes,
    compute_streaks,
    render_header_banner,
    render_profile_overview,
    render_top_langs,
    render_streaks,
    render_activity_radar,
    render_productive_time,
)


def main():
    print('Generating profile SVG visualizations for user:', USERNAME)
    
    # 1. Fetch user data and contributions from GitHub API
    user = fetch_contributions_and_user(USERNAME)
    total_contribs = user['contributionsCollection']['contributionCalendar']['totalContributions']
    contrib_calendar = user['contributionsCollection']['contributionCalendar']
    streak_info = compute_streaks(contrib_calendar)

    # 2. Fetch repository language metrics and star stats
    total_repos, languages, stars, followers_count = fetch_all_repo_language_sizes(USERNAME)
    followers = user.get('followers', {}).get('totalCount', followers_count)

    # 3. Render and save SVGs into assets/
    render_header_banner(user, total_contribs, total_repos, out='assets/header-banner.svg')
    render_profile_overview(user, total_contribs, total_repos, stars, followers, out='assets/profile-overview.svg')
    render_top_langs(languages, out='assets/top-langs.svg')
    render_streaks(streak_info, out='assets/streak.svg')
    render_activity_radar(languages, out='assets/activity-radar.svg')

    days = [d for w in contrib_calendar['weeks'] for d in w['contributionDays']]
    render_productive_time(days, out='assets/productive-time.svg')

    print("All profile stats visualizations successfully generated!")


if __name__ == '__main__':
    main()
