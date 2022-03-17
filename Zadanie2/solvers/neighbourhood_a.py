from Zadanie2.solvers.neighbourhood import Neighbourhood
#Opcja z zamianą kolejności i między cyklami
class Neighbourhood_a(Neighbourhood):

    def calc_swap_inside(self, i, j, cycle):
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
    
    def get_moves_in_cycle(self, cycle):
        # solution = [[który, z którym, jaka zmiana]]
        solutions = []
        old = 0
        new = 0
        # w ramach cyklu
        for i in range(0, len(cycle)):
            for j in range(0, len(cycle)):
                if i != j:
                    solutions.append([i, j, self.calc_swap_inside_inside(i, j, cycle)])
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


    def swap_between_cycles(self):
        solutions = []
        old = 0
        new = 0
        delta = 0

        for i in range(0, len(self.cycleA)):
            for j in range(0, len(self.cycleB)):
                solutions.append([i, j, self.calc_swap_between(i, j)])

                


    def get_moves(self):
        solutions = []
        solutions.append(self.get_moves_in_cycle(self.cycleA))
        solutions.append(self.get_moves_in_cycle(self.cycleB))
        return solutions


        




        return solutions



