"""
SVG rendering module for creating custom GitHub profile stats cards.
Includes inline SVG display utilities for Jupyter Notebooks.
"""

import math

from .config import LANG_COLORS, DEFAULT_LANG_COLOR, TOP_LANG_COUNT
from .utils import parse_iso_date


def save_svg_file(svg_content, out_path):
    """Utility helper to write SVG content to a file."""
    if out_path:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print('Wrote', out_path)


def display_svg(svg_content):
    """Display SVG content inline in Jupyter Notebook environment."""
    try:
        from IPython.display import SVG, display
        display(SVG(svg_content))
    except ImportError:
        pass


def render_header_banner(user, total_contribs, total_repos, out=None):
    """Render hero header banner SVG."""
    name = user.get('name') or user.get('login') or '1pvq1'
    login = user.get('login') or '1pvq1'
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="850" height="200" viewBox="0 0 850 200" fill="none">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f19" />
      <stop offset="50%" stop-color="#111827" />
      <stop offset="100%" stop-color="#0f172a" />
    </linearGradient>
    
    <linearGradient id="neonGlow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7c3aed" />
      <stop offset="50%" stop-color="#3b82f6" />
      <stop offset="100%" stop-color="#06b6d4" />
    </linearGradient>

    <linearGradient id="textGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f8fafc" />
      <stop offset="100%" stop-color="#38bdf8" />
    </linearGradient>
    
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#1e293b" stroke-width="0.8" opacity="0.6"/>
    </pattern>

    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background -->
  <rect width="850" height="200" rx="16" fill="url(#bgGrad)" stroke="#1e293b" stroke-width="1.5"/>
  <rect width="850" height="200" rx="16" fill="url(#grid)" />

  <!-- Top Accent Bar with Glow -->
  <rect x="0" y="0" width="850" height="4" fill="url(#neonGlow)" filter="url(#glow)" />
  <rect x="0" y="196" width="850" height="4" fill="url(#neonGlow)" filter="url(#glow)" opacity="0.7"/>

  <!-- Left Cyber Deco Circles -->
  <circle cx="60" cy="100" r="80" fill="#7c3aed" opacity="0.08" filter="url(#glow)" />
  <circle cx="780" cy="120" r="100" fill="#06b6d4" opacity="0.06" filter="url(#glow)" />

  <!-- Terminal Header / Title -->
  <g transform="translate(45, 45)">
    <!-- Terminal Prompt Icon -->
    <text x="0" y="32" font-family="'Fira Code', 'JetBrains Mono', Consolas, monospace" font-size="28" font-weight="800" fill="#38bdf8">❯</text>
    
    <text x="30" y="32" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="32" font-weight="900" fill="url(#textGrad)" letter-spacing="0.5">
      Hi, I'm <tspan fill="#a78bfa">@{login}</tspan> 👋
    </text>

    <text x="30" y="64" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="500" fill="#94a3b8">
      Polyglot Developer • Mobile, Desktop &amp; Cloud Systems • AI &amp; Software Engineering
    </text>

    <!-- Badges Capsule Row -->
    <g transform="translate(30, 88)">
      <!-- Capsule 1 -->
      <rect x="0" y="0" width="150" height="30" rx="15" fill="#1e1b4b" stroke="#6366f1" stroke-width="1"/>
      <circle cx="15" cy="15" r="5" fill="#818cf8"/>
      <text x="28" y="20" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="12" font-weight="600" fill="#c7d2fe">
        {total_contribs}+ Contributions
      </text>

      <!-- Capsule 2 -->
      <rect x="162" y="0" width="140" height="30" rx="15" fill="#064e3b" stroke="#10b981" stroke-width="1"/>
      <circle cx="177" cy="15" r="5" fill="#34d399"/>
      <text x="190" y="20" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="12" font-weight="600" fill="#a7f3d0">
        {total_repos} Repositories
      </text>

      <!-- Capsule 3 -->
      <rect x="314" y="0" width="170" height="30" rx="15" fill="#4c1d95" stroke="#a855f7" stroke-width="1"/>
      <circle cx="329" cy="15" r="5" fill="#c084fc"/>
      <text x="342" y="20" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="12" font-weight="600" fill="#e9d5ff">
        C# • Swift • Kotlin • TS
      </text>
    </g>
  </g>
</svg>'''
    save_svg_file(svg, out)
    return svg


def render_profile_overview(user, total_contribs, total_repos, stars, followers, out=None):
    """Render profile metrics overview SVG card."""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="410" height="210" viewBox="0 0 410 210" fill="none">
  <defs>
    <linearGradient id="cardBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#0b0f19" />
    </linearGradient>
    <linearGradient id="accent1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#818cf8" />
      <stop offset="100%" stop-color="#c084fc" />
    </linearGradient>
    <linearGradient id="accent2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="100%" stop-color="#34d399" />
    </linearGradient>
  </defs>

  <rect width="410" height="210" rx="16" fill="url(#cardBg)" stroke="#1e293b" stroke-width="1.5"/>

  <text x="24" y="38" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">
    📊 Profile Metrics
  </text>
  <line x1="24" y1="50" x2="386" y2="50" stroke="#334155" stroke-width="1" stroke-dasharray="4 4" />

  <g transform="translate(24, 68)">
    <rect x="0" y="0" width="174" height="54" rx="10" fill="#1e293b" opacity="0.6" stroke="#334155" stroke-width="1"/>
    <path d="M 16 18 L 22 28 L 34 16" fill="none" stroke="#818cf8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="44" y="24" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="20" font-weight="800" fill="url(#accent1)">{total_contribs}</text>
    <text x="44" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="11" font-weight="500" fill="#94a3b8">Total Contributions</text>

    <rect x="188" y="0" width="174" height="54" rx="10" fill="#1e293b" opacity="0.6" stroke="#334155" stroke-width="1"/>
    <path d="M 204 18 C 204 18, 210 16, 216 20 C 222 24, 222 30, 222 30" fill="none" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round"/>
    <circle cx="204" cy="18" r="3" fill="#38bdf8"/>
    <circle cx="222" cy="30" r="3" fill="#38bdf8"/>
    <text x="232" y="24" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="20" font-weight="800" fill="url(#accent2)">{total_repos}</text>
    <text x="232" y="40" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="11" font-weight="500" fill="#94a3b8">Public Repositories</text>

    <rect x="0" y="66" width="174" height="54" rx="10" fill="#1e293b" opacity="0.6" stroke="#334155" stroke-width="1"/>
    <polygon points="20,13 23,20 30,21 25,26 26,33 20,29 14,33 15,26 10,21 17,20" fill="#fbbf24"/>
    <text x="44" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="20" font-weight="800" fill="#fde047">{stars}</text>
    <text x="44" y="106" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="11" font-weight="500" fill="#94a3b8">Stargazers Earned</text>

    <rect x="188" y="66" width="174" height="54" rx="10" fill="#1e293b" opacity="0.6" stroke="#334155" stroke-width="1"/>
    <circle cx="206" cy="84" r="5" fill="#f43f5e"/>
    <path d="M 198 98 C 198 90, 214 90, 214 98" fill="none" stroke="#f43f5e" stroke-width="2"/>
    <text x="232" y="90" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="20" font-weight="800" fill="#fda4af">{followers}</text>
    <text x="232" y="106" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="11" font-weight="500" fill="#94a3b8">Followers</text>
  </g>
</svg>'''
    save_svg_file(svg, out)
    return svg


def render_top_langs(langs, out=None, max_items=TOP_LANG_COUNT):
    """Render top languages progress bar and legend SVG card."""
    items = sorted(langs.items(), key=lambda kv: kv[1], reverse=True)
    total = sum(v for _, v in items) or 1
    top_list = items[:max_items]
    leftover = sum(v for _, v in items[max_items:])
    if leftover > 0:
        top_list.append(('Others', leftover))

    svg_lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="410" height="210" viewBox="0 0 410 210" fill="none">',
        '  <defs>',
        '    <linearGradient id="cardBgL" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#0f172a" />',
        '      <stop offset="100%" stop-color="#0b0f19" />',
        '    </linearGradient>',
        '  </defs>',
        '  <rect width="410" height="210" rx="16" fill="url(#cardBgL)" stroke="#1e293b" stroke-width="1.5"/>',
        '  <text x="24" y="38" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">⚡ Most Used Languages</text>',
        '  <line x1="24" y1="50" x2="386" y2="50" stroke="#334155" stroke-width="1" stroke-dasharray="4 4" />',
    ]

    bar_x, bar_y, bar_w, bar_h = 24, 66, 362, 10
    svg_lines.append(f'  <g transform="translate({bar_x}, {bar_y})">')
    svg_lines.append(f'    <rect width="{bar_w}" height="{bar_h}" rx="5" fill="#1e293b"/>')

    cur_x = 0
    for name, size in top_list:
        pct = size / total
        w = pct * bar_w
        color = LANG_COLORS.get(name, DEFAULT_LANG_COLOR)
        if w > 0.5:
            svg_lines.append(f'    <rect x="{cur_x:.1f}" y="0" width="{w:.1f}" height="{bar_h}" rx="2" fill="{color}"/>')
            cur_x += w
    svg_lines.append('  </g>')

    svg_lines.append('  <g transform="translate(24, 96)">')
    for i, (name, size) in enumerate(top_list):
        pct = (size / total) * 100
        color = LANG_COLORS.get(name, DEFAULT_LANG_COLOR)
        col, row = i % 2, i // 2
        x, y = col * 186, row * 26

        svg_lines.append(f'    <g transform="translate({x}, {y})">')
        svg_lines.append(f'      <circle cx="6" cy="10" r="5" fill="{color}"/>')
        svg_lines.append(f'      <text x="18" y="14" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif" font-size="13" font-weight="600" fill="#e2e8f0">{name}</text>')
        svg_lines.append(f'      <text x="170" y="14" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif" font-size="12" font-weight="500" fill="#94a3b8" text-anchor="end">{pct:.1f}%</text>')
        svg_lines.append('    </g>')
    svg_lines.append('  </g>')

    svg_lines.append('</svg>')
    svg_content = '\n'.join(svg_lines)
    save_svg_file(svg_content, out)
    return svg_content


def render_streaks(streak_info, out=None):
    """Render contribution streak SVG banner."""
    current = streak_info.get('current', 0)
    longest = streak_info.get('longest', 0)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="850" height="150" viewBox="0 0 850 150" fill="none">
  <defs>
    <linearGradient id="streakBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f19" />
      <stop offset="100%" stop-color="#111827" />
    </linearGradient>
    <linearGradient id="fireGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#f97316" />
      <stop offset="100%" stop-color="#eab308" />
    </linearGradient>
  </defs>

  <rect width="850" height="150" rx="16" fill="url(#streakBg)" stroke="#1e293b" stroke-width="1.5"/>

  <g transform="translate(40, 25)">
    <path d="M 25 10 C 25 10, 35 25, 35 35 C 35 48, 24 55, 20 55 C 16 55, 5 48, 5 35 C 5 22, 18 12, 18 12 C 18 12, 15 22, 22 28 C 26 20, 25 10, 25 10 Z" fill="url(#fireGrad)"/>
    <text x="50" y="32" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="28" font-weight="900" fill="#f8fafc">{current} Days</text>
    <text x="50" y="52" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="13" font-weight="600" fill="#fb923c">Current Contribution Streak</text>
  </g>

  <line x1="300" y1="30" x2="300" y2="120" stroke="#334155" stroke-width="1" stroke-dasharray="4 4"/>

  <g transform="translate(340, 25)">
    <text x="0" y="32" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="28" font-weight="900" fill="#f8fafc">{longest} Days</text>
    <text x="0" y="52" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="13" font-weight="600" fill="#a78bfa">Personal Record Streak</text>
  </g>

  <line x1="580" y1="30" x2="580" y2="120" stroke="#334155" stroke-width="1" stroke-dasharray="4 4"/>

  <g transform="translate(620, 35)">
    <rect x="0" y="0" width="190" height="80" rx="12" fill="#1e1b4b" stroke="#4c1d95" stroke-width="1"/>
    <text x="95" y="35" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="12" font-weight="600" fill="#c7d2fe" text-anchor="middle">CONTRIBUTOR STATUS</text>
    <text x="95" y="60" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="16" font-weight="800" fill="#38bdf8" text-anchor="middle">⚡ Active Polyglot</text>
  </g>
</svg>'''
    save_svg_file(svg, out)
    return svg


def render_activity_radar(langs, out=None):
    """Render polar skill radar graph SVG card."""
    domains = {
        'Mobile': langs.get('Swift', 0) + langs.get('Kotlin', 0),
        'Desktop/.NET': langs.get('C#', 0),
        'Web Frontend': langs.get('TypeScript', 0) + langs.get('CSS', 0) + langs.get('HTML', 0) + langs.get('JavaScript', 0),
        'AI / Data': langs.get('Python', 0) + langs.get('Jupyter Notebook', 0),
        'Systems/CLI': langs.get('C', 0) + langs.get('Shell', 0) + langs.get('PowerShell', 0),
    }

    max_v = max(domains.values()) or 1
    normalized = {k: 0.35 + 0.60 * (v / max_v) for k, v in domains.items()}

    cx, cy, r = 205, 140, 70
    angles = [i * (2 * math.pi / 5) - math.pi / 2 for i in range(5)]
    labels = list(domains.keys())

    points = []
    for i, a in enumerate(angles):
        val = normalized[labels[i]]
        px = cx + r * val * math.cos(a)
        py = cy + r * val * math.sin(a)
        points.append(f"{px:.1f},{py:.1f}")

    poly_str = " ".join(points)

    svg_lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="410" height="230" viewBox="0 0 410 230" fill="none">',
        '  <defs>',
        '    <linearGradient id="radarBg" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#0f172a" />',
        '      <stop offset="100%" stop-color="#0b0f19" />',
        '    </linearGradient>',
        '    <linearGradient id="polyGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.6"/>',
        '      <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.6"/>',
        '    </linearGradient>',
        '  </defs>',
        '  <rect width="410" height="230" rx="16" fill="url(#radarBg)" stroke="#1e293b" stroke-width="1.5"/>',
        '  <text x="24" y="34" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">🎯 Skill Radar Matrix</text>',
        '  <line x1="24" y1="44" x2="386" y2="44" stroke="#334155" stroke-width="1" stroke-dasharray="4 4" />',
    ]

    for level in [0.33, 0.66, 1.0]:
        ring_pts = [f"{(cx + r * level * math.cos(a)):.1f},{(cy + r * level * math.sin(a)):.1f}" for a in angles]
        svg_lines.append(f'  <polygon points="{" ".join(ring_pts)}" fill="none" stroke="#334155" stroke-width="1" stroke-dasharray="2 2"/>')

    for i, a in enumerate(angles):
        ax = cx + r * math.cos(a)
        ay = cy + r * math.sin(a)
        svg_lines.append(f'  <line x1="{cx}" y1="{cy}" x2="{ax:.1f}" y2="{ay:.1f}" stroke="#334155" stroke-width="1"/>')
        
        lx = cx + (r + 22) * math.cos(a)
        ly = cy + (r + 14) * math.sin(a)
        anchor = "middle"
        if math.cos(a) > 0.3: anchor = "start"
        elif math.cos(a) < -0.3: anchor = "end"
        svg_lines.append(f'  <text x="{lx:.1f}" y="{ly:.1f}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif" font-size="11" font-weight="600" fill="#cbd5e1" text-anchor="{anchor}">{labels[i]}</text>')

    svg_lines.append(f'  <polygon points="{poly_str}" fill="url(#polyGrad)" stroke="#38bdf8" stroke-width="2"/>')
    for p in points:
        x, y = p.split(',')
        svg_lines.append(f'  <circle cx="{x}" cy="{y}" r="4" fill="#a78bfa" stroke="#f8fafc" stroke-width="1.5"/>')

    svg_lines.append('</svg>')
    svg_content = '\n'.join(svg_lines)
    save_svg_file(svg_content, out)
    return svg_content


def render_productive_time(days, out=None):
    """Render weekday activity breakdown histogram SVG card."""
    bywd = [0] * 7
    for d in days:
        dt = parse_iso_date(d['date'])
        wd = dt.weekday()
        bywd[wd] += d['contributionCount']

    labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    maxv = max(bywd) or 1
    highlight_idx = max(range(len(bywd)), key=lambda i: bywd[i]) if any(bywd) else 2

    svg_lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="410" height="230" viewBox="0 0 410 230" fill="none">',
        '  <defs>',
        '    <linearGradient id="timeBg" x1="0%" y1="0%" x2="100%" y2="100%">',
        '      <stop offset="0%" stop-color="#0f172a" />',
        '      <stop offset="100%" stop-color="#0b0f19" />',
        '    </linearGradient>',
        '    <linearGradient id="activeBar" x1="0%" y1="100%" x2="0%" y2="0%">',
        '      <stop offset="0%" stop-color="#6366f1" />',
        '      <stop offset="100%" stop-color="#38bdf8" />',
        '    </linearGradient>',
        '    <linearGradient id="peakBar" x1="0%" y1="100%" x2="0%" y2="0%">',
        '      <stop offset="0%" stop-color="#ec4899" />',
        '      <stop offset="100%" stop-color="#f43f5e" />',
        '    </linearGradient>',
        '  </defs>',
        '  <rect width="410" height="230" rx="16" fill="url(#timeBg)" stroke="#1e293b" stroke-width="1.5"/>',
        '  <text x="24" y="34" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">📈 Activity Breakdown</text>',
        '  <line x1="24" y1="44" x2="386" y2="44" stroke="#334155" stroke-width="1" stroke-dasharray="4 4" />',
    ]

    start_x, gap, bar_w, y_base, max_h = 36, 14, 36, 180, 100

    for i, val in enumerate(bywd):
        h = max(6, int((val / maxv) * max_h))
        x = start_x + i * (bar_w + gap)
        is_peak = (i == highlight_idx)
        bar_fill = "url(#peakBar)" if is_peak else "url(#activeBar)"

        svg_lines.append(f'    <rect x="{x}" y="{y_base - h}" width="{bar_w}" height="{h}" rx="6" fill="{bar_fill}"/>')
        svg_lines.append(f'    <text x="{x + bar_w/2:.1f}" y="{y_base - h - 6}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif" font-size="11" font-weight="700" fill="{"#f43f5e" if is_peak else "#94a3b8"}" text-anchor="middle">{val}</text>')
        svg_lines.append(f'    <text x="{x + bar_w/2:.1f}" y="{y_base + 18}" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif" font-size="12" font-weight="600" fill="#cbd5e1" text-anchor="middle">{labels[i]}</text>')

    svg_lines.append(f'  <text x="205" y="218" font-family="-apple-system, BlinkMacSystemFont, \'Segoe UI\', sans-serif" font-size="11" font-weight="500" fill="#94a3b8" text-anchor="middle">🔥 Peak Activity: {labels[highlight_idx]} ({bywd[highlight_idx]} contributions)</text>')
    svg_lines.append('</svg>')

    svg_content = '\n'.join(svg_lines)
    save_svg_file(svg_content, out)
    return svg_content
