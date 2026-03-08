#!/usr/bin/env python3
import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


@dataclass
class Participant:
    name: str
    tz: ZoneInfo


def parse_zones(raw: str):
    out = []
    for part in raw.split(","):
        name, tz = part.split("=", 1)
        out.append(Participant(name.strip(), ZoneInfo(tz.strip())))
    return out


def parse_hhmm(s: str) -> int:
    h, m = s.split(":", 1)
    return int(h) * 60 + int(m)


def parse_hours_range(rng: str):
    a, b = rng.split("-", 1)
    return parse_hhmm(a.strip()), parse_hhmm(b.strip())


def parse_hours_map(raw: str | None):
    out = {}
    if not raw:
        return out
    for part in raw.split(","):
        if not part.strip():
            continue
        name, rng = part.split("=", 1)
        out[name.strip()] = parse_hours_range(rng.strip())
    return out


def in_range(minutes: int, start: int, end: int) -> bool:
    return start <= minutes < end


def penalty(local_dt: datetime, pref_start: int, pref_end: int) -> int:
    mins = local_dt.hour * 60 + local_dt.minute
    if in_range(mins, pref_start, pref_end):
        return 0

    # distance from preferred bounds (same-day, simple model)
    d = min(abs(mins - pref_start), abs(mins - pref_end))
    if d <= 60:
        return 1
    if d <= 180:
        return 3
    return 5


def reason_for_penalty(name: str, p: int, local_dt: datetime) -> str | None:
    h = local_dt.hour
    if p >= 5 and (h >= 22 or h < 7):
        return f"{name} overnight"
    if p >= 3:
        return f"{name} outside preferred hours"
    return None


def fmt(dt: datetime):
    return dt.strftime("%H:%M"), dt.strftime("%-I:%M %p")


def classify(score: int):
    if score <= 1:
        return "Optimal"
    if score <= 5:
        return "Stretch"
    return "Avoid"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="Anchor date, e.g. 2026-03-06")
    ap.add_argument("--anchor", default="America/Chicago")
    ap.add_argument("--zones", required=True, help='"Chicago=America/Chicago,London=Europe/London"')
    ap.add_argument("--duration", type=int, default=60)
    ap.add_argument("--step", type=int, default=60)
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--hours", default="", help='Per-person preferred hours map, e.g. "Chicago=09:00-17:00,London=08:30-17:30"')
    ap.add_argument("--my-name", default="", help="Name key in --zones to apply --my-hours to")
    ap.add_argument("--my-hours", default="", help='Your preferred hours range, e.g. "09:00-17:00"')
    args = ap.parse_args()

    anchor_tz = ZoneInfo(args.anchor)
    participants = parse_zones(args.zones)

    hours_map = parse_hours_map(args.hours)
    if args.my_hours:
        my_name = args.my_name.strip() if args.my_name else participants[0].name
        hours_map[my_name] = parse_hours_range(args.my_hours)

    default_hours = (8 * 60, 18 * 60)

    start_day = datetime.fromisoformat(args.date).replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=anchor_tz)

    slots = []
    t = start_day
    end_day = start_day + timedelta(days=1)
    while t < end_day:
        t2 = t + timedelta(minutes=args.duration)
        score = 0
        reasons = []
        rows = []
        for p in participants:
            ls, le = t.astimezone(p.tz), t2.astimezone(p.tz)
            pref_start, pref_end = hours_map.get(p.name, default_hours)
            pen = penalty(ls, pref_start, pref_end)
            score += pen
            r = reason_for_penalty(p.name, pen, ls)
            if r:
                reasons.append(r)
            rows.append((p.name, ls, le))
        slots.append((classify(score), score, t, t2, rows, sorted(set(reasons))))
        t += timedelta(minutes=args.step)

    buckets = {"Optimal": [], "Stretch": [], "Avoid": []}
    for s in slots:
        buckets[s[0]].append(s)

    for k in buckets:
        buckets[k] = sorted(buckets[k], key=lambda x: x[1])[: args.top]

    for category in ["Optimal", "Stretch", "Avoid"]:
        icon = {"Optimal": "✅", "Stretch": "🟨", "Avoid": "🟥"}[category]
        print(f"{icon} **{category}**\n")
        if not buckets[category]:
            print("No windows found.\n")
            continue

        for i, (_, score, s, e, rows, reasons) in enumerate(buckets[category], start=1):
            a24s, a12s = fmt(s)
            a24e, a12e = fmt(e)
            print(f"{i}. **{a24s}–{a24e} {s.tzname()} ({a12s}–{a12e})**")

            for name, ls, le in rows[1:]:
                s24, s12 = fmt(ls)
                e24, e12 = fmt(le)
                plus = " +1 day" if ls.date() > s.date() else ""
                print(f"{name} {s24}–{e24} ({s12}–{e12}){plus}")

            if category in ("Stretch", "Avoid") and reasons:
                print(f"*Reason: {', '.join(reasons)}.*")

            if i != len(buckets[category]):
                print("⠀")
        print()


if __name__ == "__main__":
    main()
