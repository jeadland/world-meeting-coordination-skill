#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP_TARGET="/home/pi/.openclaw/workspace/apps/world-meeting-coordination-prod/skills/world-meeting-coordination-skill"

cd "$ROOT"

echo "[1/4] Running smoke test..."
./tests/test_smoke.sh

echo "[2/4] Syncing to apps runtime copy..."
mkdir -p "$APP_TARGET"
rsync -a --delete --exclude '.git' --exclude 'LOCAL_BACKLOG.md' ./ "$APP_TARGET/"

echo "[3/4] Git status"
git status --short

echo "[4/4] Done. Next steps:"
echo "  - Commit/push if needed"
echo "  - Publish to ClawHub when versioning:"
echo "    clawhub publish . --slug world-meeting-coordination-skill --name \"World Meeting Coordination Skill\" --version <x.y.z> --changelog \"...\""
