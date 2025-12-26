import numpy as np
import umap
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Load the PCA result from the file
pca_result = np.loadtxt('pcanew_result.txt')

# Use only the top 50 principal components
top_pcs = 20
pca_result = pca_result[:, :top_pcs]

# Standardize the PCA result
scaler = StandardScaler()
pca_result_scaled = scaler.fit_transform(pca_result)

# Load clusters from Louvain results
with open('./Sei_result/largest_clusters14.txt', 'r') as f:
    lines = f.readlines()

largest_clusters = []
for line in lines:
    if line.startswith('Cluster'):
        continue
    cluster_indices = list(map(int, line.strip().split(', ')))
    largest_clusters.append(cluster_indices)

# Assign cluster labels to each point
labels = np.full(pca_result.shape[0], -1, dtype=int)  # Initialize with -1 for unassigned points
for cluster_id, cluster_indices in enumerate(largest_clusters):
    for idx in cluster_indices:
        labels[idx] = cluster_id

# Apply UMAP to the PCA result
umap_embedding = umap.UMAP(n_neighbors=6, min_dist=0.1, metric='euclidean').fit_transform(pca_result_scaled)

# Plot the UMAP embedding colored by cluster
plt.figure(figsize=(20, 20))
for cluster_id in range(len(largest_clusters)):
    cluster_points = umap_embedding[labels == cluster_id]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1], s=1, label=f'Cluster {cluster_id + 1}')

plt.title('UMAP Embedding of Louvain Clusters')
plt.xlabel('UMAP 1')
plt.ylabel('UMAP 2')
plt.legend(markerscale=10, bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.savefig('/Sei_result/umap_louvain_clusters.png')
plt.show()

# Save the UMAP embedding and labels
np.savetxt('/Sei_result/umap_embedding.txt', umap_embedding)
np.savetxt('

cluster_labels.txt', labels, fmt='%d')

