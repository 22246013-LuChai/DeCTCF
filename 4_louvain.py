import numpy as np
import networkx as nx
import community as community_louvain
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler



# Load the k-nearest neighbors data from files
indices = np.loadtxt('./k14/nearest_neighbors_indices14.txt', dtype=int)
distances = np.loadtxt('./k14/nearest_neighbors_distances14.txt')

# Convert nearest neighbors to a graph
G = nx.Graph()
num_points = indices.shape[0]
k = indices.shape[1]

for i in range(num_points):
    for j in range(1, k):  # Skip the first neighbor (the point itself)
        G.add_edge(i, indices[i, j], weight=distances[i, j])

random_seed = 42

# Apply Louvain community clustering with a fixed random seed
partition = community_louvain.best_partition(G, random_state=random_seed, resolution=1.0)



# Step 3: Apply Louvain community clustering
#partition = community_louvain.best_partition(G)

# Convert partition dictionary to cluster list
clusters = [[] for _ in range(max(partition.values()) + 1)]
for node, cluster in partition.items():
    clusters[cluster].append(node)


#clusters = [[] for _ in range(max(partition.values()) + 1)]
#for node, cluster in partition.items():
#    clusters[cluster].append(node)

# Calculate size threshold for clusters (2.6% of the total data points)
size_threshold = 0.026 * num_points

# Filter clusters based on size
good_clusters = [cluster for cluster in clusters if len(cluster) >= size_threshold]
small_clusters = [cluster for cluster in clusters if len(cluster) < size_threshold]

# Report statistics
print(f'Total clusters found: {len(clusters)}')
print(f'Good clusters (>= 2.6% of dataset): {len(good_clusters)}')
print(f'Small clusters (< 2.6% of dataset): {len(small_clusters)}')
print(f'Total points in good clusters: {sum(len(cluster) for cluster in good_clusters)}')
print(f'Total points in small clusters: {sum(len(cluster) for cluster in small_clusters)}')



# Step 4: Filter clusters (keep the largest 40 clusters)
clusters_sorted = sorted(clusters, key=len, reverse=True)
largest_clusters = clusters_sorted[:26]
excluded_clusters = clusters_sorted[26:]

# Step 5: Visualize the largest clusters
# For visualization, we will use the first two principal components from pca_result_scaled
pca_result_scaled = np.loadtxt('pcanew_result.txt')
pca_result_scaled = StandardScaler().fit_transform(pca_result_scaled[:, :20])

plt.figure(figsize=(12, 8))
for i, cluster in enumerate(largest_clusters):
    cluster_points = pca_result_scaled[cluster]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], s=1, label=f'Cluster {i + 1}')

plt.title('Largest 40 Clusters')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend(markerscale=10, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.savefig('./k14/largest_clusters14.png')
plt.show()

# Save the clusters to files
with open('./k14/largest_clusters14.txt', 'w') as f:
    for i, cluster in enumerate(largest_clusters):
        f.write(f'Cluster {i + 1}: {len(cluster)} points\n')
        f.write(', '.join(map(str, cluster)) + '\n')

with open('./k14/excluded_clusters14.txt', 'w') as f:
    for i, cluster in enumerate(excluded_clusters):
        f.write(f'Cluster {i + 41}: {len(cluster)} points\n')
        f.write(', '.join(map(str, cluster)) + '\n')

print(f'Total clusters found: {len(clusters)}')
print(f'Largest 40 clusters contain {sum(len(cluster) for cluster in largest_clusters)} points')
print(f'Excluded clusters contain {sum(len(cluster) for cluster in excluded_clusters)} points')
