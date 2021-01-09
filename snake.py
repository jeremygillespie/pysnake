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


class graph(np.ndarray):
    def __new__(subtype, shape, dtype=float, buffer=None, offset=0,
                strides=None, order=None):
        obj = super(InfoArray, subtype).__new__(subtype, shape, dtype,
                                                buffer, offset, strides,
                                                order)

        # obj.info = info

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

        # self.info = getattr(obj, 'info', None)


def width(graph):
    return graph.shape[0]


def height(graph):
    return graph.shape[1]


def inbounds(graph, p):
    if p.x < 0 or p.y < 0:
        return False

    if p.x >= width(graph) or p.y >= height(graph):
        return False

    return True


def incoming(occ, p):
    for direc in cardinals:
        p1 = p + direc
        if inbounds(occ, p1) and occ[p1] > 0 and occ[p1] == occ[p] - 1:
            return direc * -1


def output(occ):
    result = ''
    for y in range(height(occ) - 1, -1, -1):
        for x in range(width(occ)):
            p = point(x, y)
            if incoming(occ, p) == south:
                result += '∨   '
            elif inbounds(occ, p + north) and incoming(occ, p + north) == north:
                result += '∧   '
            else:
                result += '    '

        result += '\n'

        for x in range(width(occ)):
            p = point(x, y)
            if occ[p]:
                result += '# '
            else:
                result += '. '

            if incoming(occ, p) == west:
                result += '< '
            elif inbounds(occ, p + east) and incoming(occ, p + east) == east:
                result += '> '
            else:
                result += '  '

        result += '\n'

    return result
