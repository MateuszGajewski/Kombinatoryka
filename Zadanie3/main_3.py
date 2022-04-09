from Zadanie1.solvers.greedy_cycle import GreedyCycle
from Zadanie1.solvers.random_solver import RandomSolver
from utils.instance_parser import euclidean_parser
from utils.graph_plotting.plot import Plot
from Zadanie2.entity.move_type import MoveType
from Zadanie2.entity.solution import Solution
from Zadanie2.solvers.neighbourhood import Neighbourhood
from Zadanie2.solvers.greedy_local_search import GreedyLocalSolver
from Zadanie2.solvers.steep_local_search import SteepLocalSolver
from Zadanie2.solvers.random_local_search import RandomLocalSearchSolver
from Zadanie3.neighbourhood_opt import Neighbourhood_opt
from Zadanie3.opt_moves_list import OptLocalSolver
from Zadanie3.candidate_solver import CandidateSolver
import numpy as np


def run():
    p = euclidean_parser.EuclideanParser()
    matrix = p.parse("../utils/instances/kroA100.tsp")
    points = p.get_points()

    a_moves = [MoveType.NODE_SWAP_IN_A, MoveType.NODE_SWAP_IN_B, MoveType.NODE_SWAP_BETWEEN_AB]
    b_moves = [MoveType.EDGE_SWAP_IN_A, MoveType.EDGE_SWAP_IN_B, MoveType.NODE_SWAP_BETWEEN_AB]
    c_moves = [MoveType.CANDIDATE_IN_A, MoveType.CANDIDATE_IN_B, MoveType.NODE_SWAP_BETWEEN_AB]
    random_moves = [mt for mt in MoveType]

    solutions = [
        #Solution("Random Wandering", RandomLocalSearchSolver, random_moves),
        #Solution("Greedy (nodes)", GreedyLocalSolver, a_moves),
        #Solution("Steep (nodes)", SteepLocalSolver, a_moves),
        #Solution("Greedy (edges)", GreedyLocalSolver, b_moves, Neighbourhood_opt),
        #Solution("Steep (edges)", SteepLocalSolver, b_moves)
        #Solution("TEST", OptLocalSolver, b_moves, Neighbourhood_opt)
        Solution("test", CandidateSolver, c_moves, Neighbourhood)
        ]

    for i in range(0, 1):
        print(f"Running iteration #{i}")

        instance = GreedyCycle(matrix, starting_point=i).solve()
        #instance = RandomSolver(matrix, starting_point=i).solve()

        for solution in solutions:
            solution.find(matrix, instance)

    for solution in solutions:
        print(solution)

        plot = Plot(solution.solver_name)
        plot.draw(solution.best_instance, points)


if __name__ == "__main__":
    run()
else:
    print("IMO2")
