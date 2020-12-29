import numpy as np


class Graph:
    def __init__(self, w, h):
        self.occupied = np.zeros((w, h))
        self.head = (0, 0)
