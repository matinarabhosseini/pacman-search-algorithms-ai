from copy import deepcopy
from .ghost import Ghost
from .snack import Snack

class PacmanGame:
    def __init__(self, player: tuple[int, int], ghosts: list[Ghost], snacks: list[Snack], is_wall, move_direction=None):
        self.player = player
        self.ghosts = deepcopy(ghosts)
        self.snacks = deepcopy(snacks)
        self.is_wall = is_wall
        self.height = len(is_wall) if not callable(is_wall) else None
        self.width = (len(is_wall[0]) if self.height else None) if not callable(is_wall) else None
        self.move_direction = move_direction if move_direction is not None else ''

    def get_info(self):
        return (self.move_direction, [self.player] + [ghost.get_info() for ghost in self.ghosts] + [snack.get_info() for snack in self.snacks])

    def determine_goal(self):
        remaining_snacks = [s.type for s in self.snacks if s.exists]
        if len(remaining_snacks) == 0:
            return None
        return min(remaining_snacks)

    def in_bounds(self, x, y):
        if callable(self.is_wall):
            return True
        return 0 <= x < self.height and 0 <= y < self.width

    def is_valid(self, x, y):
        if not self.in_bounds(x, y):
            return False
        w = self.is_wall
        return not (w(x, y) if callable(w) else w[x][y])

    def is_goal(self):
        return all(not b for b in [snack.exists for snack in self.snacks])

    def is_dead(self):
        px, py = self.player
        return any(g.x == px and g.y == py for g in self.ghosts)

    def is_terminal(self):
        return self.is_goal() or self.is_dead()

    def get_map(self) -> str:
        if callable(self.is_wall):
            return ""
        height = len(self.is_wall)
        width = len(self.is_wall[0])
        display_grid = [[' ' for _ in range(width)] for _ in range(height)]
        for x in range(height):
            for y in range(width):
                if self.is_wall[x][y]:
                    display_grid[x][y] = 'W'
        for snack in self.snacks:
            if snack.exists:
                display_grid[snack.x][snack.y] = f'{snack.type}'
        for g in self.ghosts:
            gx, gy = g.x, g.y
            display_grid[gx][gy] = f'{g.axis}'
        px, py = self.player
        display_grid[px][py] = 'P'
        map_string = "╔" + "═" * width + "╗" + "\n"
        for row in display_grid:
            map_string += "║" + "".join(row) + "║" + "\n"
        return map_string + "╚" + "═" * width + "╝" + "\n"

    def get_next_states(self):
        dirs = {"U": (-1, 0), "L": (0, -1), "D": (1, 0), "R": (0, 1)}
        next_states = []
        for mv, d in dirs.items():
            nx = self.player[0] + d[0]
            ny = self.player[1] + d[1]
            if not self.is_valid(nx, ny):
                continue
            ng = deepcopy(self)
            prev_pac = self.player
            ng.player = (nx, ny)
            ng.move_direction = mv
            if any(g.x == nx and g.y == ny for g in ng.ghosts):
                continue
            prev_ghosts = [(g.x, g.y) for g in ng.ghosts]
            ng._advance_ghosts()
            if ng.is_dead():
                continue
            for (gx2, gy2), (gx1, gy1) in zip([(g.x, g.y) for g in ng.ghosts], prev_ghosts):
                if (gx2, gy2) == prev_pac and (gx1, gy1) == (nx, ny):
                    break
            else:
                for s in ng.snacks:
                    if s.exists and s.x == nx and s.y == ny:
                        s.exists = False
                next_states.append((mv, ng))
        return next_states

    def _step_ghost(self, g: Ghost):
        if g.axis == "H":
            if g.direction == "L":
                tx, ty = g.x, g.y - 1
                if not self.is_valid(tx, ty):
                    g.direction = "R"
                    ty = g.y + 1
                g.y = ty
            else:
                tx, ty = g.x, g.y + 1
                if not self.is_valid(tx, ty):
                    g.direction = "L"
                    ty = g.y - 1
                g.y = ty
        else:
            if g.direction == "U":
                tx, ty = g.x - 1, g.y
                if not self.is_valid(tx, ty):
                    g.direction = "D"
                    tx = g.x + 1
                g.x = tx
            else:
                tx, ty = g.x + 1, g.y
                if not self.is_valid(tx, ty):
                    g.direction = "U"
                    tx = g.x - 1
                g.x = tx

    def _advance_ghosts(self):
        for g in self.ghosts:
            self._step_ghost(g)

    def get_state(self):
        gx = tuple((g.x, g.y, g.direction) for g in self.ghosts)
        sx = tuple(sorted(((s.x, s.y, s.type, bool(s.exists)) for s in self.snacks)))
        return (self.player[0], self.player[1], gx, sx)
