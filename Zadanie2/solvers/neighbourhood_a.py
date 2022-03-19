from Zadanie2.solvers.neighbourhood import Neighbourhood
from Zadanie2.entity.edge import Edge
from Zadanie2.entity.move import Move
from Zadanie2.entity.move_type import MoveType
import numpy as np
import random


# Opcja z zamianą kolejności i między cyklami
class Neighbourhood_a(Neighbourhood):

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
        swap_moves = self.swap_between_cycles(0, 0, 1, move_type=MoveType.NODE_SWAP_BETWEEN_AB)
        cycleA_moves = self.get_moves_in_cycle(self.cycleA, 0, 0, 1, move_type=MoveType.NODE_SWAP_IN_A)
        cycleB_moves = self.get_moves_in_cycle(self.cycleB, 0, 0, 1, move_type=MoveType.NODE_SWAP_IN_B)

        # cycleA = np.asarray(cycleA_moves, dtype=int)
        # indA = np.argwhere(cycleA[:, 2] == (np.min(cycleA[:, 2])))[0, 0]
        # cycleB = np.asarray(cycleB_moves, dtype=int)
        # indB = np.argwhere(cycleB[:, 2] == (np.min(cycleB[:, 2])))[0, 0]
        # cycleS = np.asarray(swap_moves, dtype=int)
        # indS = np.argwhere(cycleS[:, 2] == (np.min(cycleS[:, 2])))[0, 0]
        # print(cycleA[indA, 2], cycleB[indB, 2], cycleS[indS, 2])

        # if cycleA[indA, 2] < cycleB[indB, 2] and cycleA[indA, 2] < cycleS[indS, 2]:
        #     return [cycleA[indA], 'cycleA']
        # elif cycleB[indB][2] < cycleS[indS][2]:
        #     return [cycleB[indB], 'cycleB']
        # else:
        #     return [cycleS[indS], 'swap']

        cycleA_deltas = np.asarray([move.delta for move in cycleA_moves], dtype=int)
        idA = np.argwhere(cycleA_deltas == np.min(cycleA_deltas))[0, 0]
        bestA = cycleA_moves[idA]

        cycleB_deltas = np.asarray([move.delta for move in cycleB_moves], dtype=int)
        idB = np.argwhere(cycleB_deltas == np.min(cycleB_deltas))[0, 0]
        bestB = cycleB_moves[idB]

        swap_deltas = np.asarray([move.delta for move in swap_moves], dtype=int)
        idS = np.argwhere(swap_deltas == np.min(swap_deltas))[0, 0]
        bestS = swap_moves[idS]

        # print(bestA, bestB, bestS)
        if bestA < bestB and bestA < bestB:
            return bestA
        elif bestB < bestS:
            return bestB
        else:
            return bestS

    def get_greedy_random_move(self):
        n_options = 5
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
            elif r % n_options == 3:
                i = random.randint(0, len(self.cycleA))
                j = random.randint(0, len(self.cycleB))
                step = random.choice([-1, 1])
                moves = np.asarray(self.get_edge_swaps_in_cycle(self.cycleA, i, j, step, MoveType.EDGE_SWAP_IN_A))
                deltas = np.asarray([move.delta for move in moves], dtype=int)
                if any(deltas < 0):
                    improvements = moves[deltas < 0]
                    first_best_move = improvements[0]
                    return first_best_move
            elif r % n_options == 4:
                i = random.randint(0, len(self.cycleA))
                j = random.randint(0, len(self.cycleB))
                step = random.choice([-1, 1])
                moves = np.asarray(self.get_edge_swaps_in_cycle(self.cycleB, i, j, step, MoveType.EDGE_SWAP_IN_B))
                deltas = np.asarray([move.delta for move in moves], dtype=int)
                if any(deltas < 0):
                    improvements = moves[deltas < 0]
                    first_best_move = improvements[0]
                    return first_best_move
            r += 1
        return None

    def calc_gain_of_edge_swap(self, e1: Edge, e2: Edge, cycle):
        old = e1.cost + e2.cost
        new = self.matrix[cycle[e1.v1]][cycle[e2.v1]] + self.matrix[cycle[e1.v2]][cycle[e2.v2]]
        return -old + new


    def get_edge_swaps_in_cycle(self, cycle, s1, s2, step, move_type):
        moves = []

        for i in range(s1, np.sign(step) * (s1 + len(self.cycleA)), step):
            for j in range(s2, (s2 + len(self.cycleB)) * np.sign(step), step):
                if i != j:
                    real_i = i % len(cycle)
                    buddy_i = (i + 1 * np.sign(step)) % len(cycle)
                    if real_i > buddy_i or (real_i == 0 and buddy_i == 49):
                        if not (real_i == 49 and buddy_i == 0):
                            real_i, buddy_i = buddy_i, real_i  # lower index should be first (unless 49--0), swap them
                    e1 = Edge(real_i, buddy_i, self.matrix[cycle[real_i]][cycle[buddy_i]])

                    real_j = j % len(cycle)
                    buddy_j = (j + 1 * np.sign(step)) % len(cycle)
                    if real_j > buddy_j or (real_j == 0 and buddy_j == 49):
                        if not (real_j == 49 and buddy_j == 0):
                            real_j, buddy_j = buddy_j, real_j  # lower index should be first (unless 49--0), swap them
                    e2 = Edge(real_j, buddy_j, self.matrix[cycle[real_j]][cycle[buddy_j]])

                    if e1 == e2:
                        continue  # somehow ended up with the same edge

                    if e1.v1 > e2.v1:
                        e1, e2 = e2, e1  # edges should be in the order of their appearance in cycle
                    moves.append(Move(e1, e2, self.calc_gain_of_edge_swap(e1, e2, cycle), move_type))
        return moves
