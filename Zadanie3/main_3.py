import time
import numpy as np

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
from Zadanie3.neighbourhood_candidate import NeighbourhoodCandidate
from Zadanie3.opt_moves_list import OptLocalSolver
from Zadanie3.candidate_solver import CandidateSolver


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
    c_moves = [MoveType.CANDIDATE_IN_A, MoveType.CANDIDATE_IN_B, MoveType.NODE_SWAP_BETWEEN_AB]
    random_moves = [mt for mt in MoveType]

    solutions = [
        Solution("Steep", SteepLocalSolver, b_moves, Neighbourhood),
        Solution("Memory", OptLocalSolver, b_moves, Neighbourhood_opt),
        Solution("Candidate", CandidateSolver, random_moves, NeighbourhoodCandidate)
        ]

    greedy_results = []
    greedy_times = []

    for i in range(0, 100):
        print(f"Running iteration #{i}")
        greedy_start = time.time()

        instance = GreedyCycle(matrix, starting_point=i).solve()

        duration = round(time.time() - greedy_start, 3)
        greedy_times.append(duration)
        greedy_results.append(calculate_cycle_len(matrix, instance))
        print(f"Instance #{i} is ready")

        for solution in solutions:
            cycles = instance.copy()
            solution.find(matrix, cycles)

    for solution in solutions:
        print(solution)

        plot = Plot(solution.solver_name)
        plot.draw(solution.best_instance, points)

    print(f"""
---- Solved with Greedy Cycle ----
> Results:
\tmean:\t\tmin:\t\tmax:
\t{np.mean(greedy_results)}; \t{np.min(greedy_results)}; \t{np.max(greedy_results)};

> Times:
\tmean:\t\tmin:\t\tmax:
\t{np.mean(greedy_times)}; \t{np.min(greedy_times)}; \t{np.max(greedy_times)};
""")
    plot = Plot("Greedy Cycle")
    plot.draw(solution.best_instance, points)


if __name__ == "__main__":
    run()
else:
    print("IMO3")
