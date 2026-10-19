# Run from the repository root, e.g.  Rscript Scripts/figure3_nco_deepdive/build_nco_deepdive.R
OUT_DIR <- "Figures/Figure3_NCO_Deepdive"
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
  "Pan troglodytes" = "Apes", "Gorilla gorilla gorilla" = "Apes", "Hylobates lar" = "Apes",
  "Papio anubis" = "Cercopithecidae", "Papio papio" = "Cercopithecidae",
  "Macaca mulatta" = "Cercopithecidae", "Macaca nemestrina" = "Cercopithecidae",
  "Plecturocebus cupreus" = "Platyrrhini",
  "Daubentonia madagascariensis" = "Strepsirrhini"
)

# Detection method per species -- same split both panels share: direct
# pedigree transmission counts vs. pooled germline long-read
# sequencing (Porsborg et al. 2025), matching the caption's own method split.
# Shared between Panel A and Panel B, both as a shape aesthetic, so the two
# panels' shape legends merge into one under plot_layout(guides = "collect") --
# same treatment as the shared Clade color legend.
METHOD_LEVELS <- c("Pedigree", "Long-read testis/sperm")
SPECIES_METHOD <- c(
  "Papio anubis" = "Pedigree", "Macaca mulatta" = "Pedigree",
  "Plecturocebus cupreus" = "Pedigree", "Daubentonia madagascariensis" = "Pedigree",
  "Pan troglodytes" = "Long-read testis/sperm", "Gorilla gorilla gorilla" = "Long-read testis/sperm",
  "Hylobates lar" = "Long-read testis/sperm", "Papio papio" = "Long-read testis/sperm",
  "Macaca nemestrina" = "Long-read testis/sperm"
)
METHOD_SHAPES <- c("Pedigree" = 21, "Long-read testis/sperm" = 24)

make_clade_factor <- function(x) factor(x, levels = CLADE_LEVELS)
make_method_factor <- function(x) factor(x, levels = METHOD_LEVELS)

base_theme <- theme_minimal(base_size = 12) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, face = "italic"),
        panel.grid.major.x = element_blank(),
        plot.title = element_text(face = "bold", size = 12))

# ---------- Panel A: crossover homeostasis (NCO / (NCO + CO)) ----------
# Each species/study ordered by its own value, highest to lowest, matching
# Figure_2's convention (no fixed tree-order x-axis anymore).
ratio_data <- tribble(
  ~species, ~nco, ~co,
  "Papio anubis", 263, 842,
  "Macaca mulatta", 85, 165,
  "Plecturocebus cupreus", 184, 269.5,
  "Daubentonia madagascariensis", 200, 152.5,
  "Pan troglodytes", 269, 495,
  "Gorilla gorilla gorilla", 227, 215,
  "Hylobates lar", 132, 70,
  "Papio papio", 40, 69,
  "Macaca nemestrina", 131, 171
) %>%
  mutate(nco_fraction = nco / (nco + co),
         clade = make_clade_factor(SPECIES_CLADE[as.character(species)]),
         method = make_method_factor(SPECIES_METHOD[as.character(species)]))

homeostasis_order <- ratio_data %>%
  arrange(desc(nco_fraction)) %>%
  pull(species)
ratio_data <- ratio_data %>% mutate(species = factor(species, levels = homeostasis_order))

# Method shown as a small black marker just above each bar --
# bars stay clade-colored (the more important visual grouping), method is a
# secondary overlay rather than replacing the bar encoding. Fixed
# fill/color = "black" (not mapped) so only shape varies -- same shape codes
# (21/24) as Panel B's fillable points, so their legends merge into one.
panel_homeostasis <- ggplot(ratio_data, aes(x = species, y = nco_fraction)) +
  geom_col(aes(fill = clade), width = 0.65, color = "black", linewidth = 0.3) +
  geom_hline(yintercept = 0.5, linetype = "dashed", color = "grey40", linewidth = 0.3) +
  geom_point(aes(y = nco_fraction + 0.035, shape = method),
             fill = "black", color = "black", size = 2.2) +
  scale_fill_manual(values = CLADE_COLORS, name = "Clade") +
  scale_shape_manual(values = METHOD_SHAPES, name = "Detection method", drop = FALSE) +
  scale_x_discrete(limits = homeostasis_order) +
  scale_y_continuous(limits = c(0, 1), expand = c(0, 0)) +
  labs(x = NULL, y = "NCO / (NCO + CO)",
       title = "A. Crossover Homeostasis") +
  base_theme

# ---------- Panel B: mean NCO tract length (bp) -- dot plot, not bars ----------
# Individual per-sample points shown for the 2 multi-individual Porsborg species
# (chimp, gorilla). No range line/segment between a species' multiple points,
# same treatment already applied to Figure_2 -- independent
# estimates from different studies/individuals, not a continuous range. Ordered by
# each species' own mean value, highest to lowest, matching Figure_2's convention.
tract_points <- tribble(
  ~species, ~tract_bp, ~derivation,
  "Papio anubis", 167, "pedigree (raw)",
  "Macaca mulatta", 155, "pedigree (raw)",
  "Plecturocebus cupreus", 55, "pedigree (raw)",
  "Daubentonia madagascariensis", 161, "pedigree (raw)",
  "Pan troglodytes", 47, "long-read (model-fit)",
  "Pan troglodytes", 14, "long-read (model-fit)",
  "Pan troglodytes", 36, "long-read (model-fit)",
  "Pan troglodytes", 92, "long-read (model-fit)",
  "Gorilla gorilla gorilla", 32, "long-read (model-fit)",
  "Gorilla gorilla gorilla", 50, "long-read (model-fit)",
  "Gorilla gorilla gorilla", 43, "long-read (model-fit)",
  "Hylobates lar", 20, "long-read (model-fit)",
  "Papio papio", 96, "long-read (model-fit)",
  "Macaca nemestrina", 22, "long-read (model-fit)"
) %>%
  mutate(clade = make_clade_factor(SPECIES_CLADE[as.character(species)]),
         method = make_method_factor(SPECIES_METHOD[as.character(species)]))

tract_order <- tract_points %>%
  group_by(species) %>%
  summarise(mean_val = mean(tract_bp), .groups = "drop") %>%
  arrange(desc(mean_val)) %>%
  pull(species)
tract_points <- tract_points %>% mutate(species = factor(species, levels = tract_order))

# Shape encodes method -- fillable shapes (21/24, same codes as Panel A's
# overlay markers) so `derivation` (already computed) is shown directly on
# the plot. Shape legend suppressed here (guide="none") -- tried
# letting plot_layout(guides="collect") merge it with Panel A's identical
# scale, but the merge silently dropped the triangle entry from Panel B's own
# copy of the legend (a patchwork/ggplot guide-merging quirk when one panel's
# points have a fixed fill and the other's are aes-mapped). Panel A's legend
# alone is the single source of truth for what circle/triangle mean, same
# asymmetric-legend pattern already used in Figure_2 (Data type under Panel A
# only, Estimator under Panel B only).
panel_tract <- ggplot() +
  geom_point(data = tract_points, aes(x = species, y = tract_bp, fill = clade, shape = method),
             size = 3.2, color = "black", stroke = 0.4,
             position = position_jitter(width = 0.06, height = 0, seed = 1)) +
  scale_fill_manual(values = CLADE_COLORS, guide = "none") +
  scale_shape_manual(values = METHOD_SHAPES, guide = "none") +
  scale_x_discrete(limits = tract_order) +
  labs(x = NULL, y = "Mean NCO tract length (bp)",
       title = "B. Non-crossover tract length") +
  base_theme

combined <- panel_homeostasis + panel_tract +
  plot_layout(guides = "collect") &
  theme(legend.position = "bottom")

ggsave(file.path(OUT_DIR, "Figure_3_NCO_deepdive.png"),
       combined, width = 11, height = 5.5, dpi = 1200, bg = "white")
ggsave(file.path(OUT_DIR, "Figure_3_NCO_deepdive.pdf"),
       combined, width = 11, height = 5.5, bg = "white")

cat("Saved Figure_3_NCO_deepdive.png/.pdf\n")

# ---------- Combined supplemental table (both panels, one file, outer join) ----------
tract_summary <- tract_points %>%
  group_by(species) %>%
  summarise(tract_bp_values = paste(tract_bp, collapse = ";"),
            tract_bp_mean = round(mean(tract_bp), 1),
            derivation = first(derivation), .groups = "drop")

supp <- ratio_data %>%
  select(species, clade, nco, co, nco_fraction) %>%
  mutate(nco_fraction = round(nco_fraction, 4)) %>%
  full_join(tract_summary, by = "species") %>%
  arrange(desc(nco_fraction))

write.csv(supp, file.path(OUT_DIR, "supplemental_nco_deepdive_table.csv"),
          row.names = FALSE)
cat("Saved supplemental_nco_deepdive_table.csv\n")
