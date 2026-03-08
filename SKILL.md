---
name: world-meeting-coordination-skill
description: Compute best cross-timezone meeting windows with DST-safe conversion and ranked categories (Optimal, Stretch, Avoid). Use when user asks for overlap windows across 2+ cities/timezones on a given date, wants output anchored to one timezone, or asks for readable Telegram-ready scheduling output with 24h + 12h times and +1 day markers.
---

# Meeting Windows

Compute ranked meeting windows for multiple timezones.

## Inputs

- Date (YYYY-MM-DD preferred; natural date acceptable)
- Anchor timezone (default: America/Chicago)
- Cities/timezones list (IANA tz names preferred)
- Optional duration in minutes (default: 60)
- Optional preferred window per participant (default: 08:00-18:00 local)
- Optional user-specific hours via `--my-hours` (even if others unknown)

## Onboarding and settings

First run in an interactive terminal triggers onboarding automatically (3 questions):

1. your timezone
2. your preferred meeting hours
3. your flexibility (`strict|balanced|flexible`)

At any time:

```bash
python3 scripts/meeting_windows.py --setup
python3 scripts/meeting_windows.py --show-settings
```

## Example prompts

Use prompts like these in chat:

- "Find the best meeting windows for Chicago, London, and Tel Aviv on March 6, anchored to Chicago time. Return Optimal, Stretch, and Avoid windows with reasons."
- "Find overlap windows for San Francisco, New York, and Berlin on 2026-04-12 in Pacific time, 60-minute meetings."
- "Give me top 3 windows for Chicago, Paris, and Singapore tomorrow in Chicago time, with +1 day markers where needed."
- "For Tokyo, London, and Chicago on 2026-10-28, show only Optimal and Stretch windows."

Structured CLI equivalent:

```bash
python3 scripts/meeting_windows.py \
  --date 2026-03-06 \
  --anchor America/Chicago \
  --zones "Chicago=America/Chicago,London=Europe/London,Tel Aviv=Asia/Jerusalem"
```

If only your hours are known, add:

```bash
--my-name Chicago --my-hours "09:00-17:00"
```

Or set multiple participant hours:

```bash
--hours "Chicago=09:00-17:00,London=08:30-17:30"
```

## Execution

Run:

```bash
python3 scripts/meeting_windows.py \
  --date 2026-03-06 \
  --anchor America/Chicago \
  --zones "Chicago=America/Chicago,London=Europe/London,Tel Aviv=Asia/Jerusalem"
```

Optional:

```bash
--duration 60 --top 3 --step 60
```

## Output rules (Telegram format)

- Sections: `Optimal`, `Stretch`, `Avoid`
- Use numbered items (`1.`, `2.`, ...)
- Show anchor line first, then each participant local time line
- Time format: `24h (12h)`
- Append `+1 day` when local date is one day ahead of anchor date
- Add one spacer line `⠀` between items
- For Stretch/Avoid include italic reason line: `*Reason: ...*`

## Category scoring defaults

Per participant, score by local start hour:

- 09:00-17:59 -> +0
- 08:00-08:59 or 18:00-18:59 -> +1
- 07:00-07:59 or 19:00-21:59 -> +3
- 22:00-06:59 -> +5

Total slot score across participants:

- Optimal: score <= 1
- Stretch: score 2-5
- Avoid: score >= 6

## Notes

- Prefer exact IANA timezones over country names.
- If user provides city names only, map them before running.
- If no slots appear in a category, return the best available with a note.
