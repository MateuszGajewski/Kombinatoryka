from abc import ABC, abstractmethod
import numpy as np

class Neighbourhood(ABC):

    def __init__(self, matrix, cycleA, cycleB):
        self.matrix = matrix
        self.cycleA = cycleA
        self.cycleB = cycleB
        self.valA = 0
        self.valB = 0
        self.val = 0

    def make_move(self, move):
        if move[1] == 'cycleA':
            tmp = self.cycleA[move[0][0]]
            self.cycleA[move[0][0]] = self.cycleA[move[0][1]]
            self.cycleA[move[0][1]] = tmp

        elif move[1] == 'cycleB':
            tmp = self.cycleB[move[0][0]]
            self.cycleB[move[0][0]] = self.cycleB[move[0][1]]
            self.cycleB[move[0][1]] = tmp
        else:
            tmp = self.cycleA[move[0][0]]
            self.cycleA[move[0][0]] = self.cycleB[move[0][1]]
            self.cycleB[move[0][1]] = tmp


    @abstractmethod
    def get_best_move(self):
        pass

    @abstractmethod
    def get_greedy_random_move(self):
        pass



