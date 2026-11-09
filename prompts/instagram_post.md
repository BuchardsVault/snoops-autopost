# Instagram carousel run (1:07pm and 10:07pm Pacific)

Goal: post one 2-slide carousel to Instagram (@snoopsroulette) through Windsor.ai.
- Midday run (before 5pm): today's slots **1 and 2**.
- Night run (5pm or later): today's slots **3 and 4**.

## Steps
1. `git pull`, then load `queue/queue.json` and `queue/roll_counters.json`.
   Today = the current date in America/Los_Angeles.
2. Pick today's two items for this run's slots. Each needs `status: posted_x`,
   an `image_url`, and `ig_status: pending`.
   - If the items already have `ig_status: posted`, stop: this run already happened.
   - If one isn't posted to X yet (GitHub Actions runs late sometimes), wait
     5 minutes, `git pull`, and check again. Try at most 4 times.
   - If only one is ready after that, post it as a single image
     (`create_image_post`) and set the other's `ig_status` to `skip`.
   - If neither is ready, stop and report it.
3. Caption = `Roll #N`, where N = `instagram` counter + 1. Nothing else: no
   hashtags, no emojis.
4. Post with Windsor.ai `execute_action`: connector `instagram`, account
   `17841423906051846`, action `create_carousel_post`, params
   `{"image_urls": [slot A url, slot B url], "caption": "Roll #N"}` in slot order.
5. On success: set each posted item's `ig_status` to `posted`, set `ig_media_id`
   and `ig_roll` to N, and set the `instagram` counter to N.
   Commit "Instagram Roll #N" and push.
6. If Windsor returns an error, don't retry more than once. Leave the items
   `pending`, don't change the counter, and report the exact error.
