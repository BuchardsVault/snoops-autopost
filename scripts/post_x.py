"""Post the next queued quote to X, then render its screenshot card for IG/TikTok.

Run by GitHub Actions 4x/day. Needs env secrets:
  X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET
Flags:
  --dry-run   pick + render, but do not call X or modify the queue
"""
import argparse
import json
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_card import render, load_config  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "queue/queue.json")
TZ = ZoneInfo("America/Los_Angeles")
MAX_LEN = 280


def load_queue():
    with open(QUEUE) as f:
        return json.load(f)


def save_queue(q):
    with open(QUEUE, "w") as f:
        json.dump(q, f, indent=2, ensure_ascii=False)
        f.write("\n")


# Slot -> Pacific posting time. A quote is never posted before its slot time,
# so a run GitHub delays (sometimes by hours) can't post the next day's quote early.
SLOT_TIMES = {0: (0, 0), 1: (8, 0), 2: (12, 0), 3: (17, 0), 4: (21, 0)}


def due_at(p):
    h, m = SLOT_TIMES[p["slot"]]
    return datetime.fromisoformat(p["date"]).replace(hour=h, minute=m, tzinfo=TZ)


def next_item(q, now):
    due = [p for p in q["posts"] if p["status"] == "queued" and due_at(p) <= now]
    due.sort(key=lambda p: (p["date"], p["slot"]))
    return due[0] if due else None


def post_tweet(text):
    from requests_oauthlib import OAuth1Session
    s = OAuth1Session(
        os.environ["X_API_KEY"], client_secret=os.environ["X_API_SECRET"],
        resource_owner_key=os.environ["X_ACCESS_TOKEN"],
        resource_owner_secret=os.environ["X_ACCESS_SECRET"],
    )
    r = s.post("https://api.x.com/2/tweets", json={"text": text}, timeout=30)
    if r.status_code >= 300:
        raise SystemExit(f"X API error {r.status_code}: {r.text}")
    return r.json()["data"]["id"]


X_EPOCH_MS = 1288834974657  # Twitter snowflake epoch


def tweet_time(tweet_id):
    """Exact creation time encoded in the tweet ID, in Pacific time."""
    ms = (int(tweet_id) >> 22) + X_EPOCH_MS
    return datetime.fromtimestamp(ms / 1000, TZ)


def x_timestamp(dt):
    """Format like X's own screenshots: '9:08 PM · Nov 8, 2026'."""
    hour = dt.strftime("%I").lstrip("0")
    return f"{hour}:{dt:%M} {dt:%p} · {dt:%b} {dt.day}, {dt.year}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    q = load_queue()
    now = datetime.now(TZ)
    item = next_item(q, now)
    if not item:
        print("Nothing due yet: no queued quote has reached its slot time.")
        return

    text = item["text"].strip()
    if len(text) > MAX_LEN:
        raise SystemExit(f"{item['id']} is {len(text)} chars (max {MAX_LEN})")
    if "http://" in text or "https://" in text:
        raise SystemExit(f"{item['id']} contains a link (costs $0.20 on X); refusing")
    posted_texts = {p["text"].strip().lower() for p in q["posts"] if p["status"] != "queued"}
    if text.lower() in posted_texts:
        raise SystemExit(f"{item['id']} duplicates an earlier post; refusing")

    card_rel = f"docs/cards/{item['id']}.jpg"
    out = os.path.join(ROOT, card_rel)
    if args.dry_run:
        render(text, "/tmp/dryrun.jpg", timestamp=x_timestamp(now))
        print(f"[dry-run] would post {item['id']}: {text!r} -> /tmp/dryrun.jpg")
        return

    tweet_id = post_tweet(text)
    posted = tweet_time(tweet_id)
    render(text, out, timestamp=x_timestamp(posted))
    item.update({
        "status": "posted_x",
        "tweet_id": tweet_id,
        "tweet_url": f"https://x.com/{cfg['handle']}/status/{tweet_id}",
        "posted_at": posted.isoformat(timespec="seconds"),
        "image_url": f"{cfg['pages_base_url']}/cards/{item['id']}.jpg",
        "ig_status": "pending",
        "tiktok_status": "pending",
    })
    save_queue(q)
    print(f"Posted {item['id']} -> {item['tweet_url']}")


if __name__ == "__main__":
    main()
