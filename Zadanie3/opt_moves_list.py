from Zadanie2.solvers.local_search_solver import LocalSearchSolver


class OptLocalSolver(LocalSearchSolver):

    def solve(self):

        self.neighbourhood.generate_all_moves()
        i = 0

        while i < 400:
            move = self.neighbourhood.get_best_move()
            # print(move)

            if move is not None and move.delta < 0:
                print(move)
                made = self.neighbourhood.validate_move_and_make(move)
                while made == -1:
                    move = self.neighbourhood.get_best_move()
                    if move is None or move.delta > 0:
                        break
                    made = self.neighbourhood.validate_move_and_make(move)

                self.neighbourhood.update_moves(move)
            else:
                # no further improvements
                break

            if not (len(self.neighbourhood.cycleA) == len(self.neighbourhood.cycleB) == 50):
                # something went wrong
                break

            i += 1
        return [self.neighbourhood.cycleA, self.neighbourhood.cycleB]

