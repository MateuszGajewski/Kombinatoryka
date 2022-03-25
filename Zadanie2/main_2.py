from utils.instance_parser import euclidean_parser
from Zadanie1.solvers.greedy_nearest_neighbor import GreedyNearestNeighbor
from utils.graph_plotting.plot import Plot
from Zadanie2.entity.move_type import MoveType
from Zadanie2.solvers.neighbourhood import Neighbourhood
from Zadanie2.solvers.greedy_local_search import GreedyLocalSolver
from Zadanie2.solvers.random_local_search import RandomLocalSearchSolver
import numpy as np

p = euclidean_parser.EuclideanParser()
matrix = p.parse("../utils/instances/kroB100.tsp")
points = p.get_points()
print("--- GREEDY LOCAL SEARCH ---")
gc_solver = GreedyNearestNeighbor(matrix)
cycles = gc_solver.solve()

# cycles = [np.arange(0, 50, 1), np.arange(50, 100, 1)]
plot = Plot("nn")
plot.draw(cycles, points)

a_moves = [MoveType.NODE_SWAP_IN_A, MoveType.NODE_SWAP_IN_B, MoveType.NODE_SWAP_BETWEEN_AB]
b_moves = [MoveType.EDGE_SWAP_IN_A, MoveType.EDGE_SWAP_IN_B, MoveType.NODE_SWAP_BETWEEN_AB]
random_moves = [mt for mt in MoveType]

nA = Neighbourhood(matrix, cycles[0], cycles[1], available_moves=a_moves)
nB = Neighbourhood(matrix, cycles[0], cycles[1], available_moves=b_moves)
nR = Neighbourhood(matrix, cycles[0], cycles[1], available_moves=random_moves)

a_greedy_solver = GreedyLocalSolver(nA)
a_cycles = a_greedy_solver.solve()
print(len(a_cycles[0]))
print(len(a_cycles[1]))
plot1 = Plot("greedy A")
plot1.draw(a_cycles, points)

b_greedy_solver = GreedyLocalSolver(nB)
b_cycles = b_greedy_solver.solve()
print(len(b_cycles[0]))
print(len(b_cycles[1]))
plot2 = Plot("greedy B")
plot2.draw(b_cycles, points)

random_solver = RandomLocalSearchSolver(nR)
r_cycles = random_solver.solve()
print(len(r_cycles[0]))
print(len(r_cycles[1]))
plot3 = Plot("Random")
plot3.draw(r_cycles, points)
