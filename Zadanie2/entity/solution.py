import time
import numpy as np
from Zadanie2.solvers.local_search_solver import LocalSearchSolver
from Zadanie2.solvers.neighbourhood import Neighbourhood


class Solution:
    def __init__(self, solver_name: str, solver: LocalSearchSolver.__class__, move_types):
        self.solver_name = solver_name
        self.solver = solver
        self.move_types = move_types
        self.results = []
        self.times = []
        self.best_result = np.inf
        self.best_instance = None

    def __str__(self):
        return f"""
---- Solved with {self.solver_name} ----
> Results:
\tmean:\tmin:\tmax:
\t{np.min(self.results)};\t{np.max(self.results)};\t{np.mean(self.results)};

> Times:
\tmean:\tmin:\tmax:
\t{np.min(self.times)};\t{np.max(self.times)};\t{np.mean(self.times)};
"""

    def find(self, matrix, instance):
        start = time.time()

        neighbourhood = Neighbourhood(matrix, instance[0], instance[1], self.move_types)
        problem_solver = self.solver(neighbourhood)
        cycles = problem_solver.solve()

        stop = time.time()
        self.times.append(stop - start)
        self.calculate_result(matrix, cycles)
        print(self.solver_name, "done")

    def calculate_result(self, matrix, cycles):
        total = 0
        for cycle in cycles:
            for i, node in enumerate(cycle):
                total += matrix[cycle[i-1], node]

        if total < self.best_result:
            self.best_result = total
            self.best_instance = cycles

        self.results.append(total)
