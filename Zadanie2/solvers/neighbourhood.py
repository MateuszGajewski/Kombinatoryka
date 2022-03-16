from abc import ABC, abstractmethod


class Neighbourhood(ABC):

    def __init__(self, matrix, cycleA, cycleB):
        self.matrix = matrix
        self.cycleA = cycleA
        self.cycleB = cycleB
        self.valA = 0
        self.valB = 0

    @abstractmethod
    def get_moves(self):
        #moves inside

        #movesBetween

    @abstractmethod
    def make_move(self):
        raise NotImplementedError
