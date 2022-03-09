from Zadanie1.solvers.solver import Solver
import numpy as np


class GreedyNearestNeighbor(Solver):

    def solve(self):
        self.pick_initial_points()

        while len(self.cycleA) < 0.5 * self.dimension:
            new_point, position = self.find_point_to_add(self.cycleA)
            self.cycleA.insert(position, new_point)
            self.remove_from_free_points(new_point)
            if self.free_points.size > 0:
                new_point, position = self.find_point_to_add(self.cycleB)
                self.cycleB.insert(position, new_point)
                self.remove_from_free_points(new_point)

        return [self.cycleA, self.cycleB]

    def find_point_to_add(self, cycle):
        closest = None
        best_distance = np.inf
        best_place = np.nan

        for i, node in enumerate(cycle):
            for potential_point in self.free_points:
                distance = self.matrix[potential_point][node]
                if distance < best_distance:
                    closest = potential_point
                    best_distance = distance
                    best_place = i+1  # insert behind current node

        return closest, best_place
