from instance_parser import euclidean_parser
from solvers.greedy_nearest_neighbor import GreedyNearestNeighbor
p = euclidean_parser.EuclideanParser()
matrix = p.parse("instances/kroB100.tsp")
solver = GreedyNearestNeighbor(matrix)
print(solver.solve())

