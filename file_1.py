import numpy as np
import csv
import matplotlib.pyplot as plt
import networkx as nx
from segement import nodes_2_segment_dict
from shortest_path_networkx import shortest_path_networkx
from all_paths import k_shortest_paths
from collections import defaultdict
#import json


def nx_Graph(nodes,edges,pos,display = False):
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

def graph(nodes,edge):
    edges = edge
    d1 = defaultdict(list)
    for k,v in edges:
        d1[k].append(v)
    graph = dict(d1)

    return graph


def find_all_paths_in_segments(ns_dict,agv_paths):

    all_paths_segments =[]
    one_path_segments = []

    for i in range(len(agv_paths)):
        for j in range(0,len(agv_paths[i])-1):
            
            one_path_segments.append(ns_dict[(agv_paths[i][j],agv_paths[i][j+1])])
            #print(ns_dict[(agv_paths[i][j],agv_paths[i][j+1])])
        all_paths_segments.append(one_path_segments)
        one_path_segments = []

    return all_paths_segments


def intersection_length(list1,list2):
    return len(set(list1).intersection(list2))

def union_length(list1,list2):
    return len(list(set(list1) | set(list2)))


def diff_list(list1,list2):
    return list(set(list1).symmetric_difference(set(list2)))

def max_dis(all_paths_segments, lists):
    "gives maximally dissimilar paths"

    max_dis_list = []

    for i in all_paths_segments:
        max_dis_list.append(intersection_length(lists,i))

    arg_min_path = all_paths_segments[np.argmin(max_dis_list)]
    
    return arg_min_path



def three_paths(graph,G,start,end):
    # shortest_path = shortest_path_networkx(start, end, G)


    # finding the value of r by using 50pc of djkistra path length
    # r = 0.5*nx.dijkstra_path_length(G, start, end)

    # print("r: ", r)


    # all_agv_paths = find_all_paths_dj(G, start, end, r)

    # find k number of paths between start and end, beginning with the shortest path.
    all_agv_paths = k_shortest_paths(G, start, end, 50)

    # print("All agv paths : ", len(all_car_paths))

    shortest_path = all_agv_paths[0]

    # all_agv_paths = find_all_paths_networkx(G, start, end)
    ns_dict = nodes_2_segment_dict(graph)

    all_agv_paths_segments = find_all_paths_in_segments(ns_dict, all_agv_paths)

    list1 = find_all_paths_in_segments(ns_dict, [shortest_path])[0]
    list2 = max_dis(all_agv_paths_segments, list1)

    #print('1 :',all_agv_paths_segments)

    x  = find_all_paths_in_segments(ns_dict, all_agv_paths)
    #print(x)
    x.remove(list1)
    x.remove(list2)
    #print(x)

    union_list =  (list1+list2)

    #list3 = max_dis(all_agv_paths_segments, union_list)
    list3 = max_dis(x, union_list)

    #print(list1,list2,list3)

    return list1, list2, list3



def three_routes_all_agvs(G,graph,n,source,destination):

    big_three_paths_of_agv = []
    big_export_list        = []

    for i in range(n):
        start = source[i]
        end   = destination[i]
        #x = three_paths(graph,G,start,end)
        #print(x)

        three_paths_of_agv = list(three_paths(graph,G,start,end))

        export_list = [i,start,end,three_paths_of_agv]
        big_export_list.append(export_list)

        big_three_paths_of_agv.append(three_paths_of_agv)

    route_dict = {j: big_three_paths_of_agv[j] for j in range(n)}

    print("three_routes_all_cars function executed")

    return route_dict


#graph =graph(r"starting_nodes.csv",r"ending_nodes.csv",r"lengths_of_edges.csv")
#G     =nx_Graph(r"starting_nodes.csv",r"ending_nodes.csv",r"lengths_of_edges.csv", display=True)
#print(three_routes_all_agvs(G,graph,2,[1,4],[4,6]))








    
        

