# World Meeting Coordination Skill

Rank cross-timezone meeting windows as **Optimal**, **Stretch**, and **Avoid** with Telegram-friendly output formatting.

## What it does

- Computes candidate windows across a day anchored to a reference timezone
- Converts each slot to participant local times using `zoneinfo` (DST-aware)
- Scores each slot by local-hour comfort bands
- Outputs readable blocks with:
  - 24h + 12h times
  - `+1 day` marker when local date rolls forward
  - italicized reasons for Stretch/Avoid
  - spacer lines that render well in Telegram

## Usage

```bash
python3 scripts/meeting_windows.py \
  --date 2026-03-06 \
  --anchor America/Chicago \
  --zones "Chicago=America/Chicago,London=Europe/London,Tel Aviv=Asia/Jerusalem"
```

Optional flags:

- `--duration` meeting length in minutes (default: `60`)
- `--step` slot step in minutes (default: `60`)
- `--top` number of results per category (default: `3`)

## Repository workflow (Josh standard)

This project follows a two-lane workflow:

- **Development source (git):**
  - `/home/pi/.openclaw/workspace/projects/world-meeting-coordination-skill`
- **Polished runtime copy (apps):**
  - `/home/pi/.openclaw/workspace/apps/world-meeting-coordination-prod/skills/world-meeting-coordination-skill`

`/home/pi/.openclaw/workspace/skills/world-meeting-coordination-skill` is a symlink to the development source, so the skill stays discoverable during development.

## Publish + runtime sync

Use the helper script after changes:

```bash
./scripts/publish_sync.sh
```

It will:

1. run a smoke test,
2. sync files to `apps/world-meeting-coordination-prod`,
3. push git changes,
4. optionally remind you to publish a new ClawHub version.

## Smoke test

```bash
./tests/test_smoke.sh
```

## Notes

- Current engine is local `zoneinfo` based (no external API credentials required).
- Backlog for profile-based participant/company hours is tracked in GitHub issues and private local notes.
