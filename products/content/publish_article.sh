#!/bin/bash
# publish_article.sh — publish the next article from the queue
# Usage: bash publish_article.sh <article_number> [--dry-run]
# Example: bash publish_article.sh 054

set -e
cd /home/agent/company

log() { echo "[$(date -u +%H:%M:%S)] $*"; }

if [ -z "$1" ]; then
    echo "Usage: bash publish_article.sh <article_number> [--dry-run]"
    echo "Available unpublished articles:"
    grep -l "Article0" waiting.md | head -1 && grep "### Article0" waiting.md | head -11
    exit 1
fi

NUM="$1"
DRY_RUN="${2:-}"

# Article ID lookup table
declare -A ARTICLE_IDS=(
    [054]=3341101
    [055]=3341191
    [056]=3341264
    [057]=3341307
    [058]=3341366
    [059]=3341425
    [060]=3341549
    [061]=3341573
    [062]=3341598
    [063]=3341613
)

ID="${ARTICLE_IDS[$NUM]}"
if [ -z "$ID" ]; then
    log "ERROR: No article ID found for article $NUM"
    exit 1
fi

log "Publishing article $NUM (dev.to ID: $ID)"

if [ "$DRY_RUN" = "--dry-run" ]; then
    log "[DRY RUN] Would publish article $NUM (ID: $ID)"
    exit 0
fi

# Publish on dev.to
sudo -u vault /home/vault/bin/vault-devto PUT "/articles/$ID" '{"article":{"published":true}}' 2>/dev/null
log "Article $NUM published to dev.to"

# Log it
echo "- [$(date -u +%H:%MZ)] devto: article$NUM published (ID: $ID)" >> post-log.md
log "Logged to post-log.md"

log "Done. Check: https://dev.to/0coceo"
