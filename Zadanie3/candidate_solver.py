from Zadanie2.solvers.local_search_solver import LocalSearchSolver


class CandidateSolver(LocalSearchSolver):

    def solve(self):
        i = 0
        while i < 4000:
            move = self.neighbourhood.get_best_move()
            print(move)

            if move is not None and move.delta < 0:
                self.neighbourhood.make_move(move)

            else:
                break
            i += 1
        print(len(self.neighbourhood.cycleA), len(self.neighbourhood.cycleB))
        return [self.neighbourhood.cycleA, self.neighbourhood.cycleB]

