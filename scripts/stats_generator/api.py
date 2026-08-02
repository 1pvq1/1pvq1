"""
API interaction module for querying GitHub GraphQL API.
"""

import time
import requests
from collections import defaultdict
from .config import GITHUB_API, TOKEN, START_DATE


def graphql(query, variables=None, token=None):
    """Execute GraphQL query against GitHub API."""
    auth_token = token or TOKEN
    if not auth_token:
        raise ValueError("No GITHUB_TOKEN available")
    headers = {
        'Authorization': f'bearer {auth_token}',
        'Accept': 'application/vnd.github.v4+json',
    }
    r = requests.post(GITHUB_API, json={'query': query, 'variables': variables or {}}, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    if 'errors' in data:
        raise RuntimeError(data['errors'])
    return data['data']


def fetch_all_repo_language_sizes(login, token=None):
    """Fetch repository language byte sizes, stars, and repository counts."""
    auth_token = token or TOKEN
    if not auth_token:
        # Fallback sample data if token is unavailable
        return 21, {
            'C#': 3493571, 'Swift': 1994747, 'Kotlin': 990731, 
            'TypeScript': 801299, 'CSS': 511783, 'HTML': 379103, 
            'Python': 224851, 'Jupyter Notebook': 187578
        }, 15, 4
    
    after = None
    languages = defaultdict(int)
    total_repos = 0
    stars = 0
    forks = 0

    while True:
        query = '''
        query($login:String!, $after:String) {
          user(login:$login) {
            repositories(first:100, after:$after, privacy:PUBLIC, ownerAffiliations:OWNER, isFork:false) {
              totalCount
              pageInfo { hasNextPage, endCursor }
              nodes {
                name
                stargazerCount
                forkCount
                languages(first: 20, orderBy: {field: SIZE, direction: DESC}) {
                  edges { size, node { name } }
                }
              }
            }
          }
        }
        '''
        variables = {'login': login, 'after': after}
        data = graphql(query, variables, token=auth_token)
        repos = data['user']['repositories']
        total_repos = repos['totalCount']
        for node in repos['nodes']:
            stars += node.get('stargazerCount', 0)
            forks += node.get('forkCount', 0)
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
    return total_repos, languages, stars, forks


def fetch_contributions_and_user(login, from_date=START_DATE, token=None):
    """Fetch user basic info and contribution collection."""
    auth_token = token or TOKEN
    if not auth_token:
        # Fallback mock user data
        return {
            'name': '1pvq1', 'login': '1pvq1', 'bio': 'Polyglot Developer & Tech Enthusiast',
            'location': 'Earth', 'followers': {'totalCount': 7}, 'following': {'totalCount': 3},
            'contributionsCollection': {
                'totalCommitContributions': 120,
                'totalPullRequestContributions': 12,
                'contributionCalendar': {
                    'totalContributions': 141,
                    'weeks': [
                        {'contributionDays': [{'date': '2026-08-01', 'contributionCount': 5}]}
                    ]
                }
            }
        }

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
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays { date, contributionCount }
            }
          }
        }
      }
    }
    '''
    variables = {'login': login, 'from': from_date}
    data = graphql(query, variables, token=auth_token)
    return data['user']
