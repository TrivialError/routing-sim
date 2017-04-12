import networkx as nx
from simulator.road import *
from solver.solver import *
from itertools import *
from simulator.agent import *


class Generator:

    # shortest_path_dict is a map from a pair of nodes to the shortest path between them in the problem_state graph
    # shortest_distance_dict is a map from a pair of nodes to the length of the shortest path between them
    def __init__(self, problem_state):

        self.problem_state = problem_state
        self.problem_state_graph = None
        self.problem_instance_graph = None

        self.shortest_path_dict = dict()
        self.shortest_distance_dict = dict()

        self.targets = None

    def generate_problem_instance(self):

        self.build_problem_state_graph()

        self.build_problem_instance_graph()

    def build_problem_state_graph(self):
        self.problem_state_graph = nx.Graph()

        intersections = [intersection for intersection in self.problem_state.intersections
                         if not intersection.depot]
        roads = self.problem_state.roads
        pickups = self.problem_state.pickups
        agents = self.problem_state.agents
        depots = [intersection for intersection in self.problem_state.intersections
                  if intersection.depot]

        connections = []

        for agent_pickup in self.problem_state.agents + self.problem_state.pickups:
            road = agent_pickup.position[0]
            length = agent_pickup.position[0].length
            progress = agent_pickup.position[1]
            connections.append(Road((road.ends[0], agent_pickup), progress))
            connections.append(Road((road.ends[1], agent_pickup), length - progress))

        for agent in self.problem_state.agents:
            for pickup in self.problem_state.pickups:
                if agent.position[0] == pickup.position[0]:
                    connections.append(Road((agent, pickup), abs(agent.position[1] - pickup.position[1])))

        edges = [road.ends for road in roads + connections]
        nodes = intersections + pickups + agents + depots

        self.problem_state_graph.add_nodes_from(nodes)
        self.problem_state_graph.add_edges_from(edges)

        print('******************')


        return self.problem_state_graph

    def build_problem_instance_graph(self):
        self.problem_instance_graph = nx.Graph()

        depots = [intersection for intersection in self.problem_state.intersections
                  if intersection.depot]

        entities = self.problem_state.agents + self.problem_state.pickups + depots

        for (entity1, entity2) in product(entities, entities):
            if isinstance(entity1, Agent) and isinstance(entity2, Agent):
                continue
            path = nx.dijkstra_path(self.problem_state_graph, source=entity1, target=entity2, weight='length')
            length = 0
            for i in range(len(path) - 1):
                road = Road.find_by_ends((path[i], path[i+1]))
                length += road.length
            self.shortest_distance_dict[frozenset([entity1, entity2])] = length
            self.shortest_path_dict[frozenset([entity1, entity2])] = path
            self.problem_instance_graph.add_edge(entity1, entity2, {'length': length})

        return self.problem_instance_graph

    def get_targets(self):
        solver = Solver(self.problem_instance_graph, self.problem_state)
        solver.generate_program()
        solver.solve_routing()

        # TODO: convert solved qip into routes using dictionaries in Generator
        self.targets = None
        return self.targets
