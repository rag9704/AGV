#from Graph import graph
#import pandas as pd
#graphs = graph(r"C:\Users\Rag9704\Desktop\jija pd\AGV\Original\starting_nodes.csv",
#               r"C:\Users\Rag9704\Desktop\jija pd\AGV\Original\ending_nodes.csv",
#               r"C:\Users\Rag9704\Desktop\jija pd\AGV\Original\lengths_of_edges.csv")



def nodes_2_segment_dict(graph):
    """Returns a dictionary with KEYS: nodes and VALUES: segments"""

    key = []

    # this loop generates the key
    for i in graph:
        for j in graph[i]:
            key.append((i, j))
            key.append((j, i))

    ns_dict = {**{key[i]: i for i in range(0,len(key),2)},**{key[i]: i-1 for i in range(1,len(key),2)}}
    #ns_dict = {key[i]: i for i in range(len(key))}

    


    return ns_dict


def segments_2_nodes_dict(nodes_to_segment_dict):
    """Returns a dictionary with KEYS: segments and VALUES: nodes
    Inverting the above dictionary."""

    sn_dict = {v: k for k, v in nodes_to_segment_dict.items()}

    return sn_dict

print("Segment.py perfectly executed")
