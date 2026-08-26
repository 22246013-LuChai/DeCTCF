# DeCTCF

## Decoding CTCF binding sequences by leveraging predicted epigenomic features

**DeCTCF** is an integrative computational framework for characterizing the functional diversity of CTCF binding sites (CBSs). It uses epigenomic features predicted by the pretrained [Sei model](https://github.com/FunctionLab/seiframework), together with dimensionality reduction, graph-based clustering, and downstream functional annotation, to organize CBSs into distinct clusters and investigate their associations with chromatin architecture, cell-line enrichment, epigenomic context, and candidate transcription factor co-factors.

DeCTCF is not a newly developed deep learning model. The pretrained Sei model is used as a fixed feature extractor to generate sequence-predicted epigenomic features, which are subsequently analyzed using principal component analysis (PCA), K-nearest neighbor (KNN) graph construction, Louvain community detection, and downstream functional annotations.

This repository contains the source code for feature extraction, dimensionality reduction, graph construction, clustering, and visualization in the DeCTCF workflow.

## Table of Contents

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
- [Sei Model](#sei-model)

## System Requirements

- **Operating system:** Linux or macOS
- **Python:** version 3.8 or later
- **Hardware:** A GPU is recommended for the Sei prediction step.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/22246013-LuChai/DeCTCF.git
cd DeCTCF
```

### 2. Install the required Python packages

We recommend using a dedicated Conda environment or Python virtual environment.

```bash
pip install -r requirements.txt
```

The core dependencies include:

- `numpy`
- `h5py`
- `scikit-learn`
- `matplotlib`
- `networkx`
- `python-louvain`
- `umap-learn`

### 3. Install the Sei framework

The feature-extraction step uses the pretrained Sei model. Install the Sei framework and obtain the pretrained model weights by following the instructions in the official repository:

[https://github.com/FunctionLab/seiframework](https://github.com/FunctionLab/seiframework)

## Step-by-Step Usage

### 1. Feature Extraction Using Sei

The pretrained Sei model is used as a fixed feature extractor to generate a 21,907-dimensional vector of sequence-predicted epigenomic features for each input sequence.

- **Script:** `1_sei_prediction.py`
- **Input:** `CTCF-118-600bp-hg38.txt`
- **Input sequences:** 600-bp genomic sequences centered on the highest-scoring canonical CTCF motif identified by FIMO
- **Output:** `CTCF_118_600bp-hg38_predictions.h5`

Example command:

```bash
python 1_sei_prediction.py \
    <input_sequence_file> \
    <output_directory> \
    --genome=hg38 \
    --cuda
```

### 2. Dimensionality Reduction

Incremental PCA is applied to the 21,907-dimensional Sei-derived feature vectors. The first 19 principal components are retained because they reach the prespecified cumulative explained-variance threshold of 95%.

- **Script:** `2_pca.py`
- **Input:** Sei prediction file in HDF5 format
- **Batch size used in the study:** 10,000 CBSs
- **Number of retained principal components:** 19
- **Cumulative explained-variance threshold:** 95%
- **Output:** `pcanew_result.txt` and the corresponding explained-variance results

### 3. KNN Graph Construction

A K-nearest neighbor graph is constructed from the standardized PCA representation.

- **Script:** `3_knn.py`
- **Distance metric:** Euclidean distance
- **Number of neighbors:** `k = 14`
- **Outputs:**
  - `nearest_neighbors_indices14.txt`
  - `nearest_neighbors_distances14.txt`

### 4. Louvain Clustering

Louvain community detection is applied to the KNN graph to identify CBS clusters.

- **Script:** `4_louvain.py`
- **Resolution:** `1.0`
- **Random seed:** `42`
- **Number of clusters obtained in the study:** 20
- **Output:** `largest_clusters14.txt`

The cluster assignments were fixed before downstream biological annotation. Cell-line enrichment, TF motif enrichment, epigenomic profiles, and functional annotations were not used to generate the clusters.

### 5. UMAP Visualization

UMAP is used to visualize the CBS cluster assignments in two dimensions.

- **Script:** `5_umap.py`
- **Input:** PCA representation and Louvain cluster assignments
- **Output:** `umap_louvain_clusters.png`

## Downstream Annotation Tools

The resulting CBS clusters were interpreted using complementary downstream analyses. These annotations were applied after clustering and were not used to generate the original 20 clusters.

### Motif Enrichment

- **Tool:** [monaLisa](https://bioconductor.org/packages/release/bioc/html/monaLisa.html)
- **Version:** 1.10.1
- **Motif database:** JASPAR 2020 CORE vertebrate database

### Genomic Annotation

- **Tool:** [ChIPseeker](https://bioconductor.org/packages/release/bioc/html/ChIPseeker.html)
- **Version:** 1.40.1

### Gene Ontology Enrichment

- **Tool:** [GREAT](http://great.stanford.edu/public/html/)
- **Version:** 4.0.4
- **Association rule:** Basal plus extension

### Canonical CTCF Motif Scanning

- **Tool:** [FIMO](https://meme-suite.org/meme/tools/fimo)
- **Software suite:** MEME Suite
- **Version:** 5.5.0
- **Motif database:** JASPAR 2020 CORE vertebrate database
- **CTCF motif:** MA0139.1
- **Significance threshold:** `P < 1 × 10⁻⁴`
- **Background model:** uniform nucleotide frequencies (`A = C = G = T = 0.25`)
- **Strands scanned:** both DNA strands

When multiple canonical CTCF motif occurrences were detected within a ChIP-seq peak, the occurrence with the highest FIMO score was retained. Its motif center was defined as position 0, and a 600-bp genomic sequence was extracted around this position.

## Data Availability

The dataset generated in this study is publicly available on Zenodo:

**[DOI: 10.5281/zenodo.18057910](https://doi.org/10.5281/zenodo.18057910)**

The deposited files include:

- genomic coordinates of the 236,552 CBSs;
- cell-line occurrence information;
- FIMO motif-match scores;
- assigned cluster identities;
- Sei-predicted epigenomic feature names.

## Sei Model

The pretrained Sei framework used to generate the sequence-predicted epigenomic features is available at:

[https://github.com/FunctionLab/seiframework](https://github.com/FunctionLab/seiframework)

The Sei model is described in:

> Chen KM, Wong AK, Troyanskaya OG, Zhou J. A sequence-based global map of regulatory activity for deciphering human genetics. *Nature Genetics*. 2022;54:940–949.  
> [https://doi.org/10.1038/s41588-022-01102-2](https://doi.org/10.1038/s41588-022-01102-2)
