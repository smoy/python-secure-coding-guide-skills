#!/usr/bin/env bash
# Refresh a local cache of upstream OpenSSF rule READMEs so the reference files
# in the skill can be diffed and re-adapted when upstream changes.
#
# This is a repo-level maintenance utility, NOT part of the shipped skill — the
# skill never invokes it. A maintainer runs it by hand to refresh the upstream
# cache before re-adapting reference files.
#
# This does NOT overwrite the adapted references/ files — adaptation is a manual,
# judgment step (trim to ~20-line examples, preserve CWE mappings). It only pulls
# the authoritative upstream text into upstream-cache/ for comparison.
#
# Requires: gh (authenticated), base64, jq-style --jq (built into gh).
# Usage: ./scripts/sync-from-upstream.sh
set -euo pipefail

REPO="ossf/wg-best-practices-os-developers"
BASE="docs/Secure-Coding-Guide-for-Python"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Cache sits next to the adapted reference files so the two can be diffed.
CACHE="$ROOT/skills/python-secure-coding/upstream-cache"

mkdir -p "$CACHE"
echo "Caching upstream rule READMEs from $REPO/$BASE -> $CACHE"

# Each domain directory contains pyscg-XXXX rule subdirectories.
for domain in $(gh api "repos/$REPO/contents/$BASE" --jq '.[] | select(.type=="dir") | .name'); do
  case "$domain" in templates) continue ;; esac
  for rule in $(gh api "repos/$REPO/contents/$BASE/$domain" --jq '.[] | select(.type=="dir") | .name' 2>/dev/null); do
    dest_dir="$CACHE/$domain"
    mkdir -p "$dest_dir"
    if gh api "repos/$REPO/contents/$BASE/$domain/$rule/README.md" --jq '.content' 2>/dev/null \
        | base64 -d > "$dest_dir/$rule.md" 2>/dev/null; then
      echo "  cached $domain/$rule"
    fi
  done
done

echo
echo "Done. Compare upstream-cache/<domain>/<rule>.md against"
echo "references/<domain>/pyscg-XXXX-*.md and re-adapt where upstream changed."
echo "upstream-cache/ is intended to be gitignored (or committed as a snapshot baseline)."
