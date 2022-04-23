from Zadanie2.solvers.local_search_solver import LocalSearchSolver

class MLSSolver(LocalSearchSolver):

    def solve(self):
        self.neighbourhood.generate_all_moves()

        i = 0
        while i < 100:
            move = self.neighbourhood.get_best_move()
            # print(move)

            if move is not None and move.delta < 0:
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

            i += 1
            if i % 50 == 0:
                print(f"Memory #{i}")

        return [self.neighbourhood.cycleA, self.neighbourhood.cycleB]