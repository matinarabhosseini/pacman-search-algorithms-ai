from ..environment.game import PacmanGame
import time

def _dls(node, limit, t0, timeout):
    if time.time() - t0 > timeout:
        return "TIMEOUT"
    game, path = node
    if game.is_goal():
        return path
    if limit == 0:
        return None
    for mv, nxt in game.get_next_states():
        res = _dls((nxt, path + [nxt.get_info()]), limit - 1, t0, timeout)
        if res == "TIMEOUT":
            return "TIMEOUT"
        if res is not None:
            return res
    return None

def ids_solver(game: PacmanGame, max_limit: int = 100000, timeout=10):
    t0 = time.time()
    start_info = game.get_info()
    if game.is_goal():
        return [start_info]
    for depth in range(1, max_limit + 1):
        if time.time() - t0 > timeout:
            return [start_info]
        res = _dls((game, [start_info]), depth, t0, timeout)
        if res == "TIMEOUT":
            return [start_info]
        if res is not None:
            return res
    return None
