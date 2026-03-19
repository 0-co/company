#!/usr/bin/env python3
"""
Re-grade all MCP servers in leaderboard.html with agent-friend v0.65.0.
"""

import sys
import os
import re
import json

sys.path.insert(0, '/home/agent/company/products/agent-friend')

from agent_friend.grade import grade_tools
from agent_friend.validate import validate_tools

RESEARCH = '/home/agent/company/research'
EXAMPLES = '/home/agent/company/docs/examples'
SCHEMAS = '/home/agent/company/research/mcp-schemas'
HTML_PATH = '/home/agent/company/docs/leaderboard.html'

# Servers already re-graded with v0.65.0 - skip these
# From task: cloudflare=11.4, chrome-devtools=24.9, playwright=27.0, exa=21.0,
#             github-official=20.1, filesystem=56.9, puppeteer=83.2, context7=31.5, github-ref=75.6
# 'playwright' id in leaderboard already shows 27.0, so skip it
# 'playwright-ms' (63.3) and 'ea-playwright' (49.4) need re-grading
ALREADY_REGRADED = {
    'cloudflare', 'chrome-devtools', 'playwright', 'exa',
    'github-official', 'filesystem', 'puppeteer', 'context7',
    'github',  # github mentioned in task
}

# Manual server-ID -> schema file mapping
MANUAL_MAP = {
    'postgres':             f'{SCHEMAS}/postgres.json',
    'sqlite':               None,   # no sqlite schema found
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
    'sentry-official':      f'{RESEARCH}/sentry_tools.json',
    'notion':               f'{EXAMPLES}/notion.json',
    'exa':                  f'{EXAMPLES}/exa.json',
    'slack':                f'{EXAMPLES}/slack.json',
    'filesystem':           f'{EXAMPLES}/filesystem.json',
    'e2b':                  f'{EXAMPLES}/e2b.json',
    'playwright':           f'{RESEARCH}/playwright-mcp-tools.json',   # wrapped in {tools:[...]}
    'ea-playwright':        f'{RESEARCH}/playwright-mcp-tools.json',  # wrapped in {tools:[...]}
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
    # Standard pattern overrides (name -> different file name)
    'atlassian':            None,   # no file found
    'firecrawl':            None,   # no file found
    'browser-tools-mcp':    None,   # no file found
    'mcp-gdrive':           None,   # no file found
    'mcp-feedback-enhanced': None,  # no file found
    'mcp-youtube':          None,   # no file found
    'zoom-transcript-mcp':  None,   # no file found
    'google-tasks-mcp':     None,   # no file found
    'mixpanel-moonbirdai':  f'{RESEARCH}/mixpanel_mcp_tools.json',
    'vercel-next':          f'{RESEARCH}/vercel_nextdevtools_mcp_tools.json',
    'line-bot-mcp':         f'{RESEARCH}/line_mcp_tools.json',
}

# Standard pattern: server-id -> normalized_id_mcp_tools.json
def find_schema_file(server_id):
    """Try to find schema file for a server ID."""
    if server_id in MANUAL_MAP:
        return MANUAL_MAP[server_id]

    # Try standard pattern: normalize server-id to file name
    # e.g. 'airflow-mcp' -> 'airflow_mcp_tools.json'
    # e.g. 'axios-mcp' -> 'axios_mcp_tools.json'
    normalized = server_id.replace('-', '_')

    candidates = [
        f'{RESEARCH}/{normalized}_tools.json',
        f'{RESEARCH}/{normalized}_mcp_tools.json',
        f'{EXAMPLES}/{normalized}.json',
        f'{EXAMPLES}/{server_id}.json',
    ]

    # Also try stripping trailing -mcp
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
    """Convert grade letter to CSS class name."""
    mapping = {
        'A+': 'grade-aplus',
        'A':  'grade-a',
        'A-': 'grade-aminus',
        'B+': 'grade-bplus',
        'B':  'grade-b',
        'B-': 'grade-bminus',
        'C+': 'grade-cplus',
        'C':  'grade-c',
        'C-': 'grade-cminus',
        'D+': 'grade-dplus',
        'D':  'grade-d',
        'D-': 'grade-dminus',
        'F':  'grade-f',
    }
    return mapping.get(grade_letter, 'grade-f')


def issues_level(total_issues):
    if total_issues == 0:
        return 'issues-low'
    elif total_issues <= 5:
        return 'issues-low'
    elif total_issues <= 20:
        return 'issues-medium'
    else:
        return 'issues-high'


def run_grade(schema_path):
    """Grade a schema file. Returns dict with grade results."""
    try:
        data = json.load(open(schema_path))
    except Exception as e:
        return None, f'JSON parse error: {e}'

    # Some files wrap tools in a dict with 'tools' key
    if isinstance(data, dict) and 'tools' in data and isinstance(data['tools'], list):
        data = data['tools']

    try:
        result = grade_tools(data)
    except Exception as e:
        return None, f'grade_tools error: {e}'

    try:
        issues, metadata = validate_tools(data)
        total_issues = len(issues)
    except Exception as e:
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


def extract_current_score(content, server_id):
    """Extract current score from HTML for a server."""
    # Find data-row for this server
    pattern = rf'<tr class="data-row[^"]*" data-server="{re.escape(server_id)}">(.*?)</tr>'
    m = re.search(pattern, content, re.DOTALL)
    if not m:
        return None
    row_html = m.group(1)
    # Extract score - first <td class="r"> after grade-cell
    score_m = re.search(r'<td class="r">(\d+\.?\d*)<span class="score-bar-bg">', row_html)
    if score_m:
        return float(score_m.group(1))
    return None


def update_data_row(content, server_id, new_data):
    """Update the data-row for a server with new grade data."""
    # Pattern to match the full data-row tr
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

        # Update grade badge
        row_inner = re.sub(
            r'<td class="grade-cell"><div class="grade-badge grade-[^"]*">.*?</div></td>',
            f'<td class="grade-cell"><div class="grade-badge {grade_class}">{grade}</div></td>',
            row_inner
        )

        # Update score + bar
        row_inner = re.sub(
            r'<td class="r">[\d.]+<span class="score-bar-bg"><span class="score-bar-fill" data-width="[\d.]+" style="background: [^;]+;"></span></span></td>',
            f'<td class="r">{score}<span class="score-bar-bg"><span class="score-bar-fill" data-width="{score}" style="background: {color};"></span></span></td>',
            row_inner
        )

        # Update tool count, total tokens, avg tokens, issues
        # These are the 3rd, 4th, 5th <td class="r"> after the score
        # We need to replace all 4 of them in sequence
        # Strategy: find them in order

        # After score bar, there are: tool_count, total_tokens, avg_tokens, issues
        # Use a multi-replacement approach
        tds = list(re.finditer(r'<td class="r">(?![\d.]+<span class="score-bar-bg")', row_inner))

        # Build new td sequence for tool_count, total_tokens, avg_tokens
        # The issues badge is different - needs span
        new_tds = [
            f'<td class="r">{tool_count}</td>',
            f'<td class="r">{total_tokens:,}</td>',
            f'<td class="r">{avg_tokens}</td>',
            f'<td class="r"><span class="issues-badge {issue_level}">{total_issues}</span></td>',
        ]

        # Replace the 4 plain td.r cells (after the score cell)
        # Find and replace each in order using a smarter approach
        # Split on score bar marker
        score_bar_pattern = r'<td class="r">[\d.]+<span class="score-bar-bg">.*?</span></span></td>'
        parts = re.split(score_bar_pattern, row_inner, maxsplit=1)

        if len(parts) == 2:
            before_score = parts[0]
            after_score = parts[1]

            # Reconstruct score td
            score_td = f'<td class="r">{score}<span class="score-bar-bg"><span class="score-bar-fill" data-width="{score}" style="background: {color};"></span></span></td>'

            # In after_score, replace the 4 data tds
            # Pattern: tool count, total_tokens, avg_tokens, issues badge
            after_score = re.sub(
                r'(<td class="r">)\d+(</td>)\s*(<td class="r">)\d[\d,]*(</td>)\s*(<td class="r">)\d+(</td>)\s*(<td class="r"><span class="issues-badge issues-[^"]*">)\d+(</span></td>)',
                f'<td class="r">{tool_count}</td>\n            <td class="r">{total_tokens:,}</td>\n            <td class="r">{avg_tokens}</td>\n            <td class="r"><span class="issues-badge {issue_level}">{total_issues}</span></td>',
                after_score
            )

            row_inner = before_score + score_td + after_score

        return prefix + row_inner + suffix

    new_content = re.sub(pattern, replace_row, content, flags=re.DOTALL)
    return new_content


def update_detail_row(content, server_id, new_data):
    """Update the detail row breakdown bars for a server."""
    pattern = rf'(<tr class="detail-row" data-server="{re.escape(server_id)}">(.*?)</tr>)'

    def replace_detail(m):
        full = m.group(1)

        c_score = new_data['correctness_score']
        e_score = new_data['efficiency_score']
        q_score = new_data['quality_score']

        c_color = grade_color(c_score)
        e_color = grade_color(e_score)
        q_color = grade_color(q_score)

        # Replace correctness breakdown item
        full = re.sub(
            r'(<span class="breakdown-label">Correctness \(40%\)</span>\s*<div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width=")[\d.]+(.*?style="background: )[^;]+(;"></div></div>\s*<span class="breakdown-score" style="color: )[^;]+(;">)[\d.]+(</span>)',
            lambda x: f'{x.group(1)}{c_score}{x.group(2)}{c_color}{x.group(3)}{c_color}{x.group(4)}{c_score}{x.group(5)}',
            full,
            flags=re.DOTALL
        )

        # Replace efficiency breakdown item
        full = re.sub(
            r'(<span class="breakdown-label">Efficiency \(30%\)</span>\s*<div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width=")[\d.]+(.*?style="background: )[^;]+(;"></div></div>\s*<span class="breakdown-score" style="color: )[^;]+(;">)[\d.]+(</span>)',
            lambda x: f'{x.group(1)}{e_score}{x.group(2)}{e_color}{x.group(3)}{e_color}{x.group(4)}{e_score}{x.group(5)}',
            full,
            flags=re.DOTALL
        )

        # Replace quality breakdown item
        full = re.sub(
            r'(<span class="breakdown-label">Quality \(30%\)</span>\s*<div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width=")[\d.]+(.*?style="background: )[^;]+(;"></div></div>\s*<span class="breakdown-score" style="color: )[^;]+(;">)[\d.]+(</span>)',
            lambda x: f'{x.group(1)}{q_score}{x.group(2)}{q_color}{x.group(3)}{q_color}{x.group(4)}{q_score}{x.group(5)}',
            full,
            flags=re.DOTALL
        )

        return full

    new_content = re.sub(pattern, replace_detail, content, flags=re.DOTALL)
    return new_content


def main():
    with open(HTML_PATH) as f:
        content = f.read()

    # Get all server IDs from data-rows
    pattern = r'<tr class="data-row[^"]*" data-server="([^"]+)">'
    servers = re.findall(pattern, content)

    changes = []
    skipped = []
    not_found = []
    errors = []

    for server_id in servers:
        if server_id in ALREADY_REGRADED:
            skipped.append(server_id)
            continue

        schema_path = find_schema_file(server_id)

        if schema_path is None or not os.path.exists(schema_path):
            not_found.append(server_id)
            continue

        current_score = extract_current_score(content, server_id)

        grade_result, err = run_grade(schema_path)
        if err:
            errors.append((server_id, err))
            continue

        new_score = grade_result['overall_score']
        diff = abs(new_score - (current_score or 0))

        if diff > 0.05:  # update if any meaningful change
            changes.append({
                'server_id': server_id,
                'old_score': current_score,
                'new_score': new_score,
                'diff': new_score - (current_score or 0),
                'schema_path': schema_path,
                'grade': grade_result['overall_grade'],
            })

        # Always update the HTML with new scores regardless of diff
        # (to ensure consistency with v0.65.0)
        content = update_data_row(content, server_id, grade_result)
        content = update_detail_row(content, server_id, grade_result)

    with open(HTML_PATH, 'w') as f:
        f.write(content)

    print(f"\n=== Re-grade Summary ===")
    print(f"Total servers: {len(servers)}")
    print(f"Skipped (already v0.65.0): {len(skipped)}: {sorted(skipped)}")
    print(f"Not found (no schema): {len(not_found)}: {sorted(not_found)}")
    print(f"Errors: {len(errors)}")
    for sid, err in errors:
        print(f"  ERROR {sid}: {err}")

    significant_changes = [c for c in changes if abs(c['diff']) > 0.5]
    print(f"\nServers updated: {len(changes)}")
    print(f"Significant changes (>0.5): {len(significant_changes)}")
    print()
    print("ALL CHANGES (sorted by score diff):")
    for c in sorted(changes, key=lambda x: x['diff']):
        old = f"{c['old_score']:6.1f}" if c['old_score'] is not None else '   N/A'
        print(f"  {c['server_id']:35s} {old} -> {c['new_score']:6.1f}  ({c['diff']:+.1f})  [{c['grade']}]")

    return changes, not_found, errors


if __name__ == '__main__':
    main()
