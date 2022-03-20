from utils.instance_parser import euclidean_parser
from Zadanie1.solvers.greedy_nearest_neighbor import GreedyNearestNeighbor
from utils.graph_plotting.plot import Plot
from Zadanie2.solvers.neighbourhood_a import NeighbourhoodA
from Zadanie2.solvers.neighbourhood_b import NeighbourhoodB
from Zadanie2.solvers.greedy_local_search import GreedyLocalSolver
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

n = NeighbourhoodA(matrix, cycles[0], cycles[1])
nB = NeighbourhoodB(matrix, cycles[0], cycles[1])

a_greedy_solver = GreedyLocalSolver(n)
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
