from enum import Enum


class MoveType(Enum):
    # neighbourhood #1
    NODE_SWAP_IN_A = 1
    EDGE_SWAP_IN_A = 2

    NODE_SWAP_IN_B = 3
    EDGE_SWAP_IN_B = 4

    # neighbourhood #2
    NODE_SWAP_BETWEEN_AB = 5
