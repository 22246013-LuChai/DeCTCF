import h5py
import numpy as np
import matplotlib.pyplot as plt
# Load the data from the HDF5 file
file_name = '/home/chailu/enformer_venv/CTCF_118/CTCF_softmax_normalized.h5'
dataset_name = 'data'
# Function to load a batch of data safely
def load_batch(data, start_idx, end_idx):
    return data[start_idx:end_idx]
with h5py.File(file_name, 'r') as f:
    data = f[dataset_name]
    n_samples, n_features = data.shape
print(f'Data shape: {n_samples} samples, {n_features} features')
# Step 1: Define the batch size and initialize variables for incremental PCA
batch_size = 10000
n_batches = n_samples // batch_size + (1 if n_samples % batch_size != 0 else 0)
mean = np.zeros(n_features)
# Step 2: Calculate the global mean
for i in range(n_batches):
    start_idx = i * batch_size
    end_idx = min((i + 1) * batch_size, n_samples)
    with h5py.File(file_name, 'r') as f:
        batch_data = load_batch(f[dataset_name], start_idx, end_idx)
    batch_mean = np.mean(batch_data, axis=0)
    mean += (batch_mean - mean) * (end_idx - start_idx) / n_samples
# Step 3: Incremental PCA - Calculate the covariance matrix
cov_matrix = np.zeros((n_features, n_features))
for i in range(n_batches):
    start_idx = i * batch_size
    end_idx = min((i + 1) * batch_size, n_samples)
    with h5py.File(file_name, 'r') as f:
        batch_data = load_batch(f[dataset_name], start_idx, end_idx)
    centered_batch = batch_data - mean
    cov_matrix += np.dot(centered_batch.T, centered_batch) / n_samples
# Step 4: Eigen decomposition
eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
# Step 5: Sort eigenvalues and eigenvectors in descending order
sorted_idx = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[sorted_idx]
eigenvectors = eigenvectors[:, sorted_idx]
# Step 6: Calculate explained variance and determine the number of components
explained_variance_ratio = eigenvalues / np.sum(eigenvalues)
cumulative_explained_variance = np.cumsum(explained_variance_ratio)
# Set a threshold for explained variance, e.g., 95%
threshold = 0.95
num_components = np.argmax(cumulative_explained_variance >= threshold) + 1
print(f'Number of components to retain: {num_components}')
print(f'Explained variance of first {num_components} components: {explained_variance_ratio[:num_components]}')
# Save the explained variance ratio
np.savetxt('enformer_result/explained_variance_ratio2.txt', explained_variance_ratio)
# Step 7: Select the top components
top_eigenvectors = eigenvectors[:, :num_components]
# Save feature contributions (principal component loadings)
np.savetxt('enformer_result/feature_contributions2.txt', top_eigenvectors)
# Step 8: Transform the data using the selected principal components
pca_result = np.zeros((n_samples, num_components))
for i in range(n_batches):
    start_idx = i * batch_size
    end_idx = min((i + 1) * batch_size, n_samples)
    with h5py.File(file_name, 'r') as f:
        batch_data = load_batch(f[dataset_name], start_idx, end_idx)
    centered_batch = batch_data - mean
    pca_result[start_idx:end_idx] = np.dot(centered_batch, top_eigenvectors)
# Step 9: Save the PCA result to a new file
np.savetxt('enformer_result/pcanew_result2.txt', pca_result)
# Step 10: Plot the first two principal components
plt.figure(figsize=(10, 7))
plt.scatter(pca_result[:, 0], pca_result[:, 1], s=1, alpha=0.5)
plt.title('PCA Result: PC1 vs PC2')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid(True)
plt.savefig('enformer_result/pcanew_plot2.png')
plt.show()
