import time
import math
import matplotlib.pyplot as plt

from final_project_part1 import (
    DirectedWeightedGraph,
    create_random_complete_graph,
    mystery
)


def average_runtime(func, graph, trials=3):
    total = 0
    for _ in range(trials):
        start = time.perf_counter()
        func(graph)
        end = time.perf_counter()
        total += (end - start)
    return total / trials


def show_and_save(filename):
    plt.savefig(filename, bbox_inches="tight")
    plt.show()
    plt.close()


# TEST 1
# Small positive-weight graph

def test_positive_graph():
    G = DirectedWeightedGraph()

    for i in range(4):
        G.add_node(i)

    G.add_edge(0, 1, 1)
    G.add_edge(0, 2, 4)
    G.add_edge(1, 2, 2)
    G.add_edge(1, 3, 6)
    G.add_edge(2, 3, 1)

    result = mystery(G)

    print("Mystery output on positive-weight graph:")
    for row in result:
        print(row)


# TEST 2
# Small graph with a negative edge but no negative cycle

def test_negative_edge_graph():
    G = DirectedWeightedGraph()

    for i in range(4):
        G.add_node(i)

    G.add_edge(0, 1, 4)
    G.add_edge(0, 2, 5)
    G.add_edge(1, 2, -2)
    G.add_edge(2, 3, 3)
    G.add_edge(1, 3, 6)

    result = mystery(G)

    print("\nMystery output on negative-edge graph:")
    for row in result:
        print(row)


# EXPERIMENT
# Log-log plot for mystery runtime

def experiment_mystery_runtime():
    sizes = [10, 20, 30, 40, 50, 60]
    upper = 20
    runtimes = []

    for n in sizes:
        G = create_random_complete_graph(n, upper)
        runtimes.append(average_runtime(mystery, G, trials=3))

    log_sizes = [math.log(x) for x in sizes]
    log_runtimes = [math.log(y) for y in runtimes]

    plt.figure(figsize=(10, 6))
    plt.plot(log_sizes, log_runtimes, marker="o", color="purple")
    plt.xlabel("log(num of Nodes)")
    plt.ylabel("log(avg runtime in secs)")
    plt.title("Mystery Algorithm_Log-Log")
    plt.grid(True)
    show_and_save("mystery_loglog_plot.png")

    print("\nGraph sizes tested:", sizes)
    print("Measured runtimes:", runtimes)


if __name__ == "__main__":
    test_positive_graph()
    test_negative_edge_graph()
    experiment_mystery_runtime()