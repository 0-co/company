#!/usr/bin/env python3
"""
Generate self-hosted SVG badges for all graded MCP servers in the leaderboard.
Output: docs/badges/{server-slug}.svg

Badge URL format: https://0-co.github.io/company/badges/{slug}.svg
Badge link: https://0-co.github.io/company/leaderboard.html#{slug}

Usage: python3 generate_badges.py
"""

import os
import re
from html.parser import HTMLParser

LEADERBOARD_PATH = os.path.join(os.path.dirname(__file__), '../../docs/leaderboard.html')
BADGES_DIR = os.path.join(os.path.dirname(__file__), '../../docs/badges')
BASE_URL = 'https://0-co.github.io/company'

# Grade color map (matches leaderboard CSS colors)
GRADE_COLORS = {
    'A+': ('#1a7a2e', '#22c55e', '#16a34a'),  # dark, light, border
    'A':  ('#1a7a2e', '#22c55e', '#16a34a'),
    'A-': ('#1a7a2e', '#4ade80', '#16a34a'),
    'B+': ('#1d4ed8', '#60a5fa', '#2563eb'),
    'B':  ('#1d4ed8', '#60a5fa', '#2563eb'),
    'B-': ('#1d4ed8', '#93c5fd', '#2563eb'),
    'C+': ('#854d0e', '#fbbf24', '#d97706'),
    'C':  ('#854d0e', '#fbbf24', '#d97706'),
    'D+': ('#9a3412', '#fb923c', '#c2410c'),
    'D':  ('#9a3412', '#fb923c', '#c2410c'),
    'D-': ('#9a3412', '#fb923c', '#c2410c'),
    'F':  ('#7f1d1d', '#f87171', '#dc2626'),
}

DEFAULT_COLOR = ('#374151', '#9ca3af', '#4b5563')


def make_svg(grade: str) -> str:
    """Generate an SVG badge for the given grade."""
    dark, light, border = GRADE_COLORS.get(grade, DEFAULT_COLOR)

    label = 'MCP Quality'
    value = grade

    # Calculate widths
    label_width = len(label) * 6.5 + 10
    value_width = len(value) * 8.5 + 14
    total_width = label_width + value_width

    label_cx = label_width / 2
    value_cx = label_width + value_width / 2

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_width:.0f}" height="20">
  <title>MCP Quality: {grade}</title>
  <linearGradient id="g" x2="0" y2="100%">
    <stop offset="0" stop-color="#fff" stop-opacity=".2"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r">
    <rect width="{total_width:.0f}" height="20" rx="3"/>
  </clipPath>
  <g clip-path="url(#r)">
    <rect width="{label_width:.0f}" height="20" fill="#555"/>
    <rect x="{label_width:.0f}" width="{value_width:.0f}" height="20" fill="{border}"/>
    <rect width="{total_width:.0f}" height="20" fill="url(#g)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="{label_cx:.1f}" y="15" fill="#010101" fill-opacity=".3">{label}</text>
    <text x="{label_cx:.1f}" y="14">{label}</text>
    <text x="{value_cx:.1f}" y="15" fill="#010101" fill-opacity=".3" font-weight="bold">{value}</text>
    <text x="{value_cx:.1f}" y="14" font-weight="bold">{value}</text>
  </g>
</svg>'''


class LeaderboardParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.servers = {}
        self._current_server = None
        self._in_grade_badge = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'tr' and attrs_dict.get('class') == 'data-row':
            self._current_server = attrs_dict.get('data-server')
        if self._current_server and tag == 'div' and 'grade-badge' in attrs_dict.get('class', ''):
            self._in_grade_badge = True

    def handle_data(self, data):
        if self._in_grade_badge and data.strip():
            self.servers[self._current_server] = data.strip()
            self._in_grade_badge = False
            self._current_server = None


def main():
    with open(LEADERBOARD_PATH, 'r') as f:
        content = f.read()

    parser = LeaderboardParser()
    parser.feed(content)
    servers = parser.servers

    print(f'Parsed {len(servers)} servers from leaderboard')

    os.makedirs(BADGES_DIR, exist_ok=True)

    for slug, grade in servers.items():
        svg = make_svg(grade)
        badge_path = os.path.join(BADGES_DIR, f'{slug}.svg')
        with open(badge_path, 'w') as f:
            f.write(svg)

    print(f'Generated {len(servers)} badges in {BADGES_DIR}')
    print()
    print('Badge URL format:')
    print(f'  {BASE_URL}/badges/{{slug}}.svg')
    print()
    print('Markdown example:')
    example_slug = list(servers.keys())[0] if servers else 'your-server'
    example_grade = servers.get(example_slug, 'A+')
    print(f'  [![MCP Quality: {example_grade}]({BASE_URL}/badges/{example_slug}.svg)]({BASE_URL}/leaderboard.html#{example_slug})')


if __name__ == '__main__':
    main()
