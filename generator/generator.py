import networkx as nx


class Generator:

    # shortest_path_dict is a map from a pair of nodes to the shortest path between them in the problem_state graph
    # shortest_distance_dict is a map from a pair of nodes to the length of the shortest path between them
    def __init__(self, problem_state):

        self.problem_state = problem_state
        self.problem_state_graph = None
        self.problem_instance_graph = None

        self.shortest_path_dict = dict()
        self.shortest_distance_dict = dict()

    def generate_problem_instance(self):

        self.build_problem_state_graph()

        self.build_problem_instance_graph()

    def build_problem_state_graph(self):
        problem_state_graph = nx.Graph()

        intersections = [intersection for intersection in self.problem_state.intersections
                         if not intersection.depot]
        roads = self.problem_state.roads
        pickups = self.problem_state.pickups
        agents = self.problem_state.agents
        depots = [intersection for intersection in self.problem_state.intersections
                  if intersection.depot]

        edges = [road.ends for road in roads]
        nodes = intersections + pickups + agents + depots

        self.problem_state_graph.add_nodes_from(nodes)
        self.problem_state_graph.add_edges_from(edges)

        return problem_state_graph

    def build_problem_instance_graph(self):
        problem_instance_graph = nx.Graph()

        # TODO: finish this

        return problem_instance_graph
