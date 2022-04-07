from abc import ABC, abstractmethod

import numpy as np
import random
from Zadanie2.entity.edge import Edge
from Zadanie2.entity.move import Move
from Zadanie2.entity.move_type import MoveType


def swap_edges(cycle, e1, e2):
    if (e2.v1 == len(cycle) - 1) and (e2.v2 == 0):
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

def was_edge_swap_in_range(move, _range):
    return [move.s1.v1 in _range, move.s2.v1 in _range]  # [True/False, True/False]


class Neighbourhood_opt(ABC):

    def __init__(self, matrix, cycleA, cycleB, available_moves):
        self.matrix = matrix
        self.cycleA = cycleA
        self.cycleB = cycleB
        self.available_moves = available_moves
        self.best_moves = None

    def validate_move_and_make(self, move):
        made = 0
        if move.type == MoveType.NODE_SWAP_IN_A:
            #print("m", move, move.s1)

            if move.delta == self.calc_node_swap_inside(move.s1, move.s2, self.cycleA):
                self.make_move(move)
            else:
                made = -1
        elif move.type == MoveType.NODE_SWAP_IN_B:
            if move.delta == self.calc_node_swap_inside(move.s1, move.s2, self.cycleB):
                self.make_move(move)
            else:
                made = -1
        elif move.type == MoveType.NODE_SWAP_BETWEEN_AB:
            if move.delta == self.calc_swap_between(move.s1, move.s2):
                self.make_move(move)
            else:
                made = -1
        elif move.type == MoveType.EDGE_SWAP_IN_A:
            if move.delta == self.calc_edge_swap_inside(move.s1, move.s2, self.cycleA):
                self.make_move(move)
            else:
                made = -1
        elif move.type == MoveType.EDGE_SWAP_IN_B:
            if move.delta == self.calc_edge_swap_inside(move.s1, move.s2, self.cycleB):
                self.make_move(move)
            else:
                made = -1
        self.best_moves.pop(0)
        return made

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

    def update_cycles(self, cycleA, cycleB):
        self.cycleA = cycleA
        self.cycleB = cycleB

    def generate_all_moves(self):
        moves = None
        best_move = Move(None, None, np.inf)
        for move_type in self.available_moves:
            tmp_moves = []
            tmp_moves = self.get_moves_of_type(move_type)
            #print("tmp_moves", len(tmp_moves))
            if not tmp_moves:
                continue  # list of moves was empty
            deltas = np.asarray([move.delta for move in tmp_moves], dtype=int)
            ind = np.argwhere(deltas < 0)
            ind = np.transpose(ind)[0]
            tmp_moves = np.array(tmp_moves)
            #print(tmp_moves[ind.astype(int)])
            if moves is None:
                moves = tmp_moves[ind]
            else:
                moves = np.concatenate((moves, tmp_moves))
        moves = sorted(moves, key=lambda a: a.delta)
        #moves = np.asarray(moves)
        self.best_moves = (np.unique(moves)).tolist()

    def update_moves(self, move):
        #generate new moves
        if move.type == MoveType.NODE_SWAP_IN_A:
            moves_a = self.get_node_swaps_in_cycle(self.cycleA, 0, 0, 1, MoveType.NODE_SWAP_IN_A, is_update = True,
                                                   update_range = [move.s1 - 1, move.s1, move.s1+1])
            moves_b = self.get_node_swaps_in_cycle(self.cycleA, 0, 0, 1, MoveType.NODE_SWAP_IN_A, is_update = True,
                                                   update_range = [move.s2 - 1, move.s2, move.s2 + 1])

        elif move.type == MoveType.NODE_SWAP_IN_B:
            moves_a = self.get_node_swaps_in_cycle(self.cycleB, 0, 0, 1, MoveType.NODE_SWAP_IN_B, is_update=True,
                                                   update_range=[move.s1 - 1, move.s1, move.s1+1])
            moves_b = self.get_node_swaps_in_cycle(self.cycleB, 0, 0, 1, MoveType.NODE_SWAP_IN_B, is_update=True,
                                                   update_range=[move.s2 - 1, move.s2, move.s2 + 1])

        elif move.type == MoveType.NODE_SWAP_BETWEEN_AB:
            moves_a = self.get_node_swaps_in_cycle(self.cycleA, 0, 0, 1, MoveType.NODE_SWAP_IN_A, is_update = True,
                                                   update_range = [move.s1 - 1, move.s1, move.s1+1])
            moves_b = self.get_node_swaps_in_cycle(self.cycleB, 0, 0, 1, MoveType.NODE_SWAP_IN_B, is_update = True,
                                                   update_range = [move.s2 - 1, move.s2, move.s2 + 1])
        elif move.is_edge_swap():
            if (move.s2.v1 == len(self.cycleA) - 1) and (move.s2.v2 == 0):
                update_range = range(move.s1.v1-1, move.s2.v1+1)
            else:
                update_range = range(move.s1.v1-1, move.s2.v2+2)

            old_best_moves = np.copy(self.best_moves)
            # update all Best Moves that were Edge Swaps and had at least one of the Edges in update range
            for i, b_move in enumerate(old_best_moves):
                if b_move.is_edge_swap():
                    edges_affected = was_edge_swap_in_range(b_move, update_range)
                    if any(edges_affected):
                        if edges_affected[0]:
                            b_move.s1 = b_move.s1.invert()
                        if edges_affected[1]:
                            b_move.s2 = b_move.s2.invert()
                        self.best_moves[i] = b_move

            if move.type == MoveType.EDGE_SWAP_IN_A:
                moves_a = self.get_edge_swaps_in_cycle(self.cycleA, 0, 0, 1, MoveType.EDGE_SWAP_IN_A, is_update=True,
                                                       update_range=[*update_range])
            elif move.type == MoveType.EDGE_SWAP_IN_B:
                moves_a = self.get_edge_swaps_in_cycle(self.cycleB, 0, 0, 1, MoveType.EDGE_SWAP_IN_A, is_update=True,
                                                       update_range=[*update_range])
            moves_b = []

        moves = np.concatenate((moves_a, moves_b))
        new_moves = np.concatenate((self.best_moves, moves))
        new_moves = sorted(new_moves, key=lambda a: a.delta)
        self.best_moves = (np.unique(new_moves)).tolist()


    def get_best_move(self):
        if self.best_moves is None:
            self.generate_all_moves()
        if len(self.best_moves) == 0:
            return None
        return self.best_moves[0]

    def get_moves_of_type(self, move_type, i=0, j=0, step=1):
        if move_type == MoveType.NODE_SWAP_IN_A:
            return self.get_node_swaps_in_cycle(self.cycleA, i, j, step, move_type)

        elif move_type == MoveType.NODE_SWAP_IN_B:
            return self.get_node_swaps_in_cycle(self.cycleB, i, j, step, move_type)

        elif move_type == MoveType.NODE_SWAP_BETWEEN_AB:
            return self.swap_between_cycles(i, j, step, move_type)

        elif move_type == MoveType.EDGE_SWAP_IN_A:
            return self.get_edge_swaps_in_cycle(self.cycleA, i, j, step, move_type)

        elif move_type == MoveType.EDGE_SWAP_IN_B:
            return self.get_edge_swaps_in_cycle(self.cycleB, i, j, step, move_type)

        else:
            return []

    def get_node_swaps_in_cycle(self, cycle, s1, s2, step, move_type, is_update = False, update_range = []):
        # solution = [Move(który, z którym, jaka zmiana, jaki typ)]

        solutions = []
        if is_update is False:
            range_ = range(s1, np.sign(step) * (s1 + len(self.cycleA)), step)
        else:
            range_ = update_range
        for i in range_:
            for j in range(s2, (s2 + len(self.cycleB)) * np.sign(step), step):
                if i != j:
                    real_i = i % len(cycle)
                    real_j = j % len(cycle)
                    delta = self.calc_node_swap_inside(real_i, real_j, cycle)
                    solutions.append(Move(real_i, real_j, delta, move_type))

        return solutions

    def get_edge_swaps_in_cycle(self, cycle, s1, s2, step, move_type, is_update = False, update_range = []):
        # solution = [Move(który, z którym, jaka zmiana, jaki typ)]
        solutions = []
        if is_update is False:
            range_ = range(s1, np.sign(step) * (s1 + len(self.cycleA)), step)
        else:
            range_ = update_range

        for i in range_:
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

                    delta = self.calc_edge_swap_inside(e1, e2, cycle)
                    solutions.append(Move(e1, e2, delta, move_type))
        return solutions

    def calc_node_swap_inside(self, i, j, cycle):
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

    def calc_edge_swap_inside(self, e1: Edge, e2: Edge, cycle):
        old = e1.cost + e2.cost
        new = self.matrix[cycle[e1.v1]][cycle[e2.v1]] + self.matrix[cycle[e1.v2]][cycle[e2.v2]]
        return -old + new

    def swap_between_cycles(self, s1, s2, step, move_type):
        # solution = [Move(który, z którym, jaka zmiana, jaki typ)]
        solutions = []

        for i in range(s1, np.sign(step) * (s1 + len(self.cycleA)), step):
            for j in range(s2, (s2 + len(self.cycleB)) * np.sign(step), step):
                real_i = i % len(self.cycleA)
                real_j = j % len(self.cycleB)
                solutions.append(Move(real_i, real_j, self.calc_swap_between(real_i, real_j), move_type))
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
