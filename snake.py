from collections import namedtuple
import numpy as np


class point(namedtuple('point', 'x y')):
    def __add__(self, other):
        return point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return point(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return point(self.x * n, self.y * n)


north = point(0, 1)
south = point(0, -1)
east = point(1, 0)
west = point(-1, 0)
cardinals = [north, south, east, west]


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

    def inbounds(self, p):
        if p.x < 0 or p.y < 0:
            return False

        if p.x >= self.width or p.y >= self.height:
            return False

        return True

    def movable(self, p):
        return self.inbounds(p) and self.occ[p] > 1

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
        for y in range(self.height - 1, -1, -1):
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


class index(namedtuple('index', 'xx yy')):
    def __getitem__(self, key):
        return self.xx[key], self.yy[key]

    def __setitem__(self, key, val):
        self.xx[key] = val.x
        self.yy[key] = val.y


cor_right = 1
cor_none = 0
cor_left = -1


class occupied_corners(occupied):

    def __init__(self, copy=None, cor_map=None, width=10, height=10):
        super().__init__(copy, width, height)

        if copy != None:
            self.cor = copy.cor
        else:
            self.cor = np.full((width + 1, height + 1), cor_none, dtype=int)

        if cor_map != None:
            self.cor_map = cor_map
        elif copy != None:
            self.cor_map = copy.cor_map
        else:
            self.cor_map = index(*np.indices((width + 1, height + 1)))
            self.cor_map[point(1, 2)] = point(5, 6)
            # generate edge indices

    def step(self, p, length, incoming):
        super().step(p, length)

    def eat(self, p, new_length, incoming):
        super().eat(p, new_length)
