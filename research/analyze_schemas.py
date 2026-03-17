#!/usr/bin/env python3
"""Analyze collected MCP server schemas for token costs and optimization opportunities.

Reads JSON schemas from research/mcp-schemas/*.json
Outputs benchmark data as JSON for the benchmark page.
"""
import json
import os
import re
import sys

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "mcp-schemas")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "benchmark-data.json")

# Token estimation: ~4 chars per token (same as audit.html)
def estimate_tokens(obj):
    return len(json.dumps(obj)) // 4

# MCP format multiplier (from audit.html)
FORMAT_MULTIPLIERS = {
    "openai": 1.15,
    "anthropic": 1.08,
    "google": 1.0,
    "mcp": 1.12,
    "json_schema": 0.85,
}

# Optimization rules (same 7 as agent-friend optimize CLI)
def check_verbose_prefix(tools):
    """Tools with redundant prefixes like github_create_issue."""
    issues = []
    if len(tools) < 2:
        return issues
    names = [t.get("name", "") for t in tools]
    # Find common prefix
    if not names:
        return issues
    prefix = os.path.commonprefix(names)
    if "_" in prefix and len(prefix) > 3:
        prefix = prefix[:prefix.rfind("_") + 1]
        if len(prefix) > 3:
            for t in tools:
                issues.append({
                    "rule": "verbose_prefix",
                    "tool": t.get("name", ""),
                    "detail": f"Common prefix '{prefix}' adds ~{len(prefix)} chars/tool"
                })
    return issues

def check_long_description(tools):
    """Descriptions over 200 chars."""
    issues = []
    for t in tools:
        desc = t.get("description", "")
        if len(desc) > 200:
            issues.append({
                "rule": "long_description",
                "tool": t.get("name", ""),
                "detail": f"Description is {len(desc)} chars (recommended: <200)"
            })
    return issues

def check_missing_description(tools):
    """Tools or params without descriptions."""
    issues = []
    for t in tools:
        if not t.get("description"):
            issues.append({
                "rule": "missing_description",
                "tool": t.get("name", ""),
                "detail": "No tool description"
            })
        schema = t.get("inputSchema", {})
        props = schema.get("properties", {})
        for pname, pval in props.items():
            if not pval.get("description"):
                issues.append({
                    "rule": "missing_description",
                    "tool": t.get("name", ""),
                    "detail": f"Parameter '{pname}' has no description"
                })
    return issues

def check_long_param_description(tools):
    """Parameter descriptions over 100 chars."""
    issues = []
    for t in tools:
        schema = t.get("inputSchema", {})
        props = schema.get("properties", {})
        for pname, pval in props.items():
            desc = pval.get("description", "")
            if len(desc) > 100:
                issues.append({
                    "rule": "long_param_description",
                    "tool": t.get("name", ""),
                    "detail": f"Param '{pname}' description is {len(desc)} chars"
                })
    return issues

def check_deep_nesting(tools, max_depth=3):
    """Parameters nested deeper than max_depth."""
    def measure_depth(obj, depth=0):
        if not isinstance(obj, dict):
            return depth
        max_d = depth
        for v in obj.values():
            if isinstance(v, dict):
                max_d = max(max_d, measure_depth(v, depth + 1))
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        max_d = max(max_d, measure_depth(item, depth + 1))
        return max_d

    issues = []
    for t in tools:
        schema = t.get("inputSchema", {})
        depth = measure_depth(schema)
        if depth > max_depth:
            issues.append({
                "rule": "deep_nesting",
                "tool": t.get("name", ""),
                "detail": f"Schema depth: {depth} (max recommended: {max_depth})"
            })
    return issues

def check_redundant_param_description(tools):
    """Param descriptions that repeat the tool description."""
    issues = []
    for t in tools:
        tool_desc = t.get("description", "").lower()
        if not tool_desc:
            continue
        schema = t.get("inputSchema", {})
        props = schema.get("properties", {})
        for pname, pval in props.items():
            pdesc = pval.get("description", "").lower()
            if pdesc and len(pdesc) > 20:
                # Check if param desc is substring of tool desc or vice versa
                if pdesc in tool_desc or tool_desc in pdesc:
                    issues.append({
                        "rule": "redundant_param_description",
                        "tool": t.get("name", ""),
                        "detail": f"Param '{pname}' description overlaps with tool description"
                    })
    return issues

def check_duplicate_param_description(tools):
    """Multiple params with identical descriptions."""
    issues = []
    for t in tools:
        schema = t.get("inputSchema", {})
        props = schema.get("properties", {})
        descs = {}
        for pname, pval in props.items():
            desc = pval.get("description", "")
            if desc:
                if desc in descs:
                    issues.append({
                        "rule": "duplicate_param_description",
                        "tool": t.get("name", ""),
                        "detail": f"Params '{descs[desc]}' and '{pname}' share identical description"
                    })
                else:
                    descs[desc] = pname
    return issues

def analyze_server(name, tools):
    """Run full analysis on a server's tools."""
    total_tokens = sum(estimate_tokens(t) for t in tools)

    # Per-tool breakdown
    tool_details = []
    for t in tools:
        tokens = estimate_tokens(t)
        params = len(t.get("inputSchema", {}).get("properties", {}))
        tool_details.append({
            "name": t.get("name", "unknown"),
            "description": t.get("description", "")[:100],
            "tokens": tokens,
            "params": params,
        })

    # Run all 7 rules
    all_issues = []
    all_issues.extend(check_verbose_prefix(tools))
    all_issues.extend(check_long_description(tools))
    all_issues.extend(check_missing_description(tools))
    all_issues.extend(check_long_param_description(tools))
    all_issues.extend(check_deep_nesting(tools))
    all_issues.extend(check_redundant_param_description(tools))
    all_issues.extend(check_duplicate_param_description(tools))

    # Group issues by rule
    issues_by_rule = {}
    for issue in all_issues:
        rule = issue["rule"]
        if rule not in issues_by_rule:
            issues_by_rule[rule] = []
        issues_by_rule[rule].append(issue)

    # Format comparison
    format_tokens = {}
    for fmt, mult in FORMAT_MULTIPLIERS.items():
        format_tokens[fmt] = int(total_tokens * mult)

    return {
        "name": name,
        "tool_count": len(tools),
        "total_tokens_mcp": total_tokens,
        "format_tokens": format_tokens,
        "tools": sorted(tool_details, key=lambda x: -x["tokens"]),
        "issues": all_issues,
        "issues_by_rule": {k: len(v) for k, v in issues_by_rule.items()},
        "total_issues": len(all_issues),
    }

def main():
    if not os.path.exists(SCHEMA_DIR):
        print(f"Error: {SCHEMA_DIR} does not exist", file=sys.stderr)
        sys.exit(1)

    results = []

    for fname in sorted(os.listdir(SCHEMA_DIR)):
        if not fname.endswith(".json"):
            continue

        fpath = os.path.join(SCHEMA_DIR, fname)
        try:
            with open(fpath) as f:
                tools = json.load(f)
            if not isinstance(tools, list):
                tools = [tools]
        except (json.JSONDecodeError, IOError) as e:
            print(f"Skipping {fname}: {e}", file=sys.stderr)
            continue

        name = fname.replace(".json", "").replace("_", " ").replace("-", " ").title()
        result = analyze_server(name, tools)
        results.append(result)

        print(f"\n{'='*60}")
        print(f"  {result['name']}")
        print(f"  {result['tool_count']} tools | {result['total_tokens_mcp']} tokens (MCP)")
        print(f"  Issues: {result['total_issues']}")
        if result['issues_by_rule']:
            for rule, count in result['issues_by_rule'].items():
                print(f"    {rule}: {count}")
        print(f"{'='*60}")

    # Summary
    print(f"\n\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    total_servers = len(results)
    total_tools = sum(r["tool_count"] for r in results)
    total_tokens = sum(r["total_tokens_mcp"] for r in results)
    total_issues = sum(r["total_issues"] for r in results)

    print(f"  Servers analyzed: {total_servers}")
    print(f"  Total tools: {total_tools}")
    print(f"  Total tokens (MCP format): {total_tokens:,}")
    print(f"  Total optimization issues: {total_issues}")
    print(f"  Avg tokens/tool: {total_tokens // max(total_tools, 1):,}")

    # Sort by token count descending
    results.sort(key=lambda x: -x["total_tokens_mcp"])

    # Save benchmark data
    output = {
        "generated_at": "2026-03-17",
        "total_servers": total_servers,
        "total_tools": total_tools,
        "total_tokens_mcp": total_tokens,
        "total_issues": total_issues,
        "avg_tokens_per_tool": total_tokens // max(total_tools, 1),
        "servers": results,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nBenchmark data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
