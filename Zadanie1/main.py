from instance_parser import euclidean_parser
from solvers.greedy_nearest_neighbor import GreedyNearestNeighbor
from solvers.greedy_cycle import GreedyCycle
from graph_plotting.plot import Plot

p = euclidean_parser.EuclideanParser()
matrix = p.parse("instances/kroB100.tsp")
points = p.get_points()
print("--- GREEDY NEAREST NEIGHBOUR ---")
nn_solver = GreedyNearestNeighbor(matrix)
cycles = nn_solver.solve()
plot = Plot()
plot.draw(cycles, points)

print("--- GREEDY CYCLE ---")
gc_solver = GreedyCycle(matrix)
gc_solver.solve()

