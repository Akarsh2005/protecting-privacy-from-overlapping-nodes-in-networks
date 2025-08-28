import networkx as nx
from detect import load_network, detect_communities, get_node_communities
from detect_random import random_hiding  # Change this to other algorithms if needed
from detect_degree import degree_hiding
from visualize import visualize_network  # ✅ Fix this line

def evaluate_hiding(G_original, G_modified, target_node, communities_original, communities_modified):
    original_comms = len(communities_original.get(target_node, []))
    modified_comms = len(communities_modified.get(target_node, []))
    if original_comms <= 1:
        return 1.0
    return max(0, (original_comms - modified_comms) / (original_comms - 1))

if __name__ == "__main__":
    file_path = r"C:\Users\91850\OneDrive\Desktop\pw1\static_network\dolphins.gml"
    target_node = "Beak"

    G = load_network(file_path)
    result_original = detect_communities(G)
    if result_original is None:
        print("Community detection failed on original graph.")
        exit()

    communities_original = get_node_communities(result_original)
    community_ids = communities_original.get(target_node, [])
    if not community_ids:
        print(f"No communities found for node {target_node}")
        exit()

    target_community = result_original.communities[community_ids[0]]

    # 🟨 Run hiding algorithm here
    G_hidden = degree_hiding(G, target_node, target_community, T=3)

    result_hidden = detect_communities(G_hidden)
    if result_hidden is None:
        print("Community detection failed on modified graph.")
        exit()

    communities_hidden = get_node_communities(result_hidden)

    score = evaluate_hiding(G, G_hidden, target_node, communities_original, communities_hidden)
    print(f"Hiding accuracy for {target_node}: {score:.2f}")

    visualize_network(G_hidden, communities_hidden, target_node, title="After Hiding")
