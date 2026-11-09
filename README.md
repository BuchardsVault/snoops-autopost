# snoops-autopost

X-first quote posting for SnoopsRoulette. A quote goes to X as text, then a
screenshot-style card of it goes to Instagram and TikTok.

## Daily flow (Pacific time)

| When | What | Runs in |
|---|---|---|
| 8am, 12pm, 5pm, 9pm (+ backup runs) | Post the due quote to X (never before its slot time), render card (with the tweet's real timestamp) to `docs/cards/` | GitHub Actions (`post-x.yml`) |
| 1:07pm | Instagram carousel of slots 1+2, caption `Roll #N` | Claude scheduled task (`prompts/instagram_post.md`) |
| 10:07pm | Instagram carousel of slots 3+4, caption `Roll #N` | Claude scheduled task (`prompts/instagram_post.md`) |
| 10:37pm | TikTok photo post of all 4 cards (`Roll #N` + 5 hashtags), then write tomorrow's 4 quotes | Claude scheduled task (`prompts/nightly.md`) |

Quote voice and the weekly-shuffled daily vibe: `prompts/quote_style.md`, `scripts/vibe.py`.

## Queue item fields

- `status`: `queued` -> `posted_x`
- `vibe`: the day's vibe (gambler, dark humor, street wisdom, calm philosophical, stoic)
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
