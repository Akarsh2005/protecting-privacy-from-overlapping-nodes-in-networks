import networkx as nx
from cdlib import algorithms
import matplotlib.pyplot as plt


def load_network(file_path):
    try:
        G = nx.read_gml(file_path)
        return G
    except Exception as e:
        print(f"Error loading network: {e}")
        return None


def detect_communities(G):
    try:
        if not G.is_directed():
            return algorithms.kclique(G, k=3)
        else:
            return algorithms.kclique(G.to_undirected(), k=3)
    except Exception as e:
        print(f"Error in community detection: {e}")
        return None


def get_node_communities(result):
    node_communities = {}
    for i, community in enumerate(result.communities):
        for node in community:
            node_communities.setdefault(node, []).append(i)
    return node_communities


# ─────────── ✅ Visualization Function ─────────── #
def visualize_network(
    G, node_communities, target_node=None, title="Network Visualization"
):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    colors = ["red", "blue", "green", "purple", "orange", "cyan", "yellow"]
    node_colors = {}

    for node in G.nodes():
        comms = node_communities.get(node, [])
        if node == target_node:
            node_colors[node] = "black"
        elif comms:
            node_colors[node] = colors[comms[0] % len(colors)]
        else:
            node_colors[node] = "grey"

    nx.draw_networkx_nodes(
        G, pos, node_color=[node_colors[n] for n in G.nodes()], node_size=300
    )
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.title(title)
    plt.axis("off")
    plt.show()


# ─────────── ✅ MAIN EXECUTION ─────────── #
if __name__ == "__main__":
    file_path = r"C:\Users\91850\OneDrive\Desktop\pw1\static_network\dolphins.gml"

    target_node = "Beak"  # optional: highlight overlapping node

    G = load_network(file_path)
    if G is None:
        print("Failed to load the network.")
    else:
        result = detect_communities(G)
        if result is None:
            print("Failed to detect communities.")
        else:
            node_communities = get_node_communities(result)
            print(f"Number of communities detected: {len(result.communities)}")
            for i, comm in enumerate(result.communities):
                print(f"Community {i}: {comm}")

            overlapping = {
                node: comms
                for node, comms in node_communities.items()
                if len(comms) > 1
            }
            if overlapping:
                for node, comms in overlapping.items():
                    print(f"Node {node}: Communities {comms}")
            else:
                print("No nodes found in overlapping communities.")

            visualize_network(
                G,
                node_communities,
                target_node,
                title="Original Network with Communities",
            )
