from instance_parser import euclidean_parser
from solvers.greedy_nearest_neighbor import GreedyNearestNeighbor
from solvers.greedy_cycle import GreedyCycle
from solvers.regret import RegretSolver
from graph_plotting.plot import Plot
import numpy as np


def calculate_cycle_len(matrix, cycles):
    total = 0
    for cycle in cycles:
        for i, node in enumerate(cycle):
            total += matrix[cycle[i-1]][node]
    return total


def main():
    files = ["instances/kroA100.tsp", "instances/kroB100.tsp"]
    file = files[0]

    p = euclidean_parser.EuclideanParser()
    matrix = p.parse(file)
    points = p.get_points()

    best_greedy_nn = None
    best_greedy_cycle = None
    best_regret_cycle = None
    nn_distances = np.array([0 for _ in range(100)], dtype=np.int32)
    gc_distances = np.array([0 for _ in range(100)], dtype=np.int32)
    r_distances = np.array([0 for _ in range(100)], dtype=np.int32)

    for i in range(0, 100):
        print(f"Running {i}. simulation")
        nn_solver = GreedyNearestNeighbor(matrix)
        gc_solver = GreedyCycle(matrix)
        r_solver = RegretSolver(matrix)

        nn_cycles = nn_solver.solve()
        distance = calculate_cycle_len(matrix, nn_cycles)
        if distance > np.max(nn_distances):
            best_greedy_nn = nn_cycles
        nn_distances[i] = distance

        gc_cycles = gc_solver.solve()
        distance = calculate_cycle_len(matrix, gc_cycles)
        if distance > np.max(gc_distances):
            best_greedy_cycle = gc_cycles
        gc_distances[i] = distance

        r_cycles = r_solver.solve()
        distance = calculate_cycle_len(matrix, r_cycles)
        if distance > np.max(r_distances):
            best_regret_cycle = r_cycles
        r_distances[i] = distance

    print("--- GREEDY NEAREST NEIGHBOUR ---")
    print(f"MIN: {np.min(nn_distances)};  MAX: {np.max(nn_distances)};  AVG: {np.mean(nn_distances)}")
    plot = Plot("nn")
    plot.draw(best_greedy_nn, points)

    print("--- GREEDY CYCLE ---")
    print(f"MIN: {np.min(gc_distances)};  MAX: {np.max(gc_distances)};  AVG: {np.mean(gc_distances)}")
    plot2 = Plot("c")
    plot2.draw(best_greedy_cycle, points)

    print("--- 2-REGRET CYCLE ---")
    print(f"MIN: {np.min(r_distances)};  MAX: {np.max(r_distances)};  AVG: {np.mean(r_distances)}")
    plot3 = Plot("r")
    plot3.draw(best_regret_cycle, points)


if __name__ == "__main__":
    main()
else:
    print("IMO")
