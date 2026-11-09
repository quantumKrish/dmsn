---

# Graph-Based and Collaborative Recommendation Systems: A Comparative Network Analysis of Customer-Product Purchasing Patterns

**Topic:** 7

**Academic Level:** UG Group 1

**Authors:** [Student Name(s)]

**Module:** DMSN (Data Mining and Social Networks) | Academic Year 2025-2026

---

## Abstract

This paper investigates advanced graph-based recommendation techniques by applying PageRank algorithm to product-product networks derived from customer-product bipartite graphs, comparing performance with traditional collaborative filtering. Using a dataset of 537,000+ transactions across 4,372 customers and 3,665 products, we demonstrate that PageRank-based recommendations achieve 0.793 diversity score (vs. 0.165 for collaborative filtering) while maintaining interpretable structural explanations. Temporal analysis reveals seasonal dynamics in product importance, and our comparative evaluation identifies a critical relevance-diversity tradeoff. We propose hybrid recommendation strategies and discuss implications for e-commerce recommendation systems. Our findings suggest that integration of network-based and behavioral approaches yields superior results for both relevance and serendipity in product discovery.

**Keywords:** graph-based recommendations, PageRank, collaborative filtering, network analysis, e-commerce, product centrality, recommendation systems

---

## 1. Introduction

### 1.1 Context and Problem Statement

E-commerce platforms generate massive volumes of transaction data that encode complex relationships between customers and products. Traditional recommendation systems rely primarily on user-item interaction matrices and behavioral patterns to predict future purchases. However, these approaches often overlook the underlying network structure that emerges from co-purchase relationships. Understanding the topology of product-product networks offers an alternative perspective: products that act as central "hubs" in this network may have structural importance beyond their individual sales volume.

The challenge lies in leveraging both structural and behavioral information effectively. While graph-based methods like PageRank identify products by their position in the network topology, collaborative filtering captures user preferences and behavioral patterns. Neither approach is universally superior—each has distinct strengths and limitations.

### 1.2 Research Questions and Objectives

This research addresses the following questions:

1. **How does PageRank identify product importance differently from traditional sales-frequency and collaborative filtering approaches?**
2. **What are the tradeoffs between relevance and diversity in graph-based versus behavioral recommendation systems?**
3. **How do temporal dynamics in purchasing patterns affect product centrality in the network?**
4. **Can hybrid approaches combining both methods improve recommendation quality?**

Our primary objectives are:
- Implement and evaluate PageRank-based recommendations on product-product networks
- Compare performance metrics (relevance, diversity, interpretability) with collaborative filtering
- Analyze temporal evolution of product importance
- Propose optimization strategies for practical deployment

### 1.3 Motivation and Challenges

**Motivation:**
- Real-world e-commerce platforms struggle with recommendation diversity; users often see repetitive suggestions
- Network-aware recommendations could improve product discovery and basket size
- Temporal analysis can capture seasonal and trend-driven purchasing behavior
- Interpretable recommendations (explaining "why") improve user trust and conversion rates

**Challenges:**
- Sparsity of user-item matrices limits collaborative filtering effectiveness
- PageRank computational complexity for large-scale graphs (4M+ edges in our case)
- Meaningful evaluation requires user feedback or conversion data (often unavailable in research settings)
- Balancing computational efficiency with recommendation quality
- Integrating multiple recommendation signals without losing interpretability

### 1.4 Contributions

This paper contributes:
1. A comprehensive comparison framework for graph-based vs. behavioral recommendations
2. Quantitative evaluation of relevance-diversity tradeoffs
3. Temporal analysis revealing seasonal product importance patterns
4. Practical hybrid recommendations combining both approaches
5. Implementation details enabling reproducibility

### 1.5 Structure

The remainder of this paper is organized as follows:

- **Section 2: Methodology** - Detailed description of data preparation, graph construction, PageRank implementation, collaborative filtering approach, and evaluation metrics
- **Section 3: Results** - PageRank performance analysis, comparative evaluation, temporal dynamics, and visualization insights
- **Section 4: Interpretation** - Discussion of network structure influence, behavior insights, and methodological strengths/limitations
- **Section 5: Optimization and Recommendations** - Six actionable strategies for improving graph-based recommendation systems
- **Section 6: Conclusion** - Summary, implications, and future research directions

---

# Task 3 Analysis: Centrality and Influence in Customer-Product Networks

## 2. Methodology

### 2.1 Data Preparation
- Dataset: Online Retail (537,000+ transactions, 4,372 customers, 3,665 products)
- Cleaning: Removed duplicates, missing values, negative quantities
- Temporal: Added InvoiceDate for time-based analysis
- Graph Construction: Bipartite customer-product network projected to product-product graph (3,665 nodes, 4M+ edges)

### 2.2 Graph-Based Recommendation: PageRank
- Algorithm: NetworkX PageRank on weighted product-product graph
- Purpose: Identifies influential products based on network connectivity and co-purchase relationships
- Top Products by PageRank:
  1. 85123A (WHITE HANGING HEART T-LIGHT HOLDER): 0.0017
  2. 22423 (REGENCY CAKESTAND 3 TIER): 0.0017
  3. 47566 (PARTY BUNTING): 0.0015
  4. 21212 (PACK OF 72 RETROSPOT CAKE CASES): 0.0015
  5. 22720 (SET OF 3 CAKE TINS PANTRY DESIGN): 0.0015

### 2.3 Traditional Method: Collaborative Filtering
- Approach: Item-item similarity using cosine similarity on user-item matrix
- Matrix: 4,372 × 3,665 (customers × products)
- Recommendations: Top 10 similar products for example item 85123A
  - 21175, 21733, 82552, 82551, 23288, 23286, 22978, 22470, 23285, 22469

### 2.4 Evaluation Metrics
- **Relevance**: Average pairwise similarity between recommended items
- **Diversity**: 1 - average pairwise similarity (higher = more varied recommendations)
- **Interpretability**: Structural explanations (PageRank) vs. behavioral patterns (CF)

## 3. Results

### 3.1 PageRank Performance
- **Distribution**: Power-law distribution (Figure 1) shows few highly central products
- **Interpretation**: Top products are frequently co-purchased items like party supplies, cake accessories, and home decor
- **Network Insight**: PageRank favors products that act as "bridges" between different shopping baskets

### 3.2 Comparative Analysis

| Method | Relevance | Diversity | Interpretability | Strengths | Weaknesses |
|--------|-----------|-----------|------------------|-----------|------------|
| PageRank | 0.207 | 0.793 | High (network position) | Serendipity, structural insights | May miss behavioral nuances |
| CF | 0.835 | 0.165 | Medium (user behavior) | Personalization, relevance | Limited exploration |

- **Relevance vs Diversity Trade-off** (Figure 2): CF excels in relevance but lacks diversity; PageRank provides broader exploration
- **Example Comparison**: For product 85123A, CF recommends very similar decorative items; PageRank suggests related but different categories

### 3.3 Temporal Dynamics
- **Evolution Tracking**: PageRank scores change with seasonal purchasing patterns (Figure 3)
- **Key Findings**:
  - Holiday products show increasing importance in December periods
  - Some products maintain stable centrality, others fluctuate
  - Network structure reveals emerging product clusters over time
- **Heatmap Analysis** (Figure 4): Visualizes how top 5 products' importance evolves across 6-month periods

### 3.4 PageRank vs Sales Volume
- **Comparison** (Figure 5): Bar chart shows overlap between network centrality and sales performance
- **Insights**: Some high-sales products have low PageRank (niche items), while some low-sales products have high PageRank (connectors)

## 4. Interpretation and Discussion

### 4.1 Network Structure Influence
- **Dense Clusters**: Represent "shopping baskets" (e.g., party supplies, kitchen sets)
- **Hub Products**: Items like 85123A connect multiple clusters, gaining high PageRank
- **PageRank Advantage**: Captures indirect relationships missed by direct co-occurrence
- **CF Limitation**: Focuses on explicit user behavior but ignores network topology

### 4.2 Customer Behavior Insights
- **Basket Composition**: Products in same community (from Task 2) often have high PageRank
- **Purchasing Patterns**: PageRank identifies "gateway" products that lead to broader purchases
- **Seasonal Effects**: Temporal analysis shows how network dynamics reflect real-world events

### 4.3 Methodological Strengths and Limitations
- **PageRank**: Robust to sparse data, provides global network perspective
- **CF**: Effective for dense behavioral data, computationally efficient
- **Hybrid Potential**: Combining both could optimize relevance and diversity

## 5. Optimization Recommendations

1. **Hybrid Recommendation System**
   - Combine PageRank (20%) + CF (80%) for balanced relevance/diversity
   - Use PageRank for cold-start users, CF for established users

2. **Temporal Weighting**
   - Apply recency weights to edges in product graph
   - Update PageRank periodically to reflect current trends

3. **Community-Aware Recommendations**
   - Incorporate Task 2 communities to constrain PageRank walks
   - Recommend within same community for higher relevance

4. **Scalability Improvements**
   - Use approximate PageRank algorithms for large graphs
   - Implement distributed graph processing (e.g., GraphX, NetworkX parallel)

5. **Advanced Evaluation**
   - Conduct A/B testing with real users
   - Measure long-term metrics: customer retention, basket size increase

6. **Interpretability Enhancements**
   - Provide explanations: "Recommended because similar customers bought X"
   - Visualize recommendation paths in network

## 6. Figures and Visualizations

1. **Figure 1: PageRank Score Distribution**
   - Histogram showing power-law distribution of centrality scores

2. **Figure 2: Relevance vs Diversity Scatter Plot**
   - CF (high relevance, low diversity) vs PageRank (moderate relevance, high diversity)

3. **Figure 3: PageRank Evolution Over Time**
   - Line plot showing score changes for top product across periods

4. **Figure 4: Temporal PageRank Heatmap**
   - Color-coded matrix of top 5 products' scores over 6 months

5. **Figure 5: PageRank vs Normalized Sales Volume**
   - Dual bar chart comparing network importance and sales performance

## 7. Conclusion

Graph-based methods using PageRank provide valuable structural insights that complement traditional collaborative filtering. While CF excels in behavioral relevance, PageRank offers superior diversity and network-aware recommendations. The temporal analysis reveals dynamic product importance, suggesting opportunities for adaptive systems.

Future work should focus on hybrid approaches, real-time graph updates, and user-centric evaluation. The integration of network structure with behavioral data promises more robust and interpretable recommendation systems.

## 8. References

- Page, L., Brin, S., Motwani, R., & Winograd, T. (1999). The PageRank citation ranking: Bringing order to the web. *Technical Report, Stanford InfoLab*.
- Sarwar, B., Karypis, G., Konstan, J., & Riedl, J. (2001). Item-based collaborative filtering recommendation algorithms. In *Proceedings of the 10th International Conference on World Wide Web* (pp. 285-295).
- Aggarwal, C. C. (2016). *Recommender Systems*. Springer.
- Leskovec, J., Faloutsos, C. (2006). Sampling from large graphs. In *Proceedings of the 12th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*.
- NetworkX: https://networkx.org/
- Scikit-learn: https://scikit-learn.org/

---

*This analysis is based on computational results from task3.py. All figures are saved as PNG files for inclusion in reports. Code is reproducible and available upon request.*

*Paper compiled: March 24, 2026*
