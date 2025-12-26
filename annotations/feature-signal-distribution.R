library(tidyverse)
library(readxl)
library(RColorBrewer)
library(cowplot)

df <- read_excel("stemcell1-openchrom.xlsx", sheet = "Sheet1")

df <- df %>%
  mutate(Signal = ifelse(Signal == "ATAC", "ATAC-seq", "DNase-seq" ))

p1<-ggplot(df, aes(x = Position, y = Value, color = Signal, linetype = Cellline)) +
  geom_line(alpha = 1, linewidth = 1) +
  facet_wrap(~ Cluster, scales = "fixed", ncol = 3) + 
  #geom_vline(xintercept = 0, linetype = "dashed", alpha = 0.4) +
  scale_x_continuous(
    breaks = c(-800, -400, 0, 400, 800),
    labels = function(x) paste0(x)
  ) +
  scale_color_manual(
    values = c( "ATAC-seq" = "#F16767", "DNase-seq"= "#9FB3DF"),
    name = "Open chromsome"
  ) +
  scale_linetype_manual(
    values = c("H1-hESC" = "solid", "H9"  = "dashed", "WTC11" = "dotted"),
    name = "Cell Line"
  ) +
  labs(
    #title = ,
    #subtitle = ,
    x = "Position relative to CTCF cluster center (bp)",
    y = "Signal Intensity",
    color = "Cell Line",
    #linetype = "Assay Type"
  ) +
  theme_bw(base_size = 12) +
  theme(
    panel.grid.minor = element_blank(),         
    panel.grid.major = element_line(linewidth = 0.2, color = "grey90"),
    strip.background = element_rect(fill = "grey95"), 
    strip.text = element_text(face = "bold"),   
    legend.position = "right",               
    legend.key.width = unit(1.2, "cm"),      
    legend.text = element_text(size = 10)     
  )+
  guides(
    color = guide_legend(nrow = 2),
    linetype = guide_legend(nrow = 3)
  )

p1
df <- read_excel("stemcell1-tf.xlsx", sheet = "Sheet1")

p2<-ggplot(df, aes(x = Position, y = Value, color = Signal, linetype = Cellline)) +
  geom_line(alpha = 1, linewidth = 1) +
  facet_wrap(~ Cluster, scales = "fixed", ncol = 3) + 
  scale_x_continuous(
    breaks = c(-800, -400, 0, 400, 800),
    labels = function(x) paste0(x)
  ) +
  scale_color_manual(
    values = c("CTCF" = "#F5C191", "RAD21"= "#8ED3BB", "YY1" = "#7EB6FF"),
    name = "TFs"
  ) +
  scale_linetype_manual(
    values = c("H1-hESC" = "solid", "H9"  = "dashed", "WTC11" = "dotted"),
    name = "Cell Line"
  ) +
  
  labs(
    x = "Position relative to CTCF cluster center (bp)",
    y = "Signal Intensity"
  ) +

  theme_bw(base_size = 12) +
  theme(
    panel.grid.minor = element_blank(),
    panel.grid.major = element_line(linewidth = 0.2, color = "grey90"),
    strip.background = element_rect(fill = "grey95"),
    strip.text = element_text(face = "bold"),
    legend.position = "right",
    legend.key.width = unit(1.5, "cm"), 
    #legend.box = "horizontal",
    legend.text = element_text(size = 10), 
    legend.margin = margin(t = 0, b = 5), 
    plot.margin = margin(10, 10, 5, 10)  
  ) +

  guides(
    color = guide_legend(nrow = 4),
    linetype = guide_legend(nrow = 3)
  )

p2

df <- read_excel("stemcell1-HMs.xlsx", sheet = "Sheet1")


histone_colors <- c(
  "H3K4me1" = "#FFCB61", 
  "H3K4me2" = "#E69DB8", 
  "H3K4me3" = "#8CCDEB",
  "H3K9me3" = "#9DC08B", 
  "H3K27me3" = "#8D77AB", 
  "H3K27ac" = "#06923E"
)


p3<-ggplot(df, aes(x = Position, y = Value, color = Signal, linetype = Cellline)) +
  geom_line(alpha = 1, linewidth = 1) +
  

  facet_wrap(~ Cluster, scales = "fixed", ncol = 3) + 
  
  scale_x_continuous(
    breaks = c(-800, -400, 0, 400, 800),
    labels = function(x) paste0(x)
  ) +
  scale_color_manual(
    values = histone_colors, 
    name = "HMs" 
  ) +
  scale_linetype_manual(
    values = c("H1-hESC" = "solid", "H9" = "dashed"), 
    name = "Cell Line"
  ) +
  labs(
    x = "Position relative to CTCF cluster center (bp)",
    y = "Signal Intensity"
  ) +
  theme_bw(base_size = 12) +
  theme(
    panel.grid.minor = element_blank(),        
    panel.grid.major = element_line(linewidth = 0.2, color = "grey90"),
    strip.background = element_rect(fill = "grey95"),  
    strip.text = element_text(face = "bold"),   
    legend.position = "right",               
    legend.key.width = unit(1.2, "cm"),       
    legend.text = element_text(size = 10),       
    #legend.box = "horizontal",              
    legend.margin = margin(t = 0, b = -5)    
  ) +
  guides(
    color = guide_legend(nrow = 6),
    linetype = guide_legend(nrow = 3)
  )
p3
combined_plot <- plot_grid(p1, p2,p3, ncol = 1, align = "v")
final_plot <- ggdraw(add_sub(combined_plot, "", vpadding = unit(0, "lines")))


final_plot

