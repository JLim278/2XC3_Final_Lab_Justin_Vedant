import min_heap


def dijkstra_approx(G, source, k):
    dist = {}
    relax_count = {}
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
        relax_count[node] = 0

    dist[source] = 0
    Q.decrease_key(source, 0)

    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        for neighbour in G.adj[current_node]:
            new_distance = dist[current_node] + G.w(current_node, neighbour)
            if new_distance < dist[neighbour] and relax_count[neighbour] < k:
                dist[neighbour] = new_distance
                relax_count[neighbour] += 1
                if neighbour in Q.map:
                    Q.decrease_key(neighbour, new_distance)

    return dist


def bellman_ford_approx(G, source, k):
    dist = {}
    relax_count = {}

    for node in G.adj:
        dist[node] = float("inf")
        relax_count[node] = 0

    dist[source] = 0

    for _ in range(G.number_of_nodes()):
        updated = False
        for u in G.adj:
            if dist[u] == float("inf"):
                continue
            for v in G.adj[u]:
                new_dist = dist[u] + G.w(u, v)
                if new_dist < dist[v] and relax_count[v] < k:
                    dist[v] = new_dist
                    relax_count[v] += 1
                    updated = True

        if not updated:
            break

    return dist