from Zadanie2.entity.move_type import MoveType


class Move:
    def __init__(self, s1, s2, delta, move_type=None):
        # `s1` and `s2` can be point/node ids or objects of Edge class, depending on move_type
        self.s1 = s1
        self.s2 = s2
        self.delta = delta  # distance gain compared to current solution
        self.type = move_type  # `NODE SWAP {A,B,AB}` or `EDGE SWAP {A,B}` or None

    def __str__(self):
        return f"Move: {self.s1} <-> {self.s2} ({self.type}); Delta = {self.delta}"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.delta < other.delta

    def is_edge_swap(self):
        return self.type in [MoveType.EDGE_SWAP_IN_A, MoveType.EDGE_SWAP_IN_B]
