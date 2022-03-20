from abc import ABC, abstractmethod
import numpy as np
from Zadanie2.entity.edge import Edge
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

    def __init__(self, matrix, cycleA, cycleB):
        self.matrix = matrix
        self.cycleA = cycleA
        self.cycleB = cycleB
        self.valA = 0
        self.valB = 0
        self.val = 0

    def make_move(self, move):

        if move.type == MoveType.NODE_SWAP_IN_A:
            self.cycleA[move.s1], self.cycleA[move.s2] = self.cycleA[move.s2], self.cycleA[move.s1]
            # tmp = self.cycleA[move[0][0]]
            # self.cycleA[move[0][0]] = self.cycleA[move[0][1]]
            # self.cycleA[move[0][1]] = tmp

        elif move.type == MoveType.NODE_SWAP_IN_B:
            self.cycleB[move.s1], self.cycleB[move.s2] = self.cycleB[move.s2], self.cycleB[move.s1]
            # tmp = self.cycleB[move[0][0]]
            # self.cycleB[move[0][0]] = self.cycleB[move[0][1]]
            # self.cycleB[move[0][1]] = tmp

        elif move.type == MoveType.NODE_SWAP_BETWEEN_AB:
            self.cycleA[move.s1], self.cycleB[move.s2] = self.cycleB[move.s2], self.cycleA[move.s1]
            # tmp = self.cycleA[move[0][0]]
            # self.cycleA[move[0][0]] = self.cycleB[move[0][1]]
            # self.cycleB[move[0][1]] = tmp

        elif move.type == MoveType.EDGE_SWAP_IN_A:
            self.cycleA = swap_edges(self.cycleA, move.s1, move.s2)

        elif move.type == MoveType.EDGE_SWAP_IN_B:
            self.cycleB = swap_edges(self.cycleB, move.s1, move.s2)

        else:
            print("Outstanding move, but it's not implemented")

    @abstractmethod
    def get_best_move(self):
        pass

    @abstractmethod
    def get_greedy_random_move(self):
        pass



