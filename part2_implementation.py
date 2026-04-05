import heapq

def a_star(G, s, d, h):
    q = [(h[s], s)]
    prev = {}
    g = {s: 0}
    seen = set()
    
    while q:
        _, curr = heapq.heappop(q)
        
        if curr in seen:
            continue
        seen.add(curr)
        
        if curr == d:
            path = []
            node = curr
            while node != s:
                path.append(node)
                node = prev[node]
            path.append(s)
            return (prev, path[::-1])
            
        for nxt, cost in G.get(curr, {}).items():
            if nxt in seen:
                continue
                
            new_g = g[curr] + cost
            
            if new_g < g.get(nxt, float('inf')):
                prev[nxt] = curr
                g[nxt] = new_g
                f = new_g + h.get(nxt, float('inf'))
                heapq.heappush(q, (f, nxt))
                
    return (prev, [])