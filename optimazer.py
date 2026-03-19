from pulp import *
import pandas as pd
import argparse

def load_data(filepath):
    df = pd.read_csv(filepath)

    warehouses = {}
    for _, row in df.iterrows():
        warehouses[row["from"]] = row["supply"]
    
    stores = {}
    for _, row in df.iterrows():
        stores[row["to"]] = row["demand"]

    costs = {}
    for _, row in df.iterrows():
        costs[(row["from"], row["to"])] = row["cost"]

    return warehouses, stores,costs


def solve(warehouses, stores, costs):
    problem = LpProblem("Supply_Chain", LpMinimize)

    x = {}
    for s in warehouses:
        for m in stores:
            x[(s,m)] = LpVariable(f"{s}_to_{m}", lowBound = 0) 

    problem += lpSum(costs[(s, m)] * x[(s, m)] for s in warehouses for m in stores)

    for s in warehouses:
        problem += lpSum(x[(s,m)] for m in stores) <= warehouses[s]

    for m in stores:
        problem += lpSum(x[(s,m)] for s in warehouses) == stores[m]

    problem.solve(PULP_CBC_CMD(msg=0))

    print("Статус:", LpStatus[problem.status])

    for s in warehouses:
        for m in stores:
            value = x[(s,m)].value()
            if value > 0:
                print(f"{s} ->{m}: {value} пицц")

    print(f"Общая стоимость: {problem.objective.value()}")


parser = argparse.ArgumentParser()
parser.add_argument("--data", type=str, default="data/example.csv")
args = parser.parse_args()

warehouses, stores, costs = load_data(args.data)

solve(warehouses, stores, costs)
