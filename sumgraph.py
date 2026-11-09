import networkx as nx
import matplotlib.pyplot as plt

# 1. Filter the graph for visibility (Top 50 products + their customers)
top_products = [p for p, v in products_central[:50]]
subgraph_nodes = top_products + [n for p in top_products for n in B.neighbors(p)][:100]
sub_G = B.subgraph(subgraph_nodes)

# 2. Set up the Layout (Spring Layout is similar to ForceAtlas2)
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(sub_G, k=0.15, iterations=50)

# 3. Color nodes by type
node_colors = ['#1f77b4' if sub_G.nodes[n]['bipartite'] == 'customer' else '#ff7f0e' for n in sub_G.nodes()]

# 4. Draw the graph
nx.draw(sub_G, pos, 
        node_color=node_colors, 
        with_labels=False, 
        node_size=50, 
        edge_color='gray', 
        alpha=0.6, 
        width=0.5)

# 5. Add a legend and title
plt.title("Force-Directed Network Visualization (Top Nodes)")
plt.legend(handles=[
    plt.Line2D([0], [0], marker='o', color='w', label='Customer', markerfacecolor='#1f77b4', markersize=10),
    plt.Line2D([0], [0], marker='o', color='w', label='Product', markerfacecolor='#ff7f0e', markersize=10)
])

plt.savefig("network_vis.png", dpi=300)
plt.show()