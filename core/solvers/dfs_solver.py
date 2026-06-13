from ..environment.game import PacmanGame
import time

def dfs_solver(game: PacmanGame, timeout=10):
    t0 = time.time()
    start_info = game.get_info()
    if game.is_goal():
        return [start_info]
    stack = [(game, [start_info], set([game.get_state()]))]
    while stack:
        if time.time() - t0 > timeout:
            return [start_info]
        cur, path, seen = stack.pop()
        for mv, nxt in cur.get_next_states():
            st = nxt.get_state()
            if st in seen:
                continue
            nseen = set(seen)
            nseen.add(st)
            info = nxt.get_info()
            new_path = path + [info]
            if nxt.is_goal():
                return new_path
            stack.append((nxt, new_path, nseen))
    return None
