import networkx as nx
import matplotlib.pyplot as plt
from detect import load_network, detect_communities, get_node_communities

def based_importance_hiding(G, target_node, target_community, T=3):
    G_copy = G.copy()
    for _ in range(T):
        bet = nx.edge_betweenness_centrality(G_copy)
        edges = [(u, v) for u, v in bet if u == target_node or v == target_node]
        if not edges: break
        max_edge = max(edges, key=lambda e: bet[e] if (e[0] not in target_community or e[1] not in target_community) else -1)
        if max_edge[0] in target_community and max_edge[1] in target_community:
            continue
        G_copy.remove_edge(*max_edge)
        candidates = [(n, G_copy.degree(n)) for n in target_community if n != target_node and not G_copy.has_edge(target_node, n)]
        candidates.sort(key=lambda x: x[1], reverse=True)
        for node, _ in candidates[:2]:
            G_copy.add_edge(target_node, node)
    return G_copy

def visualize(G, node_communities, target_node, title):
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

    G = load_network(file_path)
    result = detect_communities(G)
    node_communities = get_node_communities(result)
    target_node = "Beak"
    target_community = result.communities[node_communities[target_node][0]]
    G_hidden = based_importance_hiding(G, target_node, target_community)
    result_hidden = detect_communities(G_hidden)
    node_communities_hidden = get_node_communities(result_hidden)
    visualize(G_hidden, node_communities_hidden, target_node, "Based Importance Hiding")
