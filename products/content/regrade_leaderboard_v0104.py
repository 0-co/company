#!/usr/bin/env python3
"""
Re-grade affected MCP servers with agent-friend v0.104.0.
Check 48 extended: 6 new orchestration-hint patterns.
Also corrects 4 servers mis-scored by v0.103.0 check52 double-counting.

Score changes:
  windbg: 99.1→91.1 (-8.0, A+→A-)  — 2 new 'Use this tool when' patterns
  chunkhound: 40.3→36.3 (-4.0)      — 1 new pattern
  web-eval-agent: 34.1→30.1 (-4.0)  — 1 new pattern
  genai-toolbox: 24.3→25.2 (+0.9)   — check52 double-count fix
  webex-mcp: 29.7→38.1 (+8.4)       — check52 double-count fix
  bitwarden-mcp: 11.4→34.5 (+23.1)  — check52 double-count fix
  sentry: 0.0→36.6 (+36.6)          — wrong schema file fix
"""

import sys
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
    'windbg':        f'{RESEARCH}/windbg_mcp_tools.json',
    'chunkhound':    f'{RESEARCH}/chunkhound_mcp_tools.json',
    'web-eval-agent': f'{RESEARCH}/web_eval_agent_tools.json',
    'genai-toolbox': f'{RESEARCH}/genai_toolbox_tools.json',
    'webex-mcp':     f'{RESEARCH}/webex_mcp_tools.json',
    'bitwarden-mcp': f'{RESEARCH}/bitwarden_mcp_tools.json',
    'sentry':        f'{RESEARCH}/sentry_tools.json',
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

        row_inner = re.sub(
            r'(<td class="r">)\d+\.?\d*(<span class="score-bar-bg">.*?</span></td>)',
            lambda mm: f'{mm.group(1)}{score:.1f}{mm.group(2)}',
            row_inner, flags=re.DOTALL
        )
        row_inner = re.sub(
            r'(<span class="score-bar" style="width:)\d+\.?\d*(%)',
            f'\\g<1>{score:.1f}\\2',
            row_inner
        )
        row_inner = re.sub(
            r'(<span class="score-bar-fill" data-width=)"[^"]*"',
            f'\\g<1>"{score:.1f}"',
            row_inner
        )
        row_inner = re.sub(
            r'<td><span class="grade-badge grade-[^"]*">([^<]+)</span></td>',
            f'<td><span class="grade-badge {grade_class}">{grade}</span></td>',
            row_inner
        )
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
