import networkx as nx

def load_network(file_path):
    try:
        G = nx.read_gml(file_path)
        return G
    except Exception as e:
        print(f"Error loading network: {e}")
        return None

if __name__ == "__main__":
    file_path = r"C:\Users\91850\OneDrive\Desktop\pw1\static_network\dolphins.gml"

    G = load_network(file_path)
    if G is not None:
        print("Network loaded successfully!")
        print(f"Number of nodes: {G.number_of_nodes()}")
        print(f"Number of edges: {G.number_of_edges()}")
        print(f"Nodes: {list(G.nodes())[:10]}...")
        print(f"Edges: {list(G.edges())[:10]}...")
    else:
        print("Failed to load the network.")
