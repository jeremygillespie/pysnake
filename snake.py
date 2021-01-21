from collections import namedtuple, deque
import numpy as np


class point(namedtuple('point', 'x y')):
    def __add__(self, other):
        return point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return point(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return point(self.x * n, self.y * n)

    def right(self):
        return point(self.y, self.x * -1)

    def left(self):
        return point(self.y * -1, self.x)


north = point(0, 1)
east = point(1, 0)
south = point(0, -1)
west = point(-1, 0)
cardinals = [north, east, south, west]
diagonals = [north+east, south+east, south+west, north+west]


class occupied:
    def __init__(self, copy=None, width=10, height=10):
        if copy == None:
            self.occ = np.full((width, height), 0, dtype=int)
        else:
            self.occ = np.copy(copy.grid)

    width = property(lambda self: self.occ.shape[0])
    height = property(lambda self: self.occ.shape[1])

    def step(self, p, length):
        self.occ[self.occ > 0] -= 1
        self.occ[p] = length

    def eat(self, p, new_length):
        self.occ[p] = new_length

    def movable(self, p):
        return self.inbounds(p) and self.occ[p] > 1

    def inbounds(self, p):
        if p.x < 0 or p.y < 0:
            return False

        if p.x >= self.width or p.y >= self.height:
            return False

        return True

    def on_edge(self, p):
        if p.x == 0 or p.y == 0:
            return True
        if p.x == self.width - 1 or p.y == self.height - 1:
            return True
        return False

    def incoming(self, p):
        for direc in cardinals:
            p1 = p + direc
            if self.inbounds(p1) and self.occ[p1] > 0 and self.occ[p1] == self.occ[p] - 1:
                return direc * -1

    def outgoing(self, p):
        for direc in cardinals:
            p1 = p + direc
            if self.inbounds(p1) and self.occ[p1] == self.occ[p] + 1:
                return direc


class occupied_walls(occupied):
    def __init__(self, copy=None, width=10, height=10, walls=None):
        super().__init__(copy, width, height)

        if walls is not None:
            self.walls = walls
        elif copy is not None:
            self.walls = copy.walls
        else:
            self.walls = np.full((width, height), False, dtype=bool)

    def movable(self, p):
        if not super().movable(p):
            return False
        elif self.walls[p]:
            return False
        else:
            return True


cor_sw = 0
cor_nw = 1
cor_ne = 2
cor_se = 3

corner_indices = [cor_sw, cor_nw, cor_ne, cor_se]
corner_offsets = [south+west, north+west, north+east, south+east]


def index_from_offset(offset):
    for ind, off in enumerate(corner_offsets):
        if off == offset:
            return ind


cor_pos = 1
cor_none = 0
cor_neg = -1


class occupied_walls_corners(occupied_walls):

    def __init__(self, copy=None, width=10, height=10, walls=None):
        super().__init__(copy, width, height, walls)

        if copy is not None:
            self.cor = np.copy(copy.cor)
            self.cor_dur = np.copy(copy.cor_dur)
            self.cor_map = copy.cor_map
        else:
            self._gen_cor_map()
            self._gen_wall_corners()

            corners, indices = np.unique(self.cor_map, return_inverse=True)
            self.cor = np.full_like(corners, cor_none, dtype=int)
            self.cor_dur = np.full_like(corners, 0, dtype=int)
            self.cor_map = indices.reshape(width, height, 4)

    def step(self, p, prev, length):
        super().step(p, length)
        self._decrement_corners()
        self._set_corners(p, prev, length)

    def eat(self, p, prev, new_length):
        super().eat(p, new_length)
        self._set_corners(p, prev, new_length)

    def movable(self, p, prev):
        if not super().movable(p):
            return False
        incoming = self.incoming(prev)
        outgoing = p - prev
        new = self._new_corners(incoming, outgoing)
        old = self.cor[self.cor_map[prev]]
        bad = new != cor_none & old != cor_none & new != old
        if bad.count_nonzero() == 0:
            return True
        else:
            return False

    def _gen_cor_map(self):
        row = np.arange(self.width).reshape(self.width, 1)
        col = (np.arange(self.height) * (self.width + 1)).reshape(1, self.height)
        grid = np.tile(row, (1, self.height)) + np.tile(col, (self.width, 1))
        offset = np.tile([0, self.width+1, self.width + 2, 1],
                         self.width * self.height).reshape(self.width, self.height, 4)
        self.cor_map = np.repeat(grid, 4, axis=1).reshape(
            self.width, self.height, 4) + offset

        self.cor_map[0, :, [cor_nw, cor_sw]] = 0
        self.cor_map[-1, :, [cor_ne, cor_se]] = 0
        self.cor_map[:, 0, [cor_sw, cor_se]] = 0
        self.cor_map[:, -1, [cor_nw, cor_ne]] = 0

    def _gen_wall_corners(self):
        checked = np.full_like(self.walls, False, dtype=bool)
        for p, w in np.ndenumerate(self.walls):
            if w and not checked[p]:
                wall_corner = self.cor_map[p][0]
                wall_cluster = []
                adjacent = deque([point(*p)])
                while len(adjacent) > 0:
                    p1 = adjacent.pop()
                    wall_cluster.append(p1)
                    checked[p1] = True
                    if self.on_edge(p1):
                        wall_corner = 0
                    for direc in cardinals + diagonals:
                        p2 = p1 + direc
                        if self.inbounds(p2) and self.walls[p2] and not checked[p2]:
                            adjacent.append(p2)
                for p1 in wall_cluster:
                    for direc in corner_indices:
                        offset = corner_offsets[direc]
                        for dx, dy in [(-1, -1), (-1, 0), (0, -1), (0, 0)]:
                            reverse = point(offset.x * dx, offset.y * dy)
                            if self.inbounds(p1 + reverse):
                                self.cor_map[p1 + reverse][direc] = wall_corner

    def _new_corners(self, incoming, outgoing):
        left = index_from_offset(incoming + incoming.left())
        right = index_from_offset(incoming + incoming.right())
        result = np.full((4), cor_none, dtype=int)

        if outgoing == incoming.left():
            result[left] = cor_pos
            result[right] = cor_pos
        elif outgoing == incoming.right():
            result[left] = cor_neg
            result[right] = cor_neg
        else:
            result[left] = cor_neg
            result[right] = cor_pos
        return result

    def _decrement_corners(self):
        self.cor_dur[self.cor_dur > 1] -= 1
        self.cor = np.where(self.cor_dur > 1, self.cor, cor_none)

    def _set_corners(self, p, prev, length):
        incoming = self.incoming(prev)
        outgoing = p - prev
        index = self.cor_map[prev]
        new = self._new_corners(incoming, outgoing)
        old = self.cor[index]
        self.cor[index] = np.where(new != cor_none, new, old)
        old_dur = self.cor_dur[index]
        self.cor_dur[index] = np.where(new != cor_none, length, old_dur)


class printable(occupied_walls_corners):
    def __str__(self):
        result = ''
        for y in range(self.height - 1, -1, -1):
            c = self.cor[self.cor_map[0, y, cor_nw]]
            if c > 0:
                result += '+ '
            elif c < 0:
                result += '- '
            else:
                result += '  '

            for x in range(self.width):
                p = point(x, y)
                if self.incoming(p) == south:
                    result += '∨ '
                elif self.inbounds(p + north) and self.incoming(p + north) == north:
                    result += '∧ '
                else:
                    result += '  '

                c = self.cor[self.cor_map[p][cor_ne]]
                if c > 0:
                    result += '+ '
                elif c < 0:
                    result += '- '
                else:
                    result += '  '

            result += '\n  '

            for x in range(self.width):
                p = point(x, y)
                if self.occ[p]:
                    result += '# '
                elif self.walls[p]:
                    result += 'X '
                else:
                    result += '  '

                if self.incoming(p) == west:
                    result += '< '
                elif self.inbounds(p + east) and self.incoming(p + east) == east:
                    result += '> '
                else:
                    result += '  '

            result += '\n'

        for x in range(self.width):
            c = self.cor[self.cor_map[x, 0, cor_sw]]
            if c > 0:
                result += '+   '
            elif c < 0:
                result += '-   '
            else:
                result += '    '

        c = self.cor[self.cor_map[self.width - 1, 0, cor_se]]
        if c > 0:
            result += '+'
        elif c < 0:
            result += '-'
        else:
            result += ' '

        return result
