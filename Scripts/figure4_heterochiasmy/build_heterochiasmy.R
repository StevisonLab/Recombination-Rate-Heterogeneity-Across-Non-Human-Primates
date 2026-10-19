# Run from the repository root, e.g.  Rscript Scripts/figure4_heterochiasmy/build_heterochiasmy.R
OUT_DIR <- "Figures/Figure4_Heterochiasmy"
if (!dir.exists(OUT_DIR)) stop("Run this script from the repository root.")

library(ggplot2)
library(patchwork)
library(dplyr)

CLADE_LEVELS <- c("Apes", "Cercopithecidae", "Platyrrhini", "Strepsirrhini")
CLADE_COLORS <- c(
  "Apes"        = "#d95f02",
  "Cercopithecidae"  = "#7570b3",
  "Platyrrhini" = "#1b9e77",
  "Strepsirrhini"= "#e6ab02"
)
SPECIES_CLADE <- c(
  "Papio anubis" = "Cercopithecidae",
  "Plecturocebus cupreus" = "Platyrrhini",
  "Daubentonia madagascariensis" = "Strepsirrhini",
  "Pan paniscus" = "Apes",
  "Pan troglodytes ellioti" = "Apes",
  "Gorilla gorilla gorilla" = "Apes",
  "Callithrix jacchus" = "Platyrrhini",
  "Papio papio" = "Cercopithecidae",
  "Macaca mulatta" = "Cercopithecidae"
)
# Panel B stays the original 3 species -- the only 3 pedigree studies in this review
# with BOTH sexes measured for BOTH crossovers and non-crossovers. Macaca mulatta's
# own WGS pedigree study (Versoza et al. 2024) examined paternal meioses only (its own
# stated design); the 5 Porsborg long-read species are testis-tissue samples,
# inherently male-only by what tissue was sequenced. Neither is a gap in extraction
# effort. Panel A now has 2 more species (see below) since Burt, Bell & Harvey
# (1991)'s cytogenetic chiasma data is CO-only, no NCO -- doesn't extend Panel B.
SPECIES_ORDER <- c("Papio anubis", "Plecturocebus cupreus", "Daubentonia madagascariensis")

base_theme <- theme_minimal(base_size = 12) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, face = "italic"),
        panel.grid.major.x = element_blank(),
        plot.title = element_text(face = "bold", size = 12))

# ---------- Panel A: crossover-rate sex ratio (female:male) ----------
# Papio anubis: sex-specific genetic map length stated directly in main text (Wall et
# al. 2022) -- 2,080 cM male / 2,506 cM female, over the same 2,591.3 Mb physical
# autosome length used throughout this review for this species (Mb cancels in the
# ratio, so cM ratio = cM/Mb ratio here).
# Plecturocebus cupreus and Daubentonia madagascariensis: sex-specific cM/Mb already
# stated directly in their own papers' Table 1.
# Papio papio and Macaca mulatta: Burt, Bell &
# Harvey (1991) J Evol Biol 4:259-277, as compiled/re-presented in Mank (2009) Genet
# Res 91:355-363, Table 1 -- sex-specific autosomal crossover (chiasma) counts per
# chromosome, cytogenetic method (Mank 2009's own Methods: "For all species, I only
# analysed the autosomal portions of the genome"). Values (female, male crossovers per
# chromosome): Papio papio 1.5850, 1.9800; Macaca mulatta 1.9800, 2.0750 -- both
# independently reproduce Mank's own reported heterochiasmy statistic ((F-M)/mean) to
# 4 decimal places (-0.2216, -0.0469), confirming the table was read correctly.
# NOT cM/Mb (a raw per-chromosome chiasma count instead) but the female:male RATIO is
# still directly comparable and plottable on the same axis -- ratios are unit-
# invariant as long as the same units are used for both sexes, which they are here
# (same cytogenetic count convention for both). XO only, no NCO data in Burt et al.
# 1991 -- cytogenetic chiasma counting cannot detect NCO events (same structural
# limitation already documented throughout this review) -- so these 2 species extend
# Panel A only, not Panel B. This is also this review's first-ever heterochiasmy data
# point for Macaca mulatta (its own WGS pedigree study is paternal-only) and for
# Papio papio specifically (a different baboon species than Papio anubis, already in
# this panel, and than Papio hamadryas, tracked elsewhere in this review for cM/Mb).
co_data <- tribble(
  ~species, ~female_cmmb, ~male_cmmb, ~method,
  "Papio anubis", 2506/2591.3, 2080/2591.3, "Pedigree (direct)",
  "Plecturocebus cupreus", 1.00, 1.04, "Pedigree (direct)",
  "Daubentonia madagascariensis", 0.94, 0.77, "Pedigree (direct)",
  "Papio papio", 1.5850, 1.9800, "Cytogenetic (Chiasma)",
  "Macaca mulatta", 1.9800, 2.0750, "Cytogenetic (Chiasma)"
) %>%
  mutate(ratio = female_cmmb / male_cmmb,
         clade = factor(SPECIES_CLADE[as.character(species)], levels = CLADE_LEVELS))

# Ordered by clade (matching Panel C's convention) --
# Cercopithecidae (all 3: Papio anubis, Papio papio, Macaca mulatta), then Platyrrhini
# , then Strepsirrhini.
PANEL_A_ORDER <- c("Papio anubis", "Papio papio", "Macaca mulatta",
                    "Plecturocebus cupreus", "Daubentonia madagascariensis")
co_data <- co_data %>% mutate(species = factor(species, levels = PANEL_A_ORDER))

# Shared y-axis scale across both panels for direct side-by-side comparison -- the
# max female:male ratio in this figure is Papio anubis' NCO rate (1.82), so both
# panels use the same 0-2 range regardless of which one it occurs in.
Y_MAX <- 2
Y_BREAKS <- seq(0, Y_MAX, 0.5)

# Shape marker above each bar indicates method (Pedigree vs. Cytogenetic Chiasma) --
# same technique as Figure_3's Panel A (crossover homeostasis), which faced the exact
# same problem (bars needing a secondary method encoding once more than one method
# entered the panel). Circle/diamond match this review's shape convention (circle =
# Pedigree, diamond = Cytogenetic Chiasma, per Figure_1/Figure_2-Panel-A).
# Chiasma = triangle(17), matching Figure_2 Panel A's shape convention --
# diamond(18) would collide with this same figure's own Panel C pyrho=diamond.
METHOD_SHAPES_A <- c("Pedigree (direct)" = 16, "Cytogenetic (Chiasma)" = 17)

panelA <- ggplot(co_data, aes(x = species, y = ratio)) +
  geom_col(aes(fill = clade), width = 0.5, color = "black", linewidth = 0.3) +
  geom_hline(yintercept = 1, linetype = "dashed", color = "grey40", linewidth = 0.3) +
  geom_point(aes(y = ratio + 0.06, shape = method), fill = "black", color = "black", size = 2.2) +
  scale_fill_manual(values = CLADE_COLORS, guide = "none") +
  scale_shape_manual(values = METHOD_SHAPES_A, name = "Method") +
  scale_x_discrete(limits = PANEL_A_ORDER) +
  scale_y_continuous(limits = c(0, Y_MAX), breaks = Y_BREAKS, expand = c(0, 0)) +
  labs(x = NULL, y = "Female:male ratio",
       title = "A. Crossover-rate heterochiasmy") +
  base_theme +
  theme(legend.position = "bottom")

# ---------- Panel B: non-crossover-rate sex ratio (female:male NCO rate) ----------
# All 3 rows are "Pedigree (direct)" -- the only method that can detect NCO
# events at all in this review (cytogenetic chiasma/MLH1 counting structurally
# cannot; see the Panel A note above on why Burt/Mank's 1991 data doesn't
# extend to this panel). Added the same method marker as Panel A/C anyway
# purely for transparency/consistency across the
# figure, even though every point here shares one shape -- a reader shouldn't
# have to infer "these must all be pedigree" from Panel A's absence of a
# cytogenetic Panel B counterpart.
nco_data <- tribble(
  ~species, ~female_rate, ~male_rate, ~method,
  "Papio anubis", 9.71, 5.34, "Pedigree (direct)",
  "Plecturocebus cupreus", 4.20, 3.69, "Pedigree (direct)",
  "Daubentonia madagascariensis", 6.4, 7.4, "Pedigree (direct)"
) %>%
  mutate(ratio = female_rate / male_rate,
         species = factor(species, levels = SPECIES_ORDER),
         clade = factor(SPECIES_CLADE[as.character(species)], levels = CLADE_LEVELS))

panelB <- ggplot(nco_data, aes(x = species, y = ratio)) +
  geom_col(aes(fill = clade), width = 0.5, color = "black", linewidth = 0.3) +
  geom_hline(yintercept = 1, linetype = "dashed", color = "grey40", linewidth = 0.3) +
  geom_point(aes(y = ratio + 0.06, shape = method), fill = "black", color = "black", size = 2.2) +
  scale_fill_manual(values = CLADE_COLORS, guide = "none") +
  scale_shape_manual(values = METHOD_SHAPES_A, name = "Method") +
  scale_y_continuous(limits = c(0, Y_MAX), breaks = Y_BREAKS, expand = c(0, 0)) +
  labs(x = NULL, y = "Female:male NCO rate ratio",
       title = "B. Non-crossover-rate heterochiasmy") +
  base_theme +
  theme(legend.position = "bottom")

# ---------- Panel C: X-vs-autosome (X/A) recombination ratio ----------
# 5 species / 6 estimates -- the only species in this review with any real X/A
# recombination data (see Figure_4/Primate_XvA_Survey.txt and
# supplemental_XvA_table.csv for the full derivation of every value here).
# Plots the RAW X/A ratio only, not the Ne-corrected NeX/NeA figure -- the raw
# ratio is the one quantity genuinely available and comparable across all 5
# species; the Ne-corrected version (which isolates the demographic/breeding-
# sex-ratio signal from the mechanical male-X-hemizygosity effect) only exists
# for the 3 great apes (Woerner 2016 dissertation, via an independent method
# not replicated for aye-aye or marmoset) -- mixing the two would itself be a
# methods mismatch, so the corrected apes-only figures are reported in the
# text/caption instead, not plotted here.
#
# Great apes: chrX and autosomal rho/kb (Stevison, Woerner et al., unpublished
# maps) converted to cM/Mb using this project's own already-validated,
# independently-sourced Ne per species (same values used for each species'
# autosomal cM/Mb in Central_Comparison_Table.xlsx) -- the autosomal cM/Mb
# recovered this way reproduces the central table to 4 decimal places, and
# since the same Ne is applied to both X and A, the ratio is numerically
# identical to the raw rho ratio either way.
# Aye-aye: direct pedigree cM/Mb, sex-averaged, no Ne needed at all -- the
# most secure ratio in this panel.
# Marmoset: LD-based dual-estimator, ratio-only (X and A cM/Mb deliberately
# not computed -- no independently-validated Ne exists for this species, per
# CLAUDE.md; the ratio itself doesn't require one, since Ne cancels).
xva_data <- tribble(
  ~species, ~xa_ratio, ~method, ~estimator, ~X_cM_Mb, ~A_cM_Mb, ~Ne_used, ~Ne_source,
  ~NeX_NeA_corrected, ~Nf_Nm_corrected, ~corrected_value_source, ~reference, ~notes,
  "Pan paniscus", 0.5237, "LD-based, Ne-converted", "LDhat", 0.3610, 0.6893, "23230",
  "Han et al. 2024 Curr Biol", 0.85, 2.06, "Woerner 2016 dissertation (Appendix B)",
  "Stevison, Woerner et al. (unpublished chrX map)",
  "A cM/Mb reproduces central-table autosomal value to 4 decimals -- validated conversion. Raw ratio conflates demographic signal with male X-hemizygosity; NeX/NeA is the demography-isolated figure.",

  "Pan troglodytes ellioti", 0.6191, "LD-based, Ne-converted", "LDhat", 0.4457, 0.7199, "27795",
  "de Manuel et al. 2016 Science (via Fontsere et al. 2022)", 1.00, 7.19,
  "Woerner 2016 dissertation (Appendix B)", "Stevison, Woerner et al. (unpublished chrX map)",
  "A cM/Mb reproduces central-table autosomal value to 4 decimals -- validated conversion. Highest Nf:Nm skew of the three apes.",

  "Gorilla gorilla gorilla", 0.5069, "LD-based, Ne-converted", "LDhat", 0.3764, 0.7424, "31777",
  "McManus et al. 2015 MBE", 0.82, 1.70, "Woerner 2016 dissertation (Appendix B)",
  "Stevison, Woerner et al. (unpublished chrX map)",
  "A cM/Mb reproduces central-table autosomal value to 4 decimals -- validated conversion.",

  "Daubentonia madagascariensis", 0.7180, "Pedigree (direct)", "n/a", 0.61, 0.85,
  "n/a (direct pedigree cM/Mb, no Ne needed)", "n/a", NA, NA,
  "n/a -- 0.5 breeding sex ratio via SFS-based demographic inference, a different method, not directly comparable to NeX/NeA",
  "Terbot et al. 2025 Am J Primatol (X vs. autosomal diversity paper)",
  "Only row needing no Ne at all -- direct, most secure ratio. ~30% X reduction framed by the paper as mechanical (males contribute zero non-PAR X recombination), not a finding requiring explanation.",

  "Callithrix jacchus", 0.3600, "LD-based, ratio-only", "LDhat", NA, NA,
  "n/a -- ratio only, no Ne applied", "not independently validated for this species",
  NA, NA, "n/a", "Soni, Versoza, Shah, Pfeifer & Jensen 2026 GBE (X-chromosome dynamics paper)",
  "X and A cM/Mb deliberately left blank -- converting would require an unvalidated implicit Ne (same caveat as Xue et al. 2020 macaque). Ratio itself needs no Ne (cancels out).",

  "Callithrix jacchus", 0.5100, "LD-based, ratio-only", "pyrho", NA, NA,
  "n/a -- ratio only, no Ne applied", "not independently validated for this species",
  NA, NA, "n/a", "Soni, Versoza, Shah, Pfeifer & Jensen 2026 GBE (X-chromosome dynamics paper)",
  "Same species as row above, second estimator. Paper's own benchmarking suggests LDhat overestimates the X rate less than pyrho under twin-birth/chimerism-violated assumptions, but neither is picked as definitively more reliable."
) %>%
  mutate(clade = factor(SPECIES_CLADE[as.character(species)], levels = CLADE_LEVELS),
         # Shape encodes the actual estimator (LDhat vs. pyrho), not the
         # Ne-conversion status -- "Ne-converted" vs.
         # "ratio-only" isn't a meaningful distinction for a ratio itself
         # (Ne cancels identically either way). LDhat/pyrho is the real
         # methodological axis, and it's especially informative for
         # marmoset's own two points, which previously shared one shape
         # despite using different estimators.
         method_group = case_when(
           estimator == "LDhat" ~ "LDhat",
           estimator == "pyrho" ~ "pyrho",
           TRUE ~ "Pedigree (direct)"
         ))

# Ordered by clade (Apes -> Cercopithecidae -> Platyrrhini -> Strepsirrhini),
# not by ratio value -- rank-ordering by value would visually
# imply these 6 estimates are directly cross-comparable, which cuts against
# the whole point of shape-coding by method (they're method-heterogeneous,
# not a clean ranked series the way Figure_2/Figure_3's raw/unbinned Gini
# values are). Within Apes (the only clade with >1 species here), ordered
# bonobo/Nigerian chimp/gorilla to match this project's usual ape ordering
# elsewhere.
xva_order <- c("Pan paniscus", "Pan troglodytes ellioti", "Gorilla gorilla gorilla",
               "Callithrix jacchus", "Daubentonia madagascariensis")

# Deterministic fan-out for marmoset's 2 points (same species, same x slot) --
# matches the fixed-offset convention used in Figure_2/build_gini_dotplot.R,
# not random jitter, so multi-estimate species stay visible and reproducible.
xva_data <- xva_data %>%
  mutate(species = factor(species, levels = xva_order)) %>%
  group_by(species) %>%
  mutate(x_num = as.numeric(species) + (row_number() - (n() + 1) / 2) * 0.25) %>%
  ungroup()

# Shape consistency: circle is reserved for
# Pedigree everywhere in this review (Figure_1's Method ring, Figure_2 Panel
# A, Figure_3's METHOD_SHAPES), so LDhat does not use circle here,
# especially since Pedigree (direct) is also a real category in
# this same panel. Matches Figure_2/build_gini_dotplot.R's
# ESTIMATOR_SHAPES exactly: LDhat = square (this review's predominant
# LD-based estimator, same shape Figure_1/Figure_2-Panel-A use for generic
# "LD-based"), pyrho = diamond, Pedigree (direct) = circle.
XVA_SHAPES <- c("LDhat" = 15, "pyrho" = 18, "Pedigree (direct)" = 16)

panelC <- ggplot(xva_data, aes(x = x_num, y = xa_ratio, color = clade, shape = method_group)) +
  geom_hline(yintercept = 0.81, linetype = "dotted", color = "grey50", linewidth = 0.4) +
  annotate("text", x = 0.55, y = 0.81, label = "human", hjust = 0, vjust = -0.6,
           size = 3, color = "grey40") +
  geom_point(size = 3.5, stroke = 1.1) +
  scale_color_manual(values = CLADE_COLORS, guide = "none") +
  scale_shape_manual(values = XVA_SHAPES, name = "Detection method") +
  scale_x_continuous(breaks = seq_along(xva_order), labels = xva_order,
                      limits = c(0.5, length(xva_order) + 0.5), expand = c(0, 0)) +
  scale_y_continuous(limits = c(0, 1), breaks = seq(0, 1, 0.25), expand = expansion(mult = c(0.02, 0.06))) +
  labs(x = NULL, y = "X / Autosome recombination-rate ratio",
       title = "C. X-vs-Autosome Recombination") +
  base_theme +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, face = "italic", size = 10),
        legend.position = "bottom")

# ---------- Shared clade legend strip ----------
# Built from real per-clade points (not borrowed from a panel's own bar/point
# legend) -- a panel-native legend only shows clades actually present in that
# panel's own data (e.g. Panel B has no Apes rows at all), and forcing extra
# levels via drop=FALSE on a geom_col produces an invisible/empty swatch for
# the absent level (confirmed -- Apes' key rendered blank). Same fix already
# used in Figure_2/build_gini_dotplot.R: a dedicated strip with one real point
# per clade, alpha=0 to hide the (identically-positioned, so visually
# stacked) points themselves while keeping the legend swatches opaque via
# override.aes. All 3 real panels' own clade fill/color guides are
# suppressed (guide="none") so this strip is the only source of the Clade
# legend.
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

# All 3 panels side by side in one row -- (A+B) stacked above C left C
# stretched out disproportionately wide relative to its 5 species. Width
# ratio 3:3:5 matches each panel's species
# count (A/B = 3 species each, C = 5) directly, so panel width scales with
# how much x-axis content each one actually has.
combined <- clade_legend_plot / (panelA + panelB + panelC + plot_layout(widths = c(5, 3, 5))) +
  plot_layout(heights = c(0.1, 1))

ggsave(file.path(OUT_DIR, "Figure_4_heterochiasmy.png"),
       combined, width = 16, height = 6.5, dpi = 1200, bg = "white")
ggsave(file.path(OUT_DIR, "Figure_4_heterochiasmy.pdf"),
       combined, width = 16, height = 6.5, bg = "white")

cat("Saved Figure_4_heterochiasmy.png/.pdf\n")

supp <- co_data %>%
  select(species, clade, method, female_cmmb, male_cmmb, co_ratio_female_over_male = ratio) %>%
  left_join(nco_data %>% select(species, female_rate, male_rate, nco_ratio_female_over_male = ratio),
            by = "species") %>%
  arrange(match(species, PANEL_A_ORDER))

write.csv(supp, file.path(OUT_DIR, "supplemental_heterochiasmy_table.csv"),
          row.names = FALSE)
cat("Saved supplemental_heterochiasmy_table.csv\n")

write.csv(xva_data %>%
            select(species, clade, method, estimator, X_cM_Mb, A_cM_Mb, xa_ratio_raw = xa_ratio,
                   Ne_used, Ne_source, NeX_NeA_corrected, Nf_Nm_corrected,
                   corrected_value_source, reference, notes) %>%
            arrange(match(species, xva_order)),
          file.path(OUT_DIR, "supplemental_XvA_table.csv"),
          row.names = FALSE)
cat("Saved supplemental_XvA_table.csv\n")
