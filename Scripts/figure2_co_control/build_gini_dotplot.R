# Run from the repository root, e.g.  Rscript Scripts/figure2_co_control/build_gini_dotplot.R
OUT_DIR <- "Figures/Figure2_CO_Control"
if (!dir.exists(OUT_DIR)) stop("Run this script from the repository root.")

library(ggplot2)
library(dplyr)
library(patchwork)

CLADE_LEVELS <- c("Apes", "Cercopithecidae", "Platyrrhini", "Strepsirrhini")
CLADE_COLORS <- c(
  "Apes"               = "#d95f02",
  "Cercopithecidae"  = "#7570b3",
  "Platyrrhini"  = "#1b9e77",
  "Strepsirrhini"             = "#e6ab02"
)

# ============================================================================
# PANEL A: crossover assurance (broad-scale CO control) -- chromosome vs. arm
# ============================================================================
# One obligate crossover per chromosome/bivalent is required for correct
# homolog segregation at meiosis I (Jones & Franklin 2006) -- directly stated
# and confirmed in this review's own source papers for macaque (Versoza et al.
# 2024), aye-aye (Versoza et al. 2025), and chimp (Auton et al. 2012 SOM).
# This panel checks that floor across every species/study in the review with
# enough information to compute it: implied COs per bivalent =
# (total sex-averaged autosomal cM) / 50 / (number of autosome pairs).
#
# Deliberately broader coverage than Panel B (Gini) -- this only needs a total
# genetic map length and a chromosome count, not a fine-scale positional map,
# so it includes species/studies that could never support a Gini value at all
# (the older microsatellite pedigree maps: Rogers 2000, Cox 2006, Rogers 2006).
# The two panels are NOT meant to share one x-axis/species list the way
# Figure_3/4's panels do -- Panel A's species set is intentionally wider.
#
# Method preference per species: direct observation (pedigree CO count or
# cytogenetic MLH1/chiasma count per cell, both already a per-meiosis/per-cell
# count) used wherever available, in preference to an LD-based
# population-scaled cM/Mb figure for that same species. Where only an LD-based
# value exists (all 5 apes' primary metric, marmoset), that is used with the
# caveat noted below -- an LD-derived total is a historical, population-scaled
# estimate, not a literal per-generation count, so it can and should still
# recover the obligate-CO floor if the floor is real, but isn't as direct a
# check as a pedigree/cytogenetic count.
#
# Excluded: Porsborg et al. (2025) long-read species (gorilla, chimp, lar
# gibbon, Guinea baboon, pig-tailed macaque, where no pedigree/LD alternative
# exists for that exact population) -- testis long-read sequencing samples
# many pooled germ cells, not a countable number of discrete meioses, so a
# per-meiosis normalization isn't a meaningful quantity from that data
# structure. Where an LD or pedigree alternative already represents that
# species (chimp, gorilla), that alternative is used instead.
#
# Chromosome/bivalent (autosome pair) counts verified directly against this
# project's own deposited map file counts where possible (bonobo/chimp/
# gorilla, gibbon, Auton chimp, vervet, marmoset, titi monkey) or against
# primary-literature karyotype statements (macaque/baboon 20; aye-aye 2n=30 ->
# 14, per Versoza et al. 2025; Cebus/Sapajus 2n=54 -> 26 and Alouatta caraya
# 2n=52 -> 25, per Garcia-Cruz et al. 2009/2011, fetched directly for this
# panel) -- not assumed from general recollection. A legacy duplicate chr2
# file affecting the great-ape physical-length/chromosome-count figures was
# identified and fixed before this panel was built.
#
# CHROMOSOME vs. ARM: Dumont (2017, Genetics 205:155-168) tests
# whether the obligate-CO floor operates at the level of the whole chromosome
# (implied COs per bivalent >= 1, using autosome-PAIR count n_bivalents -- the
# panel's original scope) or at the level of the chromosome ARM (implied COs
# per arm >= 1, using autosomal fundamental number aFN -- each metacentric
# autosome contributes 2 arms, each acrocentric 1, so aFN >= n_bivalents
# always and the arm-level value is always <= the chromosome-level value for
# the same species). This is the central methodological point of her paper,
# not a new idea introduced here -- adding it lets this panel actually test
# it. aFN sourced from Dumont's own Table S1 (`papers/tables1.xlsx`) for the
# 11 new species added below,
# AND, where her table happens to independently cover a species already in
# this panel, backfilled onto the existing rows too (Alouatta caraya, 3
# Cebus/Sapajus species, Macaca mulatta, Pan troglodytes, Papio hamadryas --
# 8 species, 10 rows) -- cross-checked first: her own 2N figure for every one
# of these already implies the same n_bivalents already used in this panel
# (e.g. Papio hamadryas 2N=42 -> 20 autosome pairs, matching the existing
# row), confirming this is the same convention, not a second inconsistent
# source. No aFN exists in Dumont's table for the other 8 species/rows in
# this panel (Pan paniscus, Gorilla gorilla gorilla, Nomascus leucogenys,
# Papio anubis, Chlorocebus sabaeus, Callithrix jacchus, Plecturocebus
# cupreus, Daubentonia madagascariensis) -- these simply have
# no arm-level point rather than an invented/approximated one (e.g. NOT
# extending chimp's aFN to bonobo despite the shared 2n=48 karyotype and close
# relatedness -- Dumont's own table has no bonobo row, so none is added here).

# `species` is the true biological species (grouping/x-axis key, matching
# Panel B's convention); `study_label` keeps the study-specific detail (e.g.
# which of the 2 baboon/macaque pedigree maps, or Nigerian vs. western chimp)
# for the supplemental table and hover-level detail without splitting the
# x-axis. Species with >1 estimate below (Pan troglodytes, Papio hamadryas,
# Macaca mulatta, Cebuella pygmaea, Saguinus oedipus) are shown as multiple
# jittered points + a range segment, the same convention Panel B already uses.
# All 4 great-ape LD-based cM/Mb values use a dedicated demographic
# study's point estimate rather than a Prado-Martinez et al. (2013) Ne range
# midpoint (bonobo: Han et al. 2024; Nigerian + western chimp:
# de Manuel et al. 2016 via Fontsere et al. 2022; gorilla: McManus et al.
# 2015).
assurance_data <- tribble(
  ~species, ~study_label, ~clade, ~total_cM, ~n_bivalents, ~aFN, ~aFN_reference, ~source_type, ~reference,
  # Apes -- all LD-based (no pedigree/cytogenetic alternative in this review); no aFN
  # available anywhere in this clade (Dumont's table has no Pan paniscus, Gorilla, or
  # gibbon rows).
  # aFN_reference column: the karyotype source for aFN is a DIFFERENT
  # citation than `reference` (which is the source of the crossover count/total_cM).
  # Where aFN comes from Dumont's own Table S1, cited via Dumont's own "KARYOTYPE
  # REFERENCE" column (papers/tables1.xlsx) -- the primary karyotype paper Dumont
  # herself cites, not the Dumont 2017 compilation itself, per this project's
  # standing citation policy.
  # aFN=82 reuses chimp's own Dumont-sourced aFN, since
  # bonobo/chimp are sister species with a near-identical 2n=48 karyotype -- see
  # Figure_1/build_itol_arm_assurance_binary.py for the full reasoning.
  "Pan paniscus", "Pan paniscus", "Apes", 0.6893 * 2403.18, 23, 82, "Yunis 1982 Science 215:1525-1530 (Pan troglodytes karyotype, reused via sister-species 2n=48 conservation -- no bonobo-specific karyotype source found)", "LD-based", "Stevison et al. 2016 MBE (independent Ne)",
  "Pan troglodytes", "Pan troglodytes (Nigerian)", "Apes", 0.7199 * 2429.53, 23, 82, "Yunis 1982 Science 215:1525-1530 (Dumont et al. 2017 Table S1 karyotype source)", "LD-based", "Stevison et al. 2016 MBE (independent Ne)",
  "Pan troglodytes", "Pan troglodytes (western)", "Apes", 0.9931 * 2647.2, 23, 82, "Yunis 1982 Science 215:1525-1530 (Dumont et al. 2017 Table S1 karyotype source)", "LD-based", "Auton et al. 2012 Science (independent Ne)",
  # Apes -- found via a full re-audit of Dumont's Table S1 against
  # every species already in this review (not just species with zero prior data) --
  # this row was silently skipped in the original cross-check pass because chimp
  # already had LD-based data. This is the ONLY cytogenetic data point for any ape
  # anywhere in Dumont's table (no bonobo/gorilla/gibbon rows exist there). Shown
  # under the shared "Pan troglodytes" x-axis grouping this panel already uses for
  # both subspecies, so this row's own subspecies attribution doesn't change the
  # x-axis position -- the study_label/reference reflect the following reasoning:
  # Pardo-Manuel de Villena & Sapienza (2001) themselves cite no subspecies, and the
  # citation trail (via Burt & Bell 1987) dead-ends 3 compilations deep with no
  # recoverable subspecies attribution -- assigned to western chimp on a historical-
  # plausibility argument (meiotic chiasma counting requires captive-animal testicular
  # tissue, and mid-20th-century Western biomedical/zoo chimp collections were
  # overwhelmingly West African; the Nigeria-Cameroon population wasn't even
  # recognized as a distinct subspecies until molecular work in the 1990s-2000s).
  "Pan troglodytes", "Pan troglodytes (Chiasma, western)", "Apes", 52.5 * 50, 23, 82, "Yunis 1982 Science 215:1525-1530 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (Chiasma)", "Pardo-Manuel de Villena & Sapienza 2001 Mamm Genome (western chimp per historical-plausibility inference, not a confirmed citation)",
  # aFN=80 (Gorilla beringei source, genus-level extrapolation -- see
  # Figure_1/build_itol_arm_assurance_binary.py for the full reasoning).
  "Gorilla gorilla gorilla", "Gorilla gorilla gorilla", "Apes", 0.7424 * 2419.07, 23, 80, "Mai 1983 (Gorilla beringei karyotype description; genus-level extrapolation to G. g. gorilla -- full bibliographic detail beyond author/year not independently verified)", "LD-based", "Stevison et al. 2016 MBE (independent Ne)",
  # aFN=90 (Harding 2013 Mammalian Species account, FN=94
  # citing Chiarelli 1972, converted to aFN via the female-XX-complement
  # convention -- see Figure_1/build_itol_arm_assurance_binary.py).
  "Nomascus leucogenys", "Nomascus leucogenys", "Apes", 1.5498 * 2650.18, 25, 90, "Harding 2013 Mammalian Species 44(890):1-15, citing Chiarelli 1972 (FN=94, converted to aFN=90)", "LD-based", "Stevison, unpublished",
  # Cercopithecidae -- pedigree preferred where available
  # aFN=80 (reused Papio hamadryas's own Dumont-sourced aFN
  # via same-genus conservation -- see Figure_1/build_itol_arm_assurance_binary.py).
  "Papio anubis", "Papio anubis", "Cercopithecidae", 2293.5, 20, 80, "Moore et al. 1999 Am J Phys Anthropol 110:119-127 (Papio hamadryas karyotype, Dumont et al. 2017 Table S1 source, reused via same-genus conservation)", "Pedigree", "Wall, Robinson & Cox 2022 GBE",
  "Papio hamadryas", "Papio hamadryas (Rogers 2000)", "Cercopithecidae", 2375, 20, 80, "Moore et al. 1999 Am J Phys Anthropol 110:119-127 (Dumont et al. 2017 Table S1 karyotype source)", "Pedigree", "Rogers et al. 2000 Genomics",
  "Papio hamadryas", "Papio hamadryas (Cox 2006)", "Cercopithecidae", 2354, 20, 80, "Moore et al. 1999 Am J Phys Anthropol 110:119-127 (Dumont et al. 2017 Table S1 karyotype source)", "Pedigree", "Cox et al. 2006 Genomics",
  "Macaca mulatta", "Macaca mulatta (Indian, captive)", "Cercopithecidae", 2357, 20, 80, "Small et al. 1985 Am J Primatol 9:63-67 (Dumont et al. 2017 Table S1 karyotype source)", "Pedigree (paternal-only)", "Versoza et al. 2024 GBE",
  "Macaca mulatta", "Macaca mulatta (Rogers 2006)", "Cercopithecidae", 2048, 20, 80, "Small et al. 1985 Am J Primatol 9:63-67 (Dumont et al. 2017 Table S1 karyotype source)", "Pedigree", "Rogers et al. 2006 Genomics",
  # aFN=116 (Stock & Hsu 1973, Cercopithecus aethiops species
  # group total FN=120 minus X/Y -- flagged BORDERLINE, +/-2-4 arm uncertainty --
  # see Figure_1/build_itol_arm_assurance_binary.py for the full reasoning).
  "Chlorocebus sabaeus", "Chlorocebus sabaeus", "Cercopithecidae", 2726, 29, 116, "Stock & Hsu 1973 Chromosoma 43:211-224 (Cercopithecus aethiops species group; BORDERLINE, +/-2-4 arm uncertainty per 7 disputed 'short second arm' pairs)", "Pedigree", "Jasinska et al. 2007 Mamm Genome",
  # Cercopithecidae -- from Dumont et al. 2017 Table S1, all
  # Cytogenetic; cite the original measurement, not the Dumont compilation, per this
  # project's standing citation policy. The two
  # Macaca mulatta rows (and Macaca nemestrina below) were, like chimp above, silently
  # skipped in the original cross-check pass since these species already had other
  # data -- found via the same re-audit.
  "Macaca mulatta", "Macaca mulatta (MLH1)", "Cercopithecidae", 39.0 * 50, 20, 80, "Small et al. 1985 Am J Primatol 9:63-67 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (MLH1)", "Hassold et al. 2009 Cytogenet Genome Res",
  "Macaca mulatta", "Macaca mulatta (Chiasma)", "Cercopithecidae", 38.0 * 50, 20, 80, "Small et al. 1985 Am J Primatol 9:63-67 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (Chiasma)", "Pardo-Manuel de Villena & Sapienza 2001 Mamm Genome",
  "Macaca nemestrina", "Macaca nemestrina", "Cercopithecidae", 40.0 * 50, 20, 80, "Brown et al. 1986 Folia Primatol 46:164-172 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (Chiasma)", "Pardo-Manuel de Villena & Sapienza 2001 Mamm Genome",
  "Macaca fuscata", "Macaca fuscata", "Cercopithecidae", 36.7 * 50, 20, 80, "Wienberg et al. 1992 Chromosoma 101:265-270 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (Chiasma)", "Pardo-Manuel de Villena & Sapienza 2001 Mamm Genome",
  "Macaca nigra", "Macaca nigra", "Cercopithecidae", 39.0 * 50, 20, 80, "Brown et al. 1986 Folia Primatol 46:164-172 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (Chiasma)", "Burt & Bell 1987 Nature",
  "Mandrillus sphinx", "Mandrillus sphinx", "Cercopithecidae", 45.0 * 50, 20, 80, "Ruiz-Herrera et al. 2005 Cytogenet Genome Res 108:234-247 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (Chiasma)", "Pardo-Manuel de Villena & Sapienza 2001 Mamm Genome",
  "Miopithecus talapoin", "Miopithecus talapoin", "Cercopithecidae", 39.7 * 50, 27, 92, "Dutrillaux et al. 1978 Hum Genet 45:283-296 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (MLH1)", "Segura et al. 2013 Proc R Soc B",
  # Platyrrhini -- cytogenetic (direct per-cell count) or pedigree preferred
  "Cebus paraguayanus", "Cebus paraguayanus", "Platyrrhini", 43.22 * 50, 26, 72, "Amaral et al. 2008 BMC Evol Biol 8:169 (Dumont et al. 2017 Table S1 karyotype source, listed there as Cebus libidinosus paraguayanus)", "Cytogenetic (MLH1)", "Garcia-Cruz et al. 2009 BMC Genetics",
  "Cebus libidinosus", "Cebus libidinosus", "Platyrrhini", 41.3 * 50, 26, 72, "Amaral et al. 2008 BMC Evol Biol 8:169 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (MLH1)", "Garcia-Cruz et al. 2011 Chromosoma",
  "Cebus nigritus", "Cebus nigritus", "Platyrrhini", 39.2 * 50, 26, 72, "Amaral et al. 2008 BMC Evol Biol 8:169 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (MLH1)", "Garcia-Cruz et al. 2011 Chromosoma",
  "Alouatta caraya", "Alouatta caraya", "Platyrrhini", 40.6 * 50, 25, 66, "Mudry et al. 1998 Hereditas 128:9-16 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (MLH1)", "Garcia-Cruz et al. 2011 Chromosoma",
  # n_bivalents corrected 20 -> 22: a karyotype source for
  # this species (Comparative chromosomal study of five taxa of genus Callithrix,
  # group Jacchus, Am J Primatol 41(1)) states 2n=46, 14 uniarmed + 30 biarmed
  # autosomes = 44 autosomes = 22 pairs, not 20 -- confirmed independently against
  # Soni et al.'s own marmoset paper, which explicitly labels marmoset autosomes as
  # "chromosomes 1-22." The old n=20 was a real error in this project's data, not a
  # source disagreement; cos_per_bivalent for marmoset in Figure_2 Panel A drops
  # from 2.4128 to 2.1934 (still clearing the obligate-minimum line comfortably, no
  # pass/fail change at the chromosome level).
  "Callithrix jacchus", "Callithrix jacchus", "Platyrrhini", 0.91 * 2651.4, 22, 74, "\"Comparative chromosomal study of five taxa of genus Callithrix, group Jacchus (Platyrrhini, primates),\" Am J Primatol 41(1) -- not in Dumont's table; author names not independently verified beyond this citation form", "LD-based", "Soni, Versoza et al. 2025/26 bioRxiv (preprint)",
  # aFN=58 (Plecturocebus caquetensis source, explicitly
  # stated in the literature as "very similar to P. cupreus" -- see
  # Figure_1/build_itol_arm_assurance_binary.py for the full reasoning).
  "Plecturocebus cupreus", "Plecturocebus cupreus", "Platyrrhini", 2450, 22, 58, "Bueno & Defler 2010 (Plecturocebus caquetensis karyotype), citing Defler et al. 2010 for explicit cross-species similarity to P. cupreus -- not in Dumont's table; full bibliographic detail beyond author/year not independently verified", "Pedigree", "Versoza et al. 2026 GBE",
  # Platyrrhini -- from Dumont et al. 2017 Table S1
  "Cebuella pygmaea", "Cebuella pygmaea (MLH1)", "Platyrrhini", 36.9 * 50, 21, 74, "Nagamachi et al. 1992 Genetica 85:249-257 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (MLH1)", "Segura et al. 2013 Proc R Soc B",
  "Cebuella pygmaea", "Cebuella pygmaea (Chiasma)", "Platyrrhini", 41.7 * 50, 21, 74, "Nagamachi et al. 1992 Genetica 85:249-257 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (Chiasma)", "Pardo-Manuel de Villena & Sapienza 2001 Mamm Genome",
  "Cebus capucinus", "Cebus capucinus", "Platyrrhini", 40.5 * 50, 26, 68, "Richard et al. 1996 Genomics 36:417-423 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (Chiasma)", "Pardo-Manuel de Villena & Sapienza 2001 Mamm Genome",
  "Saguinus oedipus", "Saguinus oedipus (MLH1)", "Platyrrhini", 38.9 * 50, 22, 86, "Segura et al. 2013 Proc R Soc B 280:20131945 (Dumont et al. 2017 Table S1 karyotype source; same paper as this row's own crossover-count reference)", "Cytogenetic (MLH1)", "Segura et al. 2013 Proc R Soc B",
  "Saguinus oedipus", "Saguinus oedipus (Chiasma)", "Platyrrhini", 39.6 * 50, 22, 86, "Segura et al. 2013 Proc R Soc B 280:20131945 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (Chiasma)", "Pardo-Manuel de Villena & Sapienza 2001 Mamm Genome",
  # Strepsirrhini
  # aFN=52 (direct species match, no substitution needed -- see
  # Figure_1/build_itol_arm_assurance_binary.py for the full reasoning).
  "Daubentonia madagascariensis", "Daubentonia madagascariensis", "Strepsirrhini", 1525, 14, 52, "Poorman-Allen & Izard 1990; Rumpler et al. 1988 (direct species match) -- not in Dumont's table; full bibliographic detail beyond author/year not independently verified", "Pedigree", "Versoza et al. 2025 GBE",
  # Strepsirrhini -- from Dumont et al. 2017 Table S1
  "Lemur catta", "Lemur catta", "Strepsirrhini", 35.9 * 50, 27, 62, "Cardone et al. 2002 Chromosoma 111:348-356 (Dumont et al. 2017 Table S1 karyotype source)", "Cytogenetic (MLH1)", "Segura et al. 2013 Proc R Soc B",
  "Eulemur fulvus", "Eulemur fulvus (nominate)", "Strepsirrhini", 36.3 * 50, 29, 62, "Hamilton et al. 1979 Int J Primatol 1:81-93 (Dumont et al. 2017 Table S1 karyotype source, listed there as Lemur fulvus)", "Cytogenetic (Chiasma)", "Pardo-Manuel de Villena & Sapienza 2001 Mamm Genome",
  "Eulemur fulvus albocollaris", "Eulemur fulvus albocollaris", "Strepsirrhini", 35.2 * 50, 23, 62, "Hamilton et al. 1979 Int J Primatol 1:81-93 (Dumont et al. 2017 Table S1 karyotype source, listed there as Lemur fulvus albocollaris)", "Cytogenetic (Chiasma)", "Pardo-Manuel de Villena & Sapienza 2001 Mamm Genome",
  "Eulemur fulvus collaris", "Eulemur fulvus collaris", "Strepsirrhini", 36.0 * 50, 24, 62, "Hamilton et al. 1979 Int J Primatol 1:81-93 (Dumont et al. 2017 Table S1 karyotype source, listed there as Lemur fulvus collaris)", "Cytogenetic (Chiasma)", "Pardo-Manuel de Villena & Sapienza 2001 Mamm Genome"
) %>%
  mutate(cos_per_bivalent = total_cM / 50 / n_bivalents,
         # aFN is a DIPLOID-scale count (same convention as 2N), matching Dumont
         # (2017)'s own explicit definition of the haploid arm count as aFN/2 (her
         # p.160: "the haploid number of autosomal chromosome arms (aFN/2)") -- so
         # the correct per-arm comparison is nXO vs aFN/2, i.e. total_cM/50/(aFN/2).
         # CORRECTED (was total_cM/50/aFN, exactly half what it should be)
         # -- that bug made every species in this review fail the arm-level test
         # uniformly; the corrected version reproduces real, mixed pass/fail results
         # matching Dumont's own reported primate pattern (e.g. "three of the four
         # macaque species... exhibit fewer crossovers... than chromosome arms").
         # A binarized (pass/fail) version of this same result also lives in Figure 1
         # (ArmAssurance_binary.txt, matching Dumont's own tree-coloring convention);
         # this continuous version is plotted directly in Panel A below,
         # once aFN coverage grew enough (28 of 30 tips) to make it the
         # more informative choice than chromosome-level -- see Panel A's own note.
         cos_per_arm = total_cM / 50 / (aFN / 2),
         clade = factor(clade, levels = CLADE_LEVELS),
         source_type = factor(source_type,
                               levels = c("Pedigree", "Pedigree (paternal-only)",
                                          "Cytogenetic (MLH1)", "Cytogenetic (Chiasma)",
                                          "LD-based")))

# Ordered by arm-level mean -- matches what's actually plotted below.
assurance_order <- assurance_data %>%
  group_by(species) %>%
  summarise(mean_val = mean(cos_per_arm), .groups = "drop") %>%
  arrange(desc(mean_val)) %>%
  pull(species)
assurance_data <- assurance_data %>% mutate(species = factor(species, levels = assurance_order))

# No range-line/segment between a species' multiple points -- independent
# estimates from different studies, not a continuous range. Same decision
# applied to Panel B below.

# Deterministic (not random-jitter) horizontal fan-out for species with >1
# point: random position_jitter left some points still
# overlapping -- e.g. Pan troglodytes' western-chimp LD estimate (cos_per_arm =
# 1.2818) and its Chiasma estimate (1.2805) are nearly identical in y, so no jitter
# width reliably separates them, and Macaca mulatta's 4 estimates cluster the same
# way. Fanning each species' points out by a fixed offset (independent of their
# y-value) guarantees all points stay visible regardless of how close their values
# happen to be, and is reproducible without relying on a fixed random seed.
assurance_data <- assurance_data %>%
  group_by(species) %>%
  mutate(x_num = as.numeric(species) + (row_number() - (n() + 1) / 2) * 0.3) %>%
  ungroup()

# Chiasma is triangle(17), MLH1 is diamond(18) -- diamond alone would collide
# with Figure_4 Panel C's pyrho=diamond within the same review once Figure_4
# Panel A also needed a Cytogenetic (Chiasma) shape. This keeps the two sets
# of panels (crossover-assurance/Gini vs. heterochiasmy/X-A) visually
# distinct from each other.
SOURCE_SHAPES <- c("Pedigree" = 16, "Pedigree (paternal-only)" = 1,
                    "Cytogenetic (MLH1)" = 18, "Cytogenetic (Chiasma)" = 17,
                    "LD-based" = 15)

# ARM-LEVEL ONLY: now that aFN coverage has grown to 28 of 30 tree tips, and
# every species currently in this tribble has an aFN value, arm-level is both
# more complete AND more informative than chromosome-level -- essentially
# every species in this review clears the chromosome-level floor (confirmed
# true from the same data -- see this file's earlier "CORRECTED" note and
# Figure_1/ArmAssurance_binary.txt's per-species detail), so plotting it added
# little visual information, while arm-level has real, mixed pass/fail
# variation -- a better match for Panel B's own style (continuous,
# clade-colored, genuine cross-species signal) than a chromosome-level plot
# would be.
#
# Clade color legend is suppressed here (guide = "none") -- shown once, larger,
# in its own strip above both panels instead (see clade_legend_plot below), so
# it's unambiguous the clade colors apply to both panels while "Data type"
# (this panel) and "Estimator" (Panel B) stay local to their own panel.
panelA <- ggplot() +
  geom_hline(yintercept = 1, linetype = "dashed", color = "grey40", linewidth = 0.5) +
  geom_point(data = assurance_data, aes(x = x_num, y = cos_per_arm, color = clade, shape = source_type),
             size = 3.2, stroke = 1.1) +
  scale_color_manual(values = CLADE_COLORS, guide = "none") +
  scale_shape_manual(values = SOURCE_SHAPES, name = "Data type") +
  scale_x_continuous(breaks = seq_along(assurance_order), labels = assurance_order,
                      limits = c(0.5, length(assurance_order) + 0.5), expand = c(0, 0)) +
  # Lower limit set to 0.5 -- 0.6 with no tick mark visible read as too close
  # to the binary pass/fail information already in Figure 1's crossover-
  # assurance ring; a real tick (0.5) below the dashed obligate-minimum line
  # at 1.0 is clearer. Space is instead reclaimed from the species-name
  # labels below, which is what was actually eating the vertical budget (see
  # axis.text.x size cut below), not from the data's own y-range.
  scale_y_continuous(limits = c(0.5, NA), breaks = seq(0.5, 2, 0.5), expand = expansion(mult = c(0.02, 0.06))) +
  # Short y-axis title ("Implied COs per arm") -- at this panel height, a
  # longer rotated title does not fit within the panel's vertical extent and
  # overflows into the rotated x-axis labels below it. Shorter text needs
  # less vertical room when rotated 90 degrees.
  labs(x = NULL, y = "Implied COs per arm",
       title = "A. Crossover Assurance per Chromosome Arm",
       subtitle = "Dashed line = obligate minimum (1 CO per arm, nXO > aFN/2).") +
  theme_minimal(base_size = 13) +
  # x-axis species-name font reduced -- the 27 rotated species names, not the
  # data itself, are the real space cost in this panel; shrinking them
  # (rather than the y-axis data range) reclaims vertical room without
  # compressing the data.
  theme(axis.text.x = element_text(angle = 45, hjust = 1, face = "italic", size = 7.5),
        axis.title.y = element_text(size = 11),
        panel.grid.major.x = element_blank(),
        plot.title = element_text(face = "bold", size = 13),
        plot.subtitle = element_text(size = 10, color = "grey30"),
        legend.position = "bottom")

write.csv(assurance_data %>%
            select(species, study_label, clade, source_type, total_cM, n_bivalents, aFN,
                   aFN_reference, cos_per_bivalent, cos_per_arm, reference) %>%
            rename(crossover_count_reference = reference) %>%
            arrange(match(species, assurance_order)),
          file.path(OUT_DIR, "supplemental_crossover_assurance_table.csv"),
          row.names = FALSE)
cat("Saved supplemental_crossover_assurance_table.csv\n")

# ============================================================================
# PANEL B: fine-scale recombination-rate unevenness (Gini coefficient)
# ============================================================================
ESTIMATOR_LEVELS <- c("LDhat", "LDhelmet", "pyrho")
# Shape consistency: circle is reserved for Pedigree everywhere in this
# review (Figure_1's Method ring, Panel A's own SOURCE_SHAPES above,
# Figure_3's METHOD_SHAPES), so LDhat does not use circle here. LDhat is this
# review's predominant LD-based estimator, so it keeps square (the same
# shape Figure_1/Panel A use for generic "LD-based"); pyrho uses diamond
# (unused elsewhere as an estimator shape, though Panel A above uses diamond
# for the unrelated "Cytogenetic (Chiasma)" category -- acceptable since each
# panel has its own separately-titled legend, same reasoning applied to
# LDhelmet=triangle below, which is otherwise used for Cytogenetic MLH1 in
# Panel A but only appears once here, unambiguous in context). LDhelmet uses
# triangle -- single use, already clear.
ESTIMATOR_SHAPES <- c("LDhat" = 15, "LDhelmet" = 17, "pyrho" = 18)  # filled square/triangle/diamond

# ALL available Gini estimates -- unlike the earlier bar chart, nothing is dropped here,
# including the two previously-excluded alternates (Macaca mulatta's Terbot et al. 2025
# pyrho value, 0.2813 -- an oddly low outlier -- and
# Pan troglodytes' Auton et al. 2012 value, 0.7766, and Plecturocebus cupreus' LDhat
# value, 0.6025). See Figure_1/iTOL_datasets/supplemental_gini_table.csv for the source
# of every value here. Bonobo/gorilla values were corrected for a legacy duplicate
# chr2 file (see Panel A note) -- change was within rounding (<0.001).
# Macaca mulatta's 3rd point (0.7944, LDhat) is from Xue et al. 2020,
# upgraded from Tier 1 to Tier 2 after the dataset author recovered its deposited
# fine-scale track. Directly confirms the
# macaque-vs-vervet Gini gap is mostly a pyrho-vs-LDhat estimator artifact: this
# LDhat value sits far closer to vervet's own LDhat value (0.9523) than to either
# of macaque's own pyrho values (0.6144, 0.2813).
gini_data <- tribble(
  ~species, ~gini, ~clade, ~estimator, ~reference,
  "Macaca mulatta", 0.7944, "Cercopithecidae", "LDhat", "Xue et al. 2020 PLoS ONE",
  "Chlorocebus sabaeus", 0.9523, "Cercopithecidae", "LDhat", "Pfeifer 2020 MBE",
  "Plecturocebus cupreus", 0.8968, "Platyrrhini", "LDhelmet", "Soni, Versoza et al. 2026 Heredity",
  "Plecturocebus cupreus", 0.6025, "Platyrrhini", "LDhat", "Soni, Versoza et al. 2026 Heredity",
  "Nomascus leucogenys", 0.8441, "Apes", "LDhat", "Stevison, unpublished",
  "Pan troglodytes", 0.8210, "Apes", "LDhat", "Stevison et al. 2016 MBE",
  "Pan troglodytes", 0.7766, "Apes", "LDhat", "Auton et al. 2012 Science",
  "Pan paniscus", 0.8128, "Apes", "LDhat", "Stevison et al. 2016 MBE",
  "Gorilla gorilla gorilla", 0.8119, "Apes", "LDhat", "Stevison et al. 2016 MBE",
  "Callithrix jacchus", 0.8068, "Platyrrhini", "LDhat", "Soni, Versoza et al. 2025/26 bioRxiv (preprint)",
  "Papio anubis", 0.7511, "Cercopithecidae", "pyrho", "Wall, Robinson & Cox 2022 GBE",
  "Macaca mulatta", 0.6144, "Cercopithecidae", "pyrho", "Versoza et al. 2024 GBE (companion map)",
  "Macaca mulatta", 0.2813, "Cercopithecidae", "pyrho", "Terbot, Calahorra-Oliart, Versoza et al. 2025 Am J Primatol",
  "Daubentonia madagascariensis", 0.4509, "Strepsirrhini", "pyrho", "Soni, Versoza et al. 2025 Ecology and Evolution"
) %>%
  mutate(clade = factor(clade, levels = CLADE_LEVELS),
         estimator = factor(estimator, levels = ESTIMATOR_LEVELS))

species_order <- gini_data %>%
  group_by(species) %>%
  summarise(mean_gini = mean(gini), .groups = "drop") %>%
  arrange(desc(mean_gini)) %>%
  pull(species)

gini_data <- gini_data %>% mutate(species = factor(species, levels = species_order))

# Same deterministic fan-out as Panel A instead of random jitter.
gini_data <- gini_data %>%
  group_by(species) %>%
  mutate(x_num = as.numeric(species) + (row_number() - (n() + 1) / 2) * 0.3) %>%
  ungroup()

panelB <- ggplot() +
  geom_point(data = gini_data, aes(x = x_num, y = gini, color = clade, shape = estimator),
             size = 3.5, stroke = 1.2) +
  scale_color_manual(values = CLADE_COLORS, guide = "none") +
  scale_shape_manual(values = ESTIMATOR_SHAPES, name = "Estimator") +
  scale_x_continuous(breaks = seq_along(species_order), labels = species_order,
                      limits = c(0.5, length(species_order) + 0.5), expand = c(0, 0)) +
  scale_y_continuous(limits = c(0, 1), breaks = seq(0, 1, 0.25), expand = expansion(mult = c(0.02, 0.04))) +
  labs(x = NULL, y = "Gini coefficient",
       title = "B. Distribution of Recombination across the Genome",
       subtitle = "Lorenz-curve method; <0.5 = more evenly distributed, >0.5 = more concentrated in hotspots.") +
  theme_minimal(base_size = 13) +
  # x-axis species-name font matched to Panel A's 7.5 -- a smaller,
  # panel-specific size (9, since Panel B only has 10 species vs. Panel A's
  # 27) read as visually inconsistent across the two panels; matching sizes
  # also recoups a bit more vertical room in Panel B.
  theme(axis.text.x = element_text(angle = 45, hjust = 1, face = "italic", size = 7.5),
        panel.grid.major.x = element_blank(),
        plot.title = element_text(face = "bold", size = 13),
        plot.subtitle = element_text(size = 10, color = "grey30"),
        legend.position = "bottom")

# ============================================================================
# Combine -- three fully independent legends: Clade shown ONCE, larger, in
# its own strip above both panels (unambiguous that it applies to both);
# "Data type" stays attached directly under Panel A; "Estimator" stays
# attached directly under Panel B. No guide collection -- each legend is
# deliberately placed, not pooled.
# ============================================================================
clade_legend_data <- tibble(clade = factor(CLADE_LEVELS, levels = CLADE_LEVELS), x = 1, y = 1)
clade_legend_plot <- ggplot(clade_legend_data, aes(x = x, y = y, color = clade)) +
  # All 4 points sit at the same (x,y), so with theme_void() (which hides axes/
  # background but NOT the actual data points) they stack and the last-drawn one
  # (Strepsirrhini, gold -- last in CLADE_LEVELS) would visibly bleed through as a stray
  # circle above Panel A. alpha=0 hides the real plotted points; override.aes below
  # keeps the legend swatches themselves fully opaque.
  geom_point(size = 4.5, alpha = 0) +
  scale_color_manual(values = CLADE_COLORS, name = "Clade") +
  guides(color = guide_legend(override.aes = list(alpha = 1))) +
  theme_void() +
  theme(legend.position = "top",
        legend.title = element_text(face = "bold", size = 15),
        legend.text = element_text(size = 13),
        legend.key.size = unit(1.3, "lines"))

# Single-height panelA (not a faceted chromosome+arm layout).
combined <- clade_legend_plot / panelA / panelB +
  plot_layout(heights = c(0.14, 1, 1.1))

# Figure height set to 9in -- the axis-floor/label-font changes above
# reclaimed enough room that a shorter height felt slightly tight in Panel B
# specifically.
ggsave(file.path(OUT_DIR, "Figure_2_Gini_dotplot.png"),
       combined, width = 10, height = 9, dpi = 1200, bg = "white")
ggsave(file.path(OUT_DIR, "Figure_2_Gini_dotplot.pdf"),
       combined, width = 10, height = 9, bg = "white")

cat("Saved Figure_2_Gini_dotplot.png/.pdf (2 panels: crossover assurance + Gini)\n")

write.csv(gini_data %>% select(species, clade, gini, estimator, reference) %>%
            arrange(match(species, species_order)),
          file.path(OUT_DIR, "supplemental_gini_dotplot_table.csv"),
          row.names = FALSE)
cat("Saved supplemental_gini_dotplot_table.csv\n")
