# Manual grafts to Primates.nwk

TimeTree's output for the 30-species `Primates.txt` list came back with only 26
tips. Two substitutions were self-reported by TimeTree in its output message
("Eulemur fulvus (replaced with Eulemur coronatus)", "Gorilla gorilla gorilla
(replaced with Gorilla gorilla)"); direct inspection of the returned
`Primates.nwk` found two further, unreported gaps: both chimp entries (`Pan
troglodytes ellioti`, `Pan troglodytes verus`) and two of the three Eulemur
fulvus subspecies (`Eulemur fulvus albocollaris`, `Eulemur fulvus collaris`)
were silently dropped rather than substituted. Likely cause for the chimp case:
two different subspecies-level inputs both resolve to the same species-level
name (`Pan troglodytes`) in TimeTree's database, and TimeTree couldn't
disambiguate them into two separate tips (unlike Gorilla, which only had one
subspecies-level entry, so its species-level fallback was unambiguous).

## Gorilla gorilla gorilla -> Gorilla gorilla substitution: no action needed
Only cosmetic — TimeTree retained the input tip label `Gorilla_gorilla_gorilla`
in the output file despite using `Gorilla gorilla` (species-level) for
placement/branch-length calculation. No subspecies-level divergence data is
being lost here since gorilla's own recombination data in this review is at
this same subspecies (western gorilla) regardless.

## Eulemur fulvus -> Eulemur coronatus substitution: assessed, not corrected
The returned tip labeled `Eulemur_fulvus` actually carries `Eulemur
coronatus`'s branch length/placement (depth 19.73 Myr from the Lemur
catta split). Assessed as **not a meaningful problem**: this branch
represents the deep Lemur-vs-Eulemur *genus*-level split, which predates the
entire Eulemur radiation (including the fulvus/coronatus split) by a wide
margin — any Eulemur species substituted here would place this particular
branch at essentially the same depth, since the intra-Eulemur diversification
is nested entirely within it. Left as-is; not worth a second TimeTree
round-trip.

## Pan troglodytes ellioti / verus — manually grafted in
Original single tip: `Pan_paniscus:8.60000000` (i.e., no internal Pan
resolution at all — Gorilla-Pan split at 8.60 Mya, Pan collapsed to one tip).

Replaced with:
```
(Pan_paniscus:2.00000000,(Pan_troglodytes_verus:0.50000000,(Pan_troglodytes_ellioti:0.40000000)'B':0.10000000)'PtAnc':1.50000000)'PanAnc':6.60000000
```
- Pan paniscus / Pan troglodytes split set to **2.0 Mya**, following de Manuel
  et al. (2016) *Science* 354:477-481 (same paper already used in this
  project for chimp-subspecies Ne), whose own figure marks a
  "2 Mya" reference tick on the bonobo/chimp divergence timeline.
- Within *P. troglodytes*: western chimp (verus) set as the deepest-diverging
  subspecies at **0.5 Mya**, with Nigeria-Cameroon (ellioti) nested slightly
  more recently at **0.4 Mya** — following de Manuel et al. (2016)'s own
  figure ticks (500 kya / 400 kya) marking chimp subspecies divergence times;
  central and eastern chimp (not tracked in this review, so not added as
  tips) would nest even more recently within the same 0.4 Mya branch under
  the true topology.
- All branch lengths sum to the original 8.60 Mya depth at every tip
  (verified: paniscus = 6.60+2.00 = 8.60; verus = 6.60+1.50+0.50 = 8.60;
  ellioti = 6.60+1.50+0.10+0.40 = 8.60), so nothing outside this Pan subclade
  (e.g. the Gorilla split) was disturbed.

## Eulemur fulvus albocollaris / collaris — manually grafted in, literature-dated
Original single tip: `Eulemur_fulvus:19.73000000`.

**Superseded placeholder**: an arbitrary near-zero-length
polytomy (0.1-0.2 Myr branches), not literature-derived — flagged at the time
as needing a real source.

**Current version**, dated using **Markolf & Kappeler (2013)**
*Frontiers in Zoology* 10:70 (including its supplement), a coalescent-based phylogeographic study of genus Eulemur with a
time-calibrated, fossil-anchored Bayesian species-tree analysis (multiple
nuclear + mitochondrial loci; Table 2). Two dating columns are given (cytb-
only vs. the combined multi-locus species tree); the species-tree column is
used here, following the paper's own stated caveat that mtDNA-only dating
systematically runs older due to mtDNA's smaller effective population size:
- **MRCA of the whole "brown lemur complex"** (which includes *E. fulvus* —
  this is the node replacing the old `EfAnc` placeholder) = **0.93 Mya**
  (95% HPD 0.33-1.43) — this is also the paper's own headline abstract
  figure, and the number originally cited elsewhere that prompted tracking
  this source down.
- **MRCA of *E. cinereiceps* + *E. collaris*** (= this project's *E. f.
  albocollaris* + *E. f. collaris* — this is the node replacing the old
  `EfSub` placeholder) = **0.51 Mya** (95% HPD 0.22-0.79).
- *E. fulvus* (nominate) itself has further real internal splits in the
  source paper (from *E. albifrons*/*E. sanfordi* at 0.27/0.17/0.09 Mya) but
  those sister taxa aren't tracked in this review, so *E. fulvus*'s branch
  here runs uninterrupted from the 0.93 Mya complex root straight to its own
  tip — a defensible simplification given the excluded taxa are real but out
  of this project's scope, not evidence *E. fulvus* has no closer relatives.

Replaced with:
```
(Eulemur_fulvus:0.93000000,(Eulemur_fulvus_albocollaris:0.51000000,Eulemur_fulvus_collaris:0.51000000)'EfSub':0.42000000)'EfAnc':18.80000000
```
- EfAnc branch (node '14' -> EfAnc) = 19.73 - 0.93 = 18.80 Myr (unchanged
  outer Lemur/Eulemur genus-level split depth, per TimeTree).
- All three tips still sum to the original 19.73 Mya depth (verified:
  fulvus = 18.80+0.93 = 19.73; albocollaris = collaris =
  18.80+0.42+0.51 = 19.73), so nothing outside this Eulemur subclade was
  disturbed.

## Net result
`Primates.nwk` now has all 30 species from `Primates.txt` as tips, verified
by direct extraction (30 unique tip labels) and a balanced-parentheses /
trailing-semicolon structural check. Not re-validated against a tree-parsing
library (Bio.Phylo/ete3 not installed in this environment) — recommend a
quick visual sanity check when this file is next opened in iTOL.
