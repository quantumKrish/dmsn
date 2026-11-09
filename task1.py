import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

df = pd.read_excel("Online Retail.xlsx")
df.head()

#clean data
df_clean = df.drop_duplicates()
df_clean = df_clean.dropna(subset=["InvoiceNo", "CustomerID", "StockCode"])
df_clean = df_clean[df_clean["Quantity"]>0]
df_clean["CustomerID"] = df_clean["CustomerID"].astype(str)
df_clean["StockCode"] = df_clean["StockCode"].astype(str)
#print("shape: ", df_clean.shape)
#print(df_clean.head())

#create the bipartite graph
B = nx.Graph()

#customer nodes
customers = df_clean["CustomerID"].unique()
B.add_nodes_from(customers, bipartite = "customer")

#product nodes
products = df_clean["StockCode"].unique()
B.add_nodes_from(products, bipartite = "product")

#edge weights
edges = (df_clean.groupby(["CustomerID", "StockCode"])
                 .size()
                 .reset_index(name = "weight")
        )

for _, row in edges.iterrows():
    B.add_edge(row["CustomerID"], row["StockCode"], weight = row["weight"])

#print("total nodes: ", B.number_of_nodes())
#print("total edges: ", B.number_of_edges())

#create separate node sets 
customer_nodes = {n for n, d in B.nodes(data=True) if d["bipartite"] == "customer"}
product_nodes = set(B) - customer_nodes

# --- Task 1 analytics commented out for Task 2-only run ---
# (retain these lines if you later want customer/program analysis)
# customer_degree = dict(B.degree(customer_nodes))
# product_degree = dict(B.degree(product_nodes))
# avg_customer_degree = sum(customer_degree.values()) / len(customer_degree)
# avg_product_degree = sum(product_degree.values()) / len(product_degree)
# print("average customer degree: ", round(avg_customer_degree, 2))
# print("average product degree: ", round(avg_product_degree, 2))
# degree_centrality = nx.degree_centrality(B)
# ... etc ...

# Degree Distribution Histogram (optional, comment for speed)
#plt.figure(figsize=(10, 6))
#degrees = [val for node, val in B.degree()]
#plt.hist(degrees, bins=50, color='skyblue', edgecolor='black', log=True)
#plt.title("Network Degree Distribution (Log Scale)")
#plt.xlabel("Degree (Connections)")
#plt.ylabel("Number of Nodes")
#plt.tight_layout()
#plt.savefig("degree_distribution.png", dpi=150, bbox_inches='tight')
#plt.close()
#print("\nDegree distribution chart saved as 'degree_distribution.png'")

# 1. Filter the graph for visibility (Top 50 products + their customers) (optional)
# top_products = [p for p, v in products_central[:50]]
# subgraph_nodes = top_products + [n for p in top_products for n in B.neighbors(p)][:100]
# sub_G = B.subgraph(subgraph_nodes)

# 2. Set up the Layout (Spring Layout is similar to ForceAtlas2)
# ... graph plotting is optional for Task 2 ...

# -------------------------------------------
# Task 2: Product–Product Network + Community Detection
# -------------------------------------------

# 2.1 Build product–product projection from bipartite network
product_graph = bipartite.weighted_projected_graph(B, product_nodes)
print("\nProduct–product graph:", product_graph.number_of_nodes(), "nodes," , product_graph.number_of_edges(), "edges")

# 2.1.1: prune very small weight edges for clarity
min_weight = 1
edges_to_remove = [(u, v) for u, v, d in product_graph.edges(data=True) if d.get('weight', 0) < min_weight]
if edges_to_remove:
    product_graph.remove_edges_from(edges_to_remove)

# 2.2 Community detection using Louvain otherwise greedy modularity
try:
    import community as community_louvain
    partition = community_louvain.best_partition(product_graph, weight='weight')
    method_used = 'Louvain'
except Exception as e:
    print("Louvain package unavailable or failed: ", e)
    print("Falling back to greedy modularity communities.")
    try:
        communities = list(nx.community.greedy_modularity_communities(product_graph, weight='weight'))
        method_used = 'Greedy modularity'
    except Exception as e2:
        print("Greedy modularity failed: ", e2)
        print("Falling back to asynchronous label propagation communities.")
        communities = list(nx.community.asyn_lpa_communities(product_graph, weight='weight'))
        method_used = 'Label propagation'
    partition = {node: idx for idx, comm in enumerate(communities) for node in comm}

# 2.3 Organize communities
from collections import defaultdict
comm_nodes = defaultdict(list)
for node, comm_id in partition.items():
    comm_nodes[comm_id].append(node)

# sort communities by size desc
sorted_comms = sorted(comm_nodes.items(), key=lambda x: len(x[1]), reverse=True)

# map StockCode to Description if available
code_to_desc = df_clean.set_index('StockCode')['Description'].to_dict()

print(f"\nCommunity detection method: {method_used}")
print(f"Detected {len(sorted_comms)} communities")

for i, (comm_id, nodes) in enumerate(sorted_comms[:8], start=1):
    print(f"\nCommunity {i} (id={comm_id}, size={len(nodes)})")
    sample_nodes = nodes[:10]
    for code in sample_nodes:
        desc = code_to_desc.get(code, '<no description>')
        print(f" - {code}: {desc}")

# 2.4 Basic evaluation and interpretation hints
print("\nInterpretation notes:")
print("- Each community groups products that share customer purchase history.")
print("- Strong communities likely represent frequently co-purchased clusters, e.g., stationary, household, personal care.")
print("- Check if similar product descriptions appear together, this validates practical basket affinities.")

# 2.5 Save community labels for later analysis
community_df = pd.DataFrame([{'StockCode': code, 'Community': comm_id, 'Description': code_to_desc.get(code, '')} for code, comm_id in partition.items()])
community_df.to_csv('product_communities.csv', index=False)
print("Product communities exported to product_communities.csv")

# Only export edges where the weight is 5 or higher
# This keeps the 'backbone' of the 4 communities but removes the 4 million 'noisy' edges
strong_edges = [(u, v, d) for u, v, d in product_graph.edges(data=True) if d['weight'] >= 5]
L = nx.Graph()
L.add_edges_from(strong_edges)

# Export this smaller version
edges_df = nx.to_pandas_edgelist(L)
edges_df.columns = ['Source', 'Target', 'Weight']
edges_df.to_csv("product_edges_LIGHT.csv", index=False)
print(f"Light edges exported: {len(edges_df)} edges (down from 4 million!)")

