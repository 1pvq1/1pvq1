"""
Configuration and constants for GitHub profile stats generation.
"""

import os
import subprocess

GITHUB_API = "https://api.github.com/graphql"

USERNAME = os.environ.get('USERNAME', '1pvq1')
TOKEN = os.environ.get('GITHUB_TOKEN')
START_DATE = os.environ.get('CONTRIB_START_DATE', '2022-03-19T00:00:00Z')
TOP_LANG_COUNT = int(os.environ.get('TOP_LANG_COUNT', '6'))

# Fallback token detection via `gh auth token` if available in shell environment
if not TOKEN:
    try:
        token_out = subprocess.check_output(['gh', 'auth', 'token'], text=True).strip()
        if token_out:
            TOKEN = token_out
    except Exception:
        pass

# Palette mapping for popular languages
LANG_COLORS = {
    'C#': '#a179dc',
    'Swift': '#f05138',
    'Kotlin': '#a97bfc',
    'TypeScript': '#3178c6',
    'CSS': '#563d7c',
    'HTML': '#e34c26',
    'Python': '#3572a5',
    'Jupyter Notebook': '#da5b0b',
    'JavaScript': '#f1e05a',
    'PowerShell': '#012456',
    'Shell': '#89e051',
    'C': '#555555',
    'C++': '#f34b7d',
    'Go': '#00ADD8',
    'Rust': '#dea584',
    'Java': '#b07219',
    'Ruby': '#701516',
    'PHP': '#4F5D95',
    'Vue': '#41b883',
    'Dart': '#00B4AB'
}

DEFAULT_LANG_COLOR = '#38bdf8'
