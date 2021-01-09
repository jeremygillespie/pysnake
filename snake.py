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


class graph:
    def __init__(self, width, height, fill_value=0, dtype=bool):
        self.val = np.full((width, height), fill_value, dtype=dtype)

    width = property(lambda self: self.val.shape[0])
    height = property(lambda self: self.val.shape[1])

    def __call__(self):
        return self.val

    def inbounds(self, p):
        if p.x < 0 or p.y < 0:
            return False

        if p.x >= self.width or p.y >= self.height:
            return False

        return True


class occupied(graph):
    def __init__(self, width, height):
        graph.__init__(self, width, height, dtype=int)

    def movable(self, p):
        return self()[p] > 1

    def incoming(self, p):
        for direc in cardinals:
            p1 = p + direc
            if self.inbounds(p1) and self()[p1] > 0 and self()[p1] == self()[p] - 1:
                return direc * -1

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
                if self()[p]:
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
