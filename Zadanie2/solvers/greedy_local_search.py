from Zadanie2.solvers.local_search_solver import LocalSearchSolver


class GreedyLocalSolver(LocalSearchSolver):

    def solve(self):
        print(self.neighbourhood.matrix)
        i = 0
        while i < 400:
            move = self.neighbourhood.get_greedy_random_move()
            print(move)

            if move is not None and move.delta < 0:
                self.neighbourhood.make_move(move)

            else:
                break

            i += 1
        return [self.neighbourhood.cycleA, self.neighbourhood.cycleB]



