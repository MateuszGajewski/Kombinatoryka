import array
from abc import ABC, abstractmethod
import numpy as np
import random
from utils.solvers.solver import Solver


class Solver_euclidean(Solver):

    def __init__(self, matrix: np.ndarray, starting_point=None):
        self.cycleA = []
        self.cycleB = []
        self.dimension = len(matrix)
        self.free_points = np.array(range(0, self.dimension))
        self.matrix = matrix
        self.starting_point = starting_point

    def __str__(self):
        return f"A ({len(self.cycleA)} nodes):\n {self.cycleA} \n\nB ({len(self.cycleB)} nodes):\n {self.cycleB} \n\n"

    @abstractmethod
    def solve(self):
        self.pick_initial_points()
        return NotImplementedError

    @abstractmethod
    def find_point_to_add(self, cycle: array.array):
        return NotImplementedError

    def find_closest(self, point_id: int):
        # potentially broken
        row = self.matrix[point_id]
        available = np.take(row, self.free_points)
        return np.where(row == np.min(available[np.nonzero(available)]))[0][0]  # ugly

    def find_farthest(self, point_id: int):
        # potentially broken
        row = self.matrix[point_id]
        available = np.take(row, self.free_points)
        return np.where(row == np.max(available[np.nonzero(available)]))[0][0]  # ugly

    def pick_initial_points(self):
        chosen = self.starting_point if self.starting_point is not None else random.randrange(self.dimension)
        self.cycleA.append(chosen)
        self.remove_from_free_points(chosen)
        farthest = self.find_farthest(chosen)
        self.cycleB.append(farthest)
        self.remove_from_free_points(farthest)

    def remove_from_free_points(self, taken: int):
        self.free_points = np.delete(self.free_points, np.where(self.free_points == taken))

