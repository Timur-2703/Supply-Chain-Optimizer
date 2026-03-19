import pytest
from optimazer import load_data, solve


def test_load_data():
    warehouses, stores, costs = load_data("data/example.csv")
    assert len(warehouses) == 2
    assert len(stores) == 3
    assert len(costs) == 6


def test_solve_optimal():
    warehouses, stores, costs = load_data("data/example.csv")
    results, total_cost = solve(warehouses, stores, costs)
    assert total_cost == 420.0


def test_solve_all_demand_met():
    warehouses, stores, costs = load_data("data/example.csv")
    results, total_cost = solve(warehouses, stores, costs)
    # Проверяем что каждый магазин получил нужное количество
    demand = {"R1": 60, "R2": 70, "R3": 50}
    delivered = {}
    for src, dst, amount in results:
        delivered[dst] = delivered.get(dst, 0) + amount
    for store, needed in demand.items():
        assert delivered[store] == needed


def test_solve_supply_not_exceeded():
    warehouses, stores, costs = load_data("data/example.csv")
    results, total_cost = solve(warehouses, stores, costs)
    # Проверяем что ни один склад не превысил запас
    supply = {"A": 100, "B": 80}
    sent = {}
    for src, dst, amount in results:
        sent[src] = sent.get(src, 0) + amount
    for wh, limit in supply.items():
        assert sent.get(wh, 0) <= limit


def test_large_data():
    warehouses, stores, costs = load_data("data/large_example.csv")
    results, total_cost = solve(warehouses, stores, costs)
    assert total_cost == 2100.0
    assert len(results) > 0
