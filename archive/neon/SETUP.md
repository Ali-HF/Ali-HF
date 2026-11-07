# Setup (10 minutes)

## 1. Profile repo
1. Create a **public** repo named exactly `Ali-HF` (same as your username).
2. Copy everything in this folder (except `portfolio-site/`) into it and push to `main`.
3. Repo **Settings > Actions > General > Workflow permissions**: select **Read and write permissions**.
4. Go to the **Actions** tab and run these once with "Run workflow":
   - `Generate snake` (creates the `output` branch the snake image reads)
   - `Daily profile update` (fills neofetch, XP bar, recent pushes, rotating banner)
5. Make sure **Issues** are enabled on the repo (Settings > Features). The guestbook and tic-tac-toe run on issues.

## 2. Terminal site
1. Create a **public** repo named `Ali-HF.github.io`.
2. Put `portfolio-site/index.html` in its root as `index.html` and push.
3. It goes live at `https://ali-hf.github.io` (the README contact button already points there).
4. Edit the `born` date near the top of the script to when you started coding.

## 3. Optional extras (commented out in README.md)
- LeetCode card: put your LeetCode username in the commented block and uncomment it.
- Spotify now playing: set it up at spotify-github-profile.kittinunf.com, then uncomment.
- WakaTime: needs a WakaTime account and the `athul/waka-readme` action.

## How the automation works
- `scripts/update.py` rewrites the sections between `<!--START_SECTION:name-->` and `<!--END_SECTION:name-->` markers. Don't delete those comments.
- `scripts/interact.py` handles issues whose title starts with `guestbook` or `ttt|`. Guestbook text is sanitized (links removed, 140 chars max) and shown inside a code block so visitors can't inject markdown.
- `scripts/make_pixel_art.py` regenerates `assets/avatar.svg` and `assets/divider.svg`.
- To test locally: `python scripts/interact.py render` and `python scripts/update.py`.

## Note on the snake
It is the contribution-grid snake recolored in neon. A real Pac-Man or Space Invaders animation is not available as a standard Action, so the snake stays.
