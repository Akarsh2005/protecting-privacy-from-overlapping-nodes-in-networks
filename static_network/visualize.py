import networkx as nx
import matplotlib.pyplot as plt

def visualize_network(G, node_communities, target_node=None, title="Network Visualization"):
    # Use a spring layout with a fixed seed for consistent layout
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(10, 8))

    # Get a colormap with many distinct colors
    cmap = plt.cm.get_cmap('tab20')  # supports 20 colors
    node_colors = []

    for node in G.nodes():
        comms = node_communities.get(node, [])
        if node == target_node:
            color = 'black'  # Highlight the target node
        elif comms:
            color = cmap(comms[0] % 20)  # Pick first community ID for color
        else:
            color = 'grey'  # Node not in any community
        node_colors.append(color)

    # Draw nodes, edges, and labels
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=300, edgecolors='white')
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    nx.draw_networkx_labels(G, pos, font_size=8)

    plt.title(title, fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    from detect import load_network, detect_communities, get_node_communities

    file_path = r"C:\Users\91850\OneDrive\Desktop\pw1\dolphins.gml"
    G = load_network(file_path)
    result = detect_communities(G)

    if result is None:
        print("Community detection failed.")
    else:
        node_communities = get_node_communities(result)
        target_node = "Beak"
        visualize_network(G, node_communities, target_node, title="Original Dolphin Network")

