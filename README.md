# THE WORLD TODAY — Friday 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/queenxaz/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/queenxaz/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

Entry for [Sum up 20 November's world news in one image](https://make.fun/bounty/news-image-20261120) — a one-page newspaper front page drawn programmatically with Pillow: 20 stories from Friday 20 November 2026, led by the AI-driven plunge in Asian markets (Nikkei −4.8%, SoftBank −16%), with a markets ticker, a story grid, and a small world map of the day's hot spots.

## How it works

- `render.py` draws the 1024×1024 front page with Pillow (no network, no randomness).
- `main.py` renders the page and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png` (JPEG bytes under the `.png` name, as the rules allow). If Pillow is unavailable it falls back to the pre-rendered `entry.jpg` shipped in the repo, so both runs write identical bytes either way.
- `entry.jpg` is the pre-rendered front page.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
