# Nightly run (10:37pm Pacific): TikTok post + tomorrow's quotes

## Part 1: TikTok (all of today's tweets in one photo post)
1. `git pull`, then load `queue/queue.json` and `queue/roll_counters.json`.
   Today = the current date in America/Los_Angeles.
2. Collect today's items (`date` = today, not the `-test` item) that have
   `status: posted_x` and `tiktok_status: pending`, in slot order.
   - If none, skip to Part 2 and report it.
   - If any have `tiktok_status: scheduled` already, skip to Part 2: this run
     already happened.
3. N = `tiktok` counter + 1.
4. Build the TikTok caption: `Roll #N` + a blank line + 5 hashtags on one line.
   - Always include `#snoopsroulette` and `#fyp`.
   - Pick 3 more from the lists below that fit today's quotes and vibe.
   - Vary the picks from day to day; don't reuse yesterday's exact set.
   - Topic tags: #relationships #relatable #quotes #lifelessons #mindset
     #situationship #loyalty #family #money #grind #realtalk #motivation
     #deepthoughts #toxicrelationships #selfgrowth
   - Vibe tags: gambler: #takerisks #allin. Dark humor: #darkhumor #relatablememes.
     Street wisdom: #streetwisdom #realquotes. Calm philosophical: #philosophy
     #deepquotes. Stoic: #stoicism #stoic.
   - Example: `Roll #7\n\n#snoopsroulette #fyp #relationships #allin #realtalk`
5. Schedule with Metricool `createScheduledPost`: blogId `7911679`, date = now +
   5 minutes (America/Los_Angeles, not in the past), `providers`
   `[{"network":"tiktok"}]`, `media` = the items' `image_url`s in slot order,
   `text` = the caption from step 4, and `tiktokData`
   `{"title":"Roll #N","privacyOption":"PUBLIC_TO_EVERYONE","autoAddMusic":true,"photoCoverIndex":0}`
   (the `title` is just `Roll #N`; the hashtags go only in `text`)
   with the other tiktokData flags false.
6. On success: set those items' `tiktok_status` to `scheduled`,
   `tiktok_metricool_id`, and `tiktok_roll` to N, and set the `tiktok` counter
   to N. Commit "TikTok Roll #N" and push.
   On error: don't change the counter, and report the exact error. If it
   mentions a monthly limit or plan, say so plainly: the free Metricool plan
   may cap scheduled posts.

## Part 2: write tomorrow's 4 quotes
1. Tomorrow = today + 1 day. If `queue/queue.json` already has 4 items dated
   tomorrow, stop.
2. `python scripts/vibe.py <tomorrow>` gives the vibe. Read
   `prompts/quote_style.md` and follow it exactly.
3. Write 4 original quotes in that vibe, at least one each on relationships,
   work or money, and family. Check each against every existing `text` in the
   queue and rewrite anything too close.
4. Append 4 items:
   `{"id":"<tomorrow>-<slot>","date":"<tomorrow>","slot":1-4,"vibe":"<vibe>","text":"...","status":"queued"}`.
   Each text must be at most 280 characters, with no links and no hashtags.
5. Commit "Quotes for <tomorrow> (<vibe>)" and push.

## Report
End with: the TikTok Roll number or error, tomorrow's vibe, and the 4 quotes.
