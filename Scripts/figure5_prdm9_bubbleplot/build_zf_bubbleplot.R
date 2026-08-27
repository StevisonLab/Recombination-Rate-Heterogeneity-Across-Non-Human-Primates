library(ggplot2)
library(dplyr)
library(patchwork)
library(tidyr)

# ============================================================================
# PRDM9 zinc-finger array size across primates -- a modernized version of
# Schwartz et al. (2014)'s Figure 3 bubble plot. Same underlying idea (bubble
# size = number of sequenced alleles at a given array size), but:
#  - grouped by this review's own 4 clades (Apes/Old World Monkeys/New World
#    Monkeys/Lemurs) instead of Schwartz's own ad hoc categories, with the
#    same clade color scheme used throughout Figures 1-4, PLUS a 5th
#    "Tarsiers" category -- tarsiers aren't part
#    of any of the other 4 clades (their own infraorder, Tarsiiformes, not a
#    monkey or a lemur), so folding them into an existing color would repeat
#    the same taxonomic mistake already caught and fixed elsewhere in this
#    project ("Catarrhini" wrongly used as if exclusive of apes). Given pink
#    (#e7298a) as the 5th color: the existing 4 are drawn from ColorBrewer's
#    Dark2 qualitative palette, and pink is both part of that same palette
#    (so it stays visually harmonious) and the most hue-distinct remaining
#    option from all 4 existing colors.
#  - combines FOUR sources: Schwartz et al. (2014)'s own raw Supplementary
#    Data 1 (parsed directly, not their summary figure -- their figure pools
#    New World/Old World monkeys into single unresolved categories), the
#    unpublished Segurel/Przeworski allele set, this project's own new
#    tBLASTn/GeneWise/Princeton-ZF-tool annotation work, and Heerschop et al.
#    (2016)'s own Table 1 tarsier allele survey (28 alleles/23 individuals/
#    15 heterozygous, transcribed directly and cross-checked against those
#    same three summary counts before use)
#  - deliberately includes every primate genus any source sequenced, not
#    just this review's own species list -- matching the
#    Figure 2A precedent (crossover assurance includes species without a
#    computable cM/Mb) of showing gaps/extremes rather than only species
#    with a complete data picture elsewhere in this review
# ============================================================================

CLADE_LEVELS <- c("Apes", "Old World Monkeys", "New World Monkeys", "Tarsiers", "Lemurs")
CLADE_COLORS <- c(
  "Apes"               = "#d95f02",
  "Old World Monkeys"  = "#7570b3",
  "New World Monkeys"  = "#1b9e77",
  "Tarsiers"           = "#e7298a",
  "Lemurs"             = "#e6ab02"
)

alleles <- read.csv("/Users/lss0021/Documents/Primate_Maps/Primate_PRDM9/prdm9_zf_alleles.csv",
                     stringsAsFactors = FALSE) %>%
  mutate(clade = factor(clade, levels = CLADE_LEVELS))

# Species ordering: by clade, then by descending mean ZF count within clade --
# same convention as Figure_2's ranked panels, lets the size extremes within
# each clade read immediately left-to-right.
species_order <- alleles %>%
  group_by(species, clade) %>%
  summarise(mean_zf = mean(zf), .groups = "drop") %>%
  arrange(clade, desc(mean_zf)) %>%
  pull(species)

# Plecturocebus cupreus: genuinely zero PRDM9 data recovered (no annotation,
# GeneWise returned no zinc fingers, no allele-level sequencing in either
# Schwartz or Segurel/Przeworski) -- added as an empty x-axis category so the
# gap is visible as negative space, not just missing from the review's text.
species_order <- append(species_order, "Plecturocebus cupreus",
                          after = which(species_order == "Callithrix jacchus"))

alleles <- alleles %>% mutate(species = factor(species, levels = species_order))

# in_review_gini controls fill: solid = this review has fine-scale (Gini-
# capable) recombination-rate data for this species elsewhere; hollow = PRDM9
# is characterized here but no fine-scale RR map exists for the species at
# all -- not just "no Gini computed here" but no fine-scale RR data in this
# review, and as far as this review's literature search found, in the field
# generally -- the "literally no recombination anywhere" species
# (orangutan, siamang, etc.). Renamed from the original Gini-specific framing
# since the gap is broader than Gini reliance alone.
alleles <- alleles %>%
  mutate(fill_group = ifelse(in_review_gini == "yes", "Fine-scale RR data",
                              "No RR data exists"))

has_gini <- alleles %>% filter(in_review_gini == "yes")
no_gini  <- alleles %>% filter(in_review_gini == "no")

p_main <- ggplot(mapping = aes(x = species, y = zf)) +
  # Genuinely hollow triangles (fill=NA, colored outline only) for species with
  # PRDM9 characterized but no recombination map anywhere -- two separate
  # geom_count layers rather than one shared fill scale, since shape 24 (like
  # shape 21) accepts its own fill and a single scale_fill_manual would have
  # colored both categories identically regardless of the intended hollow/solid
  # distinction (confirmed by the first draft render -- the triangles came out
  # solid, not hollow, which defeated the point of the encoding).
  geom_count(data = no_gini, aes(color = clade, shape = "No RR data exists"),
             fill = NA, stroke = 1.3) +
  geom_count(data = has_gini, aes(color = clade, fill = clade, shape = "Fine-scale RR data"),
             stroke = 1.1) +
  scale_color_manual(values = CLADE_COLORS, guide = "none") +
  scale_fill_manual(values = CLADE_COLORS, guide = "none") +
  scale_shape_manual(values = c("Fine-scale RR data" = 21,
                                 "No RR data exists" = 24),
                      name = NULL,
                      # Legend key glyphs default to an unfilled outline for
                      # both levels since the "Fine-scale RR data" fill comes
                      # from a per-layer clade mapping, not a fixed value the
                      # legend can infer -- override.aes forces that key to
                      # render filled (black, matching the plot's own black
                      # stroke color for both shapes) so it visually matches
                      # the actual filled points on the plot.
                      guide = guide_legend(override.aes = list(fill = c("black", NA)))) +
  scale_size_area(max_size = 9, breaks = c(1, 3, 6, 10, 20, 34), name = "Alleles sequenced") +
  scale_x_discrete(drop = FALSE) +
  scale_y_continuous(breaks = seq(0, 20, 2), limits = c(0, 20), expand = expansion(mult = c(0.02, 0.05))) +
  labs(x = NULL, y = "Zinc finger array size per PRDM9 allele",
       title = "PRDM9 Zinc-Finger Array Size Heterogeneity Across Non-Human Primates") +
  theme_minimal(base_size = 13) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, face = "italic", size = 9),
        panel.grid.major.x = element_blank(),
        plot.title = element_text(face = "bold", size = 15),
        legend.position = "bottom",
        legend.box = "vertical")

# ---------- Shared clade legend strip (matches Figure_2/Figure_4 pattern) ----------
clade_legend_data <- tibble(clade = factor(CLADE_LEVELS, levels = CLADE_LEVELS), x = 1, y = 1)
clade_legend_plot <- ggplot(clade_legend_data, aes(x = x, y = y, color = clade)) +
  geom_point(size = 4.5, alpha = 0) +
  scale_color_manual(values = CLADE_COLORS, name = "Clade") +
  guides(color = guide_legend(override.aes = list(alpha = 1))) +
  theme_void() +
  theme(legend.position = "top",
        legend.title = element_text(face = "bold", size = 13),
        legend.text = element_text(size = 11),
        legend.key.size = unit(1.1, "lines"))

combined <- clade_legend_plot / p_main + plot_layout(heights = c(0.1, 1))

ggsave("/Users/lss0021/Documents/Primate_Maps/PRDM9_Synthesis_Figure/PRDM9_ZF_bubbleplot.png",
       combined, width = 14, height = 8, dpi = 1200, bg = "white")
ggsave("/Users/lss0021/Documents/Primate_Maps/PRDM9_Synthesis_Figure/PRDM9_ZF_bubbleplot.pdf",
       combined, width = 14, height = 8, bg = "white")
# EPS format for Elsevier ELSA submission -- their upload page accepts
# JPG/TIFF/PNG/EPS/CDX specifically (not PDF), so this is the vector option that
# actually satisfies their format list while sidestepping the DPI question the
# same way the PDF above already does.
ggsave("/Users/lss0021/Documents/Primate_Maps/PRDM9_Synthesis_Figure/PRDM9_ZF_bubbleplot.eps",
       combined, device = "eps", width = 14, height = 8, bg = "white")

write.csv(alleles %>% select(species, clade, zf, source, in_review_gini) %>% arrange(clade, species, zf),
          "/Users/lss0021/Documents/Primate_Maps/PRDM9_Synthesis_Figure/supplemental_zf_alleles_table.csv",
          row.names = FALSE)

cat("Saved PRDM9_ZF_bubbleplot.png/.pdf and supplemental_zf_alleles_table.csv\n")
