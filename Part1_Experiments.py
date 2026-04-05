import time
import matplotlib.pyplot as plt

from final_project_part1 import (
    create_random_complete_graph,
    dijkstra,
    bellman_ford,
    total_dist
)
from part1_approx import dijkstra_approx, bellman_ford_approx


def average_runtime(func, graph, source, k=None, trials=5):
    total = 0
    for _ in range(trials):
        start = time.perf_counter()
        if k is None:
            func(graph, source)
        else:
            func(graph, source, k)
        end = time.perf_counter()
        total += (end - start)
    return total / trials


def show_and_save(filename):
    plt.savefig(filename, bbox_inches="tight")
    plt.show()
    plt.close()


# EXPERIMENT 1
# Runtime vs k
# Fix one complete graph and vary k

def experiment_1():
    n = 80
    upper = 20
    source = 0
    k_values = [1, 2, 3, 5, 10, 20]

    G = create_random_complete_graph(n, upper)

    dijkstra_times = []
    bellman_times = []

    for k in k_values:
        dijkstra_times.append(average_runtime(dijkstra_approx, G, source, k))
        bellman_times.append(average_runtime(bellman_ford_approx, G, source, k))

    plt.figure(figsize=(10, 6))
    plt.plot(k_values, dijkstra_times, marker="o", label="Dijkstra Approx")
    plt.plot(k_values, bellman_times, marker="o", label="Bellman-Ford Approx")
    plt.xlabel("k")
    plt.ylabel("Average runtime (seconds)")
    plt.title("Experiment 1: Runtime vs k")
    plt.grid(True)
    plt.legend()
    show_and_save("exp1_runtime_vs_k.png")


# EXPERIMENT 2
# Total distance vs k
# Fix one complete graph and vary k

def experiment_2():
    n = 80
    upper = 20
    source = 0
    k_values = [1, 2, 3, 5, 10, 20]

    G = create_random_complete_graph(n, upper)

    exact_total = total_dist(dijkstra(G, source))

    dijkstra_totals = []
    bellman_totals = []

    for k in k_values:
        dijkstra_totals.append(total_dist(dijkstra_approx(G, source, k)))
        bellman_totals.append(total_dist(bellman_ford_approx(G, source, k)))

    plt.figure(figsize=(10, 6))
    plt.plot(k_values, dijkstra_totals, marker="o", label="Dijkstra Approx")
    plt.plot(k_values, bellman_totals, marker="o", label="Bellman-Ford Approx")
    plt.axhline(exact_total, color="green", linestyle="--", label="Exact total distance")
    plt.xlabel("k")
    plt.ylabel("Total distance")
    plt.title("Experiment 2: Total Distance vs k")
    plt.grid(True)
    plt.legend()
    show_and_save("exp2_total_distance_vs_k.png")


# EXPERIMENT 3
# Runtime vs graph size
# Fix k and vary number of nodes

def experiment_3():
    sizes = [30, 60, 90, 120, 150, 180]
    upper = 20
    source = 0
    k = 3

    dijkstra_times = []
    bellman_times = []

    for n in sizes:
        G = create_random_complete_graph(n, upper)
        dijkstra_times.append(average_runtime(dijkstra_approx, G, source, k, trials=8))
        bellman_times.append(average_runtime(bellman_ford_approx, G, source, k, trials=8))

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, dijkstra_times, marker="o", label="Dijkstra Approx")
    plt.plot(sizes, bellman_times, marker="o", label="Bellman-Ford Approx")
    plt.xlabel("Num of nodes")
    plt.ylabel("Average runtime (seconds)")
    plt.title("Experiment 3: Runtime vs Graph Size")
    plt.grid(True)
    plt.legend()
    show_and_save("exp3_runtime_vs_graph_size.png")


if __name__ == "__main__":
    experiment_1()
    experiment_2()
    experiment_3()