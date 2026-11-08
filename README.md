# snoops-autopost

X-first quote posting for SnoopsRoulette. A quote goes to X as text, then a
screenshot-style card of it goes to Instagram and TikTok.

## Daily flow (Pacific time)

| When | What | Runs in |
|---|---|---|
| Morning | Write the day's 4 quotes into `queue/queue.json` | Claude scheduled task |
| 8am, 12pm, 5pm, 9pm | Post next quote to X, render card to `docs/cards/` | GitHub Actions (`post-x.yml`) |
| 12:30pm, 9:30pm | Post the slot-2 and slot-4 cards to Instagram | Claude scheduled task, via Windsor.ai |
| 10pm | Post all 4 of the day's cards as one TikTok photo post | Claude scheduled task, via Metricool |

## Queue item fields

- `status`: `queued` -> `posted_x`
- `to_instagram`: marks the 2 per day that also go to Instagram
- `ig_status` / `tiktok_status`: `pending` -> `posted` (or `skip`)
- `image_url`: GitHub Pages URL of the card

## Secrets (Settings -> Secrets and variables -> Actions)

`X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_SECRET`

## Local test

```
pip install -r requirements.txt
python scripts/render_card.py --text "test" --out /tmp/t.jpg
python scripts/post_x.py --dry-run
```

## Rules

- No links in tweets: each one raises that post's X API cost to $0.20.
- 280 characters max.
- `post_x.py` refuses duplicate posts.
- Change the name, handle, theme, and verified badge in `config.json`. Drop
  a profile picture at `assets/avatar.png`.
