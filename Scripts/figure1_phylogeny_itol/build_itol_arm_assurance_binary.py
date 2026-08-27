ALL_TAXA = ['Alouatta_caraya','Callithrix_jacchus','Cebuella_pygmaea','Cebus_capucinus',
    'Chlorocebus_sabaeus','Daubentonia_madagascariensis','Eulemur_fulvus',
    'Eulemur_fulvus_albocollaris','Eulemur_fulvus_collaris','Gorilla_gorilla_gorilla',
    'Hylobates_lar','Lemur_catta','Macaca_fuscata','Macaca_mulatta','Macaca_nemestrina',
    'Macaca_nigra','Mandrillus_sphinx','Miopithecus_talapoin','Nomascus_leucogenys',
    'Pan_paniscus','Pan_troglodytes_ellioti','Pan_troglodytes_verus','Papio_anubis',
    'Papio_hamadryas','Papio_papio','Plecturocebus_cupreus','Saguinus_oedipus',
    'Sapajus_cay','Sapajus_libidinosus','Sapajus_nigritus']

# Arm-level obligate-crossover assurance (Dumont 2017, Genetics 205:155-168): does
# mean crossover count (nXO) exceed the HAPLOID autosomal arm count (aFN/2)? Per
# Dumont's own explicit definition (p.160): "the haploid number of autosomal
# chromosome arms (aFN/2)" -- aFN itself is diploid-scale (same convention as 2N),
# matching how n_bivalents = 2N/2 is the haploid chromosome count used in this
# project's chromosome-level check (Figure_2's Panel A / crossover-assurance table).
# This ring reproduces Dumont's own tree-coloring convention directly (her Figure 5:
# nXO < aFN/2 vs nXO > aFN/2), moved here after Figure_2's Panel A was
# simplified back to chromosome-level only.
#
# Formula correction: an earlier version of this analysis
# (briefly a second facet in Figure_2's Panel A) used aFN directly as the arm-level
# denominator instead of aFN/2 -- exactly double what Dumont's own test requires.
# That bug made every species fail uniformly; the corrected version below reproduces
# real, mixed pass/fail results that closely match Dumont's own reported primate
# pattern as a sanity check -- e.g. she states "three of the four macaque species...
# exhibit fewer crossovers per meiosis than chromosome arms" and "the cotton-top
# tamarin (Saguinus oedipus) also conforms to this trend [nXO < aFN/2]"; the
# corrected numbers below reproduce exactly that (Macaca fuscata/nigra/nemestrina
# fail, Macaca mulatta passes via its pedigree/linkage-map value; both Saguinus
# oedipus rows fail).
#
# ONE representative value per tip (matching how a tree can only show one state per
# tip, and how Dumont herself must have picked one value per species for her own
# tree). Precedence where a tip has multiple aFN-eligible measurements: direct
# count (pedigree/linkage-map or cytogenetic) preferred over LD-based (same
# precedence already established in Figure_2 Panel A's original design); within
# direct counts, pedigree/linkage-map preferred as the most modern/precise
# technique, then MLH1 (immunofluorescence, more modern) over Chiasma (classical
# light-microscopy, older) -- matching this project's own established chronology-
# of-technology framing (see Marker_binary.txt). Exact XO, aFN, and source for
# every tip with a value:
#   Pan_troglodytes_verus:  XO=52.5 (Chiasma, Pardo-Manuel de Villena & Sapienza
#     2001), aFN=82 -> aFN/2=41.0 -> PASS (52.5 > 41.0). Also cross-checked against
#     this species' own LD-based total (Auton 2012: XO-equivalent=52.58) -- agrees.
#   Pan_troglodytes_ellioti: XO-equivalent=34.98 (LD-based, Stevison 2016 MBE, no
#     direct/cytogenetic value exists for this subspecies specifically -- the
#     Chiasma value is attributed to western chimp only, see above),
#     aFN=82 -> aFN/2=41.0 -> FAIL (34.98 < 41.0).
#   Papio_hamadryas: XO=47.08 (LinkageMap, Cox et al. 2006), aFN=80 -> aFN/2=40.0
#     -> PASS (47.08 > 40.0).
#   Macaca_mulatta: XO=40.96 (LinkageMap, Rogers et al. 2006 -- preferred over this
#     species' own MLH1 XO=39.0 and Chiasma XO=38.0, both of which also fail),
#     aFN=80 -> aFN/2=40.0 -> PASS (40.96 > 40.0, narrowly).
#   Macaca_fuscata: XO=36.7 (Chiasma), aFN=80 -> aFN/2=40.0 -> FAIL.
#   Macaca_nigra: XO=39.0 (Chiasma), aFN=80 -> aFN/2=40.0 -> FAIL.
#   Macaca_nemestrina: XO=40.0 (Chiasma), aFN=80 -> aFN/2=40.0 -> TIE, treated as
#     FAIL (does not strictly exceed the threshold) -- flagged explicitly since this
#     is the one genuinely ambiguous case in this dataset.
#   Mandrillus_sphinx: XO=45.0 (Chiasma), aFN=80 -> aFN/2=40.0 -> PASS.
#   Miopithecus_talapoin: XO=39.7 (MLH1), aFN=92 -> aFN/2=46.0 -> FAIL.
#   Alouatta_caraya: XO=40.6 (MLH1), aFN=66 -> aFN/2=33.0 -> PASS.
#   Sapajus_cay: XO=43.22 (MLH1), aFN=72 -> aFN/2=36.0 -> PASS.
#   Sapajus_libidinosus: XO=41.3 (MLH1), aFN=72 -> aFN/2=36.0 -> PASS.
#   Sapajus_nigritus: XO=39.2 (MLH1), aFN=72 -> aFN/2=36.0 -> PASS.
#   Cebuella_pygmaea: XO=36.9 (MLH1 -- preferred over this species' own Chiasma
#     XO=41.7, which alone would PASS), aFN=74 -> aFN/2=37.0 -> FAIL (36.9 < 37.0,
#     narrowly) -- the one species where method choice flips the outcome; flagged.
#   Cebus_capucinus: XO=40.5 (Chiasma), aFN=68 -> aFN/2=34.0 -> PASS.
#   Saguinus_oedipus: XO=38.9 (MLH1 -- Chiasma XO=39.6 also fails, no conflict),
#     aFN=86 -> aFN/2=43.0 -> FAIL.
#   Lemur_catta: XO=35.9 (MLH1), aFN=62 -> aFN/2=31.0 -> PASS.
#   Eulemur_fulvus: XO=36.3 (Chiasma), aFN=62 -> aFN/2=31.0 -> PASS.
#   Eulemur_fulvus_albocollaris: XO=35.2 (Chiasma), aFN=62 -> aFN/2=31.0 -> PASS.
#   Eulemur_fulvus_collaris: XO=36.0 (Chiasma), aFN=62 -> aFN/2=31.0 -> PASS.
# EXTENDED BEYOND DUMONT 2017: Nomascus_leucogenys -- Dumont's own
# table has no gibbon row at all, but a species-level karyotype
# source with an explicit fundamental number was found: Harding, L.E. (2013)
# "Nomascus leucogenys (Primates: Hylobatidae)," Mammalian Species 44(890):1-15,
# citing Chiarelli (1972) -- states FN=94 directly (X chromosome explicitly
# metacentric, Y explicitly "appears to be acrocentric"). An earlier attempt to
# derive this from a different paper's Table 1 (a FISH fosmid-mapping study, Chen
# et al. 2007, which only samples ~100 randomly selected clones, not an exhaustive
# physical map) gave aFN=78-82 depending on how the 2 chromosomes with zero mapped
# clones were treated -- superseded by this cleaner, explicit, directly-cited source.
# Converted FN=94 (total, diploid) to aFN (autosomal only) using the same
# female-XX-complement convention that exactly reproduces Dumont's own human entry
# (FN=82, aFN=78 -- her FN also implicitly uses 2 metacentric X's, since
# 82-2*2=78 matches exactly): aFN = FN - 2*(X arms) = 94 - 2*2 = 90 (X stated
# metacentric = 2 arms; using 2 X's per the standard female-complement FN
# convention, not the male X+Y complement, which would give an odd, internally
# inconsistent aFN=91 -- autosomal FN must be even since autosomes are always
# matched pairs, confirming the female-complement reading is correct here).
# aFN/2 = 45. Gibbon's own LD-based total (Stevison, unpublished: 1.5498 cM/Mb x
# 2650.18 Mb = 4107.25 cM, XO-equivalent = 82.14) clears this easily (82.14 > 45,
# ratio 1.83) -- consistent with gibbon also being the single highest cM/Mb value
# in this entire review.
#
# EXTENDED BEYOND DUMONT 2017: Gorilla_gorilla_gorilla -- a
# karyotype description was found stating "The diploid (2n) number is 48
# chromosomes in Gorilla beringei (Mai 1983). The autosomes include 34
# metacentric and submetacentric and 12 acrocentric with satellites on their
# arms." Two things to flag: (1) this describes Gorilla beringei (eastern
# gorilla), not this project's tracked Gorilla gorilla gorilla (western
# lowland gorilla) -- applied across the genus since gorilla karyotypes are
# well-conserved (2n=48 throughout Gorilla, unlike Pan where subspecies-level
# chiasma attribution genuinely mattered), but flagged as a genus-level
# extrapolation, not a species-exact match, matching this project's
# established practice for cross-species karyotype/assembly substitutions.
# (2) 34+12=46 autosomes = 23 pairs, matching this project's own
# already-established n_bivalents=23 for gorilla (independently verified from
# deposited map file chromosome counts) -- a clean consistency check that this
# source describes the same karyotype convention already in use here.
# aFN = 34*2 (metacentric/submetacentric, 2 arms each) + 12*1 (acrocentric, 1 arm
# each) = 80 (even, as required for autosomes). aFN/2 = 40. Gorilla's own LD-based
# total (Stevison et al. 2016, independent Ne: 0.7424 cM/Mb x 2419.07 Mb = 1795.92
# cM, XO-equivalent = 35.92) does NOT clear this (35.92 < 40, ratio 0.898) -- FAILS.
#
# EXTENDED BEYOND DUMONT 2017: Pan_paniscus -- no bonobo-specific
# karyotype source found, but bonobo and chimp are sister species (both genus Pan)
# with a famously near-identical 2n=48 karyotype -- the most directly justified
# cross-species substitution in this whole batch. Reused chimp's own aFN=82 (from
# Dumont's Table S1, already applied to both Pan troglodytes subspecies). aFN/2=41.
# Bonobo's own LD-based total (Stevison et al. 2016, independent Ne: 0.6893 cM/Mb x
# 2403.18 Mb = 1656.51 cM, XO-equivalent = 33.13) does NOT clear this (33.13 < 41,
# ratio 0.808) -- FAILS.
#
# EXTENDED BEYOND DUMONT 2017: Plecturocebus_cupreus -- a
# karyotype description was found for the closely related Plecturocebus caquetensis
# (Caqueta titi monkey): "diploid number (2n) of 46 chromosomes consisting of seven
# metacentric and 15 acrocentric pairs; the X chromosome is submetacentric but the
# morphology of the Y chromosome is unknown (Bueno and Defler 2010)," with the
# source text itself stating directly "This karyomorph is very similar to P.
# cupreus (Defler et al. 2010)" -- an explicit, literature-stated cross-species
# justification, not just an inference from genus-level conservation the way the
# gorilla/bonobo substitutions above are. 7+15=22 autosome pairs, matching this
# project's own already-established n_bivalents=22 for P. cupreus exactly -- a
# clean consistency check. aFN = 7*2*2 (metacentric pairs, 2 arms each) + 15*2*1
# (acrocentric pairs, 1 arm each) = 28+30 = 58. aFN/2 = 29. Titi monkey's own
# pedigree total (Versoza et al. 2026 GBE: 2450 cM, XO-equivalent = 49.0) clears
# this comfortably (49.0 > 29, ratio 1.69) -- PASSES.
#
# EXTENDED BEYOND DUMONT 2017: Daubentonia_madagascariensis -- direct
# species match (no cross-species substitution needed): "Daubentonia
# madagascariensis has 2n=30 chromosomes. Karyotype consists of 14 autosomal
# metacentrics, 10 autosomal submetacentrics, and 4 autosomal acrocentrics. The X
# and Y chromosomes are metacentric (Poorman-Allen and Izard 1990; Rumpler et al.
# 1988)." 14+10+4=28 individual autosomes = 14 pairs, matching this project's own
# already-established n_bivalents=14 for aye-aye exactly -- a clean consistency
# check. aFN = (14+10)*2 (metacentric+submetacentric, 2 arms each) + 4*1
# (acrocentric, 1 arm) = 48+4 = 52. aFN/2 = 26. Aye-aye's own pedigree total
# (Versoza et al. 2025 GBE: 1525 cM, XO-equivalent = 30.5) clears this (30.5 > 26,
# ratio 1.17) -- PASSES.
#
# RESOLVED: Callithrix jacchus -- a direct species-specific source
# found this time (superseding the earlier declined Mico humeralifer substitution):
# "Comparative chromosomal study of five taxa of genus Callithrix, group Jacchus
# (Platyrrhini, primates)," Am J Primatol 41(1) -- states all five taxa including
# C. jacchus have 2n=46, 14 uniarmed and 30 biarmed autosomes, submetacentric X.
# This ALSO caught a real bug: this project's own existing n_bivalents for
# Callithrix jacchus was 20, but 14+30=44 autosomes = 22 pairs, not 20 -- confirmed
# independently against Soni et al.'s own marmoset paper, which labels marmoset
# autosomes as "chromosomes 1-22." Fixed in both this ring and Figure_2's Panel A
# (`build_gini_dotplot.R`) -- cos_per_bivalent there drops from 2.4128 to 2.1934,
# no pass/fail change at the chromosome level. aFN = 14*1 + 30*2 = 74. aFN/2 = 37.
# Marmoset's own LD-based total (Soni/Versoza preprint: 0.91 cM/Mb x 2651.4 Mb =
# 2412.77 cM, XO-equivalent = 48.26) clears this comfortably (48.26 > 37, ratio
# 1.30) -- PASSES.
#
# EXTENDED BEYOND DUMONT 2017: Papio_anubis -- reused Papio hamadryas's
# own aFN=80 (already sourced directly from Dumont's Table S1) rather than the
# cross-genus macaque-homology chain also considered, since baboon species within
# genus Papio are famously near-identical karyotypically -- a same-genus reuse is
# more directly justified than a cross-genus inference, though it's reassuring that
# an independent homology-based estimate also converged on aFN=80. aFN/2=40.
# Papio anubis's own pedigree total (Wall, Robinson & Cox 2022 GBE: 2293.5 cM,
# XO-equivalent = 45.87) clears this (45.87 > 40, ratio 1.15) -- PASSES.
#
# EXTENDED BEYOND DUMONT 2017: Chlorocebus_sabaeus -- Stock & Hsu
# (1973, Chromosoma 43:211-224) states the Cercopithecus aethiops species group
# (which explicitly includes C. sabaeus per Dutrillaux et al.) has 120 total arms,
# all chromosomes biarmed, with the caveat that 7 pairs carry "short heterochromatic
# second arms" not all cytogeneticists count as true second arms. aFN = 120 - 4
# (X+Y, both biarmed) = 116; aFN/2 = 58. Vervet's own pedigree total (Jasinska et
# al. 2007: 2726 cM, n_bivalents=29, matching this species' own established value)
# gives XO-equivalent=54.52, which does NOT clear 58 (ratio 0.940) -- FAILS, but
# flagged as BORDERLINE given the acknowledged +/-2-4 arm uncertainty in aFN itself
# (if even 4 of the disputed 7 "short second arms" don't count, aFN drops enough to
# flip this to a pass) -- treat this result with more caution than the others.
#
# NOT APPLICABLE: Hylobates lar and Papio papio both have karyotype
# sources now (Tantravahi et al. 1975 for gibbon; homology-based for baboon), but
# NEITHER has a usable crossover count in this review -- both species' only data
# point is Porsborg et al. (2025) long-read raw counts, which this project already
# excludes from crossover-assurance entirely (pooled germ cells from long-read
# testis sequencing aren't a countable per-meiosis quantity the way pedigree/
# cytogenetic/LD data are -- same exclusion rule already applied throughout this
# ring and Figure_2's Panel A). A good aFN doesn't help without a comparable nXO;
# both remain omitted (-1).
ARM_ASSURANCE = {
    'Pan_paniscus': 0,
    'Pan_troglodytes_verus': 1,
    'Pan_troglodytes_ellioti': 0,
    'Gorilla_gorilla_gorilla': 0,
    'Plecturocebus_cupreus': 1,
    'Daubentonia_madagascariensis': 1,
    'Callithrix_jacchus': 1,
    'Papio_anubis': 1,
    'Chlorocebus_sabaeus': 0,   # borderline -- see note above, +/-2-4 arm aFN uncertainty
    'Papio_hamadryas': 1,
    'Macaca_mulatta': 1,
    'Macaca_fuscata': 0,
    'Macaca_nigra': 0,
    'Macaca_nemestrina': 0,   # tie (nXO == aFN/2), treated as fail -- see note above
    'Mandrillus_sphinx': 1,
    'Miopithecus_talapoin': 0,
    'Alouatta_caraya': 1,
    'Sapajus_cay': 1,
    'Sapajus_libidinosus': 1,
    'Sapajus_nigritus': 1,
    'Cebuella_pygmaea': 0,
    'Cebus_capucinus': 1,
    'Saguinus_oedipus': 0,
    'Lemur_catta': 1,
    'Eulemur_fulvus': 1,
    'Eulemur_fulvus_albocollaris': 1,
    'Eulemur_fulvus_collaris': 1,
    'Nomascus_leucogenys': 1,
}

n_pass = sum(1 for v in ARM_ASSURANCE.values() if v == 1)
n_fail = sum(1 for v in ARM_ASSURANCE.values() if v == 0)
print(f"{len(ARM_ASSURANCE)} of {len(ALL_TAXA)} tips have an arm-assurance value: "
      f"{n_pass} pass, {n_fail} fail.")

binary_lines = []
for taxon in ALL_TAXA:
    val = ARM_ASSURANCE.get(taxon, -1)
    binary_lines.append(f"{taxon},{val}")

out = """DATASET_BINARY
#Arm-level obligate-crossover assurance (Dumont 2017, Genetics 205:155-168): does mean
#crossover count (nXO) exceed the haploid autosomal arm count (aFN/2)? Directly
#reproduces Dumont's own tree-coloring convention (her Figure 5). Distinct from the
#chromosome-level check in Figure_2's Panel A (implied COs per bivalent >= 1, which
#holds for every species in this review) -- this ring tests the stricter, per-ARM
#version of the same obligate-crossover floor, which does NOT hold universally: see
#the per-tip XO/aFN/source breakdown in this file's own build script
#(build_itol_arm_assurance_binary.py) for exactly which value was used per species and
#why, including the one genuine tie (Macaca_nemestrina) and the one species where
#method choice flips the outcome (Cebuella_pygmaea).
#1 = filled shape (nXO > aFN/2, passes arm-level assurance), 0 = empty/outline shape
#(nXO <= aFN/2, fails arm-level assurance), -1 = omitted entirely (no aFN available in
#Dumont's Table S1 for this species).
#Black (matching Marker_binary.txt/Method_binary.txt) -- shape fill (not color)
#distinguishes pass from fail. MARGIN,100 matches Gini_piechart.txt/cMMb_boxplot.txt/
#NCO_rate_boxplot.txt's spacing.

SEPARATOR COMMA

DATASET_LABEL,Arm-level CO assurance (Dumont 2017)
COLOR,#000000

FIELD_SHAPES,2
FIELD_LABELS,nXO > aFN/2
FIELD_COLORS,#000000

DASHED_LINES,1
SHOW_LABELS,1
MARGIN,100

LEGEND_TITLE,Arm-level CO assurance
LEGEND_SHAPES,2
LEGEND_COLORS,#000000
LEGEND_LABELS,nXO > aFN/2

DATA
""" + '\n'.join(binary_lines) + '\n'

with open('/Users/lss0021/Documents/Primate_Maps/Figure_1/iTOL_datasets/ArmAssurance_binary.txt', 'w') as f:
    f.write(out)

print("Wrote ArmAssurance_binary.txt:", len(binary_lines), "species rows")
