from ..environment.game import PacmanGame
from .heuristics import h_nearest_snack
from .weighted_astar_solver import weighted_astar_solver

def astar_solver(game: PacmanGame, timeout=10):
    return weighted_astar_solver(game, heuristic_func=h_nearest_snack, weight=1, timeout=timeout)
