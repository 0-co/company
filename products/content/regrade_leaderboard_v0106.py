#!/usr/bin/env python3
"""
Re-grade affected MCP servers with agent-friend v0.106.0.
Check 54: optional_string_no_minlength — optional content-like string params with no minLength.

50 servers affected, 119 param hits.
No score changes (all affected servers already have correctness=0).
Issues count increases for all 50 affected servers.
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
    'algolia-mcp':       f'{RESEARCH}/algolia_mcp_tools.json',
    'amplitude-mcp':     f'{RESEARCH}/amplitude_mcp_tools.json',
    'argocd-mcp':        f'{RESEARCH}/argocd_mcp_tools.json',
    'asana-mcp':         f'{RESEARCH}/asana_mcp_tools.json',
    'auth0-mcp':         f'{RESEARCH}/auth0_mcp_tools.json',
    'aws':               f'{RESEARCH}/aws_mcp_tools.json',
    'azure-devops':      f'{RESEARCH}/azure_devops_mcp_tools.json',
    'bitwarden-mcp':     f'{RESEARCH}/bitwarden_mcp_tools.json',
    'chunkhound':        f'{RESEARCH}/chunkhound_mcp_tools.json',
    'cloudflare':        f'{RESEARCH}/cloudflare-mcp-tools.json',
    'cloudinary-mcp':    f'{RESEARCH}/cloudinary_mcp_tools.json',
    'codex-mcp':         f'{RESEARCH}/codex_mcp_tools.json',
    'contentful-mcp':    f'{RESEARCH}/contentful_mcp_tools.json',
    'datadog-mcp':       f'{RESEARCH}/datadog_mcp_tools.json',
    'docker-mcp':        f'{RESEARCH}/docker_mcp_tools.json',
    'drawio':            f'{RESEARCH}/drawio_mcp_tools.json',
    'ea-playwright':     f'{RESEARCH}/ea_playwright_mcp_tools.json',
    'github':            f'{RESEARCH}/github-mcp-tools.json',
    'gitlab-mcp':        f'{RESEARCH}/gitlab_mcp_tools.json',
    'google-sheets':     f'{RESEARCH}/google_sheets_mcp_tools.json',
    'google-workspace':  f'{RESEARCH}/google_workspace_mcp_tools.json',
    'grafana':           f'{RESEARCH}/grafana_mcp_tools.json',
    'groq-mcp':          f'{RESEARCH}/groq_mcp_tools.json',
    'hf-mcp':            f'{RESEARCH}/hf_mcp_tools.json',
    'klaviyo-mcp':       f'{RESEARCH}/klaviyo_mcp_tools.json',
    'korotovsky-slack':  f'{RESEARCH}/korotovsky_slack_mcp_tools.json',
    'mcp-chrome':        f'{RESEARCH}/mcp_chrome_tools.json',
    'mslearn':           f'{RESEARCH}/mslearn_mcp_tools.json',
    'n8n-mcp':           f'{RESEARCH}/n8n_mcp_tools.json',
    'neon':              f'{RESEARCH}/neon_mcp_tools.json',
    'notion':            f'{RESEARCH}/notion_mcp_tools.json',
    'okta-mcp':          f'{RESEARCH}/okta_mcp_tools.json',
    'pagerduty-mcp':     f'{RESEARCH}/pagerduty_mcp_tools.json',
    'planetscale-mcp':   f'{RESEARCH}/planetscale_mcp_tools.json',
    'playwright':        f'{RESEARCH}/playwright-mcp-tools.json',
    'playwright-ms':     f'{RESEARCH}/playwright_mcp_microsoft_tools.json',
    'postman-mcp':       f'{RESEARCH}/postman_mcp_tools.json',
    'redis-mcp':         f'{RESEARCH}/redis_mcp_tools.json',
    'sentry':            f'{RESEARCH}/sentry_mcp_tools.json',
    'sentry-official':   f'{RESEARCH}/sentry_tools.json',
    'shadcn':            f'{RESEARCH}/shadcn_mcp_tools.json',
    'snyk-mcp':          f'{RESEARCH}/snyk_mcp_tools.json',
    'suekou-notion':     f'{RESEARCH}/suekou_notion_mcp_tools.json',
    'tavily':            f'{RESEARCH}/tavily-mcp-tools.json',
    'telegram-mcp':      f'{RESEARCH}/telegram_mcp_tools.json',
    'temporal-mcp':      f'{RESEARCH}/temporal_mcp_tools.json',
    'todoist-mcp':       f'{RESEARCH}/todoist_mcp_tools.json',
    'unity-mcp':         f'{RESEARCH}/unity_mcp_tools.json',
    'wandb-mcp':         f'{RESEARCH}/wandb_mcp_tools.json',
    'whatsapp':          f'{RESEARCH}/whatsapp_mcp_tools.json',
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
    row_start = html.find(f'data-server="{server_id}"')
    if row_start == -1:
        print(f"  WARNING: {server_id} not found in HTML")
        return html

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
