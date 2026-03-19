# 📦 Supply Chain Optimizer

> Linear programming solution for the Transportation Problem — minimizing delivery costs across warehouses and stores

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)

## Problem

The **Transportation Problem** is a classic Operations Research challenge: given a set of warehouses with limited supply and stores with specific demand, find the optimal distribution plan that **minimizes total delivery cost** while satisfying all constraints.

This problem appears everywhere in industry — Amazon optimizing warehouse-to-customer routes, Uber matching drivers to riders, airlines scheduling crew assignments, and manufacturing plants distributing products to retail locations.

## Approach

This project uses **Linear Programming (LP)** — a mathematical optimization technique that finds the exact optimal solution (not an approximation). The solver guarantees that no better solution exists.

The optimization model:
- **Variables**: amount shipped from each warehouse to each store
- **Objective**: minimize total transportation cost
- **Constraints**: supply limits per warehouse, demand requirements per store

### Tech Stack

| Tool | Purpose |
|------|---------|
| **PuLP** | Linear programming modeling and solving |
| **pandas** | Data loading and processing from CSV |
| **matplotlib** | Network flow visualization |
| **argparse** | CLI interface |
| **pytest** | Unit testing |

## Results

### Small example (2 warehouses, 3 stores)

```
$ python3 optimazer.py --data data/example.csv

Status: Optimal
A → R1: 60.0 units
A → R3: 40.0 units
B → R2: 70.0 units
B → R3: 10.0 units
Total cost: 420.0
```

### Large example (4 warehouses, 5 stores)

```
$ python3 optimazer.py --data data/large_example.csv

Status: Optimal
W1 → S1: 50.0 units
W1 → S4: 120.0 units
W2 → S2: 150.0 units
W2 → S5: 100.0 units
W3 → S3: 180.0 units
W4 → S1: 150.0 units
Total cost: 2100.0
```

### Network Visualization

The optimizer generates a visual network diagram showing optimal flows between warehouses and stores, with arrow thickness proportional to shipment volume.

## Project Structure

```
Supply-Chain-Optimizer/
├── optimazer.py              # Main optimizer with LP model and CLI
├── visualizer.py             # Network flow visualization
├── data/
│   ├── example.csv           # Small dataset (2 warehouses, 3 stores)
│   └── large_example.csv     # Large dataset (4 warehouses, 5 stores)
├── tests/
│   ├── __init__.py
│   └── test_optimizer.py     # 5 tests covering solver correctness
└── conftest.py               # pytest configuration
```

## Getting Started

### Installation

```bash
git clone https://github.com/Timur-2703/Supply-Chain-Optimizer.git
cd Supply-Chain-Optimizer
pip install pulp pandas matplotlib pytest
```

### Usage

**Run with default data:**
```bash
python3 optimazer.py
```

**Specify custom dataset:**
```bash
python3 optimazer.py --data data/large_example.csv
```

**Run tests:**
```bash
pytest tests/ -v
```

### Custom Data Format

Create a CSV file with these columns:

```csv
from,to,cost,supply,demand
WarehouseA,Store1,5,100,60
WarehouseA,Store2,3,100,40
WarehouseB,Store1,4,80,60
WarehouseB,Store2,2,80,40
```

- `from` — warehouse name
- `to` — store name
- `cost` — shipping cost per unit
- `supply` — warehouse capacity (same value for all rows with this warehouse)
- `demand` — store requirement (same value for all rows with this store)

## How It Works

1. **Load data** — read CSV into warehouse supplies, store demands, and cost matrix
2. **Build model** — define LP variables, objective function (minimize cost), and constraints (supply/demand)
3. **Solve** — PuLP calls the CBC solver to find the mathematically optimal solution
4. **Visualize** — generate network diagram showing optimal flows

Unlike heuristic approaches (greedy, genetic algorithms), Linear Programming guarantees the **exact optimal solution** — mathematically proven to be the best possible.

## Connection to Other Work

This project complements my [Route Optimizer](https://github.com/Timur-2703/Route-optimizer) which solves the Traveling Salesman Problem using metaheuristics (Greedy, Genetic, 2-opt, Simulated Annealing, Ant Colony). Together, they demonstrate two fundamental approaches in Operations Research:

| Approach | When to use | Example |
|----------|-------------|---------|
| **Linear Programming** (this project) | Problem can be expressed with linear equations | Transportation, resource allocation |
| **Metaheuristics** (Route Optimizer) | NP-hard problems, no exact solution feasible | TSP, scheduling, combinatorial optimization |

## Future Improvements

- [ ] Multi-objective optimization (cost + delivery time)
- [ ] Capacity constraints on transportation routes
- [ ] Integration with Google OR-Tools for larger-scale problems
- [ ] Web API (FastAPI) for optimization-as-a-service
- [ ] Real-world geographic data and distance matrices

## Author

**Timur** — CS student passionate about optimization, operations research, and mathematical modeling.

- GitHub: [@Timur-2703](https://github.com/Timur-2703)