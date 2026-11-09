"""Daily vibe for the quotes, reshuffled every week.

Each ISO week (Mon-Sun) gets a fresh random order of the 5 vibes plus 2 repeats,
with no vibe on two days in a row. The shuffle is seeded by the week number, so
every run that week computes the same schedule: no state file needed.

  python scripts/vibe.py                # today's vibe
  python scripts/vibe.py 2026-11-09     # vibe for a date
  python scripts/vibe.py --week         # this week's full schedule
"""
import random
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

VIBES = {
    "gambler": "Risk-taker energy. Odds, all-in, doubling down, cashing out, reading the table. "
               "Confident and a little reckless.",
    "dark humor": "Bleak, funny, self-roasting. Laughing at losing: in love, at work, with family. "
                  "The joke lands because it's true.",
    "street wisdom": "Hard-earned lessons. Loyalty, snakes, money, who's really in your corner. "
                     "Said like an older cousin who's seen it.",
    "calm philosophical": "Quiet and reflective. Life as probability, chance, timing. "
                          "Makes people stop scrolling and think.",
    "stoic": "Control what you can, accept the loss, keep your composure. Discipline over emotion. "
             "Original lines in a stoic spirit, never quotes from real philosophers.",
}


def week_schedule(d):
    year, week, _ = d.isocalendar()
    rng = random.Random(f"{year}-W{week:02d}")
    names = list(VIBES)
    while True:
        days = names + rng.sample(names, 2)
        rng.shuffle(days)
        if all(days[i] != days[i + 1] for i in range(6)):
            monday = d - timedelta(days=d.weekday())
            return [(monday + timedelta(days=i), v) for i, v in enumerate(days)]


def vibe_for(d):
    return dict(week_schedule(d))[d]


if __name__ == "__main__":
    args = sys.argv[1:]
    today = datetime.now(ZoneInfo("America/Los_Angeles")).date()
    if args and args[0] == "--week":
        for d, v in week_schedule(today):
            print(f"{d:%a %b %d}: {v}")
    else:
        d = date.fromisoformat(args[0]) if args else today
        v = vibe_for(d)
        print(f"{d}: {v} - {VIBES[v]}")
