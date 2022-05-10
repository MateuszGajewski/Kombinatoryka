import numpy as np


class PartiallyGreedyCycle:
    # Parts of the cycles are already built, but there are some free_points we'd like to use
    def __init__(self, matrix: np.ndarray, cycles, free_points):
        self.matrix = matrix
        self.dimension = len(matrix)
        self.cycles = cycles
        self.free_points = free_points

    def solve(self):
        cycle_id = 0
        while len(self.free_points) > 0:  # while there are free points
            new_point, new_position, pid = self.find_point_to_add(self.cycles[cycle_id])
            self.cycles[cycle_id].insert(new_position, new_point)
            del self.free_points[pid]
            cycle_id = 1 - cycle_id

        return self.cycles

    def find_point_to_add(self, cycle):
        best_point = None
        best_distance = np.inf
        best_place = np.nan
        best_id = None

        for i, node in enumerate(cycle):
            for pid, potential_point in enumerate(self.free_points):
                curr_distance = self.matrix[cycle[i-1]][node]  # existing edge
                new_distance = self.matrix[node][potential_point]
                new_distance += self.matrix[cycle[i-1]][potential_point]
                added_distance = new_distance - curr_distance  # cost of breaking edge and adding two new ones
                if added_distance < best_distance:
                    best_distance = added_distance
                    best_point = potential_point
                    best_place = i  # break existing edge, insert between last and current nodes
                    best_id = pid

        return best_point, best_place, best_id

    def remove_from_free_points(self, taken: int):
        self.free_points = np.delete(self.free_points, np.where(self.free_points == taken))
