import networkx as nx
from load import load_network
from detect import detect_communities, get_node_communities
from evaluate import random_hiding, betweenness_hiding, bhh_hiding, degree_hiding, evaluate_hiding
from visualize import visualize_network

def main():
    # Load the dolphin network
    file_path = r"C:\Users\91850\OneDrive\Desktop\pw1\dolphins.gml"
    G = load_network(file_path)
    if G is None:
        print("Failed to load network")
        return
    
    # Detect communities
    result = detect_communities(G)
    if result is None:
        print("Failed to detect communities")
        return
    node_communities = get_node_communities(result)
    
    # Find a node in overlapping communities (more than one community)
    target_node = None
    for node, comms in node_communities.items():
        if len(comms) > 1:
            target_node = node
            break
    
    if target_node is None:
        print("No node found in overlapping communities")
        return
    
    # Select the first community as the target community
    target_community_idx = node_communities[target_node][0]
    target_community = result.communities[target_community_idx]
    
    print(f"Target node: {target_node}, in communities: {node_communities[target_node]}")
    print(f"Target community: {target_community}")
    
    # Visualize original network
    visualize_network(G, node_communities, target_node, "Original Dolphin Network")
    
    # Apply hiding algorithms
    hiding_algorithms = [
        ("Random Hiding", random_hiding),
        ("Betweenness Hiding", betweenness_hiding),
        ("BHH Hiding", bhh_hiding),
        ("Degree Hiding", degree_hiding)
    ]
    
    for name, hiding_func in hiding_algorithms:
        G_modified = hiding_func(G, target_node, target_community, T=3)
        modified_result = detect_communities(G_modified)
        modified_communities = get_node_communities(modified_result)
        
        # Evaluate hiding effectiveness
        accuracy = evaluate_hiding(G, G_modified, target_node, node_communities, modified_communities)
        print(f"{name} Accuracy: {accuracy:.2f}")
        
        # Visualize modified network
        visualize_network(G_modified, modified_communities, target_node, f"{name} Modified Network")

if __name__ == "__main__":
    main()