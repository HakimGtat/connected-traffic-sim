# Connected Traffic Simulator

A traffic simulation where cars talk to each other (V2V) and to traffic lights (V2I). The question I want to answer: how much faster does traffic move when nobody has to wait on human reaction time, and how much message delay can the system handle before cars start crashing?

Built on [SUMO](https://eclipse.dev/sumo/) with Python. The full roadmap is in [docs/plan.md](docs/plan.md).

## Status

Phase 0 (setup) is done. A 3×3 grid of signalized intersections runs from Python and logs every car's speed.

## Setup (Windows)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

SUMO itself installs through pip (`eclipse-sumo`), so there's no separate installer.

## Run

```bash
python sim/hello_grid.py          # headless, fast
python sim/hello_grid.py --gui    # watch it in sumo-gui
```

Output goes to `output/speeds.csv` (one row per car per simulated second).

## Layout

```
scenarios/grid/   grid network, route generator, SUMO config
sim/              simulation scripts
docs/             project plan
output/           run logs (git-ignored)
```
