from Zadanie1.solvers.solver import Solver
import numpy as np


class GreedyCycle(Solver):

    def solve(self):
        self.pick_initial_points()

        while len(self.cycleA) < 0.5 * self.dimension:
            new_point, position = self.find_point_to_add(self.cycleA)
            self.cycleA.insert(position, new_point)
            self.remove_from_free_points(new_point)

        while self.free_points.size > 0:
            new_point, position = self.find_point_to_add(self.cycleB)
            self.cycleB.insert(position, new_point)
            self.remove_from_free_points(new_point)

        print(self)
        return [self.cycleA, self.cycleB]

    def find_point_to_add(self, cycle):
        best_point = None
        best_distance = np.inf
        best_place = np.nan

        for i, node in enumerate(cycle):
            for potential_point in self.free_points:
                curr_distance = self.matrix[cycle[i-1]][node]  # existing edge
                new_distance = self.matrix[node][potential_point]
                new_distance += self.matrix[cycle[i-1]][potential_point]
                added_distance = new_distance - curr_distance  # cost of breaking edge and adding two new ones
                if added_distance < best_distance:
                    best_distance = added_distance
                    best_point = potential_point
                    best_place = i  # break existing edge, insert between last and current nodes

        return best_point, best_place
