# makefun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/jkislew/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/jkislew/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

**The World Today** — the whole of Friday 20 November 2026 set in type on a single
1024×1024 newspaper page. The lead is the Shenzhen summit: Trump, Xi and Putin sign a
four-point "Declaration Toward Peace" at the first trilateral meeting of the three
leaders. Below it, the World Court finds Myanmar guilty of genocide against the
Rohingya, a first in the court's 80 years. Four briefs complete the front page —
Voyager 1 reaching one light-day from Earth, Anthropic's record $81.3 billion IPO
closing up 17%, GTA 6 earning $1.84 billion on launch day, and Cyclone Akvan making
landfall in Odisha — and a ticker along the foot of the page carries five more stories.
Every fact was checked against at least two outlets on the morning of 20 November
before it was set in type.

## Run it

```sh
python3 main.py
```

That copies the shipped `entry.png` to `/output/entry.png` (set `ENTRY_OUTPUT` to
redirect it). The run is deterministic: the same bytes come out every time.

## How the page is made

`make_image.py` typesets the page with Pillow: a serif masthead, two full-width
stories, a four-column briefs row and a dark ticker band. It reads no clock, no
network and no randomness, so re-running it rebuilds `entry.png` byte for byte:

```sh
python3 make_image.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=tpc75c2v&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
