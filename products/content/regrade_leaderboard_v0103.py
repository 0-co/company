#!/usr/bin/env python3
"""
Re-grade affected MCP servers with agent-friend v0.103.0.
Check 52: number_should_be_integer — param named page/limit/offset/count etc.
uses type 'number' instead of 'integer', allowing fractional values that most
APIs reject.

Score changes:
  sentry: 36.6→0.0 (206 warnings, at correctness floor)
  flightradar-mcp: 77.3→73.3 (-4.0)
  dbhub: 66.3→62.3 (-4.0)
"""

import sys
import os
import re
import json

sys.path.insert(0, '/tmp/af-new-session220')

from agent_friend.grade import grade_tools
from agent_friend.validate import validate_tools

RESEARCH = '/home/agent/company/research'
HTML_PATH = '/home/agent/company/docs/leaderboard.html'


def grade_color(score):
    if score >= 90: return '#22c55e'
    if score >= 80: return '#86efac'
    if score >= 70: return '#fbbf24'
    if score >= 60: return '#fb923c'
    if score >= 50: return '#f87171'
    return '#ef4444'


def grade_to_css_class(grade):
    return 'grade-' + grade.replace('+', 'plus').replace('-', 'minus')


def issues_level(n):
    if n <= 5: return 'issues-low'
    if n <= 20: return 'issues-medium'
    return 'issues-high'


SERVERS_TO_REGRADE = {
    'sentry':         f'{RESEARCH}/sentry_mcp_tools.json',
    'flightradar-mcp': f'{RESEARCH}/flightradar_mcp_tools.json',
    'dbhub':          f'{RESEARCH}/dbhub_mcp_tools.json',
}


def run_grade(schema_path):
    try:
        data = json.load(open(schema_path))
    except Exception as e:
        return None, f'JSON parse error: {e}'
    if isinstance(data, dict) and 'tools' in data:
        data = data['tools']
    try:
        result = grade_tools(data)
    except Exception as e:
        return None, f'grade_tools error: {e}'
    try:
        issues, _ = validate_tools(data)
        total_issues = len(issues)
    except:
        total_issues = 0
    return {
        'overall_score': result['overall_score'],
        'overall_grade': result['overall_grade'],
        'correctness_score': result['correctness']['score'],
        'efficiency_score': result['efficiency']['score'],
        'quality_score': result['quality']['score'],
        'tool_count': result['tool_count'],
        'total_tokens': result['total_tokens'],
        'avg_tokens': round(result['total_tokens'] / result['tool_count']) if result['tool_count'] > 0 else 0,
        'total_issues': total_issues,
    }, None


def update_server_in_html(content, server_id, new_data):
    pattern = rf'(<tr class="data-row[^"]*" data-server="{re.escape(server_id)}">)(.*?)(</tr>)'

    def replace_row(m):
        prefix = m.group(1)
        row_inner = m.group(2)
        suffix = m.group(3)
        score = new_data['overall_score']
        grade = new_data['overall_grade']
        grade_class = grade_to_css_class(grade)
        color = grade_color(score)
        tool_count = new_data['tool_count']
        total_tokens = new_data['total_tokens']
        avg_tokens = new_data['avg_tokens']
        total_issues = new_data['total_issues']
        issue_level = issues_level(total_issues)

        # Update score bar
        row_inner = re.sub(
            r'(<td class="r">)\d+\.?\d*(<span class="score-bar-bg">.*?</span></td>)',
            lambda mm: f'{mm.group(1)}{score:.1f}{mm.group(2)}',
            row_inner, flags=re.DOTALL
        )
        # Update score bar fill width
        row_inner = re.sub(
            r'(<span class="score-bar" style="width:)\d+\.?\d*(%)',
            f'\\g<1>{score:.1f}\\2',
            row_inner
        )
        # Update grade badge
        row_inner = re.sub(
            r'<td><span class="grade-badge grade-[^"]*">([^<]+)</span></td>',
            f'<td><span class="grade-badge {grade_class}">{grade}</span></td>',
            row_inner
        )
        # Update numeric columns
        row_inner = re.sub(
            r'(<td class="r">)\d+(</td>)\s*(<td class="r">)\d[\d,]*(</td>)\s*(<td class="r">)\d+(</td>)\s*(<td class="r"><span class="issues-badge issues-[^"]*">)\d+(</span></td>)',
            f'<td class="r">{tool_count}</td>\n            <td class="r">{total_tokens:,}</td>\n            <td class="r">{avg_tokens}</td>\n            <td class="r"><span class="issues-badge {issue_level}">{total_issues}</span></td>',
            row_inner
        )
        return prefix + row_inner + suffix

    new_content, count = re.subn(pattern, replace_row, content, flags=re.DOTALL)
    return new_content, count


def main():
    with open(HTML_PATH) as f:
        content = f.read()

    updates = []
    for server_id, path in SERVERS_TO_REGRADE.items():
        result, err = run_grade(path)
        if err:
            print(f"ERROR {server_id}: {err}")
            continue

        # Get current score from HTML
        m = re.search(rf'data-server="{re.escape(server_id)}"[^>]*>.*?<td class="r">(\d+\.?\d*)<span', content, re.DOTALL)
        old_score = float(m.group(1)) if m else None

        content, count = update_server_in_html(content, server_id, result)
        if count:
            print(f"Updated {server_id}: {old_score}→{result['overall_score']:.1f} ({result['overall_grade']})")
            updates.append((server_id, old_score, result['overall_score']))
        else:
            print(f"WARNING: Could not find/update {server_id} in HTML")

    with open(HTML_PATH, 'w') as f:
        f.write(content)

    print(f"\nDone. {len(updates)} servers updated.")
    for sid, old, new in updates:
        print(f"  {sid}: {old}→{new:.1f}")


if __name__ == '__main__':
    main()
