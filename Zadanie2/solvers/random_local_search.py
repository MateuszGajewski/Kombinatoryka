from Zadanie2.solvers.local_search_solver import LocalSearchSolver


class RandomLocalSearchSolver(LocalSearchSolver):

    def __init__(self, neighbourhood):
        self.neighbourhood = neighbourhood

    def solve(self):
        pass
