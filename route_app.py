import heapq
import webbrowser
import urllib.parse
import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt

# ----------------------------------
# GRAPH (BENGALURU)
# ----------------------------------
graph = {
    'Anekal': [('Attibele', 6)],
    'Attibele': [('Anekal', 6), ('Electronic City', 8)],
    'Electronic City': [('Attibele', 8), ('HSR Layout', 10)],
    'HSR Layout': [('Electronic City', 10), ('BTM Layout', 4)],
    'BTM Layout': [('HSR Layout', 4), ('Koramangala', 3)],
    'Koramangala': [('BTM Layout', 3), ('Jayanagar', 5), ('Marathahalli', 8)],
    'Jayanagar': [('Koramangala', 5), ('Lalbagh', 3)],
    'Lalbagh': [('Jayanagar', 3), ('Cubbon Park', 5)],
    'Cubbon Park': [('Lalbagh', 5), ('Mahatma Gandhi Road', 2)],
    'Mahatma Gandhi Road': [('Cubbon Park', 2), ('Indiranagar', 6), ('Rajajinagar', 8)],
    'Indiranagar': [('Mahatma Gandhi Road', 6), ('Marathahalli', 5)],
    'Marathahalli': [('Indiranagar', 5), ('Whitefield', 6)],
    'Whitefield': [('Marathahalli', 6)],
    'Rajajinagar': [('Mahatma Gandhi Road', 8), ('ISKCON Temple', 4)],
    'ISKCON Temple': [('Rajajinagar', 4)]
}

# ----------------------------------
# GOOGLE MAPS NAMES
# ----------------------------------
place_map = {p: p + " Bangalore" for p in graph}

# ----------------------------------
# DFS (ALL PATHS)
# ----------------------------------
def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]

    paths = []
    for neighbor, _ in graph.get(start, []):
        if neighbor not in path:
            paths.extend(find_all_paths(graph, neighbor, end, path))
    return paths

# ----------------------------------
# DISTANCE
# ----------------------------------
def calculate_distance(path):
    total = 0
    for i in range(len(path)-1):
        for nei, w in graph[path[i]]:
            if nei == path[i+1]:
                total += w
                break
    return total

# ----------------------------------
# TIME (HR + MINS)
# ----------------------------------
def calculate_time(distance):
    mins = int((distance / 30) * 60)
    h = mins // 60
    m = mins % 60
    return f"{h} hr {m} mins" if h else f"{m} mins"

# ----------------------------------
# DIJKSTRA
# ----------------------------------
def dijkstra(start, end):
    dist = {n: float('inf') for n in graph}
    parent = {n: None for n in graph}
    dist[start] = 0

    pq = [(0, start)]

    while pq:
        d, node = heapq.heappop(pq)
        if node == end:
            break

        for nei, w in graph[node]:
            nd = d + w
            if nd < dist[nei]:
                dist[nei] = nd
                parent[nei] = node
                heapq.heappush(pq, (nd, nei))

    path = []
    cur = end
    while cur:
        path.append(cur)
        cur = parent[cur]

    return path[::-1], dist[end]

# ----------------------------------
# A* (OPTIONAL)
# ----------------------------------
def a_star(start, end):
    return dijkstra(start, end)  # simplified

# ----------------------------------
# GOOGLE MAPS
# ----------------------------------
def open_maps(path):
    base = "https://www.google.com/maps/dir/?api=1"
    o = urllib.parse.quote(place_map[path[0]])
    d = urllib.parse.quote(place_map[path[-1]])
    url = f"{base}&origin={o}&destination={d}&travelmode=driving"
    webbrowser.open(url)

# ----------------------------------
# VISUALIZATION
# ----------------------------------
def visualize(path):
    G = nx.Graph()

    for node in graph:
        for nei, _ in graph[node]:
            G.add_edge(node, nei)

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(8,6))
    nx.draw(G, pos, node_color='lightgray', with_labels=True)

    edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=3)
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red')

    plt.title("Route Visualization")
    plt.show()

# ----------------------------------
# GUI FUNCTION
# ----------------------------------
def find_route():
    start = start_var.get()
    end = end_var.get()

    all_paths = find_all_paths(graph, start, end)

    result = ""

    for i, p in enumerate(all_paths[:3]):
        d = calculate_distance(p)
        t = calculate_time(d)
        result += f"{i+1}. {' → '.join(p)}\n   {d} KM | {t}\n\n"

    path, dist = dijkstra(start, end)

    result += "\nSHORTEST PATH:\n"
    result += f"{' → '.join(path)}\n{dist} KM | {calculate_time(dist)}"

    output_text.set(result)

    global current_path
    current_path = path

# ----------------------------------
# GUI SETUP
# ----------------------------------
root = tk.Tk()
root.title("🚗 Route Optimizer (Uber Style)")
root.geometry("550x600")

places = list(graph.keys())

start_var = tk.StringVar()
end_var = tk.StringVar()

tk.Label(root, text="Pickup Location").pack(pady=5)
ttk.Combobox(root, textvariable=start_var, values=places).pack()

tk.Label(root, text="Drop Location").pack(pady=5)
ttk.Combobox(root, textvariable=end_var, values=places).pack()

tk.Button(root, text="Find Route", command=find_route).pack(pady=10)

output_text = tk.StringVar()
tk.Label(root, textvariable=output_text, wraplength=500, justify="left").pack(pady=10)

tk.Button(root, text="📊 Show Graph", command=lambda: visualize(current_path)).pack(pady=5)
tk.Button(root, text="🌍 Open Google Maps", command=lambda: open_maps(current_path)).pack(pady=5)

root.mainloop()