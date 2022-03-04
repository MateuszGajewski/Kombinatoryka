from instance_parser import euclidean_parser
from solvers.greedy_nearest_neighbor import GreedyNearestNeighbor
from solvers.greedy_cycle import GreedyCycle


p = euclidean_parser.EuclideanParser()
matrix = p.parse("instances/kroB100.tsp")

print("--- GREEDY NEAREST NEIGHBOUR ---")
nn_solver = GreedyNearestNeighbor(matrix)
nn_solver.solve()

print("--- GREEDY CYCLE ---")
gc_solver = GreedyCycle(matrix)
gc_solver.solve()

