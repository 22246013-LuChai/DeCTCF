# DeCTCF
Decoding CTCF binding sequences by leveraging predicted epigenomic features

**DeCTCF** is a deep learning-based computational framework designed to systematically decode the functional diversity of CTCF binding sites (CBSs). By integrating sequence-based feature embeddings from the [Sei model](https://github.com/calico/sei) with graph-based clustering, DeCTCF classifies CBSs into distinct functional clusters, revealing their roles in chromatin architecture, lineage-specific regulation, and TF cooperation.

This repository contains the source code for the DeCTCF workflow, covering feature extraction, dimensionality reduction, graph-based clustering, and visualization.

## 📋 Table of Contents
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Workflow Overview](#workflow-overview)
- [Step-by-Step Usage](#step-by-step-usage)
  - [1. Feature Extraction (Sei)](#1-feature-extraction-sei)
  - [2. Dimensionality Reduction (PCA)](#2-dimensionality-reduction-pca)
  - [3. Graph Construction (KNN)](#3-graph-construction-knn)
  - [4. Clustering (Louvain)](#4-clustering-louvain)
  - [5. Visualization (UMAP)](#5-visualization-umap)
- [Downstream Annotation](#downstream-annotation)
- [Data Availability](#data-availability)
- [Citation](#citation)

## ⚙️ System Requirements

* **OS:** Linux / macOS
* **Python:** >= 3.8
* **Hardware:** A GPU is recommended for the Sei model prediction step. Typically requires >16GB RAM for PCA and clustering on large datasets (~230k sites).

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YourUsername/DeCTCF.git](https://github.com/YourUsername/DeCTCF.git)
    cd DeCTCF
    ```

2.  **Install Python dependencies:**
    We recommend using a virtual environment (Conda or venv).
    ```bash
    pip install -r requirements.txt
    ```
    *Core dependencies include:* `numpy`, `h5py`, `scikit-learn`, `matplotlib`, `networkx`, `python-louvain` (for community detection), and `umap-learn`.

3.  **Install Sei Framework:**
    The feature extraction step relies on the Sei model. Please verify the installation and download model weights following the official instructions: [https://github.com/calico/sei](https://github.com/calico/sei).

## 🚀 Step-by-Step Usage

### 1. Feature Extraction (Sei)
First, we use the Sei framework to generate high-dimensional sequence embeddings (21,907 features) for the input sequences.

* **Input:** `CTCF-118-600bp-hg38.txt` (600bp genomic sequences centered on CTCF motifs)
* **Command:**
    ```bash
    python scripts/1_sei_prediction.py \
        <input_sequence_file> \
        <output_directory> \
        --genome=hg38 \
        --cuda
    ```
* **Output:** `CTCF_118_600bp-hg38_predictions.h5`

### 2. Dimensionality Reduction (PCA)
We perform Incremental PCA to reduce the high-dimensional features to the top principal components.

* **Script:** `scripts/2_pca.py`
* **Function:** Loads the H5 file, performs batch-wise PCA, and selects components explaining 95% variance.
* **Output:** `pcanew_result.txt` (PCA embeddings), Explained variance plots.

### 3. Graph Construction (KNN)
Construct a K-Nearest Neighbor (KNN) graph based on the PCA embeddings.

* **Script:** `scripts/3_knn.py`
* **Parameters:** `k=14` (adjustable in script).
* **Output:** `nearest_neighbors_indices14.txt`, `nearest_neighbors_distances14.txt`.

### 4. Clustering (Louvain)
Apply the Louvain community detection algorithm to partition the KNN graph into functional clusters.

* **Script:** `scripts/4_louvain.py`
* **Parameters:** `resolution=1.0`. Clusters smaller than 2.6% of the dataset are filtered out or merged.
* **Output:** `largest_clusters14.txt` (Cluster assignments).

### 5. Visualization (UMAP)
Visualize the clustering results using UMAP (Uniform Manifold Approximation and Projection).

* **Script:** `scripts/5_umap.py`
* **Input:** PCA embeddings and Cluster assignments.
* **Output:** `umap_louvain_clusters.png` (2D visualization).

## 🧬 Downstream Annotation tools

Following the clustering, functional annotations were performed using standard external tools. The specific parameters and versions used in this study are listed below:

* **Motif Enrichment:** [monaLisa](https://bioconductor.org/packages/release/bioc/html/monaLisa.html) (v1.10.1) using JASPAR 2020 vertebrate database.
* **Genomic Annotation:** [ChIPseeker](https://bioconductor.org/packages/release/bioc/html/ChIPseeker.html) (v11.40.1) R package.
* **GO Enrichment:** [GREAT](http://great.stanford.edu/public/html/) (v4.0.4) using the "Basal plus extension" model.
* **Sequence Scanning:** [FIMO](https://meme-suite.org/meme/tools/fimo) (MEME Suite v5.5.0).

## 📂 Data Availability

The complete dataset generated in this study, including the classified CTCF binding sites and cluster IDs, is available on Zenodo: **[DOI: 10.5281/zenodo.18057910](https://doi.org/10.5281/zenodo.18057910)**.

The Sei model code is available at: https://doi.org/10.1038/s41588-022-01102-2.

## 📄 Citation

If you use DeCTCF in your research, please cite:
> [Your Name], et al. "DeCTCF: Decoding CTCF binding sequences by leveraging predicted epigenomic features." *Nature Communications* (Submitted), 2025.
