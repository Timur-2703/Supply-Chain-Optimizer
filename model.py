from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, PULP_CBC_CMD
import pandas as pd
from visualizer import draw_network


class Warehouse:
    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory

class Store:
    def __init__(self, name, demand):
        self.name = name
        self.demand = demand

costs = {
    ("Склад A", "Магазин 1"): 2,
    ("Склад A", "Магазин 2"): 3,
    ("Склад B", "Магазин 1"): 1,
    ("Склад B", "Магазин 2"): 4,
}

warehouse1 = Warehouse("Склад A", 100)
warehouse2 = Warehouse("Склад B", 80)
store1 = Store("Магазин 1", 70)
store2 = Store("Магазин 2", 90)


def load_data(filepath):
    df = pd.read_csv(filepath)
    
    # создаём склады — уникальные значения из колонки "from"
    warehouses = []
    for name in df["from"].unique():
        inventory = df[df["from"] == name]["supply"].iloc[0]
        warehouses.append(Warehouse(name, inventory))
    
    # создаём магазины — уникальные значения из колонки "to"
    stores = []
    for name in df["to"].unique():
        demand = df[df["to"] == name]["demand"].iloc[0]
        stores.append(Store(name, demand))
    
    # создаём словарь стоимостей
    costs = {}
    for _, row in df.iterrows():
        costs[(row["from"], row["to"])] = row["cost"]
    
    return warehouses, stores, costs

def solve(warehouses, stores, costs):
    # создаём задачу — минимизация
    problem = LpProblem("Supply_Chain", LpMinimize)
    
    # создаём переменные x[(склад, магазин)]
    x = {}
    for w in warehouses:
        for s in stores:
            x[(w.name, s.name)] = LpVariable(f"{w.name}_to_{s.name}", lowBound=0)
    
    # целевая функция — минимизируем стоимость
    problem += lpSum(costs[(w.name, s.name)] * x[(w.name, s.name)] 
                     for w in warehouses for s in stores)
    
    # ограничения по складам — не превышаем запас
    for w in warehouses:
        problem += lpSum(x[(w.name, s.name)] for s in stores) <= w.inventory
    
    # ограничения по магазинам — удовлетворяем спрос
    for s in stores:
        problem += lpSum(x[(w.name, s.name)] for w in warehouses) == s.demand
    
    # решаем
    problem.solve(PULP_CBC_CMD(msg=0))
    
    return x, problem


if __name__ == "__main__":
    warehouses, stores, costs = load_data("data/example.csv")
    
    x, problem = solve(warehouses, stores, costs)
    
    print(f"Статус: {LpStatus[problem.status]}")
    print(f"Оптимальная стоимость: {problem.objective.value()}")
    print()
    
    for w in warehouses:
        for s in stores:
            value = x[(w.name, s.name)].value()
            if value > 0:
                print(f"{w.name} → {s.name}: {value} единиц")

# красивая таблица результатов
rows = []
for w in warehouses:
    for s in stores:
        value = x[(w.name, s.name)].value()
        if value > 0:
            rows.append({
                "Откуда": w.name,
                "Куда": s.name,
                "Количество": value,
                "Стоимость": value * costs[(w.name, s.name)]
            })

df_result = pd.DataFrame(rows)
print(df_result.to_string(index=False))
print(f"\nОбщая стоимость: {problem.objective.value()}")


results = [(row["Откуда"], row["Куда"], row["Количество"]) 
           for _, row in df_result.iterrows()]
draw_network(warehouses, stores, results, costs)