from pulp import *

problem = LpProblem("Pizza_delivery", LpMinimize)

x_a1 = LpVariable("A_to_R1", lowBound = 0)
x_a2 = LpVariable("A_to_R2", lowBound = 0)
x_a3 = LpVariable("A_to_R3", lowBound = 0)
x_b1 = LpVariable("B_to_R1", lowBound = 0)
x_b2 = LpVariable("B_to_R2", lowBound = 0)
x_b3 = LpVariable("B_to_R3", lowBound = 0)

problem += 2*x_a1 + 4*x_a2 + 5*x_a3 + 3*x_b1 + 1*x_b2 + 3*x_b3

problem += x_a1 + x_a2 + x_a3 <=100
problem += x_b1 + x_b2 + x_b3 <= 80

problem += x_a1 + x_b1 == 60
problem += x_a2 + x_b2 == 70
problem += x_a3 + x_b3 == 50

problem.solve()

print("Статус:", LpStatus[problem.status])
print(f"A -> Район 1: {x_a1.value()} пицц")
print(f"A -> Район 2: {x_a2.value()} пицц")
print(f"A -> Район 3: {x_a3.value()} пицц")
print(f"B -> Район 1: {x_b1.value()} пицц")
print(f"B -> Район 2: {x_b2.value()} пицц")
print(f"B -> Район 3: {x_b3.value()} пицц")

print(f"Общая стоимость: {problem.objective.value()}")



