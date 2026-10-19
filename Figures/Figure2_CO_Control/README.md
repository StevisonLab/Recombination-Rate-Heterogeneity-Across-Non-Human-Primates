# Figure 2: Crossover control: crossover assurance and Gini coefficient

![Figure 2](Figure_2_Gini_dotplot.png)

## Caption

**Figure 2. Crossover assurance and genome-wide recombination distribution across non-human primates.**

Companion figure to Figure 1, giving a more detailed, method-annotated view of two metrics Figure 1 summarizes on the tree itself. Point color indicates major clade (Apes, orange; Cercopithecidae, purple; Platyrrhini, teal; Strepsirrhini, gold), as in Figure 1, shown once in a shared legend above both panels. Within each panel, species are ordered independently by mean value, highest to lowest; where more than one estimate is available for a species, all estimates are shown as separate jittered points, not connected by a range line or averaged into a single symbol — these are independent per-study (or per-method) measurements, not repeated samples of one population quantity.

**(A)** Crossover assurance per chromosome arm, for the 27 species in this review with a computable value (35 estimates total across species with more than one study or method). Tests the stricter, chromosome-**arm** version of the obligate-crossover floor from Dumont (2017) — implied crossovers per arm (nXO) compared against the haploid autosomal arm count (aFN/2) — rather than the chromosome-level floor (≥1 crossover per bivalent), which holds for essentially every species in this review and is not plotted separately (see main text). Dashed line marks the obligate minimum (nXO = aFN/2); points above the line pass, points below fail. Point shape indicates data type (circle = pedigree; open circle = pedigree, paternal-only; diamond = cytogenetic MLH1 foci; triangle = cytogenetic chiasma count; square = LD-based). Species and methods span a wide split: Strepsirrhini passes unanimously, while Apes, Cercopithecidae, and (to a lesser extent) Platyrrhini show real cross-species and, in Macaca mulatta and Cebuella pygmaea, within-species cross-method disagreement — see main text and Figure_1's ArmAssurance_binary.txt for the full per-species breakdown.

**(B)** Distribution of recombination across the genome, measured as the Gini coefficient of the fine-scale recombination-rate distribution (Lorenz-curve method, computed raw/unbinned; 0 = perfectly even, 1 = maximally uneven), for the ten species in this review with at least one available fine-scale genetic map. Point shape indicates the rate estimator used to build the underlying genetic map (square = LDhat, triangle = LDhelmet, diamond = pyrho; square is reused from Panel A's own LD-based shape since LDhat is this review's predominant LD-based estimator). All points are LD-based, even for the four species here (Papio anubis, Macaca mulatta, Plecturocebus cupreus, Daubentonia madagascariensis) that also have a dedicated pedigree study elsewhere in this review: pedigree crossover counts at these sample sizes (150-850 events genome-wide) are too sparse to resolve fine-scale rate variation, so each pedigree paper's own companion LD-based map is used instead, not the raw pedigree crossovers. Two species show substantial disagreement between estimates: Plecturocebus cupreus (LDhelmet 0.90 vs. LDhat 0.60, same population) and Macaca mulatta (0.61 in a captive Indian-origin population vs. 0.28 in a wild Chinese-origin population, both pyrho, vs. 0.79 in a third, LDhat-based estimate). The pyrho estimator's block-penalty smoothing is known to produce mechanically lower Gini values than LDhat or LDhelmet even at matched map resolution (see main text), which likely contributes to Macaca mulatta's low pyrho values independent of any true population difference between studies. The remaining species surveyed in this review have no Gini value: cytogenetic (MLH1-foci or chiasma-count) and pedigree-microsatellite methods cannot resolve a fine-scale recombination map, so a Gini coefficient cannot be computed regardless of sample size.

Full values, data types/estimators, and references for both panels are provided in Supplemental Tables S4 and S5.

## Files

| File | Contents |
|---|---|
| `Figure_2_Gini_dotplot.png / .pdf` | Final figure |
| `supplemental_crossover_assurance_table.csv` | Panel A values |
| `supplemental_gini_dotplot_table.csv` | Panel B values |

## Regenerate

Run from the repository root:

```bash
Rscript Scripts/figure2_co_control/build_gini_dotplot.R
```
