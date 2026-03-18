#!/usr/bin/env python3
"""Wrapper that reads campaign_queue.json and runs the campaign poster."""

import json
import os
import subprocess
import sys

QUEUE_FILE = "/home/agent/company/products/content/campaign_queue.json"

if not os.path.exists(QUEUE_FILE):
    print("No campaign queue file found, skipping")
    sys.exit(0)

with open(QUEUE_FILE) as f:
    data = json.load(f)

article_id = data.get("article_id")
if not article_id:
    print("No article_id in campaign queue")
    sys.exit(0)

print(f"Running campaign for article {article_id}")
result = subprocess.run(
    [sys.executable, "/home/agent/company/products/content/post_article_campaign.py", str(article_id)],
    capture_output=False
)
sys.exit(result.returncode)
