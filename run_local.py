import argparse, os, sys, glob, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.environment.map_loader import MapLoader
from core.environment.game import PacmanGame
from core.solvers.bfs_solver import bfs_solver
from core.solvers.dfs_solver import dfs_solver
from core.solvers.ids_solver import ids_solver
from core.solvers.astar_solver import astar_solver
from core.solvers.weighted_astar_solver import weighted_astar_solver
from core.solvers.heuristics import h_nearest_snack, h_zero

ALGOS = {
    "bfs": lambda g, t, w: bfs_solver(g, timeout=t),
    "dfs": lambda g, t, w: dfs_solver(g, timeout=t),
    "ids": lambda g, t, w: ids_solver(g, timeout=t),
    "astar": lambda g, t, w: astar_solver(g, timeout=t),
    "wastar": lambda g, t, w: weighted_astar_solver(g, heuristic_func=h_nearest_snack, weight=w, timeout=t)
}

def build_game(map_path):
    is_wall, player, ghosts, snacks = MapLoader(file_path=map_path).load()
    return PacmanGame(player=player, ghosts=ghosts, snacks=snacks, is_wall=is_wall, move_direction="")

class _Metrics:
    def __init__(self):
        self.expanded = 0

def _wrap_get_next_states(metrics):
    orig = PacmanGame.get_next_states
    def wrapped(self):
        res = orig(self)
        metrics.expanded += len(res)
        return res
    return orig, wrapped

def run_one(map_path, algo, timeout, weight, show_moves, metrics_flag):
    game = build_game(map_path)
    fn = ALGOS[algo]
    metrics = _Metrics()
    if metrics_flag:
        orig, wrapped = _wrap_get_next_states(metrics)
        PacmanGame.get_next_states = wrapped
    t0 = time.time()
    path = fn(game, timeout, weight)
    dt = time.time() - t0
    if metrics_flag:
        PacmanGame.get_next_states = orig
    if path is None:
        print(f"{algo.upper()} | {os.path.basename(map_path)} | path=None")
        return
    moves = [step[0] for step in path if isinstance(step, tuple) and len(step) > 0]
    seq = "".join(m for m in moves if m)
    steps = max(0, len(moves) - 1)
    if metrics_flag:
        print(f"{algo.upper()} | {os.path.basename(map_path)} | steps={steps} | expanded={metrics.expanded} | time_ms={int(dt*1000)}")
    else:
        print(f"{algo.upper()} | {os.path.basename(map_path)} | steps={steps}")
    if show_moves:
        print(seq)

def run_all(maps_glob, algo, timeout, weight, show_moves, metrics_flag):
    files = sorted(glob.glob(maps_glob))
    if not files:
        print("no maps")
        return
    for mp in files:
        run_one(mp, algo, timeout, weight, show_moves, metrics_flag)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--map", type=str, default="maps/map1.txt")
    p.add_argument("--algo", type=str, choices=list(ALGOS.keys()), default="astar")
    p.add_argument("--timeout", type=int, default=10)
    p.add_argument("--weight", type=int, default=10)
    p.add_argument("--show_moves", type=int, default=0)
    p.add_argument("--all", action="store_true")
    p.add_argument("--glob", type=str, default="maps/map*.txt")
    p.add_argument("--metrics", type=int, default=0)
    a = p.parse_args()
    if a.all:
        run_all(a.glob, a.algo, a.timeout, a.weight, a.show_moves, a.metrics)
    else:
        run_one(a.map, a.algo, a.timeout, a.weight, a.show_moves, a.metrics)
