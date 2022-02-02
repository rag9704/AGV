import networkx as nx
from itertools import islice
#from Graph import nx_Graph

def find_all_paths_networkx(graph,start,end):
    print("Searching all paths")

    all_paths = list(nx.shortest_simple_paths(graph,start,end))

    # all_paths = list(nx.all_simple_paths(graph,start, end, cutoff = 500))
    # all_paths.sort(key=len)

    return all_paths

def k_shortest_paths(G,source,target,k):

    return list(islice(nx.shortest_simple_paths(G,source,target),k))

#G = nx_Graph(r"starting_nodes.csv",r"ending_nodes.csv",r"lengths_of_edges.csv", display=True)

print("all_paths.py executed")
