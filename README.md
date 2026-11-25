# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/hakeno337/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/hakeno337/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One image that sums up the world's news of Wednesday 25 November 2026, set as an illustrated broadsheet front page under a black date band: Australia signing the Solomon Islands security treaty in Canberra, China launching Pakistan's first astronaut to the Tiangong station, and all hostages freed in the Cartagena supermarket siege as the three drawn lead panels; a big-number stat strip (€115bn for Ukraine, a 36% garment-wage rise in Dhaka, gold at $3,545, the 5.1 Panay quake); a numbered grid of fifteen more stories, each with its own drawn icon; a dotted world map whose numbered pins match the story numbers; an ALSO ON WEDNESDAY list of sixteen further stories; and a DATE CHECK box that names the stories deliberately left out as 24 November's news. Every story was date-checked against 25 November 2026 reporting.

## Run it

```sh
node main.ts
```

The program copies the repository's `entry.png` to `/output/entry.png` (or to `$MAKEFUN_OUTPUT_DIR/entry.png` outside the grader), after checking it against the gate's limits (PNG or JPEG, at most 1 MiB, at most 1024 by 1024). Node 22, standard library only.

The image itself is composed by `compose.py` (Python + PIL): the day's stories, researched from 25 November's reporting, drawn and set as a legible illustrated front page at 1024 by 1024. Rebuild it with `python3 compose.py`.
