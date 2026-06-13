from ..environment.game import PacmanGame

def h_zero(game: PacmanGame):
    return 0

def h_nearest_snack(game: PacmanGame):
    px, py = game.player
    ds = []
    for s in game.snacks:
        if s.exists:
            ds.append(abs(s.x - px) + abs(s.y - py))
    if not ds:
        return 0
    return min(ds)

def h_remaining_count(game: PacmanGame):
    return sum(1 for s in game.snacks if s.exists)
