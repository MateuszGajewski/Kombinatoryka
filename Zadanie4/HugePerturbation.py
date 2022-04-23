import random
from Zadanie4.PartiallyGreedyCycle import PartiallyGreedyCycle
from Zadanie4.Perturbation import Perturbation


class HugePerturbation(Perturbation):

    def __init__(self, percent=20):
        self.to_change = percent  # percentage of total number of edges that should be destroyed

    def __call__(self, cycles, instance):
        free_points = []
        for cycle in cycles:
            n = len(cycle)
            num_to_destroy = int(n/2 * self.to_change/100)  # n/2 since we want to destroy edges in both cycles
            starting_point = int((n-1) * random.random())

            if starting_point + num_to_destroy > n:
                free_points.extend(cycle[starting_point:])
                del cycle[starting_point:]
                remaining = starting_point + num_to_destroy - n
                free_points.extend(cycle[:remaining])
                del cycle[:remaining]
            else:
                free_points.extend(cycle[starting_point : starting_point + num_to_destroy])
                del cycle[starting_point : starting_point + num_to_destroy]

        # print(num_to_destroy, len(cycles[0]), len(cycles[1]))
        heuristics = PartiallyGreedyCycle(instance, cycles, free_points)
        new_cycles = heuristics.solve()

        return new_cycles
