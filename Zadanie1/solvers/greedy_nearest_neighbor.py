from solver import Solver
import numpy as np
import random

class GreedyNearestNeibourgh(Solver):
    matrix = 0
    cycle1 = 0
    cycle2 = 0
    visited = 0

    def __init__(self, array):
        self.matrix = array
        self.cycle1 = np.array(np.ceil(self.matrix.shape[0]/2))
        self.cycle2 = np.array(np.floor(self.matrix.shape[0]/2))
        self.visited = np.zeros(self.matrix.shape[0])

    def find_nearest_neibourgh(self, index):
        pass


    def solve(self, array=np.array):
        self.matrix = array
        index = 0
        self.cycle1[0] = random.randint(0, self.matrix.shape[0])
        while index != np.ceil(self.matrix.shape[0]/2):


