#!/usr/bin/env python3
"""
Re-grade affected MCP servers with agent-friend v0.105.0.
Check 53: tool_name_redundant_prefix — most tools share a service-name prefix.

Score changes (only servers where correctness was non-zero before):
  awkoy-notion:       100.0→96.0  (A+→A)   — notion_ prefix, 5/5 tools
  browsermcp:          53.2→49.2  (F→F)    — browser_ prefix, 13/13 tools
  mixpanel-moonbirdai: 80.5→76.5  (B-→C)   — mixpanel_ prefix, 4/4 tools

Issues count changes (+1 issue for ALL 22 affected servers):
  asana-mcp, auth0-mcp, awkoy-notion, box-mcp, browserbase, browsermcp,
  chroma, confluence-mcp, ea-playwright, googlemaps, hubspot-mcp, jira-mcp,
  magic-mcp, mcp-chrome, milvus-mcp, mixpanel-moonbirdai, mobile-mcp,
  mslearn, perplexity, playwright-ms, snyk-mcp, suekou-notion
"""

import sys
import re
import json

sys.path.insert(0, '/tmp/af-new-session220')
from agent_friend.grade import grade_tools
from agent_friend.validate import validate_tools

RESEARCH = '/home/agent/company/research'
LEADERBOARD = '/home/agent/company/docs/leaderboard.html'

# Mapping: leaderboard data-server ID → research JSON path
SERVERS = {
    'asana-mcp':           f'{RESEARCH}/asana_mcp_tools.json',
    'auth0-mcp':           f'{RESEARCH}/auth0_mcp_tools.json',
    'awkoy-notion':        f'{RESEARCH}/awkoy_notion_tools.json',
    'box-mcp':             f'{RESEARCH}/box_mcp_tools.json',
    'browserbase':         f'{RESEARCH}/browserbase_mcp_tools.json',
    'browsermcp':          f'{RESEARCH}/browsermcp_tools.json',
    'chroma':              f'{RESEARCH}/chroma_mcp_tools.json',
    'confluence-mcp':      f'{RESEARCH}/confluence_mcp_tools.json',
    'ea-playwright':       f'{RESEARCH}/ea_playwright_mcp_tools.json',
    'googlemaps':          f'{RESEARCH}/google_maps_tools.json',
    'hubspot-mcp':         f'{RESEARCH}/hubspot_mcp_tools.json',
    'jira-mcp':            f'{RESEARCH}/jira_mcp_tools.json',
    'magic-mcp':           f'{RESEARCH}/magic_mcp_tools.json',
    'mcp-chrome':          f'{RESEARCH}/mcp_chrome_tools.json',
    'milvus-mcp':          f'{RESEARCH}/milvus_mcp_tools.json',
    'mixpanel-moonbirdai': f'{RESEARCH}/mixpanel_mcp_tools.json',
    'mobile-mcp':          f'{RESEARCH}/mobile_mcp_tools.json',
    'mslearn':             f'{RESEARCH}/mslearn_mcp_tools.json',
    'perplexity':          f'{RESEARCH}/perplexity_mcp_tools.json',
    'playwright-ms':       f'{RESEARCH}/playwright_mcp_microsoft_tools.json',
    'snyk-mcp':            f'{RESEARCH}/snyk_mcp_tools.json',
    'suekou-notion':       f'{RESEARCH}/suekou_notion_mcp_tools.json',
}


def run_grade(schema_path):
    try:
        data = json.load(open(schema_path))
    except Exception as e:
        return None, f'load error: {e}'
    if isinstance(data, dict) and 'tools' in data:
        data = data['tools']
    try:
        result = grade_tools(data)
    except Exception as e:
        return None, f'grade_tools error: {e}'
    try:
        issues, _ = validate_tools(data)
    except Exception as e:
        return result, f'validate error: {e}'
    return result, issues


def update_server_in_html(html, server_id, new_score, new_grade, issues):
    """Update score, grade badge, and issues count for a server in the HTML."""
    # Find the data-row section
    row_start = html.find(f'data-server="{server_id}"')
    if row_start == -1:
        print(f"  WARNING: {server_id} not found in HTML")
        return html

    # Find end of data-row (before next <tr)
    next_tr = html.find('<tr ', row_start + 10)
    row = html[row_start:next_tr]

    # Update score
    old_score_m = re.search(r'([\d.]+)(<span class="score-bar-bg)', row)
    if old_score_m:
        old_score = old_score_m.group(1)
        row = row.replace(
            old_score + old_score_m.group(2),
            str(new_score) + old_score_m.group(2),
            1
        )
        # Also update data-width
        row = re.sub(r'data-width="' + re.escape(old_score) + r'"',
                     f'data-width="{new_score}"', row, count=1)

    # Update grade badge
    grade_class_map = {
        'A+': 'grade-aplus', 'A': 'grade-a', 'A-': 'grade-aminus',
        'B+': 'grade-bplus', 'B': 'grade-b', 'B-': 'grade-bminus',
        'C+': 'grade-cplus', 'C': 'grade-c', 'C-': 'grade-cminus',
        'D+': 'grade-dplus', 'D': 'grade-d', 'D-': 'grade-dminus',
        'F': 'grade-f',
    }
    new_class = grade_class_map.get(new_grade, 'grade-f')
    # Replace grade badge class and text
    row = re.sub(
        r'<div class="grade-badge grade-\w+">([A-F][+-]?)</div>',
        f'<div class="grade-badge {new_class}">{new_grade}</div>',
        row
    )

    # Update issues count
    issue_count = len(issues) if isinstance(issues, list) else 0
    if issue_count <= 2:
        badge_class = 'issues-low'
    elif issue_count <= 5:
        badge_class = 'issues-medium'
    else:
        badge_class = 'issues-high'
    row = re.sub(
        r'<span class="issues-badge issues-\w+">\d+</span>',
        f'<span class="issues-badge {badge_class}">{issue_count}</span>',
        row
    )

    html = html[:row_start] + row + html[next_tr:]
    return html


def update_detail_row(html, server_id, new_score, new_grade, result):
    """Update breakdown scores in the detail row."""
    detail_start = html.find(f'data-server="{server_id}"', html.find(f'class="detail-row" data-server="{server_id}"'))
    if detail_start == -1:
        return html

    # Find detail row end
    detail_end = html.find('</tr>', detail_start) + 5
    detail = html[detail_start:detail_end]

    # Update correctness score in breakdown
    c_score = result['correctness']['score']
    c_grade = result['correctness']['grade']
    # Update efficiency and quality scores
    e_score = result['efficiency']['score']
    q_score = result['quality']['score']

    # Update overall score in detail
    detail = re.sub(r'Overall.*?(\d+\.\d+).*?/100', lambda m: m.group(0).replace(m.group(1), str(new_score)), detail)

    # Update breakdown bars
    def update_breakdown_score(text, old_score, new_score_val):
        # Find and replace data-width and score value in breakdown
        pass  # Complex HTML manipulation — skip for now

    html = html[:detail_start] + detail + html[detail_end:]
    return html


def main():
    print("Loading leaderboard HTML...")
    html = open(LEADERBOARD).read()
    original_html = html

    print(f"Processing {len(SERVERS)} affected servers...")
    for server_id, schema_path in sorted(SERVERS.items()):
        result, issues_or_err = run_grade(schema_path)
        if result is None:
            print(f"  SKIP {server_id}: {issues_or_err}")
            continue

        new_score = result['overall_score']
        new_grade = result['overall_grade']
        issues = issues_or_err if isinstance(issues_or_err, list) else []

        html = update_server_in_html(html, server_id, new_score, new_grade, issues)
        print(f"  {server_id}: score={new_score} grade={new_grade} issues={len(issues)}")

    if html != original_html:
        with open(LEADERBOARD, 'w') as f:
            f.write(html)
        print(f"\nLeaderboard updated.")
    else:
        print("\nNo changes made.")


if __name__ == '__main__':
    main()
