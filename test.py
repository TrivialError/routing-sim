from gurobipy import *

m = Model("Quad Test")

x = m.addVar(vtype=GRB.INTEGER)
y = m.addVar(0, vtype=GRB.INTEGER)

m.setObjective(x*x + y, GRB.MINIMIZE)

m.addConstr()

m.optimize()

print(x.x)
