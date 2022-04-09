from abc import ABC, abstractmethod

import numpy as np
import random
from Zadanie2.entity.edge import Edge
from Zadanie2.entity.move import Move
from Zadanie2.entity.move_type import MoveType


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


class Neighbourhood(ABC):

    def __init__(self, matrix, cycleA, cycleB, available_moves):
        self.matrix = matrix
        self.cycleA = cycleA
        self.cycleB = cycleB
        self.available_moves = available_moves

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

        elif move.type == MoveType.CANDIDATE_IN_A:
            self.cycleA = self.make_candidate_move(self.cycleA, move)

        elif move.type == MoveType.CANDIDATE_IN_B:
            self.cycleB = self.make_candidate_move(self.cycleB, move)


        else:
            print("Outstanding move, but it's not implemented")
    def make_candidate_move(self, cycle, move):
        if move.s1 > move.s2:
            move.s1, move.s2 = move.s2, move.s1
        print(move)
        if move.direction == 1:
            p1 = cycle[:move.s1+1]
            p2 = cycle[move.s1+1: move.s2+1]
            p2.reverse()
            p3 = cycle[move.s2+1:]

            cycle = p1 + p2 + p3
        else:
            p1 = cycle[:move.s1]
            p2 = cycle[move.s1: move.s2]
            p2.reverse()
            p3 = cycle[move.s2:]
            cycle = p1 + p2 + p3
        return cycle





    def update_cycles(self, cycleA, cycleB):
        self.cycleA = cycleA
        self.cycleB = cycleB

    def get_best_move(self):
        best_move = Move(None, None, np.inf)
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
            i = random.randint(0, len(self.cycleA)-1)
            j = random.randint(0, len(self.cycleB)-1)
            step = random.choice([-1, 1])
            moves = np.asarray(self.get_moves_of_type(move_type, i, j, step))
            deltas = np.asarray([move.delta for move in moves], dtype=int)
            if any(deltas < 0):
                improvements = moves[deltas < 0]
                first_best_move = improvements[0]
                return first_best_move
        # if all available_moves were considered, but no improvement was found, return None
        return None

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

        elif move_type == MoveType.CANDIDATE_IN_A:
            return self.get_candidate_moves_in_cycle(self.cycleA, 0, move_type, 10)
        elif move_type == MoveType.CANDIDATE_IN_B:
            return self.get_candidate_moves_in_cycle(self.cycleB, 0, move_type, 10)
        else:
            return []

    def get_n_closest_points(self, cycle, s, n):
        point = cycle[s]
        results = []
        distances = self.matrix[point, :]
        distances = np.argsort(distances)
        for i in distances:
            if i in cycle and i != point:
                results.append(i)
        return results[0:n]

    def calc_candidates(self, i, j, cycle, direction):
        old = self.matrix[cycle[i]][cycle[(i+direction)% len(cycle)]] + self.matrix[cycle[j]][cycle[(j+direction)% len(cycle)]]
        new = self.matrix[cycle[i]][cycle[j]] + self.matrix[cycle[(i+direction) % len(cycle)]][cycle[(j+direction)% len(cycle)]]
        return -old + new


    def get_candidate_moves_in_cycle(self, cycle, s1, move_type, n):
        solutions = []
        for i in range(s1, np.sign(1) * (s1 + len(self.cycleA)), 1):
            real_i = i % len(cycle)
            nearest_n = self.get_n_closest_points(cycle, real_i, n)
            for j in nearest_n:
                real_j = cycle.index(j)
                if real_i != real_j and abs(real_i - real_j) != 1:
                    delta = self.calc_candidates(real_i, real_j, cycle, 1)
                    solutions.append(Move(real_i, real_j, delta, move_type, 1))
                    delta = self.calc_candidates(real_i, real_j, cycle, -1)
                    solutions.append(Move(real_i, real_j, delta, move_type, -1))
        #print(solutions)
        return solutions


    def get_node_swaps_in_cycle(self, cycle, s1, s2, step, move_type):
        # solution = [Move(który, z którym, jaka zmiana, jaki typ)]
        solutions = []

        for i in range(s1, np.sign(step) * (s1 + len(self.cycleA)), step):
            for j in range(s2, (s2 + len(self.cycleB)) * np.sign(step), step):
                if i != j:
                    real_i = i % len(cycle)
                    real_j = j % len(cycle)
                    delta = self.calc_node_swap_inside(real_i, real_j, cycle)
                    solutions.append(Move(real_i, real_j, delta, move_type))

        return solutions

    def get_edge_swaps_in_cycle(self, cycle, s1, s2, step, move_type):
        # solution = [Move(który, z którym, jaka zmiana, jaki typ)]
        solutions = []

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

                    delta = self.calc_edge_swap_inside(e1, e2, cycle)
                    solutions.append(Move(e1, e2, delta, move_type))
        return solutions

    def calc_node_swap_inside(self, i, j, cycle):
        if i == j:
            return 0

        i_0, i_1, i_2 = cycle[(i-1) % len(cycle)], cycle[i], cycle[(i+1) % len(cycle)]
        j_0, j_1, j_2 = cycle[(j-1) % len(cycle)], cycle[j], cycle[(j+1) % len(cycle)]

        if (i, j) == (0, len(cycle)-1):
            old = self.matrix[i_1, i_2] + self.matrix[j_1, j_0]
            new = self.matrix[j_1, i_2] + self.matrix[i_1, j_0]
            return -old + new

        elif (i, j) == (len(cycle)-1, 0):
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
        old = self.matrix[self.cycleA[i]][self.cycleA[((i-1) % len(self.cycleA))]] + \
              self.matrix[self.cycleA[i]][self.cycleA[(i+1) % len(self.cycleA)]] + \
              self.matrix[self.cycleB[j]][self.cycleB[(j-1) % len(self.cycleB)]] + \
              self.matrix[self.cycleB[j]][self.cycleB[(j+1) % len(self.cycleB)]]

        new = self.matrix[self.cycleB[j]][self.cycleA[((i-1) % len(self.cycleA))]] + \
              self.matrix[self.cycleB[j]][self.cycleA[(i+1) % len(self.cycleA)]] + \
              self.matrix[self.cycleA[i]][self.cycleB[(j-1) % len(self.cycleB)]] + \
              self.matrix[self.cycleA[i]][self.cycleB[(j+1) % len(self.cycleB)]]
        return -old + new
