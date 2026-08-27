# Recombination Rate Heterogeneity Across Non-Human Primates

**Companion data and code repository for a book chapter synthesizing genome-wide recombination rate (cM/Mb), non-crossover (NCO) rate, and fine-scale rate heterogeneity (Gini coefficient) across 30 non-human primate species.**

This repository contains the compiled comparison table, the figure-generation code, and the supplementary analytical notes underlying the chapter. 

Citation to Book Chapter:
> Stevison, L.S. 2026. Chapter 5: Recombination Rate Heterogeneity Across Non-Human Primates. In _Evolutionary Genomics of Non-Human Primates_ Ed. S. P. Pfiefer and J. D. Jensen. Elsevier.

---

## 1. Overview

The review presented in this chapter is **not a meta-analysis**. Rather than pooling published summary statistics, it standardizes extraction and (where raw or deposited data allowed) independent recomputation of three metrics across non-human primate recombination studies identified in the literature:

- **cM/Mb** — genome-wide average recombination rate
- **Non-crossover (NCO) rate** — where a study's method can detect it
- **Gini coefficient** — a measure of how unevenly recombination is distributed along the genome, computed raw/unbinned from fine-scale maps wherever one existed

Three methodological families are represented, and are **not treated as interchangeable**: LD-based (population-scaled, historical) recombination maps, pedigree-based (direct meiotic transmission) maps, and cytogenetic (MLH1 immunofluorescent foci or classical chiasma counts) genome-wide estimates. Every table and figure in this repository retains a Method column specifically so this distinction isn't lost in the visualization.

## 2. Repository Structure

```
GitHub Repository/
├── Central_Comparison_Table.xlsx      Central data table (species x method x cM/Mb x NCO x Gini)
├── Data/                             Raw data for the 3 studies with no other public source (see Data/README.md)
│   ├── Auton2012_chimp_LDmap/
│   ├── GreatApe_chrX_maps/
│   └── Xue2020_macaque_LDmap/
├── Scripts/                          All figure- and table-generation code
│   ├── central_table/                Builds Central_Comparison_Table.xlsx
│   ├── figure1_phylogeny_itol/       Figure 1: iTOL phylogeny + annotation rings
│   ├── figure2_co_control/           Figure 2: CO Control with CO assurance and gini coefficient dot plot
│   ├── figure3_nco_deepdive/         Figure 3: NCO tract length / CO:NCO ratio
│   ├── figure4_heterochiasmy/        Figure 4: sex-specific (heterochiasmy) rates
│   └── figure5_prdm9_bubbleplot/     Figure 5: PRDM9 zinc-finger array size
├── Figures/                          Final rendered figures (PNG/PDF/EPS), captions, and per-figure supplementary CSVs
│   ├── Figure1_Phylogeny/
│   ├── Figure2_CO_Control/
│   ├── Figure3_NCO_Deepdive/
│   ├── Figure4_Heterochiasmy/
│   └── Figure5_PRDM9_Bubbleplot/
└── Tables/                           Standalone cross-species analytical notes (not tied to one figure)
    ├── Primate_cMMb_Baseline_Average.txt
    ├── Primate_NCO_Baseline_Average.txt
    └── Primate_Pedigree_vs_LD_cMMb_Comparison.txt
```

## 3. Central_Comparison_Table.xlsx

The central data product, used to generate Figure 1 and referenced throughout the chapter. One row per species x method x source study (50 rows, 27 unique studies). Columns:

| Column | Description |
|---|---|
| Group | One of the 4 major clades used throughout this review (Apes, Old World Monkeys, New World Monkeys, Lemurs) |
| Species | Full binomial, with common name |
| Method | LD-based / Pedigree-based / Cytogenetic (MLH1 or chiasma) / Testis long-read |
| Marker Type | Underlying raw data type (short-read WGS, long-read WGS, microsatellite, chiasma count, MLH1 foci) |
| Scale | Population / Individual / Transmission, as applicable |
| Reference | Source study |
| cM/Mb | Genome-wide recombination rate |
| cM/Mb status | How the value was derived (recomputed from raw/deposited data vs. extracted from the paper's own text/tables), and any Ne or calibration choice made |
| Gini (raw/unbinned) | Fine-scale rate heterogeneity, always computed raw/unbinned (see caveats below) |
| Gini status | Whether independently computed here or structurally not possible for this method |
| NCO rate / count | Non-crossover rate or raw event count, where the method can detect it |
| CO count or genetic map length | Supporting count/length figure |
| Notes / caveats | Row-specific caveats — congener substitutions, citation cross-checks, calibration choices |

Regenerate this file with `Scripts/central_table/build_public_central_table.py` (writes to the repository root; no external dependencies beyond `openpyxl`).

### Standing methodological notes (apply across the whole table)

- **Gini is always computed raw/unbinned**, never from a binned/smoothed map. This is a deliberate standard for reproducibility and cross-study consistency, not an attempt to reproduce each paper's own published Gini exactly — the recomputed Gini often runs higher than a paper's own published figure as a direct consequence.
- **Gini computed from pyrho output is not directly comparable to Gini computed from LDhat/LDhelmet output**, even at matched raw/unbinned resolution — pyrho's block-penalty smoothing produces mechanically smoother maps. Always check the rate estimator alongside any Gini value.
- **cM/Mb from several LD-based studies is a calibrated/normalized value, not an independent measurement.** Some studies force the total genetic map length to match an assumed-equal human map (Stevison 2016, Auton 2012); others rescale their own LD map to match their own companion pedigree study's map length (Wall 2022, Versoza 2025, Soni 2026) — a more defensible, study-specific calibration. The "cM/Mb status" column flags which kind of calibration underlies each value.
- **Cross-species physical-genome-length substitution** (using a same-genus or same-family congener's assembly when a study's own species has no chromosome-level assembly) is used for several cytogenetic rows, flagged individually. Physical assembly statistics were pulled via the [NCBI Datasets API](https://api.ncbi.nlm.nih.gov/datasets/v2/genome/).
- **Pedigree CO/NCO calling and long-read recombination calling from raw sequencing data are out of scope for this review** — every value here uses a study's own published counts/rates or deposited processed maps, never a re-derivation from raw FASTQ/BAM/VCF.
- cM/Mb from LD-based, pedigree-based, and cytogenetic methods are not strictly the same quantity (historical/coalescent-scaled vs. direct meiotic count vs. genome-wide chiasma-based estimate) — retain the Method column in any downstream use of this table rather than treating all values as interchangeable.

## 4. Data

The vast majority of datasets underlying this review remain available at
their original public source (lab website, Dryad, Zenodo, NCBI, or a
journal's supplementary materials) — see the Reference column in
`Central_Comparison_Table.xlsx` or the citation list in Section 8 below for
exactly where. Three datasets are the exception: their original host is no
longer online, or the data was obtained directly and never had a public
host to begin with. Those are rehosted in `Data/`, alongside the scripts
used to compute cM/Mb and Gini from them, so those specific numbers remain
independently reproducible. See `Data/README.md` for the full explanation
of each.

## 5. Figures

### Figure 1 — Phylogeny with cM/Mb, Gini, and NCO annotation rings
A TimeTree-derived phylogeny of all 30 species, annotated in [iTOL](https://itol.embl.de/) with clade coloring, method/marker-type binary rings, and cM/Mb/Gini/NCO data rings (boxplot, pie chart, and boxplot respectively). `Scripts/figure1_phylogeny_itol/` contains the newick tree, the manual branch-length graft log (documenting where TimeTree's automated output needed literature-sourced correction), and the Python scripts that generate each iTOL annotation dataset from the Central table. `Figures/Figure1_Phylogeny/iTOL_datasets/` holds the generated annotation files ready for upload to iTOL, plus the supplementary CSVs behind each ring. Final figure assembly (tree layout, legend placement) was done interactively in iTOL and finished in Adobe Illustrator; the scripts here produce every input to that process, not the final layout itself.

### Figure 2 — Two Panel Crossover Control dot plot
Pnael A supplements Table S1 of Dumont et al 2017 with several additional species to compare CO assurance per chromosome arm. Panel B shows all 13 available Gini estimates across the 10 species with any Gini value, point shape encoding the rate estimator (LDhat/LDhelmet/pyrho) and color encoding clade. Built with `Scripts/figure2_gini_dotplot/build_gini_dotplot.R` (R/ggplot2). Raw datasets for both panels in `Figures/Figure2_Gini_Dotplot/`.

### Figure 3 — Non-crossover deep dive
Mean NCO tract length and the CO:NCO ratio (crossover homeostasis) across the 9 species with NCO data, split by detection method (pedigree transmission vs. Porsborg et al. 2025 long-read testis sequencing). Built with `Scripts/figure3_nco_deepdive/build_nco_deepdive.R`. 

### Figure 4 — Heterochiasmy (sex-specific recombination)
Male-vs-female recombination rate ratios and X-vs-autosome recombination ratios, across the handful of species where both sexes or both chromosome classes have been independently measured. Built with `Scripts/figure4_heterochiasmy/build_heterochiasmy.R`.

### Figure 5 — PRDM9 zinc-finger array size
A modernized version of Schwartz et al. (2014)'s Figure 3: PRDM9 zinc-finger array size across every primate genus with sequenced alleles (25 species/genera), grouped by clade, combining Schwartz et al. (2014)'s own raw allele data, unpublished sequences from Ségurel & Przeworski, new annotation work from this review (including a corrected mislabeled allele in *Papio anubis*), and Heerschop et al. (2016)'s tarsier allele survey. Species with characterized PRDM9 but no fine-scale recombination map anywhere in the literature are shown as open (hollow) points rather than omitted, to make that gap visible rather than silently absent. Built with `Scripts/figure5_prdm9_bubbleplot/build_zf_bubbleplot.R`.

All figures were exported as PNG (1200 dpi), PDF, and EPS (vector).

## 6. Tables — Standalone Analytical Notes

Three cross-species summary notes, each derived directly from `Central_Comparison_Table.xlsx` and referenced in the chapter's discussion:

- **`Primate_cMMb_Baseline_Average.txt`** — Tests the commonly-used "~1 cM/Mb" default recombination rate assumption against this review's actual 23-species distribution (mean 0.84, median 0.82, range 0.63–1.55 cM/Mb) — the default reads as a modest overestimate, not just a rough ballpark. Also resolves an apparent 8-fold disagreement in *Macaca mulatta*'s cM/Mb estimates by reframing them as two genuinely distinct populations (Indian- vs. Chinese-origin) rather than one inconsistent species.
- **`Primate_NCO_Baseline_Average.txt`** — The same exercise for NCO rate (n=9 species, 11-fold range) — considerably noisier than cM/Mb, split across two structurally different measurement approaches (direct pedigree counts vs. model-based long-read estimates) that agree at the subgroup-mean level but not in precision.
- **`Primate_Pedigree_vs_LD_cMMb_Comparison.txt`** — Every species in this review with both a pedigree-based and an LD-based cM/Mb estimate reads pedigree at or above LD, never the reverse (5 of 5 species) — including 2 fully independent comparisons where the LD estimate wasn't rescaled toward the pedigree figure. Two candidate explanations (linked-selection bias in LD-based estimates vs. a genuine historical-vs-contemporary rate difference) are laid out but not adjudicated.
- **`PRDM9_ZF_vs_Gini_Hypothesis_Test.txt`** — Tests whether PRDM9 zinc-finger array size predicts genome-wide recombination evenness (Xue et al. 2020's candidate explanation for macaque). Result: no detectable relationship (n=9, r=0.180, p=0.643; sign reverses to r=−0.343, p=0.451 when restricted to the 7 LDhat-only species) — consistent with PRDM9 structural biology, since every array in this dataset is already well above the ~4-5 zinc fingers needed to reach a typical 13-15bp binding motif.
- **`Joseph2024_DefaultHotspots_vs_Gini_Hypothesis_Test.txt`** — Tests whether reliance on PRDM9-independent ("default") hotspots (Joseph et al. 2024) tracks genome-wide unevenness. Result: a positive correlation (n=4, r=0.936, p=0.064; n=3 exact species matches, r=0.969, p=0.159) driven by vervet, which has both the highest default-hotspot activity and the highest Gini in this review. Not significant at this n, but the positive direction is the mechanistically expected sign once the two hotspot types are framed as coexisting/additive (per Joseph et al.'s own finding that they typically don't substitute for each other) rather than substitutive — of the two hypotheses tested here, this one offers the more plausible account of the pattern.
- **`compute_gini_hypothesis_correlations.py`** — Reproduces both correlations above directly from the data tables in each note (requires `scipy`).

## 7. Use in This Project

`Central_Comparison_Table.xlsx` consolidates every cM/Mb, NCO, and Gini value cited in the chapter. Any correction or addition to a per-species value is made in `Scripts/Central_table/build_public_Central_table.py` and propagated by re-running that script and every downstream figure script — the figures and the two baseline-average notes are all derived views of this one table, not independently maintained.

## 8. AI Disclosure Statement

Claude (Anthropic) was used as a collaborative tool throughout the
development of this repository: extracting and cross-checking reported
values from source publications, writing and iterating on the R/Python
scripts that produce the figures and tables, drafting and revising this
documentation, and performing the statistical computations in the PRDM9
hypothesis-test notes (`Tables/PRDM9_ZF_vs_Gini_Hypothesis_Test.txt`,
`Tables/Joseph2024_DefaultHotspots_vs_Gini_Hypothesis_Test.txt`).

All methodological decisions, source selection, interpretation of results,
and final content are the author's own responsibility. Every recomputed
value was independently cross-validated against each source study's own
published figures wherever possible, and every genuine discrepancy or
methodological caveat surfaced during that process is documented explicitly
in `Central_Comparison_Table.xlsx` and the relevant `Tables/` notes rather
than silently resolved. 

## 9. Citation

If referencing this compiled dataset or its figures, please cite the book chapter:

> Stevison, L.S. 2026. Chapter 5: Recombination Rate Heterogeneity Across Non-Human Primates. In _Evolutionary Genomics of Non-Human Primates_ Ed. S. P. Pfiefer and J. D. Jensen. Elsevier.

The table itself compiles data from the following primary sources. Full citations for every data source, plus the complete literature review this chapter is drawn from, are in the chapter's own reference list.

**LD-based:**
Auton et al. 2012 *Science* 336:193–198 (chimpanzee) · Pfeifer 2020 *MBE* 37:1855–1865 (vervet) · Stevison et al. 2016 *MBE* 33:928–945 (great apes) · Stevison 2016, unpublished LD map (gibbon) · Xue et al. 2020 *PLoS ONE* 15:e0236285 (rhesus macaque) · Terbot, Calahorra-Oliart, Versoza et al. 2025 *Am. J. Primatol.* 87:e70088 (Chinese rhesus macaque) · Soni, Versoza et al. 2025 *bioRxiv* 2025.07.01.662565 (marmoset, preprint) · Soni, Versoza et al. 2026 *Heredity* 135:476–485 (titi monkey) · Versoza et al. 2025 *GBE* 17:evaf072 (aye-aye, companion LD map)

**Pedigree-based:**
Cox et al. 2006 *Genomics* 88:274–281 and Rogers et al. 2000 *Genomics* 67:237–247 (baboon microsatellite maps) · Rogers et al. 2006 *Genomics* 87:30–38 (rhesus macaque microsatellite map) · Jasinska et al. 2007 *Mamm. Genome* 18:347–360 (vervet microsatellite map) · Wall, Robinson & Cox 2022 *GBE* 14:evac040 (baboon WGS) · Versoza et al. 2024 *GBE* 16:evad223 (rhesus macaque WGS) · Versoza et al. 2025 *GBE* 17:evaf072 (aye-aye WGS) · Versoza et al. 2026 *GBE* 18:evag186 (titi monkey WGS)

**Cytogenetic (MLH1 foci / chiasma count):**
Burt & Bell 1987 *Nature* 326:803–805 · Burt, Bell & Harvey 1991 *J. Evol. Biol.* 4:259–277 (via Mank 2009 *Genet. Res.* 91:355–363) · Pardo-Manuel de Villena & Sapienza 2001 *Mamm. Genome* 12:318–322 · Hassold et al. 2009 *Cytogenet. Genome Res.* 124:132–138 · Garcia-Cruz et al. 2009 *BMC Genet.* 10:25 and Garcia-Cruz et al. 2011 *Chromosoma* 120:521–530 (New World monkeys) · Segura et al. 2013 *Proc. R. Soc. B* 280:20131945 · Dumont 2017 *Genetics* 205:155–168 (cross-species chiasma/MLH1 compilation)

**Long-read testis/sperm sequencing:**
Porsborg et al. 2025 *Nat. Commun.* 16:10337

**Ne sources used for LD-based cM/Mb calibration:**
Han et al. 2024 *Curr. Biol.* 34:5341-5348.e3 (bonobo) · de Manuel et al. 2016 *Science* 354:477–481 (chimpanzee subspecies) · McManus et al. 2015 *MBE* 32:600–612 (gorilla) · Veeramah et al. 2015 *Genetics* 200:295–308 (gibbon)

**Figure 5 (PRDM9) sources:**
Schwartz et al. 2014 *Nat. Commun.* 5:4370 · Ségurel & Przeworski, unpublished sequences · Heerschop et al. 2016 *Sci. Rep.* 6:34618 (tarsiers)

## 9. License

Code in this repository (`Scripts/`) is released under the MIT License. Data and figures (`Central_Comparison_Table.xlsx`, `Figures/`, `Tables/`) are released under CC BY 4.0 — please cite both this repository and the original source studies listed above when reusing.
