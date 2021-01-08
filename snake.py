from collections import namedtuple
import numpy as np


class Point(namedtuple('Point', 'x y')):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return Point(self.x * n, self.y * n)


north = Point(0, 1)
south = Point(0, -1)
east = Point(1, 0)
west = Point(-1, 0)
cardinals = [north, south, east, west]


class Graph:
    def __init__(self, width, height, start=Point(0, 0)):
        self.width = width
        self.height = height
        self.head = start

        self.occupied = np.full((width, height), 0, dtype=int)

        for p in range(1, 6):
            self.occupied[p-1, 0] = p
        for p in range(6, 11):
            self.occupied[5, p-6] = p

    def decrement_occupied(self):
        self.occupied[self.occupied > 0] -= 1

    def inbounds(self, p):
        if p.x < 0 or p.y < 0:
            return False

        if p.x >= self.width or p.y >= self.height:
            return False

        return True

    def incoming(self, p):
        for direc in cardinals:
            p1 = p + direc
            if self.inbounds(p1) and self.occupied[p1] > 0 and self.occupied[p1] == self.occupied[p] - 1:
                return direc * -1

    def __str__(self):
        result = ''
        for y in range(self.height-1, -1, -1):
            for x in range(self.width):
                p = Point(x, y)
                if self.incoming(p) == south:
                    result += '∨   '
                elif self.inbounds(p + north) and self.incoming(p + north) == north:
                    result += '∧   '
                else:
                    result += '    '

            result += '\n'

            for x in range(self.width):
                p = Point(x, y)
                if self.occupied[p]:
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


g = Graph(10, 10)
print(g)
