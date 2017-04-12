from gurobipy import *
from itertools import *

LARGE_CONST = 10000


class Solver:
    def __init__(self, problem_instance_graph, problem_state):
        self.problem_instance_graph = problem_instance_graph
        self.problem_state = problem_state
        self.qip_model = None

    def generate_program(self):
        agents = self.problem_state.agents
        pickups = self.problem_state.pickups
        depots = [intersection for intersection in self.problem_state.intersections if intersection.depot]

        entities = agents + pickups + depots

        paths = [frozenset([end1, end2]) for (end1, end2) in self.problem_instance_graph.edges() if end1 != end2]
        print(paths)
        print('***********BITCH')
        model = Model('quad_routing')

        agent_path_vars = model.addVars(paths, agents, vtype=GRB.BINARY)

        pickup_sizes = {pickup: pickup.size for pickup in self.problem_state.pickups}
        path_lengths = {frozenset([tup[0], tup[1]]): tup[2]['length']
                        for tup in self.problem_instance_graph.edges(data=True)}

        model.addConstrs(agent_path_vars.sum(i, '*', '*') <= 1 for i in pickups)

        # TODO: fix this to work with the frozensets used elsewhere
        #   problem is that direction along edges is irrelevant with current formulation, so this constraint
        #   does nothing. Needs to be that sum of incident edges to every node is either 0 or 2
        model.addConstrs(agent_path_vars.sum(frozenset(['*', i]), v) == agent_path_vars.sum(frozenset([i, '*']), v)
                         for i in pickups + agents for v in agents if i != v)

        print(path_lengths)
        print('************')
        print(agent_path_vars)

        objective =\
            quicksum(
                quicksum(path_lengths[frozenset([i, j])] * agent_path_vars[frozenset([i, j]), v]
                         for i in entities for j in entities if i != j) *
                quicksum(pickup_sizes[i] * agent_path_vars[frozenset([i, j]), v]
                         for i in pickups for j in entities if i != j)
                for v in agents)\
            - LARGE_CONST * quicksum(
                pickup_sizes[i] * agent_path_vars[frozenset([i, j]), v]
                for i in pickups for j in entities for v in agents if i != j and j != v and v != i)

        model.setObjective(objective)

        model.optimize()

        solution = model.getAttr('x', agent_path_vars)
        print(solution)

    def solve_routing(self):
        pass
