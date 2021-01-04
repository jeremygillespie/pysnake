from collections import namedtuple
import numpy as np

Point = namedtuple('Point', 'x y')
Dir = namedtuple('Dir', 'dx dy')

north = Dir(0, 1)
south = Dir(0, -1)
east = Dir(1, 0)
west = Dir(-1, 0)
cardinals = [north, south, east, west]


def offset(point, dir):
    t = tuple(np.array(point) + np.array(dir))
    return Point(t[0], t[1])


class Graph:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.occupied = np.zeros((width, height))
        self.head = Point(0, 0)
        self.occupied[self.head] = 4

    def inbounds(self, point):
        if not point:
            return False
        elif point.x < 0:
            return False
        elif point.y < 0:
            return False
        elif point.x >= self.width:
            return False
        elif point.y >= self.width:
            return False
        else:
            return True

    def outgoing(self, point):
        for dir in cardinals:
            p = offset(point, dir)
            if self.occupied[p] == self.occupied[point] + 1:
                return dir
        return None
