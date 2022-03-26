import random

from Zadanie2.solvers.local_search_solver import LocalSearchSolver


class RandomLocalSearchSolver(LocalSearchSolver):

    def get_random_move(self):
        random_move_type = random.choice(self.neighbourhood.available_moves)
        i = random.randint(0, len(self.neighbourhood.cycleA)-1)
        j = random.randint(0, len(self.neighbourhood.cycleA)-1)
        step = random.choice([-1, 1])
        moves = self.neighbourhood.get_moves_of_type(random_move_type, i, j, step)
        random_move = random.choice(moves)

        return random_move

    def solve(self):
        best_cycle = [self.neighbourhood.cycleA.copy(),
                      self.neighbourhood.cycleB.copy()]
        curr_val = 0
        curr_min = 0
        i = 0
        while i < 200:
            move = self.get_random_move()
            # print(move.s1.v1, move.s2, move.type)
            self.neighbourhood.make_move(move)
            curr_val += move.delta
            if curr_val < curr_min:
                # print(f"Random #{i}: improved {curr_min} -> {curr_val}")
                curr_min = curr_val
                best_cycle = [self.neighbourhood.cycleA.copy(),
                              self.neighbourhood.cycleB.copy()]
            i += 1
            if i % 50 == 0:
                print(f"Random #{i}")

        return best_cycle
