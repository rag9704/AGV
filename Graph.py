import numpy as np
import csv
import matplotlib.pyplot as plt
import networkx as nx
import json
from collections import defaultdict

with open("instance.json") as f:
    instance = json.load(f)

nodes = instance["nodes"]
edges = instance["edges"]
edges = [tuple(e) for e in edges]

pos = instance["pos"]
pos = {int(n): tuple(pos[n]) for n in pos}



def load_data_files(starting_nodes_file,ending_nodes_file,edge_file):

    starting_nodes = np.loadtxt(starting_nodes_file)
    ending_nodes   = np.loadtxt(ending_nodes_file)
    edge_length    = np.loadtxt(edge_file)

    return starting_nodes, ending_nodes, edge_length



def graph(starting_nodes_csv_file="", ending_nodes_csv_file="", edge_length_file = "", csv_export = False):

    starting_nodes_csv,ending_nodes_csv, edge_length_csv = load_data_files(starting_nodes_csv_file,
                                                                             ending_nodes_csv_file, edge_length_file)
    starting_nodes = [0]
    ending_nodes = []
    print
    for i in range(len(starting_nodes_csv)):
        if starting_nodes[-1] != starting_nodes_csv[i]:
            if starting_nodes_csv[i] in starting_nodes:
                ending_nodes[starting_nodes.index(starting_nodes_csv[i]-1)].append(ending_nodes_csv[i])
                print('1',starting_nodes_csv[i],ending_nodes_csv[i])
            else:
                starting_nodes.append(starting_nodes_csv[i])
                ending_nodes.append([ending_nodes_csv[i]])
                print('2',starting_nodes_csv[i],ending_nodes_csv[i])
            continue
        ending_nodes[-1].append(ending_nodes_csv[i])
    starting_nodes.remove(0)
    print(starting_nodes,ending_nodes)
    graphs = dict(zip(starting_nodes,ending_nodes))
    if csv_export:
        with open('csv files/graph.csv', 'w') as f :
            w = csv.writer(f)
            w.writerows(graphs.items())
        print('grapg.csv file created')
    return graphs

def Nx_json_graph(nodes,edge):
    edges = edge
    d1 = defaultdict(list)
    for k,v in edges:
        d1[k].append(v)
    graph = dict(d1)
    return graph
     
    

def nx_Graph(starting_nodes_csv_file="", ending_nodes_csv_file="", edge_length_file="", display=True):

    starting_nodes_csv,ending_nodes_csv, edge_length_csv = load_data_files(starting_nodes_csv_file,
                                                                             ending_nodes_csv_file, edge_length_file)

    G = nx.Graph()

    G.add_nodes_from(starting_nodes_csv)

    for i in range(len(starting_nodes_csv)):
        if display:
            print("Graph Data:")
            print("start: ", starting_nodes_csv[i], " end: ", ending_nodes_csv[i], " weight: ", edge_length_csv[i])
            print()
        G.add_edge(starting_nodes_csv[i], ending_nodes_csv[i], weight=edge_length_csv[i])

    if display:
        pos = nx.spring_layout(G)

        nx.draw_networkx_nodes(G,pos,node_size = 200)

        nx.draw_networkx_edges(G,pos,width = 6)

        nx.draw_networkx_labels(G,pos,font_size=8,font_family='sans-serif')

        plt.axis('off')
        plt.show()

    return G



def Nx_json(nodes,edges,pos,display = True):
    nodes = nodes
    edges = edges
    pos = pos

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    nx.set_edge_attributes(G, values = 1, name = 'weight')

    if display:
        nx.draw_networkx_nodes(G,pos,node_size = 200)
        nx.draw_networkx_edges(G,pos,width = 2)
        nx.draw_networkx_labels(G,pos,font_size=8,font_family='sans-serif')
        plt.axis('off')

        plt.show()

    return G
        
    
x=graph(r"starting_nodes.csv",r"ending_nodes.csv",r"lengths_of_edges.csv")
#nx_Graph(r"starting_nodes.csv",r"ending_nodes.csv",r"lengths_of_edges.csv", display=True)

print("Graph.py perfectly executed")










    
        

