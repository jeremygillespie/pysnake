from collections import namedtuple
import numpy as np


class point(namedtuple('point', 'x y')):
    def __add__(self, other):
        return point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return point(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return point(self.x * n, self.y * n)


north = point(0, -1)
east = point(1, 0)
south = point(0, 1)
west = point(-1, 0)
cardinals = [north, east, south, west]


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

    def __str__(self):
        result = ''
        for y in range(self.height):
            for x in range(self.width):
                p = point(x, y)
                if self.incoming(p) == south:
                    result += '∨   '
                elif self.inbounds(p + north) and self.incoming(p + north) == north:
                    result += '∧   '
                else:
                    result += '    '

            result += '\n'

            for x in range(self.width):
                p = point(x, y)
                if self.occ[p]:
                    result += '# '
                else:
                    result += '. '

                if self.incoming(p) == west:
                    result += '< '
                elif self.inbounds(p + east) and self.incoming(p + east) == east:
                    result += '> '
                else:
                    result += '  '

            result += '\n'

        return result


class corner(namedtuple('corner', 'x, y, direc')):
    pass


top_l = 0
top_r = 1
bot_l = 2
bot_r = 3

corner_directions = [bot_l, bot_r, top_l, top_l]

cor_right = 1
cor_none = 0
cor_left = -1


class occupied_corners(occupied):

    def __init__(self, copy=None, width=10, height=10):
        super().__init__(copy, width, height)

        if copy != None:
            self.cor = np.copy(copy.cor)
            self.cor_map = copy.cor_map
        else:
            offset = np.repeat([0, 1, width, width + 1], width * height)
            grid = np.tile(np.arange(width * height), 4)
            cor_map = np.reshape(grid + offset, (4, width, height))

            cor_map[[top_l, bot_l], 0, :] = 0
            cor_map[[top_r, bot_r], -1, :] = 0
            cor_map[[top_l, top_r], :, 0] = 0
            cor_map[[bot_l, bot_r], :, -1] = 0

            corners, indices = np.unique(cor_map, return_inverse=True)
            self.cor = np.full(len(corners), cor_none, dtype=int)
            self.cor_map = indices.reshape(4, width, height)

    def step(self, p, length, incoming):
        super().step(p, length)

    def eat(self, p, new_length, incoming):
        super().eat(p, new_length)

    def movable(self, p):
        if not super().movable(p):
            return False
        return True
