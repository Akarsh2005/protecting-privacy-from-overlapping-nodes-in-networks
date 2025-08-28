import networkx as nx
import random
import matplotlib.pyplot as plt
from detect import load_network, detect_communities, get_node_communities

def random_hiding(G, target_node, target_community, T=3):
    """Randomly hides target node by adding/removing edges."""
    G_copy = G.copy()
    for _ in range(T):
        if random.random() < 0.5:
            # Add edge inside community
            non_neighbors = [
                n for n in target_community
                if n != target_node and not G_copy.has_edge(target_node, n)
            ]
            if non_neighbors:
                G_copy.add_edge(target_node, random.choice(non_neighbors))
        else:
            # Remove edge outside community
            neighbors = [
                n for n in G_copy.neighbors(target_node)
                if n not in target_community
            ]
            if neighbors:
                G_copy.remove_edge(target_node, random.choice(neighbors))
    return G_copy

def visualize(G, node_communities, target_node, title):
    """Draws network with communities and highlights target node."""
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan']
    node_colors = []
    for node in G.nodes():
        if node == target_node:
            node_colors.append('black')
        else:
            comms = node_communities.get(node, [])
            node_colors.append(colors[comms[0] % len(colors)] if comms else 'grey')
    nx.draw_networkx(G, pos, node_color=node_colors, with_labels=True, node_size=300)
    plt.title(title)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    file_path = r"C:\Users\91850\OneDrive\Desktop\pw1\static_network\dolphins.gml"
    target_node = "Beak"

    # Load network
    G = load_network(file_path)

    # Detect original communities
    result = detect_communities(G)
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

    # Hide target node randomly
    target_community = result.communities[node_communities[target_node][0]]
    G_hidden = random_hiding(G, target_node, target_community)

    # Detect communities after hiding
    result_hidden = detect_communities(G_hidden)
    node_communities_hidden = get_node_communities(result_hidden)

    print("\nAfter Random Hiding:")
    print(f"Number of communities detected: {len(result_hidden.communities)}")
    for i, comm in enumerate(result_hidden.communities):
        print(f"Community {i}: {comm}")

    overlapping_hidden = {
        node: comms
        for node, comms in node_communities_hidden.items()
        if len(comms) > 1
    }
    if overlapping_hidden:
        for node, comms in overlapping_hidden.items():
            print(f"Node {node}: Communities {comms}")
    else:
        print("No nodes found in overlapping communities.")

    # Visualize modified network
    visualize(G_hidden, node_communities_hidden, target_node, "Random Hiding")
