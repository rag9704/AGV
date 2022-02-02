import networkx as nx
#from Graph import nx_Graph




def shortest_path_networkx(u,v,G="",starting_nodes_file = "",  ending_nodes_csv_file="", edge_length_file="", display=False):
    if G =="":
        G = nx_Graph(starting_nodes_csv_file, ending_nodes_csv_file, edge_length_file, display)

        r = nx.dijkstra_path(G, u, v, weight='edge_length_file')

    return r

print("shortest_path_network.py executed")
