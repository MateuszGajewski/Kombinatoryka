from time import time
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import random

from Zadanie1.solvers.random_solver import RandomSolver
from Zadanie2.entity.move_type import MoveType
from Zadanie4.PartiallyGreedyCycle import PartiallyGreedyCycle


def plot_scores(best, worst):
    fig, ax = plt.subplots(figsize=(12, 8))
    print(f"Plotting scores from {len(best)} iterations...")
    xs = [*range(len(best))]
    ax.plot(xs, best, label='best', color='g')
    ax.plot(xs, worst, label='worst', color='r')
    ax.legend()
    plt.show()


class EvolutionarySolver:
    def __init__(self, matrix, time_limit, ls_solver, neighbourhood,
                 use_local_repair=False, use_perturbation=True, perturbation_chance=0.1, elite_pop=20):
        self.matrix = matrix
        self.dimension = len(matrix)
        self.time_limit = time_limit
        self.ls_solver = ls_solver
        self.neighbourhood_class = neighbourhood
        self.use_local_repair = use_local_repair
        self.use_perturbation = use_perturbation
        self.perturbation_chance = perturbation_chance
        self.n = elite_pop

    def solve(self):
        start = time()

        # best_scores = []
        # worst_scores = []
        iterations = 0

        population = [self.generate_initial_solution() for _ in range(self.n)]
        scores = [self.calculate_result(solution) for solution in population]
        # print("Evo: Initial population created")

        while time() - start < self.time_limit:
            pi, pj = int(self.n * random.random()), int(self.n * random.random())
            while pi == pj:
                pj = int(self.n * random.random())

            new_solution = self.recombine(population[pi], population[pj])

            if self.use_local_repair is True:
                # new_solution = self.ls_solver(new_solution)
                neighbourhood = self.neighbourhood_class(self.matrix, *new_solution, [mt for mt in MoveType])
                new_solution = self.go_steep(neighbourhood, start)

            new_score = self.calculate_result(new_solution)

            if any(score == new_score for score in scores):
                # new solution is a duplicate of existing one
                continue

            if new_score < max(scores):
                # replace worst solution in population with a new one
                worst_idx = max(range(self.n), key=scores.__getitem__)
                population[worst_idx] = new_solution
                scores[worst_idx] = new_score

            # best_scores.append(min(scores))
            # worst_scores.append(max(scores))
            iterations += 1

        # time's up, return the best solution
        # plot_scores(best_scores, worst_scores)
        print(iterations)
        best_idx = min(range(self.n), key=scores.__getitem__)
        return time() - start, population[best_idx], scores[best_idx]

    def calculate_result(self, cycles):
        total = 0
        for cycle in cycles:
            for i, node in enumerate(cycle):
                total += self.matrix[cycle[i-1], node]

        if len(cycles[0]) != len(cycles[1]):
            return np.inf

        return total

    def go_steep(self, neighbourhood, time_start):
        while time() - time_start < self.time_limit:
            move = neighbourhood.get_best_move()
            if move is not None and move.delta < 0:
                neighbourhood.make_move(move)
            else:
                break
        return [neighbourhood.cycleA, neighbourhood.cycleB]

    def generate_initial_solution(self):
        instance = RandomSolver(self.matrix).solve()
        # cycles = self.ls_solver(instance)
        move_types = [mt for mt in MoveType]
        neighbourhood = self.neighbourhood_class(self.matrix, *instance, move_types)
        problem_solver = self.ls_solver(neighbourhood)
        cycles = problem_solver.solve()
        return cycles

    def recombine(self, p1, p2):
        p1, p2 = deepcopy(p1), deepcopy(p2)
        free_points = []

        for cycle1 in p1:
            n1 = len(cycle1)
            for i in range(n1):
                i0, i1 = cycle1[i], cycle1[(i+1) % n1]
                if i0 == -1 or i1 == -1:
                    continue

                shared = False
                for cycle2 in p2:
                    n2 = len(p2)
                    for j in range(n2):
                        j0, j1 = cycle2[j], cycle2[(j+1) % n2]
                        if (i0 == j0 and i1 == j1) or (i0 == j1 and i1 == j0):
                            shared = True
                            break
                    if shared:
                        break

                if not shared:
                    free_points.append(cycle1[i])
                    cycle1[i] = -1
                    free_points.append(cycle1[(i+1) % n1])
                    cycle1[(i+1) % n1] = -1

            if self.use_perturbation:
                for i, node in enumerate(cycle1):
                    # remove shared node with a given chance
                    if node != -1 and random.random() < self.perturbation_chance:
                        free_points.append(node)
                        cycle1[i] = -1

            for i in range(1, n1):
                i0, i1, i2 = cycle1[(i-1) % n1], cycle1[i], cycle1[(i+1) % n1]
                if i0 == -1 and i2 == -1 and i1 != -1:
                    # `i1` was shared between parents, but the edges around it weren't - remove it
                    free_points.append(cycle1[i])
                    cycle1[i] = -1

        cycleA = [node for node in p1[0] if node != -1]
        cycleB = [node for node in p1[1] if node != -1]
        heuristics = PartiallyGreedyCycle(self.matrix, [cycleA, cycleB], free_points)
        new_cycles = heuristics.solve()
        return new_cycles
