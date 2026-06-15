import streamlit as st
import heapq
import urllib.parse
import random
import networkx as nx
import matplotlib.pyplot as plt

# ----------------------------------
# SESSION STATE
# ----------------------------------
if "result" not in st.session_state:
    st.session_state.result = None

# ----------------------------------
# GRAPH (ALL PLACES ADDED)
# ----------------------------------
graph = {
    'MG Road': [('Brigade Road', 1), ('Shivajinagar', 3)],
    'Brigade Road': [('MG Road', 1), ('Richmond Town', 2)],
    'Richmond Town': [('Brigade Road', 2)],
    'Shivajinagar': [('MG Road', 3), ('Vasanth Nagar', 2)],
    'Vasanth Nagar': [('Shivajinagar', 2), ('Malleshwaram', 4)],
    'Seshadripuram': [('Malleshwaram', 2)],

    'Malleshwaram': [('Vasanth Nagar', 4), ('Rajajinagar', 3), ('Seshadripuram', 2)],
    'Rajajinagar': [('Malleshwaram', 3), ('Yeshwanthpur', 4), ('Vijayanagar', 4)],
    'Yeshwanthpur': [('Rajajinagar', 4), ('Peenya', 5)],
    'Peenya': [('Yeshwanthpur', 5), ('Dasarahalli', 4)],
    'Dasarahalli': [('Peenya', 4)],

    'Basavanagudi': [('Chamrajpet', 2), ('Jayanagar', 3)],
    'Chamrajpet': [('Basavanagudi', 2)],
    'Jayanagar': [('Basavanagudi', 3), ('JP Nagar', 3), ('BTM Layout', 4)],
    'JP Nagar': [('Jayanagar', 3), ('Banashankari', 3)],
    'Banashankari': [('JP Nagar', 3), ('Kumaraswamy Layout', 3)],
    'Kumaraswamy Layout': [('Banashankari', 3), ('Uttarahalli', 4)],
    'Uttarahalli': [('Kumaraswamy Layout', 4), ('Kanakapura Road', 5)],
    'Kanakapura Road': [('Uttarahalli', 5)],

    'BTM Layout': [('Jayanagar', 4), ('HSR Layout', 4), ('Bannerghatta Road', 4)],
    'Bannerghatta Road': [('BTM Layout', 4)],
    'HSR Layout': [('BTM Layout', 4), ('Electronic City', 8), ('Sarjapur Road', 5)],
    'Sarjapur Road': [('HSR Layout', 5), ('Bellandur', 4)],
    'Bellandur': [('Sarjapur Road', 4), ('Marathahalli', 3)],

    'Marathahalli': [('Bellandur', 3), ('Whitefield', 6)],
    'Whitefield': [('Marathahalli', 6), ('Hoodi', 3)],
    'Hoodi': [('Whitefield', 3), ('KR Puram', 4)],
    'KR Puram': [('Hoodi', 4), ('CV Raman Nagar', 3)],
    'CV Raman Nagar': [('KR Puram', 3), ('Mahadevapura', 2)],
    'Mahadevapura': [('CV Raman Nagar', 2), ('Brookefield', 2)],
    'Brookefield': [('Mahadevapura', 2)],

    'Electronic City': [('HSR Layout', 8), ('Chandapura', 6)],
    'Chandapura': [('Electronic City', 6), ('Anekal', 5)],
    'Anekal': [('Chandapura', 5), ('Attibele', 4)],
    'Attibele': [('Anekal', 4)],

    'Indiranagar': [('Domlur', 3), ('CV Raman Nagar', 4)],
    'Domlur': [('Indiranagar', 3), ('Outer Ring Road', 3)],
    'Outer Ring Road': [('Domlur', 3), ('Kadubeesanahalli', 4)],
    'Kadubeesanahalli': [('Outer Ring Road', 4)],

    'Hebbal': [('Yelahanka', 5), ('RT Nagar', 3)],
    'Yelahanka': [('Hebbal', 5), ('Devanahalli', 6)],
    'Devanahalli': [('Yelahanka', 6)],
    'RT Nagar': [('Hebbal', 3), ('Sahakar Nagar', 2)],
    'Sahakar Nagar': [('RT Nagar', 2), ('Jakkur', 3)],
    'Jakkur': [('Sahakar Nagar', 3)],
    'Hennur': [('Nagawara', 3)],
    'Nagawara': [('Hennur', 3), ('Thanisandra', 3)],
    'Thanisandra': [('Nagawara', 3)],

    'Vijayanagar': [('Rajajinagar', 4), ('Nagarbhavi', 4)],
    'Nagarbhavi': [('Vijayanagar', 4), ('Kengeri', 6)],
    'Kengeri': [('Nagarbhavi', 6), ('Magadi Road', 5)],
    'Magadi Road': [('Kengeri', 5), ('Basaveshwaranagar', 3)],
    'Basaveshwaranagar': [('Magadi Road', 3)]
}

# ----------------------------------
# RANDOM COORDINATES (UNCHANGED STYLE)
# ----------------------------------
coordinates = {node: (random.random(), random.random()) for node in graph}

# ----------------------------------
# ALGORITHMS
# ----------------------------------
def find_all_paths(graph, start, end, path=None):
    if path is None:
        path = []
    path = path + [start]

    if start == end:
        return [path]

    paths = []
    for neighbor, _ in graph.get(start, []):
        if neighbor not in path:
            paths.extend(find_all_paths(graph, neighbor, end, path))
    return paths

def calculate_distance(path):
    total = 0
    for i in range(len(path)-1):
        for nei, w in graph[path[i]]:
            if nei == path[i+1]:
                total += w
                break
    return total

def calculate_time(distance):
    mins = int((distance / 30) * 60)
    return f"{mins//60} hr {mins%60} mins" if mins >= 60 else f"{mins} mins"

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
# GOOGLE MAP
# ----------------------------------
def get_google_maps_link(path):
    origin = urllib.parse.quote(path[0] + " Bangalore")
    destination = urllib.parse.quote(path[-1] + " Bangalore")

    return f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&travelmode=driving"

# ----------------------------------
# VISUALIZATION (ONLY LABEL FIX)
# ----------------------------------
def visualize_graph(graph, path):
    G = nx.Graph()

    for node in graph:
        for nei, _ in graph[node]:
            G.add_edge(node, nei)

    pos = coordinates

    plt.figure(figsize=(12, 9))

    nx.draw(G, pos, node_color='lightgray', node_size=600, with_labels=False)

    for i, (node, (x, y)) in enumerate(pos.items()):
        dx = 0.02 if i % 2 == 0 else -0.02
        dy = 0.02 if i % 3 == 0 else -0.02
        plt.text(x + dx, y + dy, node, fontsize=7,
                 bbox=dict(facecolor='white', alpha=0.6))

    edges = list(zip(path, path[1:]))

    nx.draw_networkx_edges(G, pos, edgelist=edges,
                           edge_color='red', width=3,
                           connectionstyle="arc3,rad=0.1")

    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red')

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

        st.subheader("All Paths")
        paths = find_all_paths(graph, start, end)

        for i, p in enumerate(paths[:5]):
            d = calculate_distance(p)
            st.write(f"{i+1}. {' → '.join(p)} | {d} KM")

        path, dist = dijkstra(start, end)

        st.subheader("Shortest Path")
        st.success(" → ".join(path))

        # GOOGLE MAP
        url = get_google_maps_link(path)
        st.markdown(f"[👉 Open in Google Maps]({url})")

        visualize_graph(graph, path)