from utils.instance_parser import euclidean_parser
from Zadanie1.solvers.greedy_nearest_neighbor import GreedyNearestNeighbor
from Zadanie1.solvers.greedy_cycle import GreedyCycle
from utils.graph_plotting.plot import Plot
from Zadanie2.solvers.neighbourhood_a import Neighbourhood_a
from Zadanie2.solvers.greedy_local_search import GreedyLocalSolver
import numpy as np

p = euclidean_parser.EuclideanParser()
matrix = p.parse("../utils/instances/kroB100.tsp")
points = p.get_points()
print("--- GREEDY LOCAL SEARCH ---")
gc_solver = GreedyNearestNeighbor(matrix)
cycles = gc_solver.solve()

#cycles = [np.arange(0, 50, 1), np.arange(50, 100, 1)]
plot = Plot("nn")
plot.draw(cycles, points)
n = Neighbourhood_a(matrix, cycles[0], cycles[1])
greedy_solver = GreedyLocalSolver(n)
cycles = greedy_solver.solve()
print(len(cycles[0]))
print(len(cycles[1]))
plot1 = Plot("greedy")
plot1.draw(cycles, points)
