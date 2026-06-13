import heapq
from ..environment.game import PacmanGame
from .heuristics import h_nearest_snack
import time

def weighted_astar_solver(game: PacmanGame, heuristic_func=None, weight: int = 10, timeout=10):
    if heuristic_func is None:
        heuristic_func = h_nearest_snack
    t0 = time.time()
    start_info = game.get_info()
    if game.is_goal():
        return [start_info]
    g = {game.get_state(): 0}
    pq = []
    c = 0
    heapq.heappush(pq, (weight * heuristic_func(game), 0, c, game, [start_info]))
    closed = set()
    while pq:
        if time.time() - t0 > timeout:
            return [start_info]
        f, g_cost, _, cur, path = heapq.heappop(pq)
        st = cur.get_state()
        if st in closed:
            continue
        closed.add(st)
        if cur.is_goal():
            return path
        for mv, nxt in cur.get_next_states():
            nst = nxt.get_state()
            ng = g_cost + 1
            if nst in closed:
                continue
            if ng < g.get(nst, float('inf')):
                g[nst] = ng
                c += 1
                h = heuristic_func(nxt)
                heapq.heappush(pq, (ng + weight * h, ng, c, nxt, path + [nxt.get_info()]))
    return None
