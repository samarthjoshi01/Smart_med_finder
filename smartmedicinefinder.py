import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import heapq

# Node and Store Definitions 
node_names = {
    0: "Aashu's home", 1: "H1", 2: "H2", 3: "Turn 1", 4: "Shop 1",
    5: "H3", 6: "Med2", 7: "Med1", 8: "Turn 2", 9: "Mahadev Temple",
    10: "CSIT Gate", 11: "Gate 1", 12: "Med3", 13: "Graphic Era Deemed to be University",
    14: "Vegetable Market", 15: "Gate 2", 16: "Church", 17: "Med7",
    18: "Graphic Era Hill University", 19: "Air Force", 20: "4-way (right side)",
    21: "Mess 1", 22: "Mess 2", 23: "4-way (left side)", 24: "Med6",
    25: "Med5", 26: "Turn 4", 27: "Turn 3", 28: "Sam's home", 29: "H4",
    30: "Turn 6", 31: "HDFC ATM", 32: "Med4"
}
store_nodes = {
    7: "Med1", 6: "Med2", 12: "Med3", 32: "Med4", 25: "Med5", 24: "Med6", 17: "Med7"
}
store_inventory = {
    "Med1": ["Acetaminophen", "Amoxicillin", "Ibuprofen", "Levothyroxine", "Pantoprazole"],
    "Med2": ["Losartan", "Azithromycin", "Cetirizine", "Doxycycline", "Ranitidine"],
    "Med3": ["Omeprazole", "Clopidogrel", "Amlodipine", "Salbutamol", "Montelukast"],
    "Med4": ["Metformin", "Insulin", "Acetaminophen", "Diclofenac", "Ranitidine"],
    "Med5": ["Atorvastatin", "Levothyroxine", "Omeprazole", "Hydroxychloroquine", "Montelukast"],
    "Med6": ["Ibuprofen", "Cetirizine", "Metformin", "Lisinopril", "Dexamethasone"],
    "Med7": ["Azithromycin", "Montelukast", "Insulin", "Pantoprazole", "Amlodipine"]
}

medicine_to_generic = {
    "Paracetamol": "Acetaminophen",
    "Crocin": "Acetaminophen",
    "Tylenol": "Acetaminophen",
    "Rantac": "Ranitidine",
    "Brufen": "Ibuprofen",
    "Zyrtec": "Cetirizine",
    "Augmentin": "Amoxicillin",
    "Synthroid": "Levothyroxine",
    "Pantocid": "Pantoprazole",
    "Zithromax": "Azithromycin",
    "Glucophage": "Metformin",
    "Plavix": "Clopidogrel",
    "Norvasc": "Amlodipine",
    "Ventolin": "Salbutamol",
    "Singulair": "Montelukast",
    "Lipitor": "Atorvastatin",
    "Plaquenil": "Hydroxychloroquine",
    "Prevacid": "Omeprazole",
    "Voltaren": "Diclofenac",
    "Prinivil": "Lisinopril",
    "Dexona": "Dexamethasone"
}

# Graph Construction 
def build_graph():
    G = nx.Graph()
    edges = [
        (0, 1, 1), (0, 3, 1), (0, 27, 1), (1, 2, 1), (3, 4, 1), (3, 7, 2),
        (4, 5, 1), (5, 6, 1), (7, 8, 1), (8, 9, 2), (8, 10, 1), (10, 11, 2),
        (11, 12, 1), (12, 13, 1), (13, 14, 2), (14, 15, 1), (14, 19, 3),
        (15, 16, 1), (16, 17, 1), (17, 18, 2), (20, 21, 1), (20, 16, 1),
        (20, 23, 1), (21, 22, 1), (21, 26, 2), (22, 23, 1), (23, 24, 1),
        (24, 25, 1), (25, 31, 2), (26, 27, 1), (27, 28, 1), (28, 29, 1),
        (28, 30, 2), (30, 31, 1), (31, 32, 1),
        (1, 0, 1), (2, 1, 1), (3, 0, 1), (4, 3, 1), (5, 4, 1), (6, 5, 1),
        (7, 3, 2), (8, 7, 1), (9, 8, 2), (10, 8, 1), (11, 10, 2), (12, 11, 1),
        (13, 12, 1), (14, 13, 2), (15, 14, 1), (19, 14, 3), (16, 15, 1),
        (17, 16, 1), (18, 17, 2), (21, 20, 1), (16, 20, 1), (23, 20, 1),
        (22, 21, 1), (26, 21, 2), (23, 22, 1), (24, 23, 1), (25, 24, 1),
        (31, 25, 2), (27, 26, 1), (28, 27, 1), (29, 28, 1), (30, 28, 2),
        (31, 30, 1), (32, 31, 1)
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    return G

# Dijkstra's Algorithm 
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph.nodes}
    previous = {node: None for node in graph.nodes}
    distances[start] = 0
    queue = [(0, start)]
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['weight']
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
    return distances, previous

def reconstruct_path(previous, start, end):
    path = []
    while end is not None:
        path.append(end)
        end = previous[end]
    path.reverse()
    return path if path[0] == start else []

# Drawing Graph with Multiple Paths
def draw_network_with_better_layout(G, paths=None):
    fig, ax = plt.subplots(figsize=(16, 10))
    pos = nx.kamada_kawai_layout(G)

    nx.draw(G, pos, with_labels=False, node_size=800, node_color='skyblue', edge_color='gray', ax=ax)
    nx.draw_networkx_labels(G, pos, labels=node_names, font_size=8, font_color='black', font_weight='bold', ax=ax)

    if paths:
        for path in paths:
            edge_path = list(zip(path, path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=edge_path, edge_color='red', width=3, ax=ax)

    plt.axis('off')
    st.pyplot(fig)

# Streamlit App
def main():
    st.set_page_config(page_title="Medicine Locator", layout="wide")

    st.markdown("""<div style="text-align:center; padding: 10px; border: 3px solid #4CAF50; border-radius: 10px; background-color: #e6ffe6;">
        <h1 style="color:#2e7d32;">💊 Medicine Locator & Generic Alternatives</h1>
    </div>""", unsafe_allow_html=True)

    st.markdown("Enter your prescription and location to find the nearest stores with available generic medicines.")

    meds_input = st.text_input("Enter medicines (comma-separated):", "")
    meds = [med.strip().capitalize() for med in meds_input.split(",")]
    location_input = st.text_input("Enter your location (e.g., H1, Med1, Gate 2):", "")

    if st.button("Find Medicines"):
        if not meds_input or not location_input:
            st.warning("Please enter both medicines and your current location.")
            return

        generic_meds = [medicine_to_generic.get(med.strip().capitalize(), med.strip().capitalize()) for med in meds_input.split(",")]
        
       
        st.subheader("Generic Alternatives:")
        for med, gen in zip(meds,generic_meds):
            st.write(f"**{med}** ➝ *{gen}*")
        
        G = build_graph()
        try:
            source = [k for k, v in node_names.items() if v.lower() == location_input.strip().lower()][0]
        except IndexError:
            st.error("Invalid location entered.")
            return

        distances, previous = dijkstra(G, source)
        med_results = {}
        paths = []

        for gen_med in generic_meds:
            found = False
            for node, store in store_nodes.items():
                if gen_med in store_inventory[store]:
                    path = reconstruct_path(previous, source, node)
                    if not path:
                        continue
                    total_dist = distances[node]
                    if gen_med not in med_results or total_dist < med_results[gen_med]['distance']:
                        med_results[gen_med] = {
                            'store': store,
                            'node': node,
                            'distance': total_dist,
                            'path': path
                        }
                        found = True
                        paths.append(path)  # Add path to the list
            if not found:
                med_results[gen_med] = None

        for med, info in med_results.items():
            if info:
                st.success(f"🧪 **{med}** is available at **{info['store']}** (Distance: {info['distance']})")
                st.markdown(f"**Path**: {' ➝ '.join(node_names[n] for n in info['path'])}")
            else:
                st.error(f"❌ {med} not found in nearby stores.")
        
        if paths:
            draw_network_with_better_layout(G, paths=paths)

if __name__ == "__main__":
    main()
