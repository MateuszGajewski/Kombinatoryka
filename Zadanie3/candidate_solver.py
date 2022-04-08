from Zadanie2.solvers.local_search_solver import LocalSearchSolver


class CandidateSolver(LocalSearchSolver):

    def solve(self):
        i = 0
        while i < 100:
            move = self.neighbourhood.get_best_move()
            print(move)

            if move is not None and move.delta < 0:
                self.neighbourhood.make_move(move)

            else:
                break
            i += 1
        return [self.neighbourhood.cycleA, self.neighbourhood.cycleB]

