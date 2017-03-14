import gurobi as gr


class Solver:

    def __init__(self, problem_instance):
        self.problem_instance = problem_instance
        self.mip = None

    def solve_routing(self):
        pass

    def generate_program(self):
        pass