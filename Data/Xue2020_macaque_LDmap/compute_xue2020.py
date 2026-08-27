#!/usr/bin/env python3
"""
Xue et al. 2020 PLoS ONE (rhesus macaque, Indian-origin, LDhat) -- compute
genome-wide weighted rho/kb and raw/unbinned Gini from the deposited
`all.rate.bw` BigWig track (originally an HGSC UCSC track hub; the live
ftp.hgsc.bcm.edu mirror is no longer online, so this copy is rehosted here --
see this folder's README.md).

Track structure (verified by direct inspection, not assumed): one 1bp-wide
value per SNP position -- i.e. a per-SNP-interval rho/kb point estimate, the
same LDhat "rates.txt"-style convention as every other raw map in this
review. Intervals are constructed here as [SNP_i, SNP_{i+1}) with rate =
value at SNP_i, matching that convention, then weighted-averaged and Gini'd
using the same raw/unbinned Lorenz-curve approach as every other LD map in
this review.

No chrX in this track (20 chromosomes = macaque's 20 autosomes, confirmed
directly from bw.chroms()) -- consistent with every other macaque study in
this review.

Run `gunzip -k all.rate.bw.gz` in this directory first (the file is stored
gzipped here to keep the repository small; pyBigWig needs the decompressed
.bw file).
"""
import os
import pyBigWig

BW_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all.rate.bw")


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


def main():
    bw = pyBigWig.open(BW_PATH)
    chroms = bw.chroms()
    print(f"{len(chroms)} chromosomes, total physical length "
          f"{sum(chroms.values())/1e6:.1f} Mb")

    # GAP_CUTOFF_BP: the paper's own stated QC rule (Methods) is "if a gap within
    # a window is >50kb, set the recombination rate to zero for the surrounding
    # +/-50 SNPs" -- i.e. they explicitly do not trust rate estimates spanning
    # gaps this large. A handful of such gaps in the deposited track (found by
    # direct inspection: 767 gaps >50kb, one 455kb-wide on chr7 alone, carrying
    # a rho=35/kb point value forward across the whole gap) would otherwise
    # bridge a single SNP-interval's rate across a huge, likely-unreliable
    # physical span if included naively. Adopting their own 50kb threshold here
    # rather than picking an arbitrary cutoff.
    GAP_CUTOFF_BP = 50000

    lengths = []  # bp, between consecutive SNPs
    rhos = []     # rho/kb value for that interval (value at the left SNP)
    total_snps = 0
    n_excluded_gaps = 0

    for chrom, chrom_len in sorted(chroms.items()):
        ints = bw.intervals(chrom, 0, chrom_len)
        if not ints:
            continue
        total_snps += len(ints)
        for i in range(len(ints) - 1):
            start_i = ints[i][0]
            start_next = ints[i + 1][0]
            length_bp = start_next - start_i
            if length_bp <= 0:
                continue
            if length_bp > GAP_CUTOFF_BP:
                n_excluded_gaps += 1
                continue
            lengths.append(length_bp / 1000.0)  # kb, matching project convention
            rhos.append(ints[i][2])

    print(f"total SNP positions: {total_snps}")
    print(f"intervals excluded as >{GAP_CUTOFF_BP/1000:.0f}kb gaps (paper's own QC threshold): {n_excluded_gaps}")
    print(f"total intervals used: {len(lengths)}")

    total_len_kb = sum(lengths)
    weighted_rho = sum(l * r for l, r in zip(lengths, rhos)) / total_len_kb
    gini = gini_from_lorenz(lengths, rhos)

    print(f"physical length spanned by intervals: {total_len_kb/1000:.1f} Mb")
    print(f"genome-wide weighted rho/kb: {weighted_rho:.4f}")
    print(f"Gini (raw/unbinned): {gini:.4f}")


if __name__ == "__main__":
    main()
