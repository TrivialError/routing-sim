import networkx as nx


class Generator:

    def __init__(self, problem_state):

        self.problem_state = problem_state
        self.problem_instance = None

    def generate_problem_instance(self):
        pass
        # find shortest distances from agents to all pickups and depots (and store corresponding paths)

        # build graph of shortest distances
