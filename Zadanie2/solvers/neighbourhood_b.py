from Zadanie2.solvers.neighbourhood import Neighbourhood
from Zadanie2.entity.edge import Edge
from Zadanie2.entity.move import Move
from Zadanie2.entity.move_type import MoveType
import numpy as np
import random


# Opcja z zamianą krawędzi i wymianą wierzchołkami między cyklami
class NeighbourhoodB(Neighbourhood):

    def __init__(self, matrix, cycleA, cycleB):
        super().__init__(matrix, cycleA, cycleB)
        self.available_moves = [MoveType.EDGE_SWAP_IN_A,
                                MoveType.EDGE_SWAP_IN_B,
                                MoveType.NODE_SWAP_BETWEEN_AB]

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
