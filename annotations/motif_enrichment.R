if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")

BiocManager::install("BSgenome.Hsapiens.UCSC.hg38")
install.packages("BSgenome.Hsapiens.UCSC.hg38_1.4.5.tar.gz",repos = NULL)
install.packages("BSgenome.Hsapiens.UCSC.hg19_1.4.3.tar.gz",repos = NULL)


library(monaLisa)
library(JASPAR2020)
library(rtracklayer)
library(TFBSTools)
library(BSgenome.Hsapiens.UCSC.hg38)
library(magrittr)
library(dplyr)
library(SummarizedExperiment)


rawpeak <- import.bed("E://6.Doctor-programe//5.118celllines//2.sei-framework//2.20cluster_fa//cluster-8.txt") # the cluster bed file
singleSet <- resize(rawpeak, width = median(width(rawpeak)), fix = "center")

head(singleSet,3)
singleseqs <- getSeq(BSgenome.Hsapiens.UCSC.hg38, singleSet)

pwms <- getMatrixSet(JASPAR2020,
                     opts = list(matrixtype = "PWM",
                                 tax_group = "vertebrates"))

sinse <- calcBinnedMotifEnrR(seqs = singleseqs,
                             pwmL = pwms,
                             background = "genome",
                             genome = BSgenome.Hsapiens.UCSC.hg38,
                             genome.regions = NULL, # sample from full genome
                             genome.oversample = 2,
                             BPPARAM = BiocParallel::SerialParam(RNGseed = 42),
                             verbose = TRUE)

pv <- data.frame(
  tf = names(assay(sinse, "negLog10Padj")[, 1]), 
  enr = assay(sinse, "log2enr")[, 1],           
  p = assay(sinse, "negLog10Padj")[, 1]         
) %>%
  na.omit() %>%                                 
  dplyr::mutate(enr_plus_p = enr + p) %>%        
  dplyr::filter(enr > -2) %>%               
  dplyr::arrange(desc(enr))              
# plot
plotMotifHeatmaps(x = sinse[pv$tf[1:10],],
                  which.plots = c("log2enr"),
                  width = 1.5, maxEnr = 2, maxSig = 10,
                  cluster = F,
                  show_dendrogram = T,
                  show_seqlogo = TRUE)
