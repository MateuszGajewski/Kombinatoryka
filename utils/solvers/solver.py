import array
from abc import ABC, abstractmethod
import numpy as np
import random


class Solver(ABC):

    def __init__(self, matrix: np.ndarray):
        self.cycleA = []
        self.cycleB = []
        self.dimension = len(matrix)
        self.free_points = np.array(range(0, self.dimension))
        self.matrix = matrix

    def __str__(self):
        return f"A ({len(self.cycleA)} nodes):\n {self.cycleA} \n\nB ({len(self.cycleB)} nodes):\n {self.cycleB} \n\n"

    @abstractmethod
    def solve(self):
        return NotImplementedError


