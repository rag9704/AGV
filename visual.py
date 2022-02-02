from agvsim import Agent
from agvsim import AgentAction
from agvsim import Model
from agvsim import Environment
from agvsim import GlobalState
from agvsim import AGVSimulator
import json

with open(r"C:\Users\Rag9704\Desktop\jija pd\AGV\Original\Final\instance.json") as f:
    instance = json.load(f)

nodes = instance["nodes"]

edges = instance["edges"]
edges = [tuple(e) for e in edges]

pos =  instance["pos"]
pos = {int(n): tuple(pos[n]) for n in pos}


best = [[3, 2, 1], [11, 10, 9]]


def visual(nodes,edges,pos,routes):
    agents = [Agent(v=0.2,task= routes[i],name=i) for i in range(len(routes))]

    #agents = [Agent(v = 0.2, task = [3,2,1],name = 0),
     #         Agent(v = 0.2, task = [11,10,9], name = 1)]

    
    env = Environment(agents=agents, nodes=nodes, edges=edges, pos=pos)
    sim = AGVSimulator(env)
    dt = 1
    step = 40
    sim.run(dt,step)
    sim.to_animation("sample_collision_2.gif")
    
                
if __name__ == "__main__":
    visual(nodes,edges,pos,best)
