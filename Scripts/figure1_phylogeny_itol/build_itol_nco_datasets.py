import csv
from statistics import median

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

ALL_TAXA = ['Alouatta_caraya','Callithrix_jacchus','Cebuella_pygmaea','Cebus_capucinus',
    'Chlorocebus_sabaeus','Daubentonia_madagascariensis','Eulemur_fulvus',
    'Eulemur_fulvus_albocollaris','Eulemur_fulvus_collaris','Gorilla_gorilla_gorilla',
    'Hylobates_lar','Lemur_catta','Macaca_fuscata','Macaca_mulatta','Macaca_nemestrina',
    'Macaca_nigra','Mandrillus_sphinx','Miopithecus_talapoin','Nomascus_leucogenys',
    'Pan_paniscus','Pan_troglodytes_ellioti','Pan_troglodytes_verus','Papio_anubis',
    'Papio_hamadryas','Papio_papio','Plecturocebus_cupreus','Saguinus_oedipus',
    'Sapajus_cay','Sapajus_libidinosus','Sapajus_nigritus']

# All values in units of x1e-6 per site per generation. 'points' = every individual
# measurement contributing to that species (multiple only for Porsborg species with
# >1 sequenced individual; pedigree studies already report one pooled/sex-averaged
# figure per species, so those get a single point).
# derivation: 'published' = paper's own headline number; 'derived (pedigree)' = computed
# here from a paper-stated informative-site denominator (not the paper's
# own headline figure); 'published (supplement)' = paper's own supplementary
# table, not a number we derived ourselves, just not in the main text/deposited data
# repo where it was originally (and mistakenly) assumed absent.
NCO_DATA = [
    # (species key, [points], method, derivation, reference)
    ('Papio anubis (olive baboon)', [7.52], 'Pedigree-based WGS', 'published (main text)',
     'Wall, Robinson & Cox 2022 GBE'),
    ('Daubentonia madagascariensis (aye-aye)', [0.68], 'Pedigree-based WGS', 'published (main text)',
     'Versoza et al. 2025 GBE'),
    ('Macaca mulatta (Indian-origin, captive)', [2.18], 'Pedigree-based WGS', 'derived (computed here)',
     'Versoza et al. 2024 GBE'),
    ('Plecturocebus cupreus (coppery titi monkey)', [3.95], 'Pedigree-based WGS', 'derived (computed here)',
     'Versoza et al. 2026 GBE'),
    ('Pan troglodytes verus (western chimp)', [1.26, 1.84, 2.36, 1.96], 'Testis long-read',
     'published (supplement)', 'Porsborg et al. 2025 Nat Commun'),
    ('Gorilla gorilla gorilla (western gorilla)', [3.08, 1.95, 2.60], 'Testis long-read',
     'published (supplement)', 'Porsborg et al. 2025 Nat Commun'),
    ('Hylobates lar (lar gibbon, different genus)', [3.48], 'Testis long-read',
     'published (supplement)', 'Porsborg et al. 2025 Nat Commun'),
    ('Papio papio (Guinea baboon)', [5.00], 'Testis long-read',
     'published (supplement)', 'Porsborg et al. 2025 Nat Commun'),
    ('Macaca nemestrina (pig-tailed macaque)', [2.65], 'Testis long-read',
     'published (supplement)', 'Porsborg et al. 2025 Nat Commun'),
]

# ---------- DATASET_BOXPLOT: single ring, all 9 species with any NCO rate ----------
box_lines = []
for species, points, method, derivation, ref in NCO_DATA:
    taxon = SPECIES_MAP[species]
    vals = sorted(points)
    if len(vals) == 1:
        v = vals[0]
        box_lines.append(f"{taxon},{v},{v},{v},{v},{v}")
    else:
        lo, hi = vals[0], vals[-1]
        med = median(vals)
        extremes = ','.join(str(v) for v in vals)
        box_lines.append(f"{taxon},{lo},{lo},{med},{hi},{hi},{extremes}")

NCO_COLOR = '#B2182B'
boxplot_out = f"""DATASET_BOXPLOT
#Genome-wide non-crossover (NCO) rate, per site per generation, values in units of
#x10^-6 for readable labels/scale (e.g. 7.52 = 7.52x10^-6). All 9 species in this
#review with ANY NCO data now have a genuine, directly comparable rate (previous
#version of this file split these into a 2-species "real rate" ring and a 7-species
#"raw count ratio" ring -- both retired, superseded by this single ring, after fetching
#supplementary materials that revealed usable denominators for all of them).
#Box spans min-max of individual measurements per species -- for the 5 Porsborg
#long-read species this means individual SEQUENCED INDIVIDUALS (real biological
#variation, e.g. chimp: 4 individuals, 1.26-2.36); for the 4 pedigree species this is a
#single pooled/sex-averaged point (the paper -- or our computation from a paper-stated
#denominator -- already pools across all meioses in that pedigree).
#IMPORTANT CAVEAT: two different derivation logics contribute to this one ring, same
#units but not the same kind of measurement --
#  (a) Pedigree rate = raw event count / (phase-informative sites x meioses), a direct
#      empirical count (Papio_anubis, Daubentonia_madagascariensis: published this way
#      by the authors; Macaca_mulatta, Plecturocebus_cupreus: same arithmetic, computed
#      here from a denominator stated in the paper's own text/supplement,
#      not the paper's own headline figure -- flagged 'derived (computed here)' in
#      supplemental_nco_table.csv).
#  (b) Porsborg long-read rate = a MODEL-BASED estimate (detectability x mean GC-tract
#      length x postmeiotic-cell-fraction correction, fit per sequenced individual from
#      pooled germ cells in one animal's testis/sperm), published in the paper's own
#      Supplementary Table 6 -- not something we derived, but also not a simple count
#      ratio like (a). See supplemental_nco_table.csv for the exact derivation type per
#      species.
#Do not read this ring as "9 measurements of the same thing" -- read it as "9 best-
#available estimates using 2 structurally different methods," cross-reference
#Method_binary.txt (Pedigree-based vs Testis fields) to see which is which.
#21 of 30 species have no NCO data at all (LD-based/cytogenetic methods cannot detect
#NCO events) -- see supplemental_nco_table.csv.
#MARGIN,100 and DATASET_SCALE width 2 / label size factor 1.6 chosen to match
#cMMb_boxplot.txt. BORDER_WIDTH is a best-effort try -- not a
#documented DATASET_BOXPLOT option (see cMMb_boxplot.txt's build script for the same
#caveat) -- check after upload and drop the line if it has no visible effect.

SEPARATOR COMMA

DATASET_LABEL,NCO rate (x1e-6 bp-1 gen-1)
COLOR,{NCO_COLOR}

DATASET_SCALE,0-0-#888888-2-0-1.6,2-2-#888888-2-0-1.6,4-4-#888888-2-0-1.6,6-6-#888888-2-0-1.6,8-8-#888888-2-0-1.6

DASHED_LINES,1
WIDTH,300
MARGIN,100
BORDER_WIDTH,2

DATA
""" + '\n'.join(box_lines) + '\n'

with open('/Users/lss0021/Documents/Primate_Maps/Figure_1/iTOL_datasets/NCO_rate_boxplot.txt', 'w') as f:
    f.write(boxplot_out)
print("Wrote NCO_rate_boxplot.txt:", len(box_lines), "species rows")

# ---------- Supplemental table ----------
header = ['Species', 'Individual/Sample', 'NCO rate (x1e-6 bp-1 gen-1)', 'Method', 'Derivation', 'Reference']
supp_rows = []
for species, points, method, derivation, ref in NCO_DATA:
    taxon = SPECIES_MAP[species]
    if len(points) == 1:
        supp_rows.append([taxon.replace('_', ' '), '(pooled)', points[0], method, derivation, ref])
    else:
        for v in points:
            supp_rows.append([taxon.replace('_', ' '), '', v, method, derivation, ref])

with open('/Users/lss0021/Documents/Primate_Maps/Figure_1/iTOL_datasets/supplemental_nco_table.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(supp_rows)
print("Wrote supplemental_nco_table.csv:", len(supp_rows), "rows")

nco_taxa = {SPECIES_MAP[s] for s, *_ in NCO_DATA}
print("Species with a genuine NCO rate (", len(nco_taxa), "of", len(ALL_TAXA), "):", sorted(nco_taxa))
print("Species with NO NCO data at all (", len(ALL_TAXA) - len(nco_taxa), "of", len(ALL_TAXA), "):",
      sorted(t for t in ALL_TAXA if t not in nco_taxa))
