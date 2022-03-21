import random

from Zadanie2.solvers.local_search_solver import LocalSearchSolver
from Zadanie2.entity.move_type import MoveType
from Zadanie2.entity.move import Move


class RandomLocalSearchSolver(LocalSearchSolver):

    def __init__(self, neighbourhoodA, neighbourhoodB):
        self.neighbourhoodA = neighbourhoodA
        self.neighbourhoodB = neighbourhoodB

    def get_random_move(self):
        type_ = random.randint(1, 5)

        if type_ == 1:
            i = random.randint(0, len(self.neighbourhoodA.cycleA) - 1)
            j = random.randint(0, len(self.neighbourhoodA.cycleA) - 1)
            delta = self.neighbourhoodA.calc_swap_inside(i, j, self.neighbourhoodA.cycleA)
        elif type_ == 2:
            cycleA_moves = self.neighbourhoodB.get_moves_in_cycle(self.neighbourhoodA.cycleA, 0, 0, 1,
                                                                  move_type=MoveType.EDGE_SWAP_IN_A)
            move = random.choice(cycleA_moves)
            return move
        elif type_ == 3:
            i = random.randint(0, len(self.neighbourhoodA.cycleB) - 1)
            j = random.randint(0, len(self.neighbourhoodA.cycleB) - 1)
            delta = self.neighbourhoodA.calc_swap_inside(i, j, self.neighbourhoodA.cycleB)

        elif type_ == 4:
            cycleB_moves = self.neighbourhoodB.get_moves_in_cycle(self.neighbourhoodA.cycleB, 0, 0, 1,
                                                                  move_type=MoveType.EDGE_SWAP_IN_B)
            move = random.choice(cycleB_moves)
            return move
        else:
            i = random.randint(0, len(self.neighbourhoodA.cycleA) - 1)
            j = random.randint(0, len(self.neighbourhoodA.cycleB) - 1)
            delta = self.neighbourhoodA.calc_swap_between(i, j)

        move = Move(i, j, delta, MoveType(type_))
        return move

    def solve(self):
        best_cycle = [self.neighbourhoodA.cycleA.copy(),
                      self.neighbourhoodA.cycleB.copy()]
        curr_val = 0
        curr_min = 0
        i = 0
        while i < 500:
            move = self.get_random_move()
            # print(move.s1.v1, move.s2, move.type)
            self.neighbourhoodA.make_move(move)
            curr_val += move.delta
            if curr_val < curr_min:
                curr_min = curr_val
                best_cycle = [self.neighbourhoodA.cycleA.copy(),
                              self.neighbourhoodA.cycleB.copy()]

            i += 1
        return best_cycle
