import csv
import openpyxl
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

ESTIMATOR = {
    ('Pan paniscus (bonobo)', 'Stevison et al. 2016 MBE'): 'ldhat',
    ('Pan troglodytes ellioti (Nigerian chimp)', 'Stevison et al. 2016 MBE'): 'ldhat',
    ('Gorilla gorilla gorilla (western gorilla)', 'Stevison et al. 2016 MBE'): 'ldhat',
    ('Pan troglodytes verus (western chimp)', 'Auton et al. 2012 Science'): 'ldhat',
    ('Nomascus leucogenys (northern white-cheeked gibbon)', 'Stevison, unpublished; now available in its own GitHub repo'): 'ldhat',
    ('Papio anubis (olive baboon)', 'Wall, Robinson & Cox 2022 GBE'): 'pyrho',
    ('Macaca mulatta (Indian-origin, captive)', 'Versoza et al. 2024 GBE (companion map)'): 'pyrho',
    ('Macaca mulatta (wild, Chinese-origin)', 'Terbot, Calahorra-Oliart, Versoza et al. 2025 Am J Primatol'): 'pyrho',
    ('Chlorocebus aethiops sabaeus (vervet)', 'Pfeifer 2020 MBE'): 'ldhat',
    ('Callithrix jacchus (common marmoset)', 'Soni, Versoza et al. 2025/26 bioRxiv (PREPRINT, not peer-reviewed)'): 'ldhat',
    ('Daubentonia madagascariensis (aye-aye)', 'Soni, Versoza et al. 2025 Ecology and Evolution'): 'pyrho',
}

records = []
titi_ld_seen = 0
for r in data_rows:
    species, method, reference, gini = r[1], r[2], r[5], r[9]
    if species not in SPECIES_MAP:
        continue
    if not isinstance(gini, (int, float)):
        continue
    taxon = SPECIES_MAP[species]
    key = (species, reference)
    if key == ('Plecturocebus cupreus (coppery titi monkey)', 'Soni, Versoza et al. 2026 Heredity'):
        titi_ld_seen += 1
        estimator = 'ldhelmet' if titi_ld_seen == 1 else 'ldhat'
    else:
        estimator = ESTIMATOR.get(key)
    if estimator is None:
        continue
    records.append((taxon, estimator, float(gini), reference))

by_taxon = {}
for taxon, est, val, ref in records:
    by_taxon.setdefault(taxon, []).append((est, val, ref))

ALL_TAXA = ['Alouatta_caraya','Callithrix_jacchus','Cebuella_pygmaea','Cebus_capucinus',
    'Chlorocebus_sabaeus','Daubentonia_madagascariensis','Eulemur_fulvus',
    'Eulemur_fulvus_albocollaris','Eulemur_fulvus_collaris','Gorilla_gorilla_gorilla',
    'Hylobates_lar','Lemur_catta','Macaca_fuscata','Macaca_mulatta','Macaca_nemestrina',
    'Macaca_nigra','Mandrillus_sphinx','Miopithecus_talapoin','Nomascus_leucogenys',
    'Pan_paniscus','Pan_troglodytes_ellioti','Pan_troglodytes_verus','Papio_anubis',
    'Papio_hamadryas','Papio_papio','Plecturocebus_cupreus','Saguinus_oedipus',
    'Sapajus_cay','Sapajus_libidinosus','Sapajus_nigritus']

# ---------- DATASET_PIECHART: one gauge-style pie per species, single representative value ----------
# Gini is bounded [0,1], so [value, 1-value] renders as a natural "how full" gauge.
# Only Macaca_mulatta still has >1 estimate needing disambiguation -- picking one
# representative value; both alternates and the reasoning are logged
# in the supplemental table, not silently dropped.
# NOTE: Pan_troglodytes used to need this same disambiguation (Stevison's
# Nigerian-chimp-based 0.821 vs. Auton's western-chimp-based 0.7766), back when both
# chimp subspecies collapsed onto one shared 'Pan_troglodytes' tree tip. Now that
# Primates.nwk carries them as separate tips (Pan_troglodytes_ellioti,
# Pan_troglodytes_verus -- see Primates_nwk_manual_grafts.md), each has exactly one
# Gini estimate of its own and needs no picking at all; removed from this dict.
PIE_PICK = {
    # species: (estimator, value, reference) chosen as the single representative point
    'Macaca_mulatta':  ('pyrho', 0.6144, 'Versoza et al. 2024 GBE (companion map)'),  # vs. 0.2813, Terbot et al. 2025
}
GINI_COLOR = '#332288'
REMAINDER_COLOR = '#e6e6e6'

pie_lines = []
for taxon in ALL_TAXA:
    entries = by_taxon.get(taxon, [])
    if not entries:
        continue
    if taxon in PIE_PICK:
        _, val, _ = PIE_PICK[taxon]
    else:
        val = entries[0][1]
    pie_lines.append(f"{taxon},-1,10,{round(val,2)},{round(1-val,2)}")

pie_out = f"""DATASET_PIECHART
#Fine-scale Gini coefficient as a gauge-style pie per species: 2 fields, [Gini value,
#1-Gini value], so the filled wedge directly reads as "how close to maximally uneven".
#Gini is naturally bounded [0,1], which is what makes this work as a gauge (would not
#make sense for cM/Mb, which is unbounded).
#For Macaca_mulatta (the only species left with more than one estimate, after the
#chimp-subspecies tip split -- see PIE_PICK comment above), ONE representative value
#was picked (see PIE_PICK in the build script) -- both alternates are in the
#supplemental table, not silently dropped.
#No legend block -- deliberately dropped since the "Gini coefficient" /
#"(1 - Gini)" swatch legend didn't add anything a caption wouldn't say better.
#SIZE NOTE: these are EXTERNAL pie charts (position=-1 in the DATA rows
#below) -- per iTOL's own DATASET_PIECHART template, MAXIMUM_SIZE only applies to
#INTERNAL pie charts and is a no-op here; HEIGHT_FACTOR is the setting that actually
#controls external pie chart size (a multiplier on the default leaf-space-based
#radius). This is why the circles were reading smaller than the binary symbols even
#though MAXIMUM_SIZE was already set well above their default -- HEIGHT_FACTOR
#raised to 3.6 to fix this; MAXIMUM_SIZE left in place but has no effect.
#MARGIN,100 -- matches cMMb_boxplot.txt/NCO_rate_boxplot.txt's spacing;
#this ring loads 4th (after Marker type, Method, cM/Mb), before NCO last.

SEPARATOR COMMA

DATASET_LABEL,Gini (gauge)
COLOR,{GINI_COLOR}

FIELD_COLORS,{GINI_COLOR},{REMAINDER_COLOR}
FIELD_LABELS,Gini,remainder

MAXIMUM_SIZE,25
HEIGHT_FACTOR,3.6
MARGIN,100

DATA
""" + '\n'.join(pie_lines) + '\n'

with open(os.path.join(ITOL_DIR, 'Gini_piechart.txt'), 'w') as f:
    f.write(pie_out)
print("Wrote Gini_piechart.txt:", len(pie_lines), "species rows")
print("Species with no Gini value:", [t for t in ALL_TAXA if t not in by_taxon])

# ---------- Supplemental table: full per-study breakdown (estimator identity kept out of figure) ----------
EST_TITLE = {'ldhat':'LDhat','ldhelmet':'LDhelmet','pyrho':'pyrho'}
supp_rows = []
for taxon in ALL_TAXA:
    for est, val, ref in by_taxon.get(taxon, []):
        picked = (taxon in PIE_PICK and PIE_PICK[taxon][1] == val)
        note = 'used in Gini_piechart.txt' if picked else ('alt. value, not in piechart' if taxon in PIE_PICK else '')
        supp_rows.append([taxon.replace('_', ' '), 'Gini', EST_TITLE[est], round(val, 4), ref, note])

with open(os.path.join(ITOL_DIR, 'supplemental_gini_table.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Species', 'Metric', 'Estimator', 'Value', 'Reference', 'Note'])
    writer.writerows(supp_rows)
print("Wrote supplemental_gini_table.csv:", len(supp_rows), "rows")
