import numpy as np
from overlap_count import overlap_count
import numpy as np
import time
from Q_1 import QConstructor
import openjij as oj
from file_1 import three_routes_all_agvs,graph, nx_Graph
from dwave.system.samplers import DWaveSampler
from dwave_qbsolv import QBSolv
from segement import nodes_2_segment_dict, segments_2_nodes_dict
import json
from Classical_solver import Q_dict,selection_rules,routes_from_selection_rule,best_nodes,best_routes



def main(n,r,loc,source,destination,qc):
    with open(loc) as f:
         instance = json.load(f)
    nodes = instance["nodes"]

    edges = instance["edges"]
    edges = [tuple(e) for e in edges]

    pos = instance["pos"]
    pos = {int(n): tuple(pos[n]) for n in pos}

    graph_ = graph(nodes,edges)
    G      = nx_Graph(nodes,edges,pos)

    source_ = source
    destination_ = destination
    n = len(source)

    root_function = three_routes_all_agvs(G,graph_,n,source,destination)
    ns_dict = nodes_2_segment_dict(graph_)
    sn_dict = segments_2_nodes_dict(ns_dict)
    root = root_function
    Q = QConstructor(root, make_csv=False, r=3)
    Qdict = Q_dict(Q)

    if qc.get() == False:
        sampler = oj.SASampler()
        start = time.clock()
        response = sampler.sample_qubo(Q=Qdict)       #using OpenJij
        dict_solution = response.first.sample         #using openjij
        qb_solution = [dict_solution]                 #using openJij
        end = time.clock()

    elif qc.get() == True:
        start = time.clock()
        response = QBSolv().sample_qubo(Qdict) #Dwave
        qb_solution = list(response.samples()) #Dwave
        end = time.clock()
    
    selection_rules_ = selection_rules(qb_solution, 3)
    best_routes_nodes = routes_from_selection_rule(root, selection_rules_)
    #best = best_nodes(best_routes_nodes,sn_dict)
    best_ = best_routes(best_routes_nodes,sn_dict,source_)
    
    #print("best nodes :",best_)
    #print("Overlap :",overlap_count(best_))
    elasped = end-start
    

    return best_,elasped

    
def main_1(nodes,edges,pos,source,destination,qc):
    
    nodes = nodes
    print("nodes :",nodes)

    edges = edges

    pos = pos
    
    pos = {i: tuple(pos[i]) for i in range(len(nodes))}

    graph_ = graph(nodes,edges)
    G      = nx_Graph(nodes,edges,pos)

    source_ = source
    destination_ = destination
    n = len(source)

    root_function = three_routes_all_agvs(G,graph_,n,source,destination)
    ns_dict = nodes_2_segment_dict(graph_)
    sn_dict = segments_2_nodes_dict(ns_dict)
    root = root_function
    Q = QConstructor(root, make_csv=False, r=3)
    Qdict = Q_dict(Q)

    sampler = oj.SASampler()

    if qc.get() == False:
        sampler = oj.SASampler()
        start = time.clock()
        response = sampler.sample_qubo(Q=Qdict)       #using OpenJij
        dict_solution = response.first.sample         #using openjij
        qb_solution = [dict_solution]                 #using openJij
        end = time.clock()

    elif qc.get() == True:
        start = time.clock()
        response = QBSolv().sample_qubo(Qdict) #Dwave
        qb_solution = list(response.samples()) #Dwave
        end = time.clock()
    
    selection_rules_ = selection_rules(qb_solution, 3)
    best_routes_nodes = routes_from_selection_rule(root, selection_rules_)
    #best = best_nodes(best_routes_nodes,sn_dict)
    best_ = best_routes(best_routes_nodes,sn_dict,source_)
    
    #print("best nodes :",best_)
    #print("Overlap :",overlap_count(best_))
    elasped = end-start
    

    return best_,elasped
