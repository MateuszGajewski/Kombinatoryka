from copy import deepcopy

from Zadanie1.solvers.random_solver import RandomSolver
from Zadanie4.HugePerturbation import HugePerturbation
from Zadanie4.ILSSolution import ILSSolution
from Zadanie4.SmallPerturbation import SmallPerturbation
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
    matrix = p.parse("../utils/instances/kroA200.tsp")
    points = p.get_points()

    a_moves = [MoveType.NODE_SWAP_IN_A, MoveType.NODE_SWAP_IN_B, MoveType.NODE_SWAP_BETWEEN_AB]
    b_moves = [MoveType.EDGE_SWAP_IN_A, MoveType.EDGE_SWAP_IN_B, MoveType.NODE_SWAP_BETWEEN_AB]
    random_moves = [mt for mt in MoveType]

    msls_solution = Solution("MSLS", MLSSolver, b_moves, Neighbourhood_opt)
    ils_solutions = [
        ILSSolution("ILS1", SteepLocalSolver, Neighbourhood_opt, SmallPerturbation(n=10), True),
        ILSSolution("ILS2", SteepLocalSolver, Neighbourhood_opt, HugePerturbation(percent=20), True),
        ILSSolution("ILS2a", SteepLocalSolver, Neighbourhood_opt, HugePerturbation(percent=20), False),
    ]

    for i in range(0, 10):
        instance = RandomSolver(matrix, starting_point=None).solve()

        cycles = deepcopy(instance)
        time_limit = msls_solution.find(matrix, cycles)

        for ils_solution in ils_solutions:
            cycles = deepcopy(instance)
            ils_solution.find(matrix, cycles, time_limit=time_limit)

    print(msls_solution)
    plot = Plot(msls_solution.solver_name)
    plot.draw(msls_solution.best_instance, points)

    for solution in ils_solutions:
        print(solution)
        plot = Plot(solution.solver_name)
        plot.draw(solution.best_instance, points)


if __name__ == "__main__":
    run()
else:
    print("IMO3")
