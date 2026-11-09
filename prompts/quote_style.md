# SnoopsRoulette quote style

## What the account is
A faceless quote page posted X-first: plain-text tweets, then screenshots of them
on Instagram and TikTok. The lens is gambling, used as a metaphor for **work,
relationships, and family**.

## Voice (every day)
- Blunt and first or second person ("i", "you", "y'all"). Sounds like a real
  person tweeting, not a poster.
- Mostly lowercase, casual punctuation. No emojis, or one at most.
- Under 200 characters. Hard cap 280.
- Built to start comments: people should want to say "facts", argue, confess,
  or tag someone. Relatable beats clever.
- Gambling words as metaphor: bet, odds, all in, fold, double down, cash out,
  house edge, the table, a hand, chips, the dealer, the spin, roulette.
- Spread the 4 daily quotes across topics: at least one each about
  relationships, work or money, and family.

## Daily vibe
`python scripts/vibe.py <YYYY-MM-DD>` gives the day's vibe. All 4 quotes that
day lean into it.

| Vibe | Feel |
|---|---|
| gambler | Risk-taker energy, confident, a little reckless |
| dark humor | Bleak, funny, self-roasting about losing |
| street wisdom | Hard-earned lessons, loyalty, snakes, money |
| calm philosophical | Quiet, reflective, life as chance and timing |
| stoic | Control what you can, accept the loss, discipline over emotion |

## Never
- Links (each one raises that post's X API cost to $0.20) or hashtags in the tweet.
- Quotes from real people, song lyrics, or lines lifted from other accounts.
  Every quote is original.
- Lines encouraging real gambling, chasing losses with money, or betting rent:
  the gambling is a metaphor.
- Slurs, attacks on real people, or anything aimed at minors.
- Repeats: compare against every existing `text` in `queue/queue.json` and
  rewrite anything too close to an earlier quote.
