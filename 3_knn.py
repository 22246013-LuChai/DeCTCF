import numpy as np

from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import NearestNeighbors

import matplotlib.pyplot as plt



# Load the PCA result from the file

pca_result = np.loadtxt('pcanew_result.txt')



# Use only the top 50 principal components

top_pcs = 50


pca_result = pca_result[:, :top_pcs]



# Step 1: Scale the principal components to unit variance

scaler = StandardScaler()

pca_result_scaled = scaler.fit_transform(pca_result)



# Step 2: Construct the nearest neighbor graph

k = 14  # You can adjust this value based on your requirements

nbrs = NearestNeighbors(n_neighbors=k, algorithm='auto').fit(pca_result_scaled)

distances, indices = nbrs.kneighbors(pca_result_scaled)



# Save the nearest neighbor graph to new files

np.savetxt('./k14/nearest_neighbors_indices14.txt', indices, fmt='%d')

np.savetxt('./k14/nearest_neighbors_distances14.txt', distances, fmt='%.6f')



# Plotting the nearest neighbor graph

plt.figure(figsize=(12, 8))

plt.scatter(pca_result_scaled[:, 0], pca_result_scaled[:, 1], s=1, alpha=0.5, label='Data Points')



# Draw lines between each point and its k nearest neighbors

for i in range(pca_result_scaled.shape[0]):

    for j in indices[i]:

        plt.plot([pca_result_scaled[i, 0], pca_result_scaled[j, 0]],

                 [pca_result_scaled[i, 1], pca_result_scaled[j, 1]], 'r-', alpha=0.1)



plt.title('Nearest Neighbor Graph (k=15)')

plt.xlabel('Principal Component 1')

plt.ylabel('Principal Component 2')

plt.grid(True)

plt.legend()

plt.savefig('./k14/nearest14_neighbor_graph_pc.png')

plt.show()

