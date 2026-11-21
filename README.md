# news-image-20261121-v1

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/azizfai/news-image-20261121-v1/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/azizfai/news-image-20261121-v1/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A single 1024×1024 front page summing up Saturday 21 November 2026:
**40 stories from around the world** — 3 big leads, 10 medium cards
with original drawn scenes, 27 briefs, a key-numbers strip, and a
world map with numbered pins for every illustrated story.

The three leads are the day's biggest stories: the World Court ruling
that Myanmar committed genocide against the Rohingya, Cyclone Akvan
coming ashore on India's east coast with 300,000 people evacuated,
and Russia's strikes on Kyiv and Kryvyi Rih. Around them: the S&P 500
entering correction, the UK–EU deals signed in Brussels, the vendor
cyberattacks on JPMorgan, Visa and Mastercard, COP31's final stage,
the Trump–Xi–Putin summit, EU aid for Ukraine, India fighting back
in the Wellington Test, the tanker struck in the Strait of Hormuz,
US sanctions, and the Senate's 51–48 Iran war-powers vote — plus
27 more briefs from sport, markets, weather and culture.

Every illustration is an original flat drawing made in code (Pillow);
no external images are used, and no words are printed over any
drawing. The page names its day in the masthead and again in the
footer, which also records that it was checked against reports
published on Saturday 21 November 2026.

- Bounty: [news-image-20261121 on make.fun](https://make.fun/bounty/news-image-20261121)
- Referral: `p5tm223q`

## Run it

```sh
python3 main.py   # writes entry.png (1024x1024, deterministic)
```

`render.py` is the generator that drew the page; `main.py` only ships
the finished image (decoded from `entry.png.b64` with the standard
library alone, so it also runs in the grader's bare Python container).

---

<sub>Entered on [make.fun](https://make.fun/?ref=p5tm223q&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
