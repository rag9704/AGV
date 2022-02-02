import pprint
from agvsim import Agent
from agvsim import AgentAction
from agvsim import Model
from agvsim import Environment
from agvsim import GlobalState
from agvsim import AGVSimulator
import json

#with open(r"C:\Users\Rag9704\Desktop\jija pd\AGV\Original\Final\instance.json") as f:
#    instance = json.load(f)

#nodes = instance["nodes"]

#edges = instance["edges"]
#edges = [tuple(e) for e in edges]

#pos =  instance["pos"]
#pos = {int(n): tuple(pos[n]) for n in pos}


#best = [[0, 2, 3], [4, 6, 7]]


def test_visualize(node,edge,poss,routes):
    """
    0-2-4--6
    | |    |
    1-3--5-7
    

    nodes = [0, 1, 2, 3, 4, 5, 6, 7]
    edges = [
        (0, 1),
        (0, 2),
        (2, 4),
        (2, 3),
        (4, 6),
        (1, 3),
        (3, 5),
        (5, 7),
        (6, 7),
    ]

    pos = {
        0: (0, 1),
        1: (0, 0),
        2: (1, 1),
        3: (1, 0),
        4: (2, 1),
        5: (3, 0),
        6: (4, 1),
        7: (4, 0),
    }
    
    
    """

    nodes = node
    edges = edge
    pos = poss
    
    agents = [Agent(v=0.2,task= [1, 2, 3],name=0) ]
    agent = agents[0]
    print("Agent".center(100, "="))
    print(agent.task)
    print(len(agent.task))
    print()

    print("Environment".center(100, "="))
    env = Environment(agents=agents, nodes=nodes, edges=edges, pos=pos)

    print()
    print("Model".center(100, "="))
    model = Model(env)
    print("velocity")
    agent.model = model
    print(agent.vel)
    print("to dict")
    print(agent.to_dict())
    print("observe")
    agent.model.observe()
    print("next action")
    print(agent.next_action)

    print("GlobalState".center(100, "="))
    state = GlobalState(agents)
    print("edge")
    print(state.agents[0].edge)
    print("update")
    state.update(1)
    state.update(1)
    print(state.agents[0].pos)
    print("history")
    print(state.history)
    print()
    
    print("AGVSimulator".center(100, "="))
    #agents = [Agent(v=0.2,task= [3, 2, 1],name=0)]
    agents = [Agent(v=0.2,task = routes[i],name=i) for i in range(len(routes))]
    
    env = Environment(agents=agents, nodes=nodes, edges=edges, pos=pos)
    sim = AGVSimulator(env)
    dt = 1
    step = 40

    sim.run(dt, step)
    print("history")
    pprint.pprint(sim.env.state.history)
    print()
    # print("agent 1")
    # history = [array - 1e-8 for array in sim.env.state.history[1]]
    # print(history)
    # print()
    #print(len(sim.env.state.history[0]))
    #print(len(sim.env.state.history[1]))
    #print(len(sim.env.state.history[2]))
    #print(sim.env.state.agents[0].edge_id)
    #print(sim.env.state.agents[1].edge_id)
    #print(sim.env.state.agents[2].edge_id)
    sim.to_animation("sample_collision_.gif")
    

    """
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    fig, ax = plt.subplots()
    def plot(frame):
        plt.cla()
        nx.draw(G, pos, with_labels=True)
        xs, ys = [], []
        for name, history in sim.env.state.history.items():
            x = history[frame][0]
            y = history[frame][1]
            xs.append(x)
            ys.append(y)
            ax.text(x, y, name)
        ax.scatter(xs, ys, s=100, c="lightgreen")
    ani = animation.FuncAnimation(fig, plot, frames=step, interval=200)
    ani.save("/root/data/sample_collision.gif", writer="pillow")
    plt.show()
    """

    
if __name__ == "__main__":
    test_visualize(nodes,edges,pos,best)
    

    


