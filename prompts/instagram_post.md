# Instagram carousel run (1:07pm and 10:07pm Pacific)

Goal: post one carousel to Instagram (@snoopsroulette) through Windsor.ai with
every card that is on X but not yet on Instagram. X posts are sometimes late
(GitHub delays its scheduled runs by hours), so this run catches up on anything
an earlier run missed instead of only looking at fixed slots.

## Steps
1. `git pull`, then load `queue/queue.json` and `queue/roll_counters.json`.
   Today = the current date in America/Los_Angeles.
2. Collect the backlog: every item (not a `-test` item) with `status: posted_x`,
   an `image_url`, `ig_status: pending`, and `date` within the last 3 days
   (today, or up to 3 days before). Sort by date, then slot.
   - Items with `ig_status: posted` are never posted again.
   - If the backlog is empty: it's normally because this run's X posts are
     late. Wait 5 minutes, `git pull`, and check again. Try at most 4 times.
     If it's still empty, stop and report "nothing to post" (no commit).
3. Caption = `Roll #N`, where N = `instagram` counter + 1. Nothing else: no
   hashtags, no emojis.
4. Post with Windsor.ai `execute_action`: connector `instagram`, account
   `17841423906051846`.
   - 2 to 10 items: action `create_carousel_post`, params
     `{"image_urls": [urls in order], "caption": "Roll #N"}`.
   - 1 item: action `create_image_post` with that one image and the caption.
   - More than 10: post the oldest 10 now; the rest go on the next run.
5. On success: set each posted item's `ig_status` to `posted`, set `ig_media_id`
   and `ig_roll` to N, and set the `instagram` counter to N.
   Commit "Instagram Roll #N" and push.
6. If Windsor returns an error, don't retry more than once. Leave the items
   `pending`, don't change the counter, and report the exact error.
