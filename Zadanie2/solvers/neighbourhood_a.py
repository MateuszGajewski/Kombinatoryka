from Zadanie2.solvers.neighbourhood import Neighbourhood
import numpy as np
import random
#Opcja z zamianą kolejności i między cyklami
class Neighbourhood_a(Neighbourhood):

    def calc_swap_inside(self, i, j, cycle):
        delta = 0
        if i != j and abs(i - j) != 1:
            old = self.matrix[cycle[i] - 1][cycle[i - 1] - 1] + \
                  self.matrix[cycle[i] - 1][cycle[(i + 1) % len(cycle)] - 1] + \
                  self.matrix[cycle[j] - 1][cycle[j - 1] - 1] + \
                  self.matrix[cycle[j] - 1][cycle[(j + 1) % len(cycle)] - 1]

            new = self.matrix[cycle[j] - 1][cycle[i - 1] - 1] + \
                  self.matrix[cycle[j] - 1][cycle[(i + 1) % len(cycle)] - 1] + \
                  self.matrix[cycle[i] - 1][cycle[j - 1] - 1] + \
                  self.matrix[cycle[i] - 1][cycle[(j + 1) % len(cycle)] - 1]
            delta = -old + new


        elif i != j:
            if i < j:
                old = self.matrix[cycle[i] - 1][cycle[i - 1] - 1] + \
                      self.matrix[cycle[j] - 1][cycle[(j + 1) % len(cycle)] - 1]
                new = self.matrix[cycle[j] - 1][cycle[i - 1] - 1] + \
                      self.matrix[cycle[i] - 1][cycle[(j + 1) % len(cycle)] - 1]

            else:
                old = self.matrix[cycle[j] - 1][cycle[j - 1] - 1] + \
                      self.matrix[cycle[i] - 1][cycle[(i + 1) % len(cycle)] - 1]
                new = self.matrix[cycle[i] - 1][cycle[j - 1] - 1] + \
                      self.matrix[cycle[j] - 1][cycle[(i + 1) % len(cycle)] - 1]
            delta = -old + new
        return delta
    
    def get_moves_in_cycle(self, cycle, s1, s2, step):
        # solution = [[który, z którym, jaka zmiana]]
        solutions = []
        old = 0
        new = 0
        # w ramach cyklu

        for i in range(s1, np.sign(step) * (s1 + len(self.cycleA)), step):
            for j in range(s2, (s2 + len(self.cycleB)) * np.sign(step), step):
                if i != j:
                    real_i = i % len(cycle)
                    real_j = j % len(cycle)
                    solutions.append([real_i, real_j, self.calc_swap_inside(real_i, real_j, cycle)])

        return solutions

    def calc_swap_between(self, i, j):
        old = self.matrix[self.cycleA[i] - 1][self.cycleA[i - 1] - 1] + \
              self.matrix[self.cycleA[i] - 1][self.cycleA[(i + 1) % len(self.cycleA)] - 1] + \
              self.matrix[self.cycleB[j] - 1][self.cycleB[j - 1] - 1] + \
              self.matrix[self.cycleB[j] - 1][self.cycleB[(j + 1) % len(self.cycleB)] - 1]

        new = self.matrix[self.cycleB[j] - 1][self.cycleA[i - 1] - 1] + \
              self.matrix[self.cycleB[j] - 1][self.cycleA[(i + 1) % len(self.cycleA)] - 1] + \
              self.matrix[self.cycleA[i] - 1][self.cycleB[j - 1] - 1] + \
              self.matrix[self.cycleA[i] - 1][self.cycleB[(j + 1) % len(self.cycleB)] - 1]
        return -old +new


    def swap_between_cycles(self, s1, s2, step):
        solutions = []

        for i in range(s1, np.sign(step) *(s1+len(self.cycleA)), step):
            for j in range(s2, (s2+len(self.cycleB))*np.sign(step), step):
                real_i = i % len(self.cycleA)
                real_j = j % len(self.cycleB)
                solutions.append([real_i, real_j, self.calc_swap_between(real_i, real_j)])
        return solutions

                


    def get_best_move(self):
        solutions = []
        cycleA = self.get_moves_in_cycle(self.cycleA, 0, 0, 1)
        cycleB = self.get_moves_in_cycle(self.cycleB, 0, 0, 1)
        swap_cycle = self.swap_between_cycles(22, 0, -1)
        cycleA = np.asarray(cycleA, dtype=int)
        indA = np.argwhere(cycleA[:, 2] == (np.min(cycleA[:, 2])))[0, 0]
        cycleB = np.asarray(cycleB, dtype=int)
        indB = np.argwhere(cycleA[:, 2] == (np.min(cycleA[:, 2])))[0, 0]
        cycleS = np.asarray(swap_cycle, dtype=int)
        indS = np.argwhere(cycleA[:, 2] == (np.min(cycleA[:, 2])))[0, 0]
        print(indA)
        print(cycleA[indA])
        if cycleA[indA, 2] < cycleB[indB, 2] and cycleA[indA, 2] < cycleS[indS, 2]:
            return [cycleA[indA], 'cycleA']
        elif cycleB[indB][2] < cycleS[indS][2]:
            return [cycleB[indB], 'cycleB']
        else:
            return [cycleS[indS], 'swap']


    def get_greedy_random_move(self):
        r = random.randint(0, 2)
        for i in range(0, 3):
            if r%3 == 0:
                i = random.randint(0, len(self.cycleA))
                j = random.randint(0, len(self.cycleB))
                step = random.randrange(0, 2) * 2 - 1
                solutions = self.swap_between_cycles(i,j, step)
                solutions = np.asarray(solutions, dtype=int)
                ind = np.argwhere(solutions[:, 2] < 0)
                if ind.shape[0] > 0:
                    return [solutions[ind[0, 0]], 'swap']
            elif r % 3 == 1:
                i = random.randint(0, len(self.cycleA))
                j = random.randint(0, len(self.cycleA))
                step = random.randrange(0, 2) * 2 - 1
                solutions = self.get_moves_in_cycle(self.cycleA, i, j, step)
                solutions = np.asarray(solutions, dtype=int)
                ind = np.argwhere(solutions[:, 2] < 0)
                if ind.shape[0] > 0:
                    return [solutions[ind[0, 0]], 'cycleA']
            else:
                i = random.randint(0, len(self.cycleB))
                j = random.randint(0, len(self.cycleB))
                step = random.randrange(0, 2) * 2 - 1
                solutions = self.get_moves_in_cycle(self.cycleB, i, j, step)
                solutions = np.asarray(solutions, dtype=int)
                ind = np.argwhere(solutions[:, 2] < 0)
                if ind.shape[0] > 0:
                    return [solutions[ind[0, 0]], 'cycleB']
            r += 1











