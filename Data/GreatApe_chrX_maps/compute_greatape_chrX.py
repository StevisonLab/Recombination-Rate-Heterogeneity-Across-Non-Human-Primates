#!/usr/bin/env python3
"""
Compute chrX genome-wide weighted rho/kb and raw/unbinned Gini for the
great-ape chrX maps (Stevison, Woerner et al., unpublished). These maps were
built for a never-completed X-vs-autosome comparative project: BEAGLE-phased,
haploid males concatenated into pseudo-diploid females, all female +
pseudo-female individuals used -- 13 gorillas, 12 bonobos, 8 Nigerian chimps.

Same methodology as the autosomal great-ape maps (Stevison et al. 2016):
physical-length-weighted mean rho/kb, Gini from the raw/unbinned fine-scale
map (this review's standard for cross-study consistency). Single file per
species (not per-chromosome), same column layout as the autosomal maps.

These values feed Figure 4 (heterochiasmy / X-vs-autosome comparison) and
its supplemental table.
"""
import gzip
import os

CHRX_DIR = os.path.dirname(os.path.abspath(__file__))

SPECIES = {
    "Bonobo (Pan paniscus)": ("Bonobo-chrX-map.hg18.txt.filtered.gz", 12),
    "Nigerian chimp (Pan troglodytes ellioti)": ("NigerianChimp-chrX-map.hg18.txt.filtered.gz", 8),
    "Western gorilla (Gorilla gorilla gorilla)": ("Gorilla-chrX-map.hg18.txt.filtered.gz", 13),
}

# Autosomal rho/kb values for the same species/individuals, independently
# validated against Stevison et al. 2016's own published figures.
AUTOSOME_RHO_KB = {
    "Bonobo (Pan paniscus)": 0.6405,
    "Nigerian chimp (Pan troglodytes ellioti)": 0.8004,
    "Western gorilla (Gorilla gorilla gorilla)": 0.9437,
}


def gini_from_lorenz(lengths, rhos):
    order = sorted(range(len(rhos)), key=lambda i: rhos[i])
    total_len = sum(lengths)
    total_rho = sum(lengths[i] * rhos[i] for i in range(len(rhos)))

    x_prev, y_prev = 0.0, 0.0
    area_under_lorenz = 0.0
    for i in order:
        x = x_prev + lengths[i] / total_len
        y = y_prev + (lengths[i] * rhos[i]) / total_rho
        area_under_lorenz += (x - x_prev) * (y + y_prev) / 2.0
        x_prev, y_prev = x, y

    return 1.0 - 2.0 * area_under_lorenz


def load_chrX(fname):
    lengths = []
    rhos = []
    fpath = os.path.join(CHRX_DIR, fname)
    with gzip.open(fpath, "rt") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        i_start = header.index("Gorgor3-start")
        i_end = header.index("Gorgor3-end")
        i_rho = header.index("rho/kb")
        for line in fh:
            f = line.rstrip("\n").split("\t")
            rho_str = f[i_rho]
            if rho_str == "na":
                continue
            start_mb = float(f[i_start])
            end_mb = float(f[i_end])
            length_kb = (end_mb - start_mb) * 1000.0
            if length_kb <= 0:
                continue
            lengths.append(length_kb)
            rhos.append(float(rho_str))
    return lengths, rhos


def main():
    print(f"{'Species':45s} {'n_females':>10s} {'#intervals':>11s} {'X_len_kb':>12s} "
          f"{'X rho/kb':>10s} {'A rho/kb':>10s} {'X/A ratio':>10s} {'X Gini (raw)':>13s}")
    for label, (fname, n_females) in SPECIES.items():
        lengths, rhos = load_chrX(fname)
        total_len = sum(lengths)
        weighted_rho = sum(l * r for l, r in zip(lengths, rhos)) / total_len
        gini_raw = gini_from_lorenz(lengths, rhos)
        a_rho = AUTOSOME_RHO_KB[label]
        ratio = weighted_rho / a_rho
        print(f"{label:45s} {n_females:10d} {len(lengths):11d} {total_len:12.1f} "
              f"{weighted_rho:10.4f} {a_rho:10.4f} {ratio:10.4f} {gini_raw:13.4f}")


if __name__ == "__main__":
    main()
