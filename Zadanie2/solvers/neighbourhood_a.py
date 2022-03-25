from Zadanie2.solvers.neighbourhood import Neighbourhood
from Zadanie2.entity.edge import Edge
from Zadanie2.entity.move import Move
from Zadanie2.entity.move_type import MoveType
import numpy as np
import random


# Opcja z zamianą kolejności i między cyklami
class NeighbourhoodA(Neighbourhood):

    def __init__(self, matrix, cycleA, cycleB):
        super().__init__(matrix, cycleA, cycleB)
        self.available_moves = [MoveType.NODE_SWAP_IN_A,
                                MoveType.NODE_SWAP_IN_B,
                                MoveType.NODE_SWAP_BETWEEN_AB]

    def calc_swap_inside(self, i, j, cycle):
        if i == j:
            return 0

        i_0, i_1, i_2 = cycle[(i - 1) % len(cycle)], cycle[i], cycle[(i + 1) % len(cycle)]
        j_0, j_1, j_2 = cycle[(j - 1) % len(cycle)], cycle[j], cycle[(j + 1) % len(cycle)]

        if (i, j) == (0, len(cycle) - 1):
            old = self.matrix[i_1, i_2] + self.matrix[j_1, j_0]
            new = self.matrix[j_1, i_2] + self.matrix[i_1, j_0]
            return -old + new

        elif (i, j) == (len(cycle) - 1, 0):
            old = self.matrix[j_1, j_2] + self.matrix[i_1, i_0]
            new = self.matrix[i_1, j_2] + self.matrix[j_1, i_0]
            return -old + new

        elif abs(i - j) != 1:
            """ \^/
                /v\ 
            """
            old = self.matrix[i_0, i_1] + self.matrix[i_1, i_2] + \
                  self.matrix[j_0, j_1] + self.matrix[j_1, j_2]
            new = self.matrix[i_0, j_1] + self.matrix[j_1, i_2] + \
                  self.matrix[j_0, i_1] + self.matrix[i_1, j_2]
            return -old + new

        elif i < j:
            old = self.matrix[i_0, i_1] + self.matrix[j_1, j_2]
            new = self.matrix[i_0, j_1] + self.matrix[i_1, j_2]
            return -old + new

        else:  # i > j
            old = self.matrix[j_0, j_1] + self.matrix[i_1, i_2]
            new = self.matrix[j_0, i_1] + self.matrix[j_1, i_2]
            return -old + new

    def get_moves_in_cycle(self, cycle, s1, s2, step, move_type):
        # solution = [Move(który, z którym, jaka zmiana)]
        solutions = []
        # w ramach cyklu

        for i in range(s1, np.sign(step) * (s1 + len(self.cycleA)), step):
            for j in range(s2, (s2 + len(self.cycleB)) * np.sign(step), step):
                if i != j:
                    real_i = i % len(cycle)
                    real_j = j % len(cycle)
                    solutions.append(Move(real_i, real_j, self.calc_swap_inside(real_i, real_j, cycle), move_type))

        return solutions

    def calc_swap_between(self, i, j):
        old = self.matrix[self.cycleA[i]][self.cycleA[((i - 1) % len(self.cycleA))]] + \
              self.matrix[self.cycleA[i]][self.cycleA[(i + 1) % len(self.cycleA)]] + \
              self.matrix[self.cycleB[j]][self.cycleB[(j - 1) % len(self.cycleB)]] + \
              self.matrix[self.cycleB[j]][self.cycleB[(j + 1) % len(self.cycleB)]]

        new = self.matrix[self.cycleB[j]][self.cycleA[((i - 1) % len(self.cycleA))]] + \
              self.matrix[self.cycleB[j]][self.cycleA[(i + 1) % len(self.cycleA)]] + \
              self.matrix[self.cycleA[i]][self.cycleB[(j - 1) % len(self.cycleB)]] + \
              self.matrix[self.cycleA[i]][self.cycleB[(j + 1) % len(self.cycleB)]]
        return -old + new

    def swap_between_cycles(self, s1, s2, step, move_type):
        solutions = []

        for i in range(s1, np.sign(step) * (s1 + len(self.cycleA)), step):
            for j in range(s2, (s2 + len(self.cycleB)) * np.sign(step), step):
                real_i = i % len(self.cycleA)
                real_j = j % len(self.cycleB)
                solutions.append(Move(real_i, real_j, self.calc_swap_between(real_i, real_j), move_type))
        return solutions

    def get_moves_of_type(self, move_type, i=0, j=0, step=1):
        if move_type == MoveType.NODE_SWAP_BETWEEN_AB:
            return self.swap_between_cycles(i, j, step, move_type)
        elif move_type in [MoveType.NODE_SWAP_IN_A, MoveType.EDGE_SWAP_IN_A]:
            return self.get_moves_in_cycle(self.cycleA, i, j, step, move_type)
        elif move_type in [MoveType.NODE_SWAP_IN_B, MoveType.EDGE_SWAP_IN_B]:
            return self.get_moves_in_cycle(self.cycleB, i, j, step, move_type)
        else:
            return []

    def get_best_move(self):
        best_move = Move(None, None, np.inf, None)
        for move_type in self.available_moves:
            moves = self.get_moves_of_type(move_type)
            if not moves:
                continue  # list of moves was empty
            deltas = np.asarray([move.delta for move in moves], dtype=int)
            ind = np.argwhere(deltas == np.min(deltas))[0, 0]
            if np.min(deltas) < best_move.delta:
                best_move = moves[ind]
        return best_move

    def get_greedy_random_move(self):
        shuffled_move_types = np.random.permutation(self.available_moves)
        for move_type in shuffled_move_types:
            i = random.randint(0, len(self.cycleA))
            j = random.randint(0, len(self.cycleB))
            step = random.choice([-1, 1])
            moves = np.asarray(self.get_moves_of_type(move_type, i, j, step))
            deltas = np.asarray([move.delta for move in moves], dtype=int)
            if any(deltas < 0):
                improvements = moves[deltas < 0]
                first_best_move = improvements[0]
                return first_best_move
        # if all available_moves were considered, but no improvement was found, return None
        return None
