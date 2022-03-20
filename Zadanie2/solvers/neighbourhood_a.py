from Zadanie2.solvers.neighbourhood import Neighbourhood
from Zadanie2.entity.edge import Edge
from Zadanie2.entity.move import Move
from Zadanie2.entity.move_type import MoveType
import numpy as np
import random


# Opcja z zamianą kolejności i między cyklami
class NeighbourhoodA(Neighbourhood):

    def calc_swap_inside(self, i, j, cycle):
        delta = 0

        if (i == 0 and j == 49) or (i == 49 and j == 0):
            if i == 0 and j == 49:
                old = self.matrix[cycle[i]][cycle[(i + 1) % len(cycle)]] + \
                      self.matrix[cycle[j]][cycle[(j - 1) % len(cycle)]]
                new = self.matrix[cycle[j]][cycle[((i + 1) % len(cycle))]] + \
                      self.matrix[cycle[i]][cycle[(j - 1) % len(cycle)]]
                delta = -old + new

            elif i == 49 and j == 0:
                # print(i, j)

                old = self.matrix[cycle[j]][cycle[(j + 1) % len(cycle)]] + \
                      self.matrix[cycle[i]][cycle[(i - 1) % len(cycle)]]
                new = self.matrix[cycle[i]][cycle[(j + 1) % len(cycle)]] + \
                      self.matrix[cycle[j]][cycle[(i - 1) % len(cycle)]]
                delta = -old + new
            return delta
        elif i != j and abs(i - j) != 1:
            # print(i, j)

            old = self.matrix[cycle[i]][cycle[(i - 1) % len(cycle)]] + \
                  self.matrix[cycle[i]][cycle[(i + 1) % len(cycle)]] + \
                  self.matrix[cycle[j]][cycle[(j - 1) % len(cycle)]] + \
                  self.matrix[cycle[j]][cycle[(j + 1) % len(cycle)]]

            new = self.matrix[cycle[j]][cycle[(i - 1) % len(cycle)]] + \
                  self.matrix[cycle[j]][cycle[(i + 1) % len(cycle)]] + \
                  self.matrix[cycle[i]][cycle[(j - 1) % len(cycle)]] + \
                  self.matrix[cycle[i]][cycle[(j + 1) % len(cycle)]]
            delta = -old + new
            return delta
        elif i != j:
            if i < j:
                # print(i, j)
                old = self.matrix[cycle[i]][cycle[(i - 1) % len(cycle)]] + \
                      self.matrix[cycle[j]][cycle[(j + 1) % len(cycle)]]
                new = self.matrix[cycle[j]][cycle[(i - 1) % len(cycle)]] + \
                      self.matrix[cycle[i]][cycle[(j + 1) % len(cycle)]]

            else:
                # print(i, j)
                old = self.matrix[cycle[j]][cycle[(j - 1) % len(cycle)]] + \
                      self.matrix[cycle[i]][cycle[(i + 1) % len(cycle)]]
                new = self.matrix[cycle[i]][cycle[(j - 1) % len(cycle)]] + \
                      self.matrix[cycle[j]][cycle[(i + 1) % len(cycle)]]
            delta = -old + new
        return delta

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

    def get_best_move(self):
        # wymiana wierzchołkami pomiędzy cyklami
        swap_moves = self.swap_between_cycles(0, 0, 1, move_type=MoveType.NODE_SWAP_BETWEEN_AB)
        # zamiany wierzchołków w poszczególnych cyklach
        cycleA_moves = self.get_moves_in_cycle(self.cycleA, 0, 0, 1, move_type=MoveType.NODE_SWAP_IN_A)
        cycleB_moves = self.get_moves_in_cycle(self.cycleB, 0, 0, 1, move_type=MoveType.NODE_SWAP_IN_B)

        cycleA_deltas = np.asarray([move.delta for move in cycleA_moves], dtype=int)
        idA = np.argwhere(cycleA_deltas == np.min(cycleA_deltas))[0, 0]
        bestA = cycleA_moves[idA]

        cycleB_deltas = np.asarray([move.delta for move in cycleB_moves], dtype=int)
        idB = np.argwhere(cycleB_deltas == np.min(cycleB_deltas))[0, 0]
        bestB = cycleB_moves[idB]

        swap_deltas = np.asarray([move.delta for move in swap_moves], dtype=int)
        idS = np.argwhere(swap_deltas == np.min(swap_deltas))[0, 0]
        bestS = swap_moves[idS]

        if bestA < bestB and bestA < bestB:
            return bestA
        elif bestB < bestS:
            return bestB
        else:
            return bestS

    def get_greedy_random_move(self):
        n_options = 3
        r = random.randint(0, n_options)
        for _ in range(0, n_options):
            if r % n_options == 0:
                i = random.randint(0, len(self.cycleA))
                j = random.randint(0, len(self.cycleB))
                step = random.choice([-1, 1])
                moves = np.asarray(self.swap_between_cycles(i, j, step, move_type=MoveType.NODE_SWAP_BETWEEN_AB))
                deltas = np.asarray([move.delta for move in moves], dtype=int)
                if any(deltas < 0):
                    improvements = moves[deltas < 0]
                    first_best_move = improvements[0]
                    return first_best_move
            elif r % n_options == 1:
                i = random.randint(0, len(self.cycleA))
                j = random.randint(0, len(self.cycleA))
                step = random.choice([-1, 1])
                moves = np.asarray(self.get_moves_in_cycle(self.cycleA, i, j, step, move_type=MoveType.NODE_SWAP_IN_A))
                deltas = np.asarray([move.delta for move in moves], dtype=int)
                if any(deltas < 0):
                    improvements = moves[deltas < 0]
                    first_best_move = improvements[0]
                    return first_best_move
            elif r % n_options == 2:
                i = random.randint(0, len(self.cycleB))
                j = random.randint(0, len(self.cycleB))
                step = random.choice([-1, 1])
                moves = np.asarray(self.get_moves_in_cycle(self.cycleB, i, j, step, move_type=MoveType.NODE_SWAP_IN_B))
                deltas = np.asarray([move.delta for move in moves], dtype=int)
                if any(deltas < 0):
                    improvements = moves[deltas < 0]
                    first_best_move = improvements[0]
                    return first_best_move
            r += 1
        return None
