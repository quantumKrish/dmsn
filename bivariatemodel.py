import networkx as nx
import matplotlib.pyplot as plt

# Create a small sample of your graph for the slide
sample_B = nx.Graph()
sample_customers = ['C1', 'C2', 'C3']
sample_products = ['P1', 'P2', 'P3', 'P4']

sample_B.add_nodes_from(sample_customers, bipartite=0)
sample_B.add_nodes_from(sample_products, bipartite=1)
sample_B.add_edges_from([('C1', 'P1'), ('C1', 'P2'), ('C2', 'P2'), ('C2', 'P3'), ('C3', 'P4'), ('C3', 'P1')])

# Position nodes in two straight lines (Bipartite Layout)
pos = nx.bipartite_layout(sample_B, sample_customers)

# Compress vertical spacing (scale down y coordinates) so the two lines are closer together
vertical_scale = 0.4
pos = {n: (p[0], p[1] * vertical_scale) for n, p in pos.items()}

# Smaller figure and save directly (no interactive show) to avoid large GUI windows
plt.figure(figsize=(4, 3))
nx.draw(sample_B, pos, with_labels=True, node_color=['skyblue' if n in sample_customers else 'orange' for n in sample_B.nodes()], 
        node_size=700, font_size=9, font_weight='bold')
plt.title("Bipartite Structure: Customers (Blue) to Products (Orange)")
plt.savefig("bipartite_diagram.png", dpi=150, bbox_inches='tight')
plt.close()