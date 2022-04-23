from time import time
from copy import deepcopy
import numpy as np

from Zadanie2.entity.move_type import MoveType
from Zadanie2.solvers.local_search_solver import LocalSearchSolver
from Zadanie2.solvers.neighbourhood import Neighbourhood


class ILSSolver:
    def __init__(self, matrix, time_limit, ls_solver, neighbourhood, perturbation, with_local_repair):
        self.matrix = matrix
        self.dimension = len(matrix)
        self.time_limit = time_limit
        self.ls_solver = ls_solver
        self.neighbourhood_class = neighbourhood
        self.perturbation = perturbation
        self.with_local_repair = with_local_repair

    def solve(self, initial_instance):
        start = time()
        move_types = [mt for mt in MoveType]
        neighbourhood = self.neighbourhood_class(self.matrix, initial_instance[0], initial_instance[1], move_types)
        problem_solver = self.ls_solver(neighbourhood)

        best_cycles = problem_solver.solve()
        best_result = self.calculate_result(best_cycles)

        while time() - start < self.time_limit:
            cycles = deepcopy(best_cycles)
            cycles = self.perturbation(cycles, self.matrix)

            if self.with_local_repair is True:
                neighbourhood = Neighbourhood(self.matrix, cycles[0], cycles[1], move_types)
                problem_solver = self.ls_solver(neighbourhood)
                cycles = problem_solver.solve()

            new_result = self.calculate_result(best_cycles)
            if new_result < best_result:
                best_cycles = cycles
                best_result = new_result

        return time() - start, best_cycles, best_result

    def calculate_result(self, cycles):
        total = 0
        for cycle in cycles:
            for i, node in enumerate(cycle):
                total += self.matrix[cycle[i-1], node]

        if len(cycles[0]) != len(cycles[1]):
            return np.inf

        return total
