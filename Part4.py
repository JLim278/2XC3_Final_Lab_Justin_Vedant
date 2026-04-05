from final_project_part1 import DirectedWeightedGraph, dijkstra, bellman_ford
from part2_implementation import a_star


class Graph:
    def adjacent_nodes(self, node):
        pass

    def add_node(self, node):
        pass

    def add_edge(self, node1, node2, weight):
        pass

    def number_of_nodes(self):
        pass


class WeightedGraph(DirectedWeightedGraph, Graph):
    pass


class HeuristicGraph(WeightedGraph):
    def __init__(self):
        super().__init__()
        self.heuristic = {}

    def set_heuristic(self, heuristic):
        self.heuristic = heuristic

    def get_heuristic(self):
        return self.heuristic


class SPAlgorithm:
    def calc_sp(self, graph, source, dest):
        pass


class Dijkstra(SPAlgorithm):
    def calc_sp(self, graph, source, dest):
        dist = dijkstra(graph, source)
        return dist[dest]


class Bellman_Ford(SPAlgorithm):
    def calc_sp(self, graph, source, dest):
        dist = bellman_ford(graph, source)
        return dist[dest]


class A_Star(SPAlgorithm):
    def calc_sp(self, graph, source, dest):
        converted_graph = {}
        for node in graph.adj:
            converted_graph[node] = {}
            for neighbour in graph.adj[node]:
                converted_graph[node][neighbour] = graph.w(node, neighbour)
        _, path = a_star(converted_graph, source, dest, graph.get_heuristic())
        if not path:
            return float("inf")
        return sum(graph.w(path[i], path[i + 1]) for i in range(len(path) - 1))


class ShortPathFinder:
    def __init__(self):
        self.graph = None
        self.algorithm = None

    def set_graph(self, graph):
        self.graph = graph

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def calc_short_path(self, source, dest):
        return self.algorithm.calc_sp(self.graph, source, dest)