from collections import deque
from ..environment.game import PacmanGame
import time

def bfs_solver(game: PacmanGame, timeout=10):
    t0 = time.time()
    start_info = game.get_info()
    if game.is_goal():
        return [start_info]
    q = deque()
    q.append((game, [start_info]))
    seen = set()
    seen.add(game.get_state())
    while q:
        if time.time() - t0 > timeout:
            return [start_info]
        cur, path = q.popleft()
        for mv, nxt in cur.get_next_states():
            st = nxt.get_state()
            if st in seen:
                continue
            seen.add(st)
            info = nxt.get_info()
            new_path = path + [info]
            if nxt.is_goal():
                return new_path
            q.append((nxt, new_path))
    return None
