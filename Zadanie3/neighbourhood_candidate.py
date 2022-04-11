from abc import ABC, abstractmethod

import numpy as np
import random
from Zadanie2.entity.edge import Edge
from Zadanie2.entity.move import Move
from Zadanie2.entity.move_type import MoveType
from Zadanie2.solvers.neighbourhood import Neighbourhood


def swap_edges(cycle, e1, e2):
    if (e2.v1 == len(cycle)-1) and (e2.v2 == 0):
        slice1 = cycle[:e1.v2]
        slice2 = cycle[e1.v2:e2.v1 + 1]
        slice2.reverse()
        new_order = slice1 + slice2
    else:
        slice1 = cycle[:e1.v2]
        slice2 = cycle[e1.v2:e2.v2]
        slice2.reverse()
        slice3 = cycle[e2.v2:]
        new_order = slice1 + slice2 + slice3
    return new_order


class NeighbourhoodCandidate(Neighbourhood):

    def __init__(self, matrix, cycleA, cycleB, available_moves, k=10):
        self.matrix = matrix
        self.cycleA = cycleA
        self.cycleB = cycleB
        self.available_moves = available_moves
        self.k_closest_ids = self.get_k_closest_points(k)

    def make_move(self, move):
        if move.type == MoveType.NODE_SWAP_IN_A:
            self.cycleA[move.s1], self.cycleA[move.s2] = self.cycleA[move.s2], self.cycleA[move.s1]

        elif move.type == MoveType.NODE_SWAP_IN_B:
            self.cycleB[move.s1], self.cycleB[move.s2] = self.cycleB[move.s2], self.cycleB[move.s1]

        elif move.type == MoveType.NODE_SWAP_BETWEEN_AB:
            self.cycleA[move.s1], self.cycleB[move.s2] = self.cycleB[move.s2], self.cycleA[move.s1]

        elif move.type == MoveType.EDGE_SWAP_IN_A:
            self.cycleA = swap_edges(self.cycleA, move.s1, move.s2)

        elif move.type == MoveType.EDGE_SWAP_IN_B:
            self.cycleB = swap_edges(self.cycleB, move.s1, move.s2)

        else:
            print("Outstanding move, but it's not implemented")

    def get_best_move(self):
        moves = self.get_candidate_moves()
        if len(moves) == 0:
            return None  # list of moves was empty
        deltas = np.asarray([move.delta for move in moves], dtype=int)
        best_id = np.argwhere(deltas == np.min(deltas))[0, 0]
        return moves[best_id]

    def get_k_closest_points(self, k):
        # return matrix of size [Nxk+1] with k closest points for each of the N nodes
        # taking k+1 elements, because '0' will also be present in the result and we need to skip it
        closest = np.argpartition(self.matrix, k+1, axis=1)[:, :k+1]
        return closest

    def get_candidate_moves(self):
        solutions = []
        # k_closest_ids = self.get_k_closest_points()

        for i in range(len(self.matrix)):
            for j in self.k_closest_ids[i]:
                if i != j:
                    move_type = self.check_move_type(i, j)
                    (cyc_i, pos_i) = self.check_position_in_cycle(i)
                    (cyc_j, pos_j) = self.check_position_in_cycle(j)
                    if pos_i is None or pos_j is None:
                        continue

                    if move_type == MoveType.EDGE_SWAP_IN_A:
                        moves = self.get_edge_swaps_in_cycle(self.cycleA, pos_i, pos_j, step=None, move_type=move_type)
                    elif move_type == MoveType.EDGE_SWAP_IN_B:
                        moves = self.get_edge_swaps_in_cycle(self.cycleB, pos_i, pos_j, step=None, move_type=move_type)
                    else:  # move_type == MoveType.NODE_SWAP_BETWEEN_AB:
                        if cyc_i == 'A':
                            moves = [Move(pos_i, pos_j, self.calc_swap_between(pos_i, pos_j), move_type)]
                        else:  # cyc_i = 'B':
                            moves = [Move(pos_j, pos_i, self.calc_swap_between(pos_i, pos_j), move_type)]

                    solutions = np.concatenate((solutions, moves))

        return solutions

    def get_edge_swaps_in_cycle(self, cycle, real_i, real_j, step, move_type):
        # solution = [Move(który, z którym, jaka zmiana, jaki typ)]
        solutions = []
        last_idx = len(cycle)-1

        for direction in [-1, 1]:

            buddy_i = (real_i + direction) % len(cycle)
            if real_i > buddy_i or (real_i == 0 and buddy_i == last_idx):
                if not (real_i == last_idx and buddy_i == 0):
                    real_i, buddy_i = buddy_i, real_i  # lower index should be first (unless 49--0), swap them
            e1 = Edge(real_i, buddy_i, self.matrix[cycle[real_i]][cycle[buddy_i]])

            buddy_j = (real_j - direction) % len(cycle)
            if real_j > buddy_j or (real_j == 0 and buddy_j == last_idx):
                if not (real_j == last_idx and buddy_j == 0):
                    real_j, buddy_j = buddy_j, real_j  # lower index should be first (unless 49--0), swap them
            e2 = Edge(real_j, buddy_j, self.matrix[cycle[real_j]][cycle[buddy_j]])

            if e1 == e2:
                continue  # somehow ended up with the same edge

            if e1.v1 > e2.v1:
                e1, e2 = e2, e1  # edges should be in the order of their appearance in cycle

            delta = self.calc_edge_swap_inside(e1, e2, cycle)
            solutions.append(Move(e1, e2, delta, move_type))

        return solutions

    def check_position_in_cycle(self, node):
        if node in self.cycleA:
            cyc = 'A'
            idx = np.argwhere(np.array(self.cycleA) == node).flatten()
        else:
            cyc = 'B'
            idx = np.argwhere(np.array(self.cycleB) == node).flatten()
        _id = idx[0] if len(idx) == 1 else None
        return [cyc, _id]

    def check_move_type(self, node_i, node_j):
        # check which cycle nodes belong to and return which MoveType can be performed between them
        if node_i in self.cycleA and node_j in self.cycleA:
            return MoveType.EDGE_SWAP_IN_A
        if node_i in self.cycleB and node_j in self.cycleB:
            return MoveType.EDGE_SWAP_IN_B
        else:
            return MoveType.NODE_SWAP_BETWEEN_AB
