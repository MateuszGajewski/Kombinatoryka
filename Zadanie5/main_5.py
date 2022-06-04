from copy import deepcopy

from Zadanie1.solvers.random_solver import RandomSolver
from Zadanie4.HugePerturbation import HugePerturbation
from Zadanie4.ILSSolution import ILSSolution
from Zadanie4.SmallPerturbation import SmallPerturbation
from Zadanie5.EvoSolution import EvoSolution
from utils.instance_parser import euclidean_parser
from utils.graph_plotting.plot import Plot
from Zadanie2.entity.move_type import MoveType
from Zadanie2.entity.solution import Solution
from Zadanie2.solvers.neighbourhood import Neighbourhood
from Zadanie2.solvers.steep_local_search import SteepLocalSolver
from Zadanie2.solvers.greedy_local_search import GreedyLocalSolver
from Zadanie3.neighbourhood_opt import Neighbourhood_opt
from Zadanie4.MSLSSolver import MLSSolver


def calculate_cycle_len(matrix, cycles):
    total = 0
    for cycle in cycles:
        for i, node in enumerate(cycle):
            total += matrix[cycle[i-1]][node]
    return total

def run():
    p = euclidean_parser.EuclideanParser()
    matrix = p.parse("../utils/instances/kroB200.tsp")
    points = p.get_points()

    evo_solutions = [
        EvoSolution("Evo", SteepLocalSolver, Neighbourhood, with_local_repair=True),
        EvoSolution("Evo-a", SteepLocalSolver, Neighbourhood, with_local_repair=False),
    ]

    for i in range(0, 3):
        for evo_solution in evo_solutions:
            time_limit = 60*10
            evo_solution.find(matrix, time_limit=time_limit)

    for solution in evo_solutions:
        print(solution)
        plot = Plot(solution.solver_name)
        plot.draw(solution.best_instance, points)


if __name__ == "__main__":
    run()
else:
    print("IMO5")
