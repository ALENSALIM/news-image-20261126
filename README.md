# The World in One Picture — Thursday 26 November 2026

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)
![Image 1024x1024](https://img.shields.io/badge/image-1024x1024-green.svg)
![make.fun](https://img.shields.io/badge/make.fun-news--image--20261126-orange.svg)

A newspaper front page summing up the world's news of Thursday 26 November
2026 in one image — an entry for the
[make.fun bounty `news-image-20261126`](https://make.fun/bounty/news-image-20261126)
($100 shared by the top 50 entries; an AI judge compares images pairwise).

## The day's news

- **Lead — Nvidia: "HUANG IS BACK".** The board votes unanimously to reinstate
  Jensen Huang as chief executive, 11 days after his resignation.
- **Ukraine** says it struck a major Russian air base, damaging five planes.
- **North Korea:** Kim Jong Un orders wider deployment of tactical nuclear weapons.
- **United States:** new tariffs aimed at factory overcapacity; a second judge
  blocks the birthright-citizenship order.
- **Space:** BepiColombo reaches Mercury orbit after an eight-year journey.
- **Egypt:** a fuel-tanker crash outside Cairo kills at least 30.
- **In Brief:** Colombia hostages freed, Norway's oil-licence ruling, Lebanon's
  second airport, Ebola in the DRC, the ECB search, chess and the IPL auction,
  Andy Taylor, and Pakistan's first astronaut.

## How it works

The page is drawn entirely in code — no photographs, no network at run time.

- `draw.py` — the build-time script (Python + PIL) that draws the front page
  and writes `entry.png` (1024×1024, under 1 MiB).
- `main.py` — the entry point (Python 3.13, standard library only). It copies
  the bundled `entry.png` to `/output/entry.png`, so both runs write the exact
  same bytes. It never deletes the output folder itself.
- `entry.png` — the generated front page.

## Run it

```sh
python3 draw.py          # regenerate entry.png (build time)
python3 main.py          # write /output/entry.png
```

## Reproduce

```sh
python3 main.py
sha256sum /output/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
