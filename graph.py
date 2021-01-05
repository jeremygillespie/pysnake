from collections import namedtuple
import numpy as np

Point = namedtuple('Point', 'x y')
Direc = namedtuple('Direc', 'dx dy')

north = Direc(0, 1)
south = Direc(0, -1)
east = Direc(1, 0)
west = Direc(-1, 0)
cardinals = [north, south, east, west]


def offset(point, direc):
    return Point(point.x + direc.dx, point.y + direc.dy)


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
        for direc in cardinals:
            new_point = offset(point, direc)
            if self.occupied[new_point] == self.occupied[point] + 1:
                return direc
        return None
