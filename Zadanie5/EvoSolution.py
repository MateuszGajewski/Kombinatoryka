import numpy as np

from Zadanie5.EvolutionarySolver import EvolutionarySolver


class EvoSolution:
    def __init__(self, solver_name: str, ls_solver, neighbourhood, with_local_repair):
        self.solver_name = solver_name
        self.ls_solver = ls_solver
        self.neighbourhood_class = neighbourhood
        self.with_local_repair = with_local_repair
        self.results = []
        self.times = []
        self.best_result = np.inf
        self.best_instance = None

    def __str__(self):
        return f"""
---- Solved with {self.solver_name} ----
> Results:
\tmean:\t\tmin:\t\tmax:
\t{np.mean(self.results)}; \t{np.min(self.results)}; \t{np.max(self.results)};
> Times:
\tmean:\t\tmin:\t\tmax:
\t{np.mean(self.times)}; \t{np.min(self.times)}; \t{np.max(self.times)};
"""

    def find(self, matrix, time_limit):
        new_solver = EvolutionarySolver(matrix, time_limit, self.ls_solver,
                                        self.neighbourhood_class, self.with_local_repair)

        duration, cycles, result = new_solver.solve()
        duration = round(duration, 3)

        self.times.append(duration)
        self.results.append(result)
        if result < self.best_result:
            self.best_result = result
            self.best_instance = cycles

        print(f"{self.solver_name} done - {duration}s")
        return duration
