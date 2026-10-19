# Figure 3: Non-crossover deep dive

![Figure 3](Figure_3_NCO_deepdive.png)

## Caption

**Figure 3. Non-crossover recombination characteristics across non-human primates: crossover homeostasis and tract length.**

Companion figure to Figures 1 and 2, restricted to the nine species with any published non-crossover (NCO) data; the other nine species in this review have no NCO data at all, since their only available method(s) — LD-based or cytogenetic — cannot detect non-crossover events. Bars/points colored by major clade (Apes, orange; Cercopithecidae, purple; Platyrrhini, teal; Strepsirrhini, gold), as in Figures 1 and 2. Marker shape indicates detection method (circle = direct pedigree transmission counts, triangle = pooled germline long-read sequencing), shown once in a shared legend below both panels; the same species always take the same shape in both panels (Papio anubis, Macaca mulatta, Plecturocebus cupreus, and Daubentonia madagascariensis are pedigree in both, the remaining five species are long-read in both). Species in both panels are ordered independently by value, highest to lowest, not by a shared or phylogenetic order.

**(A)** Crossover homeostasis: the non-crossover fraction of all detected recombination events, calculated as NCO / (NCO + CO) from raw event counts. Dashed line marks parity (NCO and CO equally frequent). Bars are clade-colored; the small black marker just above each bar shows detection method (see above). Values combine two structurally different detection methods, so cross-method comparisons should not be read as a clean biological signal.

**(B)** Mean NCO conversion tract length, in base pairs. Points show individual sequenced-individual estimates for the two species with more than one available measurement (Pan troglodytes, n=4; Gorilla gorilla gorilla, n=3); no summary bar or range line is drawn between a species' multiple points, since these are independent per-individual estimates, not repeated samples of one population quantity. Values derive from the same two structurally different approaches as (A): the mean minimal tract length directly observed in pedigree transmission data, or a probabilistic geometric-distribution model fit to pooled germline long-read sequencing data. Cross-species comparison of this metric should be treated with caution, as differences in marker density across studies affect resolution (a caveat noted explicitly by Versoza et al. 2025).

Full event counts, tract-length values, and references are provided in Supplemental Table S6. Sex-specific crossover and non-crossover rates, for the subset of species where both sexes were independently measured, are presented separately in Figure 4.

## Files

| File | Contents |
|---|---|
| `Figure_3_NCO_deepdive.png / .pdf` | Final figure |
| `supplemental_nco_deepdive_table.csv` | Values for both panels |

## Regenerate

Run from the repository root:

```bash
Rscript Scripts/figure3_nco_deepdive/build_nco_deepdive.R
```
