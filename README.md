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

## Repository workflow

- **Development source (git):**
  - `/home/pi/.openclaw/workspace/projects/world-meeting-coordination-skill`
- **Skill path during development:**
  - `/home/pi/.openclaw/workspace/skills/world-meeting-coordination-skill` (symlink)

This project is intentionally **not mirrored into `apps/`**.
Release/install validation should happen via ClawHub installation path.

## Publish

After changes, run smoke test, then publish a version:

```bash
./tests/test_smoke.sh
clawhub publish . --slug world-meeting-coordination-skill --name "World Meeting Coordination Skill" --version <x.y.z> --changelog "..."
```

## Smoke test

```bash
./tests/test_smoke.sh
```

## Notes

- Current engine is local `zoneinfo` based (no external API credentials required).
- Backlog for profile-based participant/company hours is tracked in GitHub issues and private local notes.
