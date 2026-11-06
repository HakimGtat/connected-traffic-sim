"""Phase 0 smoke test: run the grid scenario from Python and log every car's speed.

Usage:
    python sim/hello_grid.py          # headless, fast (libsumo)
    python sim/hello_grid.py --gui    # opens sumo-gui (TraCI)
"""
import argparse
import csv
import sys
from pathlib import Path

import sumo

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "scenarios" / "grid"
OUT_DIR = ROOT / "output"

sys.path.insert(0, str(SCENARIO))
from build_routes import build  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gui", action="store_true", help="open sumo-gui instead of running headless")
    ap.add_argument("--steps", type=int, default=9000, help="sim steps (0.1 s each)")
    args = ap.parse_args()

    if not (SCENARIO / "grid.rou.xml").exists():
        build()

    if args.gui:
        import traci as sim  # socket connection, needed for the GUI
        binary = Path(sumo.SUMO_HOME) / "bin" / "sumo-gui"
    else:
        import libsumo as sim  # in-process, much faster
        binary = Path(sumo.SUMO_HOME) / "bin" / "sumo"

    cmd = [str(binary), "-c", str(SCENARIO / "grid.sumocfg"), "--no-step-log", "true"]
    if args.gui:
        cmd += ["--start", "--quit-on-end", "--delay", "20"]
    sim.start(cmd)

    OUT_DIR.mkdir(exist_ok=True)
    out_file = OUT_DIR / "speeds.csv"
    collisions = 0
    with out_file.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["time_s", "vehicle_id", "speed_mps", "accel_mps2", "edge", "x", "y"])
        for _ in range(args.steps):
            sim.simulationStep()
            t = sim.simulation.getTime()
            collisions += sim.simulation.getCollidingVehiclesNumber()
            # log once per simulated second to keep the file small
            if round(t * 10) % 10 != 0:
                continue
            for vid in sim.vehicle.getIDList():
                x, y = sim.vehicle.getPosition(vid)
                w.writerow([
                    round(t, 1), vid,
                    round(sim.vehicle.getSpeed(vid), 2),
                    round(sim.vehicle.getAcceleration(vid), 2),
                    sim.vehicle.getRoadID(vid),
                    round(x, 1), round(y, 1),
                ])
            if sim.simulation.getMinExpectedNumber() == 0:
                break
        arrived = sim.simulation.getArrivedNumber()
    sim.close()

    import pandas as pd
    df = pd.read_csv(out_file)
    print(f"Simulated {df.time_s.max():.0f} s, {df.vehicle_id.nunique()} cars seen")
    print(f"Mean speed: {df.speed_mps.mean():.2f} m/s, "
          f"share of samples stopped (<0.1 m/s): {(df.speed_mps < 0.1).mean():.1%}")
    print(f"Collisions: {collisions}")
    print(f"Log: {out_file}")


if __name__ == "__main__":
    main()
