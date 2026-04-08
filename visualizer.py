import networkx as nx
import matplotlib.pyplot as plt

def draw_network(warehouses, stores, results, costs):
    G = nx.DiGraph()  # направленный граф
    
    # добавляем узлы
    for w in warehouses:
        G.add_node(w.name, type="warehouse")
    for s in stores:
        G.add_node(s.name, type="store")
    
    # добавляем рёбра только для активных маршрутов
    for from_node, to_node, amount in results:
        G.add_edge(from_node, to_node, weight=amount)
    
    # позиции — склады слева, магазины справа
    pos = {}
    for i, w in enumerate(warehouses):
        pos[w.name] = (0, i)
    for i, s in enumerate(stores):
        pos[s.name] = (2, i)
    
    plt.figure(figsize=(14, 8))
    
    # рисуем склады синим, магазины зелёным
    warehouse_nodes = [w.name for w in warehouses]
    store_nodes = [s.name for s in stores]
    
    nx.draw_networkx_nodes(G, pos, nodelist=warehouse_nodes, 
                           node_color="blue", node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=store_nodes, 
                           node_color="green", node_size=3000)
    nx.draw_networkx_labels(G, pos, font_color="white")
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20)
    
    # подписи на рёбрах — количество
    edge_labels = {(f, t): f"{a:.0f}" for f, t, a in results}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title("Оптимальные поставки")
    plt.axis("off")
    plt.tight_layout()
    plt.show()