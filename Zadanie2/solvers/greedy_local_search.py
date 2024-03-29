from Zadanie2.solvers.local_search_solver import LocalSearchSolver


class GreedyLocalSolver(LocalSearchSolver):

    def solve(self):
        i = 0
        while i < 400:
            move = self.neighbourhood.get_greedy_random_move()
            # print(move)

            if move is not None and move.delta < 0:
                self.neighbourhood.make_move(move)
            else:
                # no further improvements
                break

            if not (len(self.neighbourhood.cycleA) == len(self.neighbourhood.cycleB) == 50):
                # something went wrong
                break

            i += 1
        return [self.neighbourhood.cycleA, self.neighbourhood.cycleB]



