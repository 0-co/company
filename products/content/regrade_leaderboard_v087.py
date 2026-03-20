#!/usr/bin/env python3
"""
Re-grade all MCP servers in leaderboard.html with agent-friend v0.87.0.
Check 37: boolean_default_missing — optional boolean param has no 'default' field.
"""

import sys
import os
import re
import json

sys.path.insert(0, '/tmp/af-new-session220')

from agent_friend.grade import grade_tools
from agent_friend.validate import validate_tools

RESEARCH = '/home/agent/company/research'
EXAMPLES = '/home/agent/company/docs/examples'
SCHEMAS = '/home/agent/company/research/mcp-schemas'
HTML_PATH = '/home/agent/company/docs/leaderboard.html'

MANUAL_MAP = {
    'postgres':             f'{SCHEMAS}/postgres.json',
    'sqlite':               None,
    'google-tasks-mcp':     None,
    'mark3labs-filesystem': f'{RESEARCH}/mcp_filesystem_mark3labs_tools.json',
    'puppeteer':            f'{EXAMPLES}/puppeteer.json',
    'discord-v3-mcp':       f'{RESEARCH}/discordmcp_v3_tools.json',
    'brave':                f'{SCHEMAS}/brave-search.json',
    'time':                 f'{SCHEMAS}/time.json',
    'sequentialthinking':   f'{SCHEMAS}/sequentialthinking.json',
    'googlemaps':           f'{RESEARCH}/google_maps_tools.json',
    'github':               f'{RESEARCH}/github-mcp-tools.json',
    'memory':               f'{SCHEMAS}/memory.json',
    'fetch':                f'{SCHEMAS}/fetch.json',
    'chrome-devtools':      f'{RESEARCH}/chrome-devtools-mcp-tools.json',
    'playwright-ms':        f'{RESEARCH}/playwright_mcp_microsoft_tools.json',
    'blender':              f'{EXAMPLES}/blender.json',
    'github-official':      f'{EXAMPLES}/github-official.json',
    'cloudflare':           f'{EXAMPLES}/cloudflare.json',
    'tavily':               f'{EXAMPLES}/tavily.json',
    'ga4':                  f'{EXAMPLES}/ga4.json',
    'context7':             f'{RESEARCH}/context7_tools.json',
    'sentry':               f'{EXAMPLES}/sentry.json',
    'sentry-official':      f'{RESEARCH}/sentry_mcp_tools.json',
    'notion':               f'{EXAMPLES}/notion.json',
    'exa':                  f'{EXAMPLES}/exa.json',
    'slack':                f'{EXAMPLES}/slack.json',
    'filesystem':           f'{EXAMPLES}/filesystem.json',
    'e2b':                  f'{EXAMPLES}/e2b.json',
    'playwright':           f'{RESEARCH}/playwright-mcp-tools.json',
    'ea-playwright':        f'{RESEARCH}/ea_playwright_mcp_tools.json',
    'git':                  f'{SCHEMAS}/git.json',
    'mcp-everything':       f'{RESEARCH}/mcp_everything_tools.json',
    'mcp-installer':        f'{RESEARCH}/mcp_installer_tools.json',
    'mcp-taskmanager':      f'{RESEARCH}/mcp_taskmanager_tools.json',
    'mcp-chrome':           f'{RESEARCH}/mcp_chrome_tools.json',
    'korotovsky-slack':     f'{RESEARCH}/korotovsky_slack_mcp_tools.json',
    'awkoy-notion':         f'{RESEARCH}/awkoy_notion_tools.json',
    'danhilse-notion':      f'{RESEARCH}/danhilse_notion_mcp_tools.json',
    'suekou-notion':        f'{RESEARCH}/suekou_notion_mcp_tools.json',
    'discord-hanweg':       f'{RESEARCH}/discord_mcp_tools_v1.json',
    'discord-barryyip':     f'{RESEARCH}/discord_mcp_tools_v2.json',
    'google-workspace':     f'{RESEARCH}/google_workspace_mcp_tools.json',
    'google-sheets':        f'{RESEARCH}/google_sheets_mcp_tools.json',
    'google-calendar-mcp':  f'{RESEARCH}/google_calendar_mcp_tools.json',
    'calclavia-obsidian':   f'{RESEARCH}/obsidian_mcp_tools.json',
    'obsidian':             f'{RESEARCH}/obsidian_mcp_tools.json',
    'mongodb':              f'{RESEARCH}/mongodb_mcp_tools.json',
    'mongodb-lens':         f'{RESEARCH}/mongodb_lens_tools.json',
    'pinecone-official':    f'{RESEARCH}/pinecone_official_tools.json',
    'pinecone-sirmews':     f'{RESEARCH}/pinecone_sirmews_tools.json',
    'genai-toolbox':        f'{RESEARCH}/genai_toolbox_mcp_tools.json',
    'mysql-mcp':            f'{RESEARCH}/mysql_mcp_tools.json',
    'zapier-mcp':           f'{RESEARCH}/zapier_mcp_tools.json',
    'universal-db':         f'{RESEARCH}/universal_db_mcp_tools.json',
    'monday-mcp':           f'{RESEARCH}/monday_tools.json',
    'web-eval-agent':       f'{RESEARCH}/web_eval_agent_tools.json',
    'atlassian':            None,
    'firecrawl':            None,
    'browser-tools-mcp':    None,
    'mcp-gdrive':           None,
    'mcp-feedback-enhanced': None,
    'mcp-youtube':          None,
    'zoom-transcript-mcp':  None,
    'mixpanel-moonbirdai':  f'{RESEARCH}/mixpanel_mcp_tools.json',
    'vercel-next':          f'{RESEARCH}/vercel_nextdevtools_mcp_tools.json',
    'line-bot-mcp':         f'{RESEARCH}/line_mcp_tools.json',
    'chart':                f'{RESEARCH}/chart_mcp_tools.json',
}


def find_schema_file(server_id):
    if server_id in MANUAL_MAP:
        return MANUAL_MAP[server_id]
    normalized = server_id.replace('-', '_')
    candidates = [
        f'{RESEARCH}/{normalized}_tools.json',
        f'{RESEARCH}/{normalized}_mcp_tools.json',
        f'{EXAMPLES}/{normalized}.json',
        f'{EXAMPLES}/{server_id}.json',
    ]
    base = re.sub(r'[-_]mcp$', '', normalized)
    candidates.extend([
        f'{RESEARCH}/{base}_mcp_tools.json',
        f'{RESEARCH}/{base}_tools.json',
    ])
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def grade_color(score):
    if score >= 90:
        return 'var(--accent-cyan)'
    elif score >= 70:
        return 'var(--accent-gold)'
    else:
        return 'var(--accent-red)'


def grade_to_css_class(grade_letter):
    mapping = {
        'A+': 'grade-aplus', 'A': 'grade-a', 'A-': 'grade-aminus',
        'B+': 'grade-bplus', 'B': 'grade-b', 'B-': 'grade-bminus',
        'C+': 'grade-cplus', 'C': 'grade-c', 'C-': 'grade-cminus',
        'D+': 'grade-dplus', 'D': 'grade-d', 'D-': 'grade-dminus',
        'F': 'grade-f',
    }
    return mapping.get(grade_letter, 'grade-f')


def issues_level(total_issues):
    if total_issues <= 5:
        return 'issues-low'
    elif total_issues <= 20:
        return 'issues-medium'
    else:
        return 'issues-high'


def run_grade(schema_path):
    try:
        data = json.load(open(schema_path))
    except Exception as e:
        return None, f'JSON parse error: {e}'
    if isinstance(data, dict) and 'tools' in data and isinstance(data['tools'], list):
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


def get_boolean_default_details(schema_path):
    """Get details about boolean_default_missing issues in a server."""
    try:
        data = json.load(open(schema_path))
    except:
        return []
    if isinstance(data, dict) and 'tools' in data:
        data = data['tools']
    try:
        issues, _ = validate_tools(data)
        return [i for i in issues if i.check == 'boolean_default_missing']
    except:
        return []


def extract_current_score(content, server_id):
    pattern = rf'<tr class="data-row[^"]*" data-server="{re.escape(server_id)}">(.*?)</tr>'
    m = re.search(pattern, content, re.DOTALL)
    if not m:
        return None
    row_html = m.group(1)
    score_m = re.search(r'<td class="r">(\d+\.?\d*)<span class="score-bar-bg">', row_html)
    if score_m:
        return float(score_m.group(1))
    return None


def update_data_row(content, server_id, new_data):
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
            r'<td class="grade-cell"><div class="grade-badge grade-[^"]*">.*?</div></td>',
            f'<td class="grade-cell"><div class="grade-badge {grade_class}">{grade}</div></td>',
            row_inner
        )
        score_bar_pattern = r'<td class="r">[\d.]+<span class="score-bar-bg">.*?</span></span></td>'
        parts = re.split(score_bar_pattern, row_inner, maxsplit=1)
        if len(parts) == 2:
            before_score = parts[0]
            after_score = parts[1]
            score_td = f'<td class="r">{score}<span class="score-bar-bg"><span class="score-bar-fill" data-width="{score}" style="background: {color};"></span></span></td>'
            after_score = re.sub(
                r'(<td class="r">)\d+(</td>)\s*(<td class="r">)\d[\d,]*(</td>)\s*(<td class="r">)\d+(</td>)\s*(<td class="r"><span class="issues-badge issues-[^"]*">)\d+(</span></td>)',
                f'<td class="r">{tool_count}</td>\n            <td class="r">{total_tokens:,}</td>\n            <td class="r">{avg_tokens}</td>\n            <td class="r"><span class="issues-badge {issue_level}">{total_issues}</span></td>',
                after_score
            )
            row_inner = before_score + score_td + after_score
        return prefix + row_inner + suffix

    return re.sub(pattern, replace_row, content, flags=re.DOTALL)


def update_detail_row(content, server_id, new_data):
    pattern = rf'(<tr class="detail-row" data-server="{re.escape(server_id)}">(.*?)</tr>)'

    def replace_detail(m):
        full = m.group(0)
        c_score = new_data['correctness_score']
        e_score = new_data['efficiency_score']
        q_score = new_data['quality_score']
        c_color = grade_color(c_score)
        e_color = grade_color(e_score)
        q_color = grade_color(q_score)
        bars = re.findall(
            r'<div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="[\d.]+" style="background: [^;]+;"></div></div>\s*'
            r'<span class="breakdown-score" style="color: [^;]+;">[\d.]+</span>',
            full
        )
        if len(bars) >= 3:
            new_c = (f'<div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="{c_score}" '
                     f'style="background: {c_color};"></div></div>\n                    '
                     f'<span class="breakdown-score" style="color: {c_color};">{c_score}</span>')
            new_e = (f'<div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="{e_score}" '
                     f'style="background: {e_color};"></div></div>\n                    '
                     f'<span class="breakdown-score" style="color: {e_score};">{e_score}</span>')
            new_q = (f'<div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="{q_score}" '
                     f'style="background: {q_color};"></div></div>\n                    '
                     f'<span class="breakdown-score" style="color: {q_score};">{q_score}</span>')
            full = full.replace(bars[0], new_c, 1)
            full = full.replace(bars[1], new_e, 1)
            full = full.replace(bars[2], new_q, 1)
        return full

    return re.sub(pattern, replace_detail, content, flags=re.DOTALL)


def main():
    with open(HTML_PATH, 'r') as f:
        content = f.read()

    server_ids = re.findall(r'<tr class="data-row[^"]*" data-server="([^"]+)"', content)
    print(f"Found {len(server_ids)} servers in leaderboard")

    changes = []
    no_schema = []
    no_change = []
    all_fmt_issues = []

    for server_id in server_ids:
        schema_path = find_schema_file(server_id)
        if not schema_path or not os.path.exists(schema_path):
            no_schema.append(server_id)
            continue

        new_data, err = run_grade(schema_path)
        if err or new_data is None:
            print(f"  ERROR {server_id}: {err}")
            continue

        old_score = extract_current_score(content, server_id)
        new_score = round(new_data['overall_score'], 1)

        fmt_issues = get_boolean_default_details(schema_path)
        if fmt_issues:
            all_fmt_issues.append((server_id, fmt_issues))

        if old_score is not None and abs(old_score - new_score) < 0.05:
            no_change.append(server_id)
            continue

        changes.append((server_id, old_score, new_score, new_data['overall_grade']))
        content = update_data_row(content, server_id, new_data)
        content = update_detail_row(content, server_id, new_data)

    with open(HTML_PATH, 'w') as f:
        f.write(content)

    print(f"\n=== Results ===")
    print(f"Updated: {len(changes)} servers")
    print(f"No change: {len(no_change)} servers")
    print(f"No schema: {len(no_schema)} servers")

    if changes:
        print(f"\nChanges (sorted by drop):")
        for server_id, old, new, grade in sorted(changes, key=lambda x: (x[1] or 0) - x[2], reverse=True):
            arrow = f"{old}→{new}" if old else f"new: {new}"
            print(f"  {server_id}: {arrow} ({grade})")

    if all_fmt_issues:
        print(f"\n=== boolean_default_missing issues ({len(all_fmt_issues)} servers) ===")
        for server_id, issues in sorted(all_fmt_issues, key=lambda x: -len(x[1])):
            print(f"  {server_id}: {len(issues)} params")
            for iss in issues[:3]:
                print(f"    - {iss.message[:80]}")


if __name__ == '__main__':
    main()
