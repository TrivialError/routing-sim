import networkx as nx
import matplotlib.pyplot as plt
from common import *
from simulator.pickup import *
from simulator.road import *


class Arena:
    def __init__(self, problem_state):
        self.problem_state = problem_state

        self.intersections = None
        self.roads = None
        self.pickups = None
        self.agents = None
        self.depots = None

        self.intersections_with_pos = None
        self.pickups_with_pos = None
        self.agents_with_pos = None
        self.depots_with_pos = None

        self.graph = nx.Graph()
        self.nodes_with_pos = None

        self.target_roads = None

    def build(self):
        self.intersections = [intersection for intersection in self.problem_state.intersections
                              if not intersection.depot]
        self.roads = self.problem_state.roads
        self.pickups = self.problem_state.pickups
        self.agents = self.problem_state.agents
        self.depots = [intersection for intersection in self.problem_state.intersections
                       if intersection.depot]

        edges = [road.ends for road in self.roads]
        nodes = self.intersections + self.pickups + self.agents

        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)

        self.intersections_with_pos = {intersection: intersection.location for intersection in self.intersections}
        self.depots_with_pos = {depot: depot.location for depot in self.depots}
        self.pickups_with_pos = {pickup: position_to_location(pickup.position[0], pickup.position[1])
                                 for pickup in self.pickups}
        self.agents_with_pos = {agent: position_to_location(agent.position[0], agent.position[1])
                                for agent in self.agents}

        self.nodes_with_pos = {**self.intersections_with_pos, **self.pickups_with_pos,
                               **self.agents_with_pos, **self.depots_with_pos}

        self.target_roads = {}
        for agent in self.problem_state.agents:
            last_dest = agent
            for dest in agent.route:
                if isinstance(dest, Pickup):
                    continue

                road = (last_dest, dest)
                self.target_roads[road] = agent.color
                last_dest = dest

    def draw(self, save=False, filename=None):
        plt.figure(figsize=(25, 15), facecolor="#FFFFFF")

        ax = plt.subplot(111)
        pos1 = ax.get_position()  # get the original position
        pos2 = [pos1.x0 - 0.1, pos1.y0 - 0.08, pos1.width * 1.25, pos1.height * 1.2]
        ax.set_position(pos2)  # set a new position

        nx.draw_networkx_nodes(self.graph, nodelist=self.depots, node_size=300,
                               pos=self.depots_with_pos, node_color='black')
        nx.draw_networkx_nodes(self.graph, nodelist=self.intersections, node_size=100,
                               pos=self.intersections_with_pos, node_color='b')
        nx.draw_networkx_nodes(self.graph, nodelist=self.pickups, node_size=100,
                               pos=self.pickups_with_pos, node_color='r')
        nx.draw_networkx_edges(self.graph, pos=self.nodes_with_pos)
        for agent in self.problem_state.agents:
            nx.draw_networkx_nodes(self.graph, nodelist=[agent], node_size=150,
                                   pos=self.agents_with_pos, node_color=agent.color)

        if self.target_roads:
            roads, colors = zip(*self.target_roads.items())
            nx.draw_networkx_edges(self.graph, pos=self.nodes_with_pos, width=2.0, edgelist=roads, edge_color=colors)

        # nx.draw_networkx_labels(self.graph, self.nodes_with_pos, self.nodes_with_pos, font_size=10)

        # nx.draw_networkx_edge_labels(self.graph, self.nodes_with_pos, edge_labels=self.roads)

        plt.axis("off")

        if save:
            plt.savefig(filename)
        else:
            plt.show()
