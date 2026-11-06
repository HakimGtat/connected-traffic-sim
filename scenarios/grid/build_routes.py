"""Generate random traffic demand for the grid network (fixed seed, so runs repeat)."""
import os
import subprocess
import sys
from pathlib import Path

import sumo

HERE = Path(__file__).parent
SUMO_HOME = Path(sumo.SUMO_HOME)
RANDOM_TRIPS = SUMO_HOME / "tools" / "randomTrips.py"


def build(end_time: int = 600, period: float = 1.5, seed: int = 42) -> Path:
    out = HERE / "grid.rou.xml"
    env = {**os.environ, "SUMO_HOME": str(SUMO_HOME)}
    subprocess.run(
        [
            sys.executable, str(RANDOM_TRIPS),
            "-n", str(HERE / "grid.net.xml"),
            "-r", str(out),
            "-o", str(HERE / "grid.trips.xml"),
            "-b", "0", "-e", str(end_time),
            "-p", str(period),          # one new car every `period` seconds
            "--fringe-factor", "5",     # most trips start/end at the grid edges
            "--seed", str(seed),
            "--validate",
        ],
        check=True,
        env=env,
    )
    return out


if __name__ == "__main__":
    print("Wrote", build())
