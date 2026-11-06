# CLAUDE.md: connected-traffic-sim

## What this is
A traffic simulator where cars talk to each other (V2V) and to traffic lights (V2I). The goal is to measure how much traffic flow improves when we take human reaction time out of the loop (for example, the hesitation when a light turns green). Message delay is modeled realistically, so crashes caused by slow messages are allowed and are part of the study.

It's a **portfolio piece**: public repo, clear before/after results, dashboard + demo video at the end.

- Repo: https://github.com/HakimGtat/connected-traffic-sim (public, `main`)
- Full roadmap: [docs/plan.md](docs/plan.md). Read it before starting a phase.

## Decisions already made (don't re-ask)
- **Simulator:** SUMO + Python. Not CARLA (wrong tool for city-scale flow).
- **Messaging:** a simple Python model (delay, jitter, drop %, range) behind a `MessageBus` interface, so Veins/OMNeT++ can be swapped in later.
- **Light optimizer:** rule-based first (actuated → queue/max-pressure → SPaT broadcast to cars). RL with `sumo-rl` is a stretch goal.
- **Map:** 3×3 synthetic grid for development, then a real Ottawa corridor from OpenStreetMap for the showcase (Phase 5).
- **Mixed traffic:** connected-car share (0/25/50/100%) is an experiment knob.

## Status
- **Phase 0, done** (commit `8e0fb51`): SUMO 1.28 via pip, 3×3 grid, `sim/hello_grid.py` logs per-car speeds.
  - First run (simulation results, fixed-time lights, default drivers): 711 s simulated, 400 cars, mean speed 8.41 m/s, 21.9% of samples stopped, 0 collisions.
- **Next: Phase 1, baseline.** "Human" drivers (reaction time `tau`, `actionStepLength` ≈ 1 s, start-up delay at green), fixed-time lights, and a proper metrics module (travel time, delay, queue length, throughput per green, stops, CO2, collisions) with seeded, repeatable runs.

## Setup and commands (Windows)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python sim/hello_grid.py          # headless, uses libsumo (fast)
python sim/hello_grid.py --gui    # sumo-gui, uses TraCI
python scenarios/grid/build_routes.py   # regenerate demand (seed 42)
```
- SUMO binaries come from the `eclipse-sumo` pip package. Find them with `import sumo; sumo.SUMO_HOME` (`bin/sumo`, `bin/sumo-gui`, `tools/randomTrips.py`). There's no system install and no `SUMO_HOME` env var; code gets the paths from the package.
- `netgenerate` is in `.venv\Scripts\`.
- The venv uses Python 3.14 (the system default).

## Gotchas learned so far
- **libsumo vs TraCI:** libsumo runs in-process and is much faster, but it can't drive the GUI. Use TraCI only for `--gui`. Both share the same API, so import one `as sim`.
- **GUI runs need `--quit-on-end`**, or sumo-gui stays open and the Python script hangs.
- **Step length is 0.1 s** (in `grid.sumocfg`). The logger writes once per simulated second.
- **Crashes:** SUMO's default car-following models avoid collisions. For latency to cause crashes, connected cars need a custom controller with safety checks turned off via `vehicle.setSpeedMode`. Collision detection is already on (`collision.action warn`).
- `output/` is git-ignored; run logs go there.

## Layout
```
scenarios/grid/   grid.net.xml, grid.rou.xml, grid.sumocfg, build_routes.py
sim/              simulation scripts (hello_grid.py; planned: orchestrator, agents/, comms/, controllers/, metrics.py)
docs/plan.md      roadmap: phases, architecture, risks
output/           run logs (ignored)
```

## Working rules
- Ask before committing and before pushing.
- Plan or interview before anything substantial; give a recommendation with each question.
- Run the sim and check the output (and the GUI when visuals matter) before calling something done.
- Never invent numbers. Every result in the README or charts comes from an actual run and is labeled as **simulation results**.
- Be honest about prior art in write-ups (V2X, CACC, SPaT/GLOSA, SUMO/Veins/MOSAIC already exist). What's original here is the comparison setup and the latency-vs-safety curve.
- Portfolio entry happens in Phase 5 (see the portfolio repo's CLAUDE.md).
