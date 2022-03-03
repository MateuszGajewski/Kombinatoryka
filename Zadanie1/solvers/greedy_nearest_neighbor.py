import math

from Zadanie1.solvers.solver import Solver
import numpy as np
import random


class GreedyNearestNeighbor(Solver):
    matrix = 0
    cycle1 = 0
    cycle2 = 0
    visited = 0

    def __init__(self, array):
        self.matrix = array
        self.cycle1 = np.arange(np.ceil(self.matrix.shape[0] / 2), dtype=int)
        self.cycle2 = np.arange(np.floor(self.matrix.shape[0] / 2))
        self.visited = np.zeros([self.matrix.shape[0], 1])

    def find_nearest_neighbour(self, index):
        minimum = math.inf
        min_index = None
        for i, j in zip(self.matrix[index][:], range(0, self.matrix.shape[0])):
            if i < minimum and j != index and self.visited[j] == 0:
                minimum = i
                min_index = j
        return minimum, min_index

    def solve(self):
        index = 0
        self.cycle1[0] = random.randint(0, self.matrix.shape[0])
        while index < np.ceil(self.matrix.shape[0] / 2) -1:
            length, nearest = self.find_nearest_neighbour(self.cycle1[index])
            index += 1
            self.cycle1[index] = nearest
            self.visited[nearest] = 1
        return self.cycle1
