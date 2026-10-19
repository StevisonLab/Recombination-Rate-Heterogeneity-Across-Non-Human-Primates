# Rehosted Datasets

This folder contains raw/deposited recombination-map data for exactly three studies used in this review — and only these three. A fourth unpublished dataset in Gibbons has it's [own repository](https://github.com/lstevison/Gibbon-Recombination-Rate). Every other dataset this review draws on remains available at its original public source (lab website, Dryad, Zenodo, NCBI, or a journal's own supplementary materials); see `Central_Comparison_Table.xlsx`'s "Reference" column and the citation list in the main `README.md` for exactly where each of those lives. This folder exists specifically because these three could not be pointed to that way: either the original host is no longer online, or the data was obtained directly and was never hosted publicly to begin with.

Each dataset includes the compute script used to derive the cM/Mb and Gini values that feed `Central_Comparison_Table.xlsx` and Figure 4, so the published numbers in this review can be reproduced directly from the raw data included here.

## Auton2012_chimp_LDmap/

Auton et al. (2012) *Science* 336:193–198 — the western chimpanzee
(*Pan troglodytes verus*) LD-based genetic map. The original host
(panmap.uchicago.edu, `ftp://birch.well.ox.ac.uk/`) has been offline for
years — confirmed dead from two separate networks (both FTP port 21 and
HTTPS port 443 time out). The cleaned per-chromosome map files were
recovered via the [Internet Archive Wayback Machine](https://web.archive.org/),
which crawled the FTP server in December 2015. The Wayback Machine's CDX API
(`web.archive.org/cdx/search/cdx?url=<host>/<path>*&output=json`) is a
generally useful way to check whether a dead academic FTP/HTTP host's exact
files were ever archived, even when the live server has been decommissioned
for a decade.

23 files (chr1–22, with chr2 split into chr2a/chr2b), gzipped, ~58 MB total.

## GreatApe_chrX_maps/

Unpublished chrX (X chromosome) LD-based recombination maps for bonobo,
Nigerian chimp, and western gorilla (Stevison, Woerner, et al.), built as
companion X-chromosome maps to the autosomal maps published in Stevison et
al. (2016) *MBE* 33:928–945, for a never-completed X-vs-autosome comparative
project. These were never deposited publicly — the autosomal maps from the
same paper are on the paper's own public repository, but the chrX maps only
exist in the original researchers' files. Included here specifically because
they feed Figure 4's X-vs-autosome comparison and have no other public copy.

3 species files (gzipped) plus 3 chrX-specific binned summary files
(100kb/500kb/1Mb), ~15 MB total.

## Xue2020_macaque_LDmap/

Xue et al. (2020) *PLoS ONE* 15:e0236285 — the Indian-origin rhesus macaque
LD-based recombination map (`all.rate.bw`, a UCSC BigWig track). The
original host (a UCSC track hub on `ftp.hgsc.bcm.edu`) is no longer online.
This copy was obtained directly from the dataset while the original host was
still reachable and is rehosted here since no other public mirror is known.

1 file (`all.rate.bw.gz`), ~86 MB. Run `gunzip -k all.rate.bw.gz` before
running the compute script (pyBigWig needs the decompressed file; it's kept
gzipped here to keep the repository small).

## Everything else

Every other raw or deposited dataset used in this review — including the
LD-based maps for vervet, titi monkey, aye-aye, and marmoset (all mirrored
from [spfeiferlab.org/data](https://spfeiferlab.org/data)), the Porsborg et
al. (2025) long-read dataset (GitHub:
`PeterSoerud/recombination_calling`, Zenodo DOI 10.5281/zenodo.16893843),
and the pedigree/microsatellite/cytogenetic studies cited throughout the
central table — remains available at its original public source. Consult
`Central_Comparison_Table.xlsx`'s Reference column or the main `README.md`'s
citation list for the exact source per study.
