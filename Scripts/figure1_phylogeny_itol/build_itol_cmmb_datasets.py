import csv
import openpyxl
from statistics import median
import os
# Paths resolve relative to this script, so it can be run from any directory.
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ITOL_DIR = os.path.join(REPO, 'Figures', 'Figure1_Phylogeny', 'iTOL_datasets')

wb = openpyxl.load_workbook(os.path.join(REPO, 'Central_Comparison_Table.xlsx'), data_only=True)
ws = wb['Central Comparison Table']
rows = list(ws.iter_rows(values_only=True))
data_rows = rows[1:]

SPECIES_MAP = {
    'Pan paniscus (bonobo)': 'Pan_paniscus',
    'Pan troglodytes ellioti (Nigerian chimp)': 'Pan_troglodytes_ellioti',
    'Gorilla gorilla gorilla (western gorilla)': 'Gorilla_gorilla_gorilla',
    'Pan troglodytes verus (western chimp)': 'Pan_troglodytes_verus',
    'Nomascus leucogenys (northern white-cheeked gibbon)': 'Nomascus_leucogenys',
    'Hylobates lar (lar gibbon, different genus)': 'Hylobates_lar',
    'Papio anubis (olive baboon)': 'Papio_anubis',
    'Papio hamadryas (baboon)': 'Papio_hamadryas',
    'Papio papio (Guinea baboon)': 'Papio_papio',
    'Macaca mulatta (Indian-origin, captive)': 'Macaca_mulatta',
    'Macaca mulatta (wild, Chinese-origin)': 'Macaca_mulatta',
    'Macaca mulatta (Indian-origin)': 'Macaca_mulatta',
    'Macaca mulatta': 'Macaca_mulatta',
    'Macaca nemestrina (pig-tailed macaque)': 'Macaca_nemestrina',
    'Chlorocebus aethiops sabaeus (vervet)': 'Chlorocebus_sabaeus',
    'Cebus paraguayanus (= Sapajus cay, current taxonomy)': 'Sapajus_cay',
    'Cebus libidinosus': 'Sapajus_libidinosus',
    'Cebus nigritus': 'Sapajus_nigritus',
    'Alouatta caraya': 'Alouatta_caraya',
    'Callithrix jacchus (common marmoset)': 'Callithrix_jacchus',
    'Plecturocebus cupreus (coppery titi monkey)': 'Plecturocebus_cupreus',
    'Daubentonia madagascariensis (aye-aye)': 'Daubentonia_madagascariensis',
    'Cebuella pygmaea (pygmy marmoset)': 'Cebuella_pygmaea',
    'Cebus capucinus (white-headed capuchin)': 'Cebus_capucinus',
    'Macaca fuscata (Japanese macaque)': 'Macaca_fuscata',
    'Macaca nigra (Celebes crested macaque)': 'Macaca_nigra',
    'Mandrillus sphinx (mandrill)': 'Mandrillus_sphinx',
    'Miopithecus talapoin (Angolan talapoin)': 'Miopithecus_talapoin',
    'Lemur catta (ring-tailed lemur)': 'Lemur_catta',
    'Lemur fulvus (= Eulemur fulvus, nominate)': 'Eulemur_fulvus',
    'Lemur fulvus albocollaris (= Eulemur fulvus albocollaris)': 'Eulemur_fulvus_albocollaris',
    'Lemur fulvus collaris (= Eulemur fulvus collaris)': 'Eulemur_fulvus_collaris',
    'Saguinus oedipus (cotton-top tamarin)': 'Saguinus_oedipus',
}

# 4 buckets matching the project's own "Methodological caveat" section (LD-based,
# pedigree-based, cytogenetic) plus Testis long-read (Porsborg et al. 2025) --
# this 4th bucket has no numeric cM/Mb (raw counts only), so it never appears in the
# boxplot below, only in the method-presence binary (which is scoped to ALL data, not
# just cM/Mb-bearing rows).
def bucket_for(method):
    if 'long-read' in method:
        return 'sperm_testis'
    if 'hybrid' in method:
        # Wall 2022 baboon: pedigree-CALIBRATED LD/pyrho map (fine-scale, Gini reported),
        # not a direct meiotic CO count -- bucket with LD, not pedigree.
        return 'ld'
    if method.startswith('Cytogenetic'):
        return 'cyto'
    if method.startswith('Pedigree-based'):
        return 'pedigree'
    if method.startswith('LD-based'):
        return 'ld'
    return None

# Excluded from the boxplot ring specifically --
# still present as its own row in Central_Comparison_Table.xlsx and the
# supplemental table, just dropped from this ring's min/max/median so it
# doesn't visually dominate the Macaca_mulatta box. Versoza et al. 2024's
# companion pyrho/LD estimate (0.107 cM/Mb) was never stated as a headline
# figure in that paper at all (the study's own focus was NCO rate; this LD
# map was a secondary analysis) and is, by a wide margin, the single most
# extreme value across every macaque estimate in this review -- easily read
# as implausible rather than as real biological signal. A full table of
# every individual macaque estimate (this row included) is planned for the
# review text itself, so nothing is lost, just kept out of this specific
# tree-ring visualization.
#
# 6 more species excluded following a cytogenetic-scope audit. These
# species' chiasma/MLH1 counts are autosome-only but their physical-length
# denominator is still each assembly's TOTAL length -- a congener substitution
# was attempted for all 6 to fix this the same way Macaca fuscata/nigra and
# Cebuella pygmaea were fixed, but failed: no chromosome-level assembly exists
# anywhere in genus Cebus/Sapajus (4 species) or family Atelidae (Alouatta
# caraya), and genus Mandrillus has none either (nearest chromosome-level
# relatives, Papio/Theropithecus, are a different genus -- a bigger stretch
# than this project's usual same-genus congener convention, not applied
# without explicit sign-off). Excluded from this tree-ring visualization
# specifically because it would otherwise sit directly alongside corrected,
# apples-to-apples values from every other species; still fully retained in
# Central_Comparison_Table.xlsx and in Figure 2A's crossover-assurance panel,
# which uses arm-count/aFN data only and has no physical-length denominator
# to get wrong in the first place.
BOXPLOT_EXCLUDE = {
    ("Macaca mulatta (Indian-origin, captive)", "Versoza et al. 2024 GBE (companion map)"),
    ("Mandrillus sphinx (mandrill)", "Pardo-Manuel de Villena & Sapienza 2001 Mamm Genome"),
    ("Cebus paraguayanus (= Sapajus cay, current taxonomy)", "Garcia-Cruz et al. 2009 BMC Genetics"),
    ("Cebus libidinosus", "Garcia-Cruz et al. 2011 Chromosoma"),
    ("Cebus nigritus", "Garcia-Cruz et al. 2011 Chromosoma"),
    ("Cebus capucinus (white-headed capuchin)", "Pardo-Manuel de Villena & Sapienza 2001 Mamm Genome"),
    ("Alouatta caraya", "Garcia-Cruz et al. 2011 Chromosoma"),
    # Added on reconsideration: same "uncorrected TOTAL-length
    # denominator against an autosome-only MLH1 count" problem as the 6 rows
    # above, just with a different specific blocker (X-chromosome identity
    # unconfirmed rather than no congener found) -- excluding the other 6 but
    # not this one was inconsistent. Still fully visible in Figure 2A and in
    # Figure 1's own crossover-assurance ring, neither of which is affected.
    ("Miopithecus talapoin (Angolan talapoin)", "Segura et al. 2013 Proc R Soc B"),
}

# ---------- cM/Mb-bearing rows only: feeds the boxplot + supplemental table ----------
# `records` is the COMPLETE set (BOXPLOT_EXCLUDE not applied here) -- the
# supplemental table stays the full audit-trail reference, including the
# Versoza 2024 companion-map outlier, so nothing is lost from the underlying
# data even though it's dropped from the tree ring itself (see by_taxon_boxplot
# below).
records = []
for r in data_rows:
    species, method, marker, reference, cmmb = r[1], r[2], r[3], r[5], r[7]
    if species not in SPECIES_MAP:
        continue
    taxon = SPECIES_MAP[species]
    bucket = bucket_for(method)
    if bucket is None or bucket == 'sperm_testis':
        continue
    val = None
    if isinstance(cmmb, (int, float)):
        val = float(cmmb)
    elif isinstance(cmmb, str):
        try:
            val = float(cmmb.split('±')[0].strip())
        except ValueError:
            val = None
    if val is None:
        continue
    records.append((taxon, bucket, val, method, marker, reference))

by_taxon = {}
for taxon, bucket, val, method, marker, ref in records:
    by_taxon.setdefault(taxon, []).append((bucket, val, method, marker, ref))

# Boxplot-only view: same as by_taxon but with BOXPLOT_EXCLUDE applied, so the
# excluded row still appears in the supplemental table (by_taxon above) but not
# in the tree ring itself.
_boxplot_exclude_taxon_ref = {(SPECIES_MAP[sp], ref) for sp, ref in BOXPLOT_EXCLUDE if sp in SPECIES_MAP}
by_taxon_boxplot = {}
for taxon, bucket, val, method, marker, ref in records:
    if (taxon, ref) in _boxplot_exclude_taxon_ref:
        continue
    by_taxon_boxplot.setdefault(taxon, []).append((bucket, val, method, marker, ref))

# ---------- ALL rows regardless of metric: feeds the method-presence binary ----------
# Broader than `by_taxon` above on purpose -- Testis rows have no cM/Mb value at
# all, so they'd never appear if this were scoped to cM/Mb-bearing rows only. This
# same "pull from every row" approach used throughout this figure's datasets.
all_method_by_taxon = {}
for r in data_rows:
    species, method = r[1], r[2]
    if species not in SPECIES_MAP:
        continue
    taxon = SPECIES_MAP[species]
    bucket = bucket_for(method)
    if bucket is None:
        continue
    all_method_by_taxon.setdefault(taxon, set()).add(bucket)

ALL_TAXA = ['Alouatta_caraya','Callithrix_jacchus','Cebuella_pygmaea','Cebus_capucinus',
    'Chlorocebus_sabaeus','Daubentonia_madagascariensis','Eulemur_fulvus',
    'Eulemur_fulvus_albocollaris','Eulemur_fulvus_collaris','Gorilla_gorilla_gorilla',
    'Hylobates_lar','Lemur_catta','Macaca_fuscata','Macaca_mulatta','Macaca_nemestrina',
    'Macaca_nigra','Mandrillus_sphinx','Miopithecus_talapoin','Nomascus_leucogenys',
    'Pan_paniscus','Pan_troglodytes_ellioti','Pan_troglodytes_verus','Papio_anubis',
    'Papio_hamadryas','Papio_papio','Plecturocebus_cupreus','Saguinus_oedipus',
    'Sapajus_cay','Sapajus_libidinosus','Sapajus_nigritus']

# All black -- color was distracting and shape alone is
# sufficient to distinguish the 4 method buckets.
BUCKET_COLOR = {'ld':'#000000','pedigree':'#000000','cyto':'#000000','sperm_testis':'#000000'}

# ---------- DATASET_BOXPLOT: single ring, all methods pooled per species ----------
box_lines = []
for taxon in ALL_TAXA:
    entries = by_taxon_boxplot.get(taxon, [])
    if not entries:
        continue
    vals = sorted(v for _, v, _, _, _ in entries)
    if len(vals) == 1:
        v = vals[0]
        box_lines.append(f"{taxon},{v},{v},{v},{v},{v}")
    else:
        lo, hi = vals[0], vals[-1]
        med = median(vals)
        extremes = ','.join(str(v) for v in vals)
        box_lines.append(f"{taxon},{lo},{lo},{med},{hi},{hi},{extremes}")

boxplot_out = """DATASET_BOXPLOT
#Genome-wide cM/Mb, ALL methods pooled per species (box spans min-max of every
#available estimate regardless of method -- NOT statistical quartiles, these are
#distinct measurements from different studies/methods, not repeated samples of one
#population). Method identity is intentionally NOT color-coded here (DATASET_BOXPLOT
#has no per-row color field) -- see Method_binary.txt for a separate ring showing
#which method(s) contributed to each species, and the supplemental table for the full
#per-study breakdown (value, method, reference).
#Light blue -- contrasts against NCO_rate_boxplot.txt's
#red; Gini_piechart.txt stays its existing darker blue.
#Line = median; each individual study value also plotted as an extreme point.
#Single-estimate species show as a flat point.
#MARGIN,100 and DATASET_SCALE width 2 / label size factor 1.6 chosen to match the
#other rings. BORDER_WIDTH is included as a best-effort try -- it is a documented,
#working option for DATASET_SIMPLEBAR/MULTIBAR/PIECHART/COLOR_STRIP, but is NOT listed
#anywhere in iTOL's own DATASET_BOXPLOT template, so it may simply be ignored by iTOL's
#boxplot renderer; check after upload and drop the line if it has no visible effect.

SEPARATOR COMMA

DATASET_LABEL,cM/Mb (all methods pooled)
COLOR,#56B4E9

DATASET_SCALE,0-0-#888888-2-0-1.6,0.5-0.5-#888888-2-0-1.6,1-1-#888888-2-0-1.6,1.5-1.5-#888888-2-0-1.6

DASHED_LINES,1
WIDTH,300
MARGIN,100
BORDER_WIDTH,2

DATA
""" + '\n'.join(box_lines) + '\n'

with open(os.path.join(ITOL_DIR, 'cMMb_boxplot.txt'), 'w') as f:
    f.write(boxplot_out)
print("Wrote cMMb_boxplot.txt:", len(box_lines), "species rows")

# ---------- DATASET_BINARY: method presence/absence, decoupled from the boxplot ----------
# Scoped to ALL rows (all_method_by_taxon), not just cM/Mb-bearing ones -- so Testis
# shows up even though it contributes no cM/Mb value. 1 = species has >=1
# estimate from this method; -1 = omitted entirely (no data), per the template's
# convention -- cleaner than a filled/empty checkbox pair since absence here just means
# "no data of this type", not a meaningful negative result.
# Ordered by chronology of the underlying technology, oldest to newest:
# Cytogenetic (classical + immunofluorescence cytology) -> Pedigree-based
# (linkage/transmission mapping) -> LD-based (population-genetic inference) -> Testis
# (most recent, long-read haplotype-switching) last.
METHOD_ORDER = ['cyto', 'pedigree', 'ld', 'sperm_testis']
METHOD_LABEL = {'ld':'LD-based','pedigree':'Pedigree-based','cyto':'Cytogenetic','sperm_testis':'Testis'}
METHOD_SHAPE = {'ld':'1','pedigree':'2','cyto':'3','sperm_testis':'4'}  # square/circle/star/triangle

binary_lines = []
for taxon in ALL_TAXA:
    buckets_present = all_method_by_taxon.get(taxon, set())
    vals = ['1' if b in buckets_present else '-1' for b in METHOD_ORDER]
    binary_lines.append(f"{taxon}," + ','.join(vals))

field_colors = ','.join(BUCKET_COLOR[b] for b in METHOD_ORDER)
field_labels = ','.join(METHOD_LABEL[b] for b in METHOD_ORDER)
field_shapes = ','.join(METHOD_SHAPE[b] for b in METHOD_ORDER)

binary_out = f"""DATASET_BINARY
#Method presence/absence per species, pulled from EVERY row in the central table (not
#just cM/Mb-bearing rows) -- decoupled from the pooled cM/Mb boxplot (cMMb_boxplot.txt)
#so the boxplot doesn't need to color-code by method. 4 fields, ordered oldest-to-newest
#technology: Cytogenetic, Pedigree-based, LD-based, Testis (long-read haplotype
#switching, Porsborg et al. 2025 -- has no cM/Mb value of its own, raw counts only, so
#it would never show up if this ring were scoped to cM/Mb data like the boxplot is).
#All black -- shape alone distinguishes method. 1 = filled
#shape (species has >=1 estimate from this method), -1 = omitted entirely (no data of
#this type for this species). See the supplemental table for exact study/reference per
#data point.
#SHOW_LABELS,1 displays the field labels (Cytogenetic/Pedigree-based/LD-based/Testis)
#above the columns directly.
#MARGIN,150 -- this ring loads 2nd (after Marker_binary.txt), wider
#margin than the 100px used for cM/Mb/Gini/NCO to give it more spacing from the
#Marker Type ring immediately before it.

SEPARATOR COMMA

DATASET_LABEL,Method
COLOR,#000000

FIELD_SHAPES,{field_shapes}
FIELD_LABELS,{field_labels}
FIELD_COLORS,{field_colors}

DASHED_LINES,1
SHOW_LABELS,1
MARGIN,150

LEGEND_TITLE,Method
LEGEND_SHAPES,{field_shapes}
LEGEND_COLORS,{field_colors}
LEGEND_LABELS,{field_labels}

DATA
""" + '\n'.join(binary_lines) + '\n'

with open(os.path.join(ITOL_DIR, 'Method_binary.txt'), 'w') as f:
    f.write(binary_out)
print("Wrote Method_binary.txt:", len(binary_lines), "species rows")
print("Species with no method data at all:", [t for t in ALL_TAXA if t not in all_method_by_taxon])

# ---------- Supplemental table: full per-study breakdown (not encoded visually anymore) ----------
BUCKET_TITLE = {'ld':'LD-based','pedigree':'Pedigree-based','cyto':'Cytogenetic'}
supp_rows = []
for taxon in ALL_TAXA:
    for bucket, val, method, marker, ref in by_taxon.get(taxon, []):
        supp_rows.append([taxon.replace('_', ' '), 'cM/Mb', BUCKET_TITLE[bucket], method, marker, round(val, 4), ref])

with open(os.path.join(ITOL_DIR, 'supplemental_cmmb_table.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Species', 'Metric', 'Method category', 'Method (full)', 'Marker Type', 'Value', 'Reference'])
    writer.writerows(supp_rows)
print("Wrote supplemental_cmmb_table.csv:", len(supp_rows), "rows")
