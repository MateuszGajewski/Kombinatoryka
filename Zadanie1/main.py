from utils.instance_parser import euclidean_parser
from solvers.greedy_nearest_neighbor import GreedyNearestNeighbor
from solvers.greedy_cycle import GreedyCycle
from solvers.regret import RegretSolver
from utils.graph_plotting.plot import Plot

p = euclidean_parser.EuclideanParser()
matrix = p.parse("../utils/instances/kroB100.tsp")
points = p.get_points()
print("--- GREEDY NEAREST NEIGHBOUR ---")
nn_solver = GreedyNearestNeighbor(matrix)
cycles = nn_solver.solve()
plot = Plot("nn")
plot.draw(cycles, points)

print("--- GREEDY CYCLE ---")
gc_solver = GreedyCycle(matrix)
cycles = gc_solver.solve()
plot2 = Plot("c")
plot2.draw(cycles, points)

print("--- 2-REGRET CYCLE ---")
r_solver = RegretSolver(matrix)
cycles = r_solver.solve()
plot2 = Plot("r")
plot2.draw(cycles, points)
