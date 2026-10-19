#!/usr/bin/env python3
"""
Auton et al. 2012 Science (western chimpanzee, Pan troglodytes verus) -- LD-based
recombination map. The original host (panmap.uchicago.edu,
ftp://birch.well.ox.ac.uk/) is dead (confirmed by direct connection tests from
two separate networks -- both FTP port 21 and HTTPS port 443 time out).
Recovered via the Internet Archive Wayback Machine, which crawled the FTP
server in December 2015 (CDX API:
web.archive.org/cdx/search/cdx?url=birch.well.ox.ac.uk/panMap/...).

Files: panMap/haplotypes/genetic_map/chimp_Dec8_Haplotypes_Mar1_chr*-cleaned.txt.gz
(23 files: chr1-22 autosomes, with chr2 split into chr2a/chr2b per the same
human/chimp synteny convention used for the Stevison et al. 2016 great-ape
maps elsewhere in this review). Format identical to the Pfeifer 2020 vervet
data (same McVean/Auton-lineage LDhat pipeline convention):
Position(bp), Rate(4Ner/kb), Map(4Ner), Filtered -- point-based, intervals
built as position[i] -> position[i+1], Filtered==1 rows dropped.

cM/Mb conversion uses Ne=11,413, the paper's own primary chimp Ne estimate
(SOM p.19, "Estimation of the effective population size, Ne" -- obtained via
regression against the human HapMap map at 5Mb scale, under the assumption
that human and chimp total genetic map lengths are approximately equal, the
same McVean et al. 2004 calibration approach later adopted by Stevison et al.
2016). SOM also reports Ne=10,463 (1Mb scale) to Ne=11,671 (10Mb scale) as a
robustness range. Note: Central_Comparison_Table.xlsx's own cM/Mb for this
species uses a different, independently-sourced Ne (de Manuel et al. 2016)
rather than this paper's own regression-based Ne -- see the table's Notes
column for that rationale. The values below reproduce the paper's own
calibration for reference/validation, not the value used in the final table.

Gini computed raw/unbinned, this review's standard for cross-study
consistency (see Central_Comparison_Table.xlsx's Notes sheet).
"""
import glob
import os

MAPDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "genetic_map")
NE_PRIMARY = 11413
NE_RANGE = (10463, 11671)


def gini_from_lorenz(lengths, rhos):
    order = sorted(range(len(rhos)), key=lambda i: rhos[i])
    total_len = sum(lengths)
    total_rho = sum(lengths[i] * rhos[i] for i in range(len(rhos)))
    x_prev, y_prev = 0.0, 0.0
    area = 0.0
    for i in order:
        x = x_prev + lengths[i] / total_len
        y = y_prev + (lengths[i] * rhos[i]) / total_rho
        area += (x - x_prev) * (y + y_prev) / 2.0
        x_prev, y_prev = x, y
    return 1.0 - 2.0 * area


def cm_per_mb_for_ne(weighted_rho_kb, ne):
    r_per_kb = weighted_rho_kb / (4.0 * ne)
    return r_per_kb * 1e5


def main():
    import gzip
    lengths_kb = []
    rho_per_kb = []
    files = sorted(glob.glob(f"{MAPDIR}/*.gz"))

    for fpath in files:
        with gzip.open(fpath, "rt") as fh:
            header = fh.readline()
            prev_pos = None
            prev_rate = None
            prev_filtered = None
            for line in fh:
                parts = line.split()
                pos, rate, filt = int(parts[0]), float(parts[1]), int(parts[3])
                if prev_pos is not None and prev_filtered == 0:
                    length_kb = (pos - prev_pos) / 1000.0
                    if length_kb > 0:
                        lengths_kb.append(length_kb)
                        rho_per_kb.append(prev_rate)
                prev_pos, prev_rate, prev_filtered = pos, rate, filt

    total_len_kb = sum(lengths_kb)
    weighted_rho = sum(l * r for l, r in zip(lengths_kb, rho_per_kb)) / total_len_kb
    gini = gini_from_lorenz(lengths_kb, rho_per_kb)

    print(f"chromosomes: {len(files)}")
    print(f"genome length covered: {total_len_kb/1000:.1f} Mb")
    print(f"genome-wide weighted rho/kb (4Ner/kb): {weighted_rho:.4f}")
    print(f"Gini (raw/unbinned, this review's standard): {gini:.4f}")
    print()
    for ne in (NE_RANGE[0], NE_PRIMARY, NE_RANGE[1]):
        print(f"  Ne={ne:>6,d} -> {cm_per_mb_for_ne(weighted_rho, ne):.4f} cM/Mb")


if __name__ == "__main__":
    main()
