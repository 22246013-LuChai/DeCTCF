import h5py
import numpy as np
import pandas as pd

with open('target.names', 'r') as f:
    feature_names = np.array([line.strip() for line in f])
num_clusters = 19
for cluster_id in range(num_clusters):
    file_path = f'cluster_10_data.h5'
    with h5py.File(file_path, 'r') as h5_file:
        data = h5_file['data'][:]  
    #feature_variances = np.var(data, axis=0)
    feature_variances = np.mean(data, axis=0)
    sorted_indices = np.argsort(feature_variances)[::-1] 
    sorted_feature_names = feature_names[sorted_indices]
    sorted_variances = feature_variances[sorted_indices]
    result_df = pd.DataFrame({
        'Feature_Name': sorted_feature_names,
        'Variance': sorted_variances
    })
    output_file = f'cluster_10_feature_mean_importance.csv'
    result_df.to_csv(output_file, index=False)
