from utils.instance_parser import euclidean_parser
from Zadanie1.solvers.greedy_nearest_neighbor import GreedyNearestNeighbor
from utils.graph_plotting.plot import Plot
from Zadanie2.solvers.neighbourhood_a import Neighbourhood_a


p = euclidean_parser.EuclideanParser()
matrix = p.parse("../utils/instances/kroB100.tsp")
points = p.get_points()
print("--- GREEDY NEAREST NEIGHBOUR ---")
nn_solver = GreedyNearestNeighbor(matrix)
cycles = nn_solver.solve()
n = Neighbourhood_a(matrix, cycles[0], cycles[1])
print(n.make_move(n.get_greedy_random_move()))
