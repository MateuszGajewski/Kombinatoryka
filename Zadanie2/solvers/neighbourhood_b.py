from Zadanie2.solvers.neighbourhood import Neighbourhood
from Zadanie2.entity.edge import Edge
from Zadanie2.entity.move import Move
from Zadanie2.entity.move_type import MoveType
import numpy as np
import random


# Opcja z zamianą krawędzi i wymianą wierzchołkami między cyklami
class NeighbourhoodB(Neighbourhood):

    def calc_swap_inside(self, e1: Edge, e2: Edge, cycle):
        old = e1.cost + e2.cost
        new = self.matrix[cycle[e1.v1]][cycle[e2.v1]] + self.matrix[cycle[e1.v2]][cycle[e2.v2]]
        return -old + new

    def get_moves_in_cycle(self, cycle, s1, s2, step, move_type):
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
                    moves.append(Move(e1, e2, self.calc_swap_inside(e1, e2, cycle), move_type))
        return moves

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
        # zamiany krawędzi w poszczególnych cyklach
        cycleA_moves = self.get_moves_in_cycle(self.cycleA, 0, 0, 1, move_type=MoveType.EDGE_SWAP_IN_A)
        cycleB_moves = self.get_moves_in_cycle(self.cycleB, 0, 0, 1, move_type=MoveType.EDGE_SWAP_IN_B)

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
                j = random.randint(0, len(self.cycleB))
                step = random.choice([-1, 1])
                moves = np.asarray(self.get_moves_in_cycle(self.cycleA, i, j, step, MoveType.EDGE_SWAP_IN_A))
                deltas = np.asarray([move.delta for move in moves], dtype=int)
                if any(deltas < 0):
                    improvements = moves[deltas < 0]
                    first_best_move = improvements[0]
                    return first_best_move
            elif r % n_options == 2:
                i = random.randint(0, len(self.cycleA))
                j = random.randint(0, len(self.cycleB))
                step = random.choice([-1, 1])
                moves = np.asarray(self.get_moves_in_cycle(self.cycleB, i, j, step, MoveType.EDGE_SWAP_IN_B))
                deltas = np.asarray([move.delta for move in moves], dtype=int)
                if any(deltas < 0):
                    improvements = moves[deltas < 0]
                    first_best_move = improvements[0]
                    return first_best_move
            r += 1
        return None
