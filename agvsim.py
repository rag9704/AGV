from __future__ import annotations
import networkx as nx

from typing import Dict, List
from abc import ABC, abstractmethod

import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation


class Agent:
    def __init__(
        self,
        task: List[int],
        v: float = 0.0,
        a: float = 0.0,
        name: str | int = "",
    ) -> None:
        self.task = [(n, task[i + 1]) for i, n in enumerate(task[:-1])]
        self.v = v
        # self.v_func = lambda h: self.velocity*np.tanh(h)
        self.a = a
        self.name = name
        self._next_action = "move"
        self._action = AgentAction()
        self._safety_zone = 0.01
        self._wait_time = 0.0
        self._max_wait_time = int(1 / v)
        self._model = None
        self._pos = None
        self._vel = None
        self._acc = None
        self._edge_id = None
        self._edge = None

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def vel(self):
        return self._vel

    @vel.setter
    def vel(self, vel):
        self._vel = vel

    @property
    def acc(self):
        return self._acc

    @acc.setter
    def acc(self, acc):
        self._acc = acc

    @property
    def edge_id(self):
        return self._edge_id

    @edge_id.setter
    def edge_id(self, edge_id):
        self._edge_id = edge_id

    @property
    def edge(self):
        if self.edge_id >= len(self.task):
            return self.task[-1]
        else:
            return self.task[self.edge_id]

    @property
    def next_action(self):
        return self._next_action

    @next_action.setter
    def next_action(self, next_action):
        self._next_action = next_action

    @property
    def wait_time(self):
        return self._wait_time

    @wait_time.setter
    def wait_time(self, wait_time):
        self._wait_time = wait_time

    @property
    def max_wait_time(self):
        return self._max_wait_time

    @max_wait_time.setter
    def max_wait_time(self, max_wait_time):
        self._max_wait_time = max_wait_time

    @property
    def safety_zone(self):
        return self._safety_zone

    @safety_zone.setter
    def safety_zone(self, safety_zone):
        self._safety_zone = safety_zone

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        self._action = action

    def calc_vel(self):
        edge = self.task[self.edge_id]
        x0 = self.model.env.nodes_pos[edge[0]][0]
        y0 = self.model.env.nodes_pos[edge[0]][1]
        x1 = self.model.env.nodes_pos[edge[1]][0]
        y1 = self.model.env.nodes_pos[edge[1]][1]

        if x1 - x0 > 0:
            vx = self.v
        elif x1 - x0 == 0:
            vx = 0
        else:
            vx = -1 * self.v

        if y1 - y0 > 0:
            vy = self.v
        elif y1 - y0 == 0:
            vy = 0
        else:
            vy = -1 * self.v

        return np.array((vx, vy))

    def calc_acc(self):
        return np.array((0.0, 0.0))

    def to_dict(self):
        return {"edge": self.edge, "pos": self.pos, "velocity": self.vel}


class AgentAction:
    @staticmethod
    def move(agent, dt):
        env = agent.model.env
        new_pos = agent.pos + agent.vel * dt

        rom = (
            env.nodes_pos[agent.edge[1]][0] - env.nodes_pos[agent.edge[0]][0],
            env.nodes_pos[agent.edge[1]][1] - env.nodes_pos[agent.edge[0]][1],
        )

        sig_vx = np.sign(agent.vel[0])
        sig_vy = np.sign(agent.vel[1])

        res = (
            new_pos[0] - env.nodes_pos[agent.edge[0]][0] + sig_vx * 1e-8,
            new_pos[1] - env.nodes_pos[agent.edge[0]][1] + sig_vy * 1e-8,
        )

        if abs(res[0]) >= abs(rom[0]) and abs(res[1]) >= abs(rom[1]):
            agent.edge_id += 1
            if agent.edge_id < len(agent.task):
                agent.pos = env.nodes_pos[agent.edge[0]]
                agent.vel = agent.calc_vel()
                agent.acc = agent.calc_acc()
            else:
                agent.pos = new_pos
                agent.vel = np.array((0.0, 0.0))
                agent.acc = np.array((0.0, 0.0))
                return agent
        else:
            agent.vel = agent.calc_vel()
            agent.acc = agent.calc_acc()
            agent.pos = new_pos

        agent.wait_time = 0.0
        return agent

    @staticmethod
    def stop(agent, dt):
        agent.wait_time += dt
        if agent.wait_time >= agent.max_wait_time:
            agent.edge_id += 1
            agent.wait_time = 0.0
            agent.vel = agent.calc_vel()
            agent.acc = agent.calc_acc()
        return agent

    @staticmethod
    def collision(agent, dt):
        agent.wait_time += dt
        return agent


class Model:
    def __init__(self, env: Environment) -> None:
        self.env = env

    def observe(self):
        n_agents = len(self.env.state.agents)
        for i, j in itertools.combinations(range(n_agents), 2):
            ai = self.env.state.agents[i]
            aj = self.env.state.agents[j]
            u_ai_history = np.unique(self.env.state.history[ai.name], axis=0)
            u_aj_history = np.unique(self.env.state.history[aj.name], axis=0)
            if len(u_ai_history) != 1 and len(u_aj_history) != 1:
                diff = np.sqrt(((ai.pos - aj.pos) ** 2).sum())
                if diff < ai.safety_zone and diff < aj.safety_zone:
                    ai.next_action = "collision"
                    aj.next_action = "collision"

        for agent in self.env.state.agents:
            if agent.next_action != "collision":
                if agent.edge[0] != agent.edge[1]:
                    agent.next_action = "move"
                elif agent.edge[0] == agent.edge[1]:
                    agent.next_action = "stop"


class Environment:
    def __init__(self, agents: List[Agent], nodes: List, edges: List[tuple], pos: Dict):
        self.graph = nx.Graph()
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)
        self.nodes_pos = {node: np.array(pos[node], dtype="float") for node in pos}
        self.accumulated_wait_time = {node: [0.0] for node in nodes}
        self.time = [0.0]
        lim = (np.array([pos[node] for node in pos])).max(axis=0)
        self.xlim = (0, lim[0])
        self.ylim = (0, lim[1])
        for agent in agents:
            agent.edge_id = 0
            agent.pos = self.nodes_pos[agent.task[0][0]]
            agent.model = Model(self)
            agent.vel = agent.calc_vel()
            agent.acc = agent.calc_acc()
        self._state = GlobalState(agents)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def draw_map(
        self,
        node_color="gray",
        node_size=50,
        edge_color="gray",
        width=4,
        with_labels=False,
    ):
        nx.draw(
            self.graph,
            self.nodes_pos,
            node_color=node_color,
            node_size=node_size,
            edge_color=edge_color,
            width=width,
            with_labels=with_labels,
        )


class State(ABC):
    @property
    @abstractmethod
    def history(self):
        pass

    @abstractmethod
    def update(self):
        pass


class GlobalState(State):
    def __init__(self, agents: List[Agent]) -> None:
        self.agents = agents
        self._history = {agent.name: [agent.pos] for agent in agents}
        self._action_history = {agent.name: [agent.next_action] for agent in agents}

    @property
    def history(self):
        return self._history

    @property
    def action_history(self):
        return self._action_history

    def update(self, dt):
        next_actions = {}
        for agent in self.agents:
            agent.model.observe()
            next_actions[agent.name] = agent.next_action

        for agent in self.agents:
            if next_actions[agent.name] == "move":
                agent.action.move(agent, dt)
            elif next_actions[agent.name] == "stop":
                agent.action.stop(agent, dt)
            elif next_actions[agent.name] == "collision":
                agent.action.collision(agent, dt)
            self.history[agent.name].append(agent.pos)
            self.action_history[agent.name].append(agent.next_action)


class AGVSimulator:
    def __init__(self, env: Environment):
        self.env = env
        self._dt = None
        self._step = None

    def __repr__(self) -> str:
        return str(self.env.state)

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, step):
        self._step = step
    

    def run(self, dt: float, step: int):
        self.step = step
        
        for s in range(step):
            self.env.state.update(dt)
            self.env.time.append(step * dt)
            ns = [
                agent.edge[0]
                for agent in self.env.state.agents
                if agent.next_action == "stop" or agent.next_action == "collision"
            ]
            
            for node in self.env.graph.nodes:
                if node in ns:
                    t = self.env.accumulated_wait_time[node][-1] + dt
                else:
                    t = self.env.accumulated_wait_time[node][-1]
                self.env.accumulated_wait_time[node].append(t)

        
            

    def to_animation(
        self,
        save_file,
        show=True,
        figsize=(10, 6),
        interval=200,
        agv_size=100,
        agv_color="lightgreen",
        agv_marker=",",
        node_color="gray",
        node_size=50,
        edge_color="gray",
        width=4,
        with_labels=True,
    ):
        fig, ax = plt.subplots(figsize=figsize)
        action_history = np.array(list(self.env.state.action_history.values()))

        def _plot(frame):
            plt.cla()
            nx.draw(
                self.env.graph,
                self.env.nodes_pos,
                ax=ax,
                node_color=node_color,
                node_size=node_size,
                edge_color=edge_color,
                width=width,
                with_labels=with_labels,
            )

            xs, ys = [], []
            for name, history in self.env.state.history.items():
                x = history[frame][0]
                y = history[frame][1]

                xs.append(x)
                ys.append(y)

                ax.text(x, y, name)

            """

            for node in self.env.graph.nodes:
                t = self.env.accumulated_wait_time[node][frame]
                if t != 0.0:
                    x, y = self.env.nodes_pos[node]
                    circle = plt.Circle((x, y), 0.01 * t, color='k')
                    ax.add_artist(circle)
            """

            ax.scatter(xs, ys, s=agv_size, c=agv_color, marker=agv_marker)

            r_move = sum(action_history[:, frame] == "move") / len(action_history) * 100
            r_stop = 100.0 - r_move

            text = (
                "Move:"
                + "{:.1f}".format(r_move).center(8, " ")
                + "%,"
                + "Wait:".rjust(8, " ")
                + "{:.1f}".format(r_stop).center(8, " ")
                + "%"
            )
            ax.text(0, -1, text)

        ani = animation.FuncAnimation(
            fig, _plot, frames=self.step + 1, interval=interval
        )
        ani.save(save_file, writer="pillow")
        if show:
            plt.show()
"""
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
    5: (2, 0),
    6: (3, 1),
    7: (3, 0),
    }

agent = Agent(v=0.2, task=[0, 1, 3, 5, 7, 6], name=0)


env = Environment(agents=[agent], nodes=nodes, edges=edges, pos=pos)

env.draw_map(with_labels=True)
plt.show()

"""
