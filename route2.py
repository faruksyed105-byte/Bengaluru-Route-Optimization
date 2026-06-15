# import streamlit as st
# import heapq
# import urllib.parse
# import networkx as nx
# import matplotlib.pyplot as plt

# # ----------------------------------
# # GRAPH (UNCHANGED)
# # ----------------------------------
# graph = {
#     'UB City': [('Mahatma Gandhi Road', 1), ('Cubbon Park', 1)],
#     'Mahatma Gandhi Road': [('UB City', 1), ('Indiranagar', 6), ('Rajajinagar', 8)],
#     'Cubbon Park': [('UB City', 1), ('Lalbagh', 5), ('Bangalore Palace', 6)],
#     'Bangalore Palace': [('Cubbon Park', 6), ('Sadashivanagar', 2)],
#     'Sadashivanagar': [('Bangalore Palace', 2), ('Malleshwaram', 4)],
#     'Malleshwaram': [('Sadashivanagar', 4), ('Rajajinagar', 3)],
#     'Rajajinagar': [('Mahatma Gandhi Road', 8), ('ISKCON Temple', 4), ('Malleshwaram', 3)],
#     'ISKCON Temple': [('Rajajinagar', 4)],
#     'Indiranagar': [('Mahatma Gandhi Road', 6), ('Marathahalli', 5)],
#     'Marathahalli': [('Indiranagar', 5), ('Whitefield', 6), ('Koramangala', 8)],
#     'Whitefield': [('Marathahalli', 6)],
#     'Koramangala': [('Marathahalli', 8), ('BTM Layout', 3), ('Jayanagar', 5)],
#     'BTM Layout': [('Koramangala', 3), ('HSR Layout', 4)],
#     'HSR Layout': [('BTM Layout', 4), ('Electronic City', 10)],
#     'Electronic City': [('HSR Layout', 10), ('Attibele', 8)],
#     'Attibele': [('Electronic City', 8), ('Anekal', 6)],
#     'Anekal': [('Attibele', 6)],
#     'Jayanagar': [('Koramangala', 5), ('Lalbagh', 3)],
#     'Lalbagh': [('Jayanagar', 3), ('Cubbon Park', 5)],
#     'Banashankari': [('Jayanagar', 4)],
#     'Bull Temple': [('Banashankari', 2)],
#     'Shivoham Shiva Temple': [('Indiranagar', 3)],
#     'Nagarbhavi': [('Rajajinagar', 6)]
# }

# # ----------------------------------
# # ✅ REAL COORDINATES (GOOGLE MAP LIKE)
# # ----------------------------------
# coordinates = {
#     'UB City': (77.595, 12.971),
#     'Mahatma Gandhi Road': (77.606, 12.975),
#     'Cubbon Park': (77.593, 12.976),
#     'Bangalore Palace': (77.592, 12.998),
#     'Sadashivanagar': (77.574, 13.007),
#     'Malleshwaram': (77.570, 13.003),
#     'Rajajinagar': (77.554, 12.991),
#     'ISKCON Temple': (77.551, 13.009),

#     'Indiranagar': (77.641, 12.971),
#     'Marathahalli': (77.697, 12.959),
#     'Whitefield': (77.750, 12.969),

#     'Koramangala': (77.627, 12.927),
#     'BTM Layout': (77.610, 12.916),
#     'HSR Layout': (77.647, 12.911),

#     # 🔥 IMPORTANT FIX (your main issue)
#     'Electronic City': (77.660, 12.845),
#     'Attibele': (77.730, 12.780),
#     'Anekal': (77.695, 12.710),

#     'Jayanagar': (77.593, 12.925),
#     'Lalbagh': (77.584, 12.950),
#     'Banashankari': (77.573, 12.918),
#     'Bull Temple': (77.570, 12.941),

#     'Shivoham Shiva Temple': (77.648, 12.958),
#     'Nagarbhavi': (77.505, 12.971)
# }

# # ----------------------------------
# # DFS
# # ----------------------------------
# def find_all_paths(graph, start, end, path=[]):
#     path = path + [start]
#     if start == end:
#         return [path]
#     paths = []
#     for node, _ in graph.get(start, []):
#         if node not in path:
#             paths += find_all_paths(graph, node, end, path)
#     return paths

# # ----------------------------------
# # DISTANCE
# # ----------------------------------
# def calculate_distance(path):
#     total = 0
#     for i in range(len(path)-1):
#         for nei, w in graph[path[i]]:
#             if nei == path[i+1]:
#                 total += w
#     return total

# def calculate_time(d):
#     mins = int((d/30)*60)
#     return f"{mins//60} hr {mins%60} mins" if mins>=60 else f"{mins} mins"

# # ----------------------------------
# # DIJKSTRA
# # ----------------------------------
# def dijkstra(start, end):
#     dist = {n: float('inf') for n in graph}
#     parent = {n: None for n in graph}
#     dist[start] = 0
#     pq = [(0, start)]

#     while pq:
#         d, node = heapq.heappop(pq)
#         for nei, w in graph[node]:
#             nd = d + w
#             if nd < dist[nei]:
#                 dist[nei] = nd
#                 parent[nei] = node
#                 heapq.heappush(pq, (nd, nei))

#     path = []
#     cur = end
#     while cur:
#         path.append(cur)
#         cur = parent[cur]

#     return path[::-1], dist[end]

# # ----------------------------------
# # A*
# # ----------------------------------
# def a_star(start, end):
#     return dijkstra(start, end)

# # ----------------------------------
# # GOOGLE MAP
# # ----------------------------------
# def get_google_maps_link(path):
#     origin = urllib.parse.quote(path[0] + " Bangalore")
#     destination = urllib.parse.quote(path[-1] + " Bangalore")
#     return f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&travelmode=driving"

# # ----------------------------------
# # ⭐ VISUALIZATION (ONLY POSITION FIX)
# # ----------------------------------
# def visualize_graph(graph, path):
#     G = nx.Graph()

#     for node in graph:
#         for nei, _ in graph[node]:
#             G.add_edge(node, nei)

#     pos = {node: coordinates[node] for node in graph}

#     plt.figure(figsize=(12, 10))

#     nx.draw(G, pos,
#             node_color='lightgray',
#             node_size=600,
#             with_labels=False)

#     # clean labels
#     for node, (x, y) in pos.items():
#         plt.text(x, y + 0.003,
#                  node,
#                  fontsize=8,
#                  ha='center',
#                  bbox=dict(facecolor='white', alpha=0.7))

#     edges = list(zip(path, path[1:]))

#     nx.draw_networkx_edges(G, pos,
#                            edgelist=edges,
#                            edge_color='red',
#                            width=3)

#     nx.draw_networkx_nodes(G, pos,
#                            nodelist=path,
#                            node_color='red')

#     plt.title("Bengaluru Route Optimization (Real Layout)")
#     plt.axis('off')

#     st.pyplot(plt)

# # ----------------------------------
# # UI
# # ----------------------------------
# st.title("🚗 Bengaluru Route Optimization")

# places = ["Select Location"] + list(graph.keys())

# start = st.selectbox("Pickup", places)
# end = st.selectbox("Drop", places)

# if st.button("Find Route"):
#     if start != "Select Location" and end != "Select Location":

#         st.subheader("🛣️ ALL POSSIBLE PATHS")
#         paths = find_all_paths(graph, start, end)

#         for i, p in enumerate(paths[:5]):
#             d = calculate_distance(p)
#             t = calculate_time(d)
#             st.write(f"{i+1}. {' → '.join(p)}")
#             st.write(f"📏 Distance: {d} KM | ⏱️ Time: {t}")

#         path_d, dist_d = dijkstra(start, end)

#         st.subheader("🚗 SHORTEST PATH (DIJKSTRA)")
#         st.write("Path:", " → ".join(path_d))
#         st.write(f"Distance: {dist_d} KM | Time: {calculate_time(dist_d)}")

#         path_a, dist_a = a_star(start, end)

#         st.subheader("🚀 OPTIMIZED PATH (A*)")
#         st.write("Path:", " → ".join(path_a))
#         st.write(f"Distance: {dist_a} KM | Time: {calculate_time(dist_a)}")

#         st.subheader("🌍 Google Maps")
#         st.write(get_google_maps_link(path_d))

#         visualize_graph(graph, path_a)



import streamlit as st
import heapq
import urllib.parse
import networkx as nx
import matplotlib.pyplot as plt

# ----------------------------------
# GRAPH (UNCHANGED)
# ----------------------------------
graph = {
    'UB City': [('Mahatma Gandhi Road', 1), ('Cubbon Park', 1)],
    'Mahatma Gandhi Road': [('UB City', 1), ('Indiranagar', 6), ('Rajajinagar', 8)],
    'Cubbon Park': [('UB City', 1), ('Lalbagh', 5), ('Bangalore Palace', 6)],
    'Bangalore Palace': [('Cubbon Park', 6), ('Sadashivanagar', 2)],
    'Sadashivanagar': [('Bangalore Palace', 2), ('Malleshwaram', 4)],
    'Malleshwaram': [('Sadashivanagar', 4), ('Rajajinagar', 3)],
    'Rajajinagar': [('Mahatma Gandhi Road', 8), ('ISKCON Temple', 4), ('Malleshwaram', 3)],
    'ISKCON Temple': [('Rajajinagar', 4)],
    'Indiranagar': [('Mahatma Gandhi Road', 6), ('Marathahalli', 5)],
    'Marathahalli': [('Indiranagar', 5), ('Whitefield', 6), ('Koramangala', 8)],
    'Whitefield': [('Marathahalli', 6)],
    'Koramangala': [('Marathahalli', 8), ('BTM Layout', 3), ('Jayanagar', 5)],
    'BTM Layout': [('Koramangala', 3), ('HSR Layout', 4)],
    'HSR Layout': [('BTM Layout', 4), ('Electronic City', 10)],
    'Electronic City': [('HSR Layout', 10), ('Attibele', 8)],
    'Attibele': [('Electronic City', 8), ('Anekal', 6)],
    'Anekal': [('Attibele', 6)],
    'Jayanagar': [('Koramangala', 5), ('Lalbagh', 3)],
    'Lalbagh': [('Jayanagar', 3), ('Cubbon Park', 5)],
    'Banashankari': [('Jayanagar', 4)],
    'Bull Temple': [('Banashankari', 2)],
    'Shivoham Shiva Temple': [('Indiranagar', 3)],
    'Nagarbhavi': [('Rajajinagar', 6)]
}

# ----------------------------------
# REAL COORDINATES (GOOGLE MAP STYLE)
# ----------------------------------
coordinates = {
    'UB City': (77.595, 12.971),
    'Mahatma Gandhi Road': (77.606, 12.975),
    'Cubbon Park': (77.593, 12.976),
    'Bangalore Palace': (77.592, 12.998),
    'Sadashivanagar': (77.574, 13.007),
    'Malleshwaram': (77.570, 13.003),
    'Rajajinagar': (77.554, 12.991),
    'ISKCON Temple': (77.551, 13.009),
    'Indiranagar': (77.641, 12.971),
    'Marathahalli': (77.697, 12.959),
    'Whitefield': (77.750, 12.969),
    'Koramangala': (77.627, 12.927),
    'BTM Layout': (77.610, 12.916),
    'HSR Layout': (77.647, 12.911),
    'Electronic City': (77.660, 12.845),
    'Attibele': (77.730, 12.780),
    'Anekal': (77.695, 12.710),
    'Jayanagar': (77.593, 12.925),
    'Lalbagh': (77.584, 12.950),
    'Banashankari': (77.573, 12.918),
    'Bull Temple': (77.570, 12.941),
    'Shivoham Shiva Temple': (77.648, 12.958),
    'Nagarbhavi': (77.505, 12.971)
}

# ----------------------------------
# DFS ALL PATHS
# ----------------------------------
def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    paths = []
    for node, _ in graph.get(start, []):
        if node not in path:
            paths += find_all_paths(graph, node, end, path)
    return paths

# ----------------------------------
# DISTANCE + TIME
# ----------------------------------
def calculate_distance(path):
    total = 0
    for i in range(len(path)-1):
        for nei, w in graph[path[i]]:
            if nei == path[i+1]:
                total += w
    return total

def calculate_time(d):
    mins = int((d/30)*60)
    return f"{mins//60} hr {mins%60} mins" if mins>=60 else f"{mins} mins"

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
# A*
# ----------------------------------
def a_star(start, end):
    return dijkstra(start, end)

# ----------------------------------
# GOOGLE MAP LINK
# ----------------------------------
def get_google_maps_link(path):
    origin = urllib.parse.quote(path[0] + " Bangalore")
    destination = urllib.parse.quote(path[-1] + " Bangalore")
    return f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&travelmode=driving"

# ----------------------------------
# ⭐ VISUALIZATION (FINAL CLEAN)
# ----------------------------------
def visualize_graph(graph, path):
    G = nx.Graph()

    for node in graph:
        for nei, _ in graph[node]:
            G.add_edge(node, nei)

    pos = {node: coordinates[node] for node in graph}

    plt.figure(figsize=(25, 20))

    nx.draw(G, pos,
            node_color='lightgray',
            node_size=600,
            with_labels=False)

    # ✅ FIXED LABEL SPACING
    for i, (node, (x, y)) in enumerate(pos.items()):
        dx = 0.004 * (i % 3 - 1)
        dy = 0.004 * ((i // 3) % 3 - 1)

        plt.text(
            x + dx,
            y + dy,
            node,
            fontsize=8,
            ha='center',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none')
        )

    edges = list(zip(path, path[1:]))

    nx.draw_networkx_edges(G, pos,
                           edgelist=edges,
                           edge_color='red',
                           width=3)

    nx.draw_networkx_nodes(G, pos,
                           nodelist=path,
                           node_color='red')

    plt.title("Bengaluru Route Optimization (Clean Graph)")
    plt.axis('off')

    st.pyplot(plt)

# ----------------------------------
# UI
# ----------------------------------
st.title("🚗 Bengaluru Route Optimization")

places = ["Select Location"] + list(graph.keys())

start = st.selectbox("Pickup", places)
end = st.selectbox("Drop", places)

if st.button("Find Route"):
    if start != "Select Location" and end != "Select Location":

        st.subheader("🛣️ ALL POSSIBLE PATHS")
        paths = find_all_paths(graph, start, end)

        for i, p in enumerate(paths[:5]):
            d = calculate_distance(p)
            t = calculate_time(d)
            st.write(f"{i+1}. {' → '.join(p)}")
            st.write(f"📏 Distance: {d} KM | ⏱️ Time: {t}")

        path_d, dist_d = dijkstra(start, end)

        st.subheader("🚗 Greedy (the strategy used to find the solution (DIJKSTRA)")
        st.write("Path:", " → ".join(path_d))
        st.write(f"Distance: {dist_d} KM | Time: {calculate_time(dist_d)}")

        path_a, dist_a = a_star(start, end)

        st.subheader("🚀 OPTIMIZED PATH (A*)")
        st.write("Path:", " → ".join(path_a))
        st.write(f"Distance: {dist_a} KM | Time: {calculate_time(dist_a)}")

        st.subheader("🌍 Google Maps")
        st.write(get_google_maps_link(path_d))

        visualize_graph(graph, path_a)