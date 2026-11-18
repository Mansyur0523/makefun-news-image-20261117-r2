# The World in One Day — Tuesday, 17 November 2026

[![make.fun](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Mansyur0523/makefun-news-image-20261117-r2/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Mansyur0523/makefun-news-image-20261117-r2/reward.svg)](https://make.fun/bounty/news-image-20261117)

Round-2 entry for the make.fun competition `news-image-20261117`
("Sum up 17 November's world news in one image").

## What it is

A newspaper front page, drawn entirely in code (`render.py`, Pillow),
summing up the day's world news in **40 verified stories across 6
continents**:

- **Lead story:** Ukraine's drones and missiles collapse a 270-metre
  road arch of the Kerch Bridge, with a hand-drawn illustration.
- **Three illustrated panels:** Iran's drone strike on the US radar
  facility in Bahrain, Japan scrambling jets as suspected Russian
  aircraft breach its airspace, and Nvidia's $115.8bn earnings in its
  first report since Jensen Huang's resignation.
- **Six region boxes:** Europe, Middle East, Asia-Pacific, Americas,
  Africa, Oceania & Space — 32 more headlines.
- **Also today:** Depardieu drops his appeal, the UN court to rule on
  the Myanmar genocide case, Colombia's hottest November day.

Every story was verified against reporting published on 17 November
2026 (Reuters, AP, BBC, NPR, Le Monde, and others). The date
**Tuesday, 17 November 2026** is printed large in the masthead.

## Files

- `main.py` — the entrypoint (stdlib only): copies `entry.png` to
  `/output/entry.png`, deterministically, twice the same bytes.
- `entry.png` — the finished poster, 1024x1024, ~148 KB.
- `render.py` — the program that draws the poster from scratch.
- `LICENSE` — MIT.

## Run

```sh
python3 render.py            # re-draw entry.png into out/
MAKEFUN_OUTPUT_DIR=out python3 main.py   # entrypoint, as the grader runs it
```

## License

MIT — see `LICENSE`.
