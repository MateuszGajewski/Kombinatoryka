from Zadanie1.solvers.solver import Solver_euclidean
import numpy as np


class RandomSolver(Solver_euclidean):

    def solve(self):
        n = self.dimension // 2
        points = np.random.permutation(self.free_points)
        self.cycleA = points[:n]
        self.cycleB = points[n:]
        return [self.cycleA, self.cycleB]

    def find_point_to_add(self, cycle):
        pass
