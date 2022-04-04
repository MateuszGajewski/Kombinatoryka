from Zadanie2.solvers.local_search_solver import LocalSearchSolver


class OptLocalSolver(LocalSearchSolver):

    def solve(self):

        self.neighbourhood.generate_all_moves()
        move = self.neighbourhood.get_best_move()
        i = 0
        self.neighbourhood.update_moves(move)

        """while i < 400:
            move = self.neighbourhood.get_best_move()
            # print(move)

            if move is not None and move.delta < 0:
                self.neighbourhood.make_move(move)
                self.neighbourhood.update_moves(move)
            else:
                # no further improvements
                break

            if not (len(self.neighbourhood.cycleA) == len(self.neighbourhood.cycleB) == 50):
                # something went wrong
                break

            i += 1"""
        return [self.neighbourhood.cycleA, self.neighbourhood.cycleB]

