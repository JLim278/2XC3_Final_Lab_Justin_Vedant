import math
import time
import heapq
import random
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from pathlib import Path

# File Configuration
BASE = Path(__file__).resolve().parent
STATIONS_CSV = BASE / "london_stations.csv"
CONNECTIONS_CSV = BASE / "london_connections.csv"
OUT_DIR = BASE

# --- Core Math ---
def get_dist(lat1, lon1, lat2, lon2):
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))

# --- Graph Initialization ---
def init_net():
    df_st = pd.read_csv(STATIONS_CSV)
    df_cx = pd.read_csv(CONNECTIONS_CSV)
    pos, names, adj = {}, {}, defaultdict(dict)
    for row in df_st.itertuples(index=False):
        uid = int(row.id)
        pos[uid] = (float(row.latitude), float(row.longitude))
        names[uid] = str(row.name)
    for row in df_cx.itertuples(index=False):
        u, v, ln = int(row.station1), int(row.station2), int(row.line)
        w = get_dist(*pos[u], *pos[v])
        if v not in adj[u]:
            adj[u][v] = {'w': w, 'lns': set()}
            adj[v][u] = {'w': w, 'lns': set()}
        adj[u][v]['lns'].add(ln)
        adj[v][u]['lns'].add(ln)
    return adj, pos, names

# --- Routing & Transfers ---
def build_rte(prev, st, en):
    if st == en: return [st]
    if en not in prev: return []
    res = [en]
    curr = en
    while curr != st:
        curr = prev[curr]
        res.append(curr)
    return res[::-1]

def count_transfers(rte, adj):
    if len(rte) < 2: return 0
    transfers, cur_lns = 1, adj[rte[0]][rte[1]]['lns']
    for i in range(1, len(rte) - 1):
        nxt_lns = adj[rte[i]][rte[i+1]]['lns']
        shared = cur_lns.intersection(nxt_lns)
        if shared: cur_lns = shared
        else: transfers += 1; cur_lns = nxt_lns
    return transfers

# --- Pathfinding Algorithms ---
def run_dijk(adj, st, en):
    cost, prev, seen, exp = {st: 0.0}, {}, set(), 0
    pq = [(0.0, st)]
    while pq:
        c, u = heapq.heappop(pq)
        if u in seen: continue
        seen.add(u); exp += 1
        if u == en: break
        for v, data in adj[u].items():
            nc = c + data['w']
            if nc < cost.get(v, float('inf')):
                cost[v], prev[v] = nc, u
                heapq.heappush(pq, (nc, v))
    return cost.get(en, float('inf')), build_rte(prev, st, en), exp

def run_astar(adj, pos, st, en):
    e_lat, e_lon = pos[en]
    h_map = {n: get_dist(lat, lon, e_lat, e_lon) for n, (lat, lon) in pos.items()}
    cost, prev, seen, exp = {st: 0.0}, {}, set(), 0
    pq = [(h_map[st], 0.0, st)]
    while pq:
        f, c, u = heapq.heappop(pq)
        if u in seen: continue
        seen.add(u); exp += 1
        if u == en: break
        for v, data in adj[u].items():
            nc = c + data['w']
            if nc < cost.get(v, float('inf')):
                cost[v], prev[v] = nc, u
                heapq.heappush(pq, (nc + h_map[v], nc, v))
    return cost.get(en, float('inf')), build_rte(prev, st, en), exp

def bench_it(fn, reps=45):
    t0 = time.perf_counter()
    res = None
    for _ in range(reps): res = fn()
    return res, (time.perf_counter() - t0) / reps

# --- Main Suite ---
def start_experiments():
    adj, pos, names = init_net()
    nodes = list(pos.keys())
    random.seed(42)
    sample_set = random.sample(list(itertools.combinations(nodes, 2)), 120)

    c_blue, c_red, c_green = "#276CF5", "#F51C07", "#3EAB2C"

    rows = []
    print("="*40 + "\nLONDON NETWORK TRIPLE EXPERIMENT\n" + "="*40)
    for st, en in sample_set:
        raw_dist = get_dist(*pos[st], *pos[en])
        if raw_dist == 0: continue
        (_, _, d_exp), d_t = bench_it(lambda: run_dijk(adj, st, en))
        (a_km, a_rte, a_exp), a_t = bench_it(lambda: run_astar(adj, pos, st, en))
        if not a_rte: continue
        rows.append({
            "route": f"{names[st]} -> {names[en]}",
            "transfers": count_transfers(a_rte, adj),
            "km": a_km, "tort": a_km / raw_dist,
            "d_ms": d_t * 1000, "a_ms": a_t * 1000,
            "d_exp": d_exp, "a_exp": a_exp,
            "gain": d_t / a_t if a_t > 0 else 1
        })

    res_df = pd.DataFrame(rows)
    res_df.to_csv(OUT_DIR / "experiment_results.csv", index=False)

    # CHART 1: Transfer Analysis
    plt.figure(figsize=(8, 5))
    res_df.groupby('transfers')[['d_exp', 'a_exp']].mean().plot(kind='bar', color=[c_blue, c_red], ax=plt.gca(), edgecolor='black')
    plt.title("Exp 1: Search Effort by Line Complexity")
    plt.ylabel("Avg Nodes Expanded")
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.savefig(OUT_DIR / "results_transfer_effort.png")
    plt.close()

    # CHART 2: Speedup Scaling
    plt.figure(figsize=(8, 5))
    plt.scatter(res_df['km'], res_df['gain'], color=c_green, alpha=0.6, edgecolors='white')
    plt.axhline(1.0, color=c_red, linestyle='--')
    plt.title("Exp 2: A* Speedup vs. Journey Distance")
    plt.xlabel("Physical Distance (km)"); plt.ylabel("Speedup (Dijkstra/A*)")
    plt.savefig(OUT_DIR / "results_speedup_scaling.png")
    plt.close()

    # CHART 3: Tortuosity Impact
    plt.figure(figsize=(8, 5))
    plt.scatter(res_df['tort'], res_df['a_exp'], color=c_green, alpha=0.6, edgecolors='white')
    plt.title("Exp 3: Track Tortuosity vs. A* Performance")
    plt.xlabel("Tortuosity Ratio (Actual/Direct)"); plt.ylabel("Nodes Expanded")
    plt.savefig(OUT_DIR / "results_tortuosity_impact.png")
    plt.close()

    print(f"\nAll experiments complete. Outputs saved in {OUT_DIR}")

if __name__ == "__main__":
    start_experiments()