import random
from copy import deepcopy
from Zadanie2.entity.edge import Edge
from Zadanie2.entity.move import Move
from Zadanie2.entity.move_type import MoveType
from Zadanie4.Perturbation import Perturbation


def get_random_edge_swap(i, j, n):
    i2 = i + 1 % n
    j2 = j + 1 % n
    e1 = Edge(i, i2, cost=None)
    e2 = Edge(j, j2, cost=None)
    if e1.v1 > e2.v1:
        e1, e2 = e2, e1
    return Move(e1, e2, delta=None, move_type=None)

def swap_edges(cycle, move):
    e1, e2 = move.s1, move.s2
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


class SmallPerturbation(Perturbation):

    def __init__(self, n=10):
        self.to_change = n  # number of random moves that should be performed

    def __call__(self, cycles, instance):
        n = len(cycles[0])
        new_cycles = deepcopy(cycles)
        for _ in range(self.to_change):
            types = [MoveType.NODE_SWAP_BETWEEN_AB, MoveType.EDGE_SWAP_IN_A, MoveType.EDGE_SWAP_IN_B]
            i, j = int(n * random.random()), int(n * random.random())
            move_type = random.choice(types)
            if move_type == MoveType.NODE_SWAP_BETWEEN_AB:
                new_cycles[0][i], new_cycles[1][j] = new_cycles[1][j], new_cycles[0][i]
            else:
                while abs(i-j) < 2 or abs(i-j) == n-1:
                    i, j = int(n * random.random()), int(n * random.random())
                move = get_random_edge_swap(i, j, n)
                cid = 0 if move_type == MoveType.EDGE_SWAP_IN_A else 1
                new_cycles[cid] = swap_edges(new_cycles[cid], move)

        return new_cycles
