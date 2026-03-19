import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def draw_network(warehouses, stores, results, total_cost):
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # Позиции складов (слева) и магазинов (справа)
    w_list = list(warehouses.keys())
    s_list = list(stores.keys())
    
    # Рисуем склады слева
    for i, w in enumerate(w_list):
        y = i * 2
        ax.plot(0, y, 's', color='#E94560', markersize=20)
        ax.text(-0.5, y, f"{w}\n({warehouses[w]})", ha='right', va='center', fontsize=10)
    
    # Рисуем магазины справа
    for i, s in enumerate(s_list):
        y = i * 1.5
        ax.plot(4, y, 'o', color='#1D9E75', markersize=20)
        ax.text(4.5, y, f"{s}\n({stores[s]})", ha='left', va='center', fontsize=10)
    
    # Рисуем потоки (стрелки)
    for src, dst, amount in results:
        w_y = w_list.index(src) * 2
        s_y = s_list.index(dst) * 1.5
        thickness = amount / 20  # толщина линии зависит от количества
        ax.annotate("", xy=(3.8, s_y), xytext=(0.2, w_y),
                    arrowprops=dict(arrowstyle='->', lw=thickness, color='#378ADD', alpha=0.7))
        # Подпись количества
        mid_x = 2
        mid_y = (w_y + s_y) / 2
        ax.text(mid_x, mid_y, f"{amount:.0f}", ha='center', va='bottom', fontsize=9, color='#378ADD')
    
    ax.set_xlim(-2, 6)
    ax.set_title(f"Supply Chain Optimization (Total cost: {total_cost:.0f})", fontsize=14)
    ax.axis('off')
    
    # Легенда
    w_patch = mpatches.Patch(color='#E94560', label='Warehouses')
    s_patch = mpatches.Patch(color='#1D9E75', label='Stores')
    ax.legend(handles=[w_patch, s_patch], loc='upper center')
    
    plt.tight_layout()
    plt.savefig("network.png", dpi=150)
    plt.show()