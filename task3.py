import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Load and clean data (reuse from Task 1)
df = pd.read_excel("Online Retail.xlsx")
df = df.drop_duplicates()
df = df.dropna(subset=["InvoiceNo", "CustomerID", "StockCode"])
df = df[df["Quantity"] > 0]
df["CustomerID"] = df["CustomerID"].astype(str)
df["StockCode"] = df["StockCode"].astype(str)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Build bipartite graph
B = nx.Graph()
customers = df["CustomerID"].unique()
products = df["StockCode"].unique()
B.add_nodes_from(customers, bipartite="customer")
B.add_nodes_from(products, bipartite="product")
edges = df.groupby(["CustomerID", "StockCode"]).size().reset_index(name="weight")
for _, row in edges.iterrows():
    B.add_edge(row["CustomerID"], row["StockCode"], weight=row["weight"])

customer_nodes = {n for n, d in B.nodes(data=True) if d["bipartite"] == "customer"}
product_nodes = set(B) - customer_nodes

# Product-product projection
product_graph = bipartite.weighted_projected_graph(B, product_nodes)

# -------------------------------------------
# Task 3: Centrality and Influence
# -------------------------------------------

# 3.1 Graph-based recommendation: PageRank on product-product network
print("Computing PageRank on product-product graph...")
pagerank_scores = nx.pagerank(product_graph, weight='weight')
top_pagerank_products = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:20]
print("Top 20 products by PageRank:")
for prod, score in top_pagerank_products:
    print(f"{prod}: {score:.4f}")

# Plot PageRank distribution
plt.figure(figsize=(10, 6))
plt.hist(list(pagerank_scores.values()), bins=50, color='green', alpha=0.7)
plt.title("PageRank Score Distribution")
plt.xlabel("PageRank Score")
plt.ylabel("Frequency")
plt.savefig("pagerank_distribution.png")
plt.close()

# 3.2 Traditional recommendation: Collaborative Filtering (Item-Item Similarity)
print("\nComputing item-item collaborative filtering...")
# Create user-item matrix
user_item_matrix = df.pivot_table(index='CustomerID', columns='StockCode', values='Quantity', aggfunc='sum', fill_value=0)
item_similarity = cosine_similarity(user_item_matrix.T)
item_similarity_df = pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)

# Function to get recommendations for a product
def get_cf_recommendations(product, n=10):
    if product not in item_similarity_df.index:
        return []
    sim_scores = item_similarity_df[product].sort_values(ascending=False)[1:n+1]
    return list(sim_scores.index)

# Example: recommendations for top PageRank product
example_product = top_pagerank_products[0][0]
cf_recs = get_cf_recommendations(example_product, 10)
print(f"CF recommendations for {example_product}: {cf_recs}")

# 3.3 Comparison: Relevance, Diversity, Interpretability
# Relevance: Use a simple metric like average similarity score
# Diversity: Measure how different recommendations are (e.g., inverse of average similarity)
# Interpretability: Subjective, but we can note structural vs. behavioral

def evaluate_recommendations(recs, sim_df):
    if not recs:
        return 0, 0
    pairs = [(recs[i], recs[j]) for i in range(len(recs)) for j in range(i+1, len(recs))]
    similarities = [sim_df.loc[a, b] if a in sim_df.index and b in sim_df.index else 0 for a, b in pairs]
    avg_sim = np.mean(similarities) if similarities else 0
    diversity = 1 - avg_sim  # Higher diversity if less similar
    return avg_sim, diversity

pagerank_recs = [p[0] for p in top_pagerank_products[1:11]]  # Top 10 excluding itself
cf_avg_sim, cf_diversity = evaluate_recommendations(cf_recs, item_similarity_df)
pr_avg_sim, pr_diversity = evaluate_recommendations(pagerank_recs, item_similarity_df)

print("\nComparison:")
print(f"CF - Relevance (avg sim): {cf_avg_sim:.3f}, Diversity: {cf_diversity:.3f}")
print(f"PageRank - Relevance (avg sim): {pr_avg_sim:.3f}, Diversity: {pr_diversity:.3f}")
print("Interpretability: PageRank based on network structure; CF based on user behavior patterns.")

# 3.4 Track importance over time
print("\nTracking PageRank over time...")
df['YearMonth'] = df['InvoiceDate'].dt.to_period('M')
time_periods = sorted(df['YearMonth'].unique())[:6]  # First 6 months for demo

time_pagerank = {}
for period in time_periods:
    period_df = df[df['YearMonth'] == period]
    if period_df.empty:
        continue
    # Rebuild graph for period
    period_B = nx.Graph()
    period_B.add_nodes_from(customers, bipartite="customer")
    period_B.add_nodes_from(products, bipartite="product")
    period_edges = period_df.groupby(["CustomerID", "StockCode"]).size().reset_index(name="weight")
    for _, row in period_edges.iterrows():
        period_B.add_edge(row["CustomerID"], row["StockCode"], weight=row["weight"])
    period_product_graph = bipartite.weighted_projected_graph(period_B, product_nodes)
    if period_product_graph.number_of_nodes() > 0:
        period_pagerank = nx.pagerank(period_product_graph, weight='weight')
        time_pagerank[str(period)] = period_pagerank

# Plot evolution of top product
top_prod = top_pagerank_products[0][0]
evolution = [time_pagerank[p].get(top_prod, 0) for p in time_pagerank if top_prod in time_pagerank[p]]
plt.figure(figsize=(8, 5))
plt.plot(list(time_pagerank.keys())[:len(evolution)], evolution, marker='o')
plt.title(f"PageRank Evolution for Product {top_prod}")
plt.xlabel("Time Period")
plt.ylabel("PageRank Score")
plt.savefig("pagerank_evolution.png")
plt.close()

# Save results
results = {
    'top_pagerank': top_pagerank_products,
    'cf_example': cf_recs,
    'comparison': {'cf_relevance': cf_avg_sim, 'cf_diversity': cf_diversity, 'pr_relevance': pr_avg_sim, 'pr_diversity': pr_diversity},
    'time_evolution': time_pagerank
}
pd.to_pickle(results, 'task3_results.pkl')

# Additional plots for expanded analysis

# 1. Bar chart: Top PageRank vs Top Sales Products
top_sales_products = df.groupby('StockCode')['Quantity'].sum().sort_values(ascending=False)[:20]
top_sales_list = list(top_sales_products.index)
pagerank_dict = dict(top_pagerank_products[:20])
sales_dict = dict(top_sales_products[:20])

# Align for comparison
common_products = set(pagerank_dict.keys()) & set(sales_dict.keys())
if common_products:
    fig, ax = plt.subplots(figsize=(12, 6))
    products = list(common_products)[:10]
    pr_scores = [pagerank_dict[p] for p in products]
    sales_vol = [sales_dict[p] for p in products]
    x = np.arange(len(products))
    ax.bar(x - 0.2, pr_scores, 0.4, label='PageRank Score', color='blue')
    ax.bar(x + 0.2, sales_vol / max(sales_vol), 0.4, label='Normalized Sales Volume', color='red')
    ax.set_xticks(x)
    ax.set_xticklabels(products, rotation=45)
    ax.legend()
    plt.title("PageRank vs Sales Volume for Top Products")
    plt.tight_layout()
    plt.savefig("pagerank_vs_sales.png")
    plt.close()

# 2. Scatter plot: Relevance vs Diversity
methods = ['CF', 'PageRank']
relevance = [cf_avg_sim, pr_avg_sim]
diversity = [cf_diversity, pr_diversity]
plt.figure(figsize=(8, 6))
plt.scatter(relevance, diversity, s=100, c=['red', 'blue'])
for i, method in enumerate(methods):
    plt.annotate(method, (relevance[i], diversity[i]), xytext=(5, 5), textcoords='offset points')
plt.xlabel('Relevance (Avg Similarity)')
plt.ylabel('Diversity (1 - Avg Similarity)')
plt.title('Relevance vs Diversity: CF vs PageRank')
plt.grid(True)
plt.savefig("relevance_diversity_scatter.png")
plt.close()

# 3. Temporal heatmap (if enough data)
if len(time_pagerank) > 1:
    top_prods = [p[0] for p in top_pagerank_products[:5]]
    heatmap_data = []
    for prod in top_prods:
        row = [time_pagerank.get(p, {}).get(prod, 0) for p in time_pagerank]
        heatmap_data.append(row)
    if heatmap_data:
        plt.figure(figsize=(10, 6))
        plt.imshow(heatmap_data, cmap='viridis', aspect='auto')
        plt.colorbar(label='PageRank Score')
        plt.xticks(range(len(time_pagerank)), list(time_pagerank.keys()), rotation=45)
        plt.yticks(range(len(top_prods)), top_prods)
        plt.title("Temporal PageRank Heatmap for Top 5 Products")
        plt.tight_layout()
        plt.savefig("temporal_heatmap.png")
        plt.close()

print("Additional plots saved: pagerank_vs_sales.png, relevance_diversity_scatter.png, temporal_heatmap.png")
print("Task 3 results saved to task3_results.pkl")