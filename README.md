# DeCTCF

Decoding CTCF binding sequences by leveraging predicted epigenomic features

**DeCTCF** is an integrative computational framework for characterizing the functional diversity of CTCF binding sites (CBSs). It uses epigenomic features predicted by the pretrained [Sei model](https://github.com/FunctionLab/seiframework), together with dimensionality reduction, graph-based clustering, and downstream functional annotation, to organize CBSs into distinct clusters and investigate their associations with chromatin architecture, cell-line enrichment, epigenomic context, and candidate transcription factor co-factors.

DeCTCF is not a newly developed deep learning model. The pretrained Sei model is used as a fixed feature extractor to generate sequence-predicted epigenomic features, which are subsequently analyzed using PCA, KNN graph construction, Louvain community detection, and downstream annotation.

This repository contains the source code for feature extraction, dimensionality reduction, graph construction, clustering, and visualization in the DeCTCF workflow.

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Step-by-Step Usage](#step-by-step-usage)
  - [1. Feature Extraction Using Sei](#1-feature-extraction-using-sei)
  - [2. Dimensionality Reduction](#2-dimensionality-reduction)
  - [3. KNN Graph Construction](#3-knn-graph-construction)
  - [4. Louvain Clustering](#4-louvain-clustering)
  - [5. UMAP Visualization](#5-umap-visualization)
- [Downstream Annotation Tools](#downstream-annotation-tools)
- [Data Availability](#data-availability)

## ⚙️ System Requirements

- **Operating system:** Linux or macOS
- **Python:** version 3.8 or later
- **Hardware:** A GPU is recommended for the Sei prediction step.

## 📦 Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/22246013-LuChai/DeCTCF.git
   cd DeCTCF

2. Install the required Python packages:
   pip install -r requirements.txt
   We recommend using a dedicated Conda or virtual environment.
   Core dependencies include numpy, h5py, scikit-learn, matplotlib, networkx, python-louvain, and umap-learn.
3. Install the Sei framework and obtain the pretrained model weights by following the instructions in the official repository:
   https://github.com/FunctionLab/seiframework
🚀 Step-by-Step Usage
1. Feature Extraction Using Sei
The pretrained Sei model is used as a fixed feature extractor to generate a 21,907-dimensional vector of sequence-predicted epigenomic features for each input sequence.
- Script: 1_sei_prediction.py
- Input: CTCF-118-600bp-hg38.txt
- Input sequences: 600-bp genomic sequences centered on the highest-scoring CTCF motif identified by FIMO
- Example command:
  python 1_sei_prediction.py \
      <input_sequence_file> \
      <output_directory> \
      --genome=hg38 \
      --cuda
- Output: CTCF_118_600bp-hg38_predictions.h5
2. Dimensionality Reduction
Incremental PCA is applied to the 21,907-dimensional Sei-derived feature vectors. The first 19 principal components are retained because they reach the prespecified cumulative explained-variance threshold of 95%.
- Script: 2_pca.py
- Input: Sei prediction file in HDF5 format
- Batch size used in the study: 10,000 CBSs
- Retained components: 19
- Explained-variance threshold: 95%
- Output: pcanew_result.txt and the corresponding explained-variance results
3. KNN Graph Construction
A K-nearest neighbor graph is constructed using the standardized PCA representation.
- Script: 3_knn.py
- Distance metric: Euclidean distance
- Number of neighbors: k = 14
- Outputs:
  - nearest_neighbors_indices14.txt
  - nearest_neighbors_distances14.txt
4. Louvain Clustering
Louvain community detection is applied to the KNN graph to identify CBS clusters.
- Script: 4_louvain.py
- Resolution: 1.0
- Random seed: 42
- Number of clusters obtained in the study: 20
- Output: largest_clusters14.txt
The cluster assignments were fixed before downstream biological annotation. Cell-line enrichment, TF motif enrichment, epigenomic profiles, and functional annotations were not used to generate the clusters.
5. UMAP Visualization
UMAP is used to visualize the cluster assignments in two dimensions.
- Script: 5_umap.py
- Input: PCA representation and Louvain cluster assignments
- Output: umap_louvain_clusters.png
🧬 Downstream Annotation Tools
The resulting CBS clusters were interpreted using complementary downstream annotations. These annotations were applied after clustering and were not used to generate the original 20 clusters.
- Motif enrichment: monaLisa v1.10.1, using the JASPAR 2020 vertebrate motif database
- Genomic annotation: ChIPseeker v1.40.1
- Gene Ontology enrichment: GREAT v4.0.4, using the “Basal plus extension” association rule
- Canonical CTCF motif scanning: FIMO, MEME Suite v5.5.0
- CTCF motif: JASPAR 2020 CORE vertebrate motif MA0139.1
- FIMO threshold: P < 1 × 10⁻⁴
- FIMO background model: uniform nucleotide frequencies (A = C = G = T = 0.25)
- Strands scanned: both DNA strands
📂 Data Availability
The dataset generated in this study is available on Zenodo:
DOI: 10.5281/zenodo.18057910
The deposited files include the genomic coordinates of 236,552 CBSs, their cell-line occurrence information, FIMO motif scores, and assigned cluster identities.
The pretrained Sei framework used to generate the sequence-predicted epigenomic features is available at:
https://github.com/FunctionLab/seiframework
The Sei model is described in:
Chen KM, Wong AK, Troyanskaya OG, Zhou J. A sequence-based global map of regulatory activity for deciphering human genetics. Nature Genetics. 2022.
https://doi.org/10.1038/s41588-022-01102-2
