import openpyxl

wb = openpyxl.load_workbook('/Users/lss0021/Documents/Primate_Maps/Master_Comparison_Table.xlsx', data_only=True)
ws = wb['Master Comparison Table']
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

CLADE_COLORS = {
    'Apes': '#d95f02',
    'Old World Monkeys': '#7570b3',
    'New World Monkeys': '#1b9e77',
    'Lemurs': '#e6ab02',
}

ALL_TAXA = ['Alouatta_caraya','Callithrix_jacchus','Cebuella_pygmaea','Cebus_capucinus',
    'Chlorocebus_sabaeus','Daubentonia_madagascariensis','Eulemur_fulvus',
    'Eulemur_fulvus_albocollaris','Eulemur_fulvus_collaris','Gorilla_gorilla_gorilla',
    'Hylobates_lar','Lemur_catta','Macaca_fuscata','Macaca_mulatta','Macaca_nemestrina',
    'Macaca_nigra','Mandrillus_sphinx','Miopithecus_talapoin','Nomascus_leucogenys',
    'Pan_paniscus','Pan_troglodytes_ellioti','Pan_troglodytes_verus','Papio_anubis',
    'Papio_hamadryas','Papio_papio','Plecturocebus_cupreus','Saguinus_oedipus',
    'Sapajus_cay','Sapajus_libidinosus','Sapajus_nigritus']

taxon_group = {}
for r in data_rows:
    group, species = r[0], r[1]
    if species not in SPECIES_MAP:
        continue
    taxon = SPECIES_MAP[species]
    if taxon in taxon_group and taxon_group[taxon] != group:
        raise RuntimeError(f"Conflicting group for {taxon}: {taxon_group[taxon]} vs {group}")
    taxon_group[taxon] = group

missing = [t for t in ALL_TAXA if t not in taxon_group]
if missing:
    raise RuntimeError(f"No group assignment found for: {missing}")

# Clade LCA leaf-pairs re-verified by hand against the expanded 30-tip
# Figure_1/Primates.nwk topology (up from 18 tips -- Dumont et al. 2017 species batch
# plus the manually-grafted chimp subspecies and Eulemur fulvus complex):
#   Apes              = LCA(Hylobates_lar, Pan_troglodytes_ellioti) -- 6 tips
#   Old World Monkeys = LCA(Chlorocebus_sabaeus, Macaca_nigra) -- 10 tips
#   New World Monkeys = LCA(Plecturocebus_cupreus, Alouatta_caraya) -- 9 tips
#   Lemurs            = LCA(Daubentonia_madagascariensis, Eulemur_fulvus_collaris) -- 5
#                        tips (no longer a single leaf now that Lemur_catta and the 3
#                        Eulemur fulvus-complex taxa were added -- 'branch' type below
#                        would now be wrong for this clade, needs 'clade' like the rest)
# Each pair's descendant leaf set matches the master table's Group column exactly
# (5+9+6+10 = 30, confirmed against ALL_TAXA above).
CLADE_LCA = [
    ('Hylobates_lar', 'Pan_troglodytes_ellioti', 'Apes'),
    ('Chlorocebus_sabaeus', 'Macaca_nigra', 'Old World Monkeys'),
    ('Plecturocebus_cupreus', 'Alouatta_caraya', 'New World Monkeys'),
    ('Daubentonia_madagascariensis', 'Eulemur_fulvus_collaris', 'Lemurs'),
]

# ---------- TREE_COLORS: branch color per clade + label color per leaf, one file ----------
data_lines = []
for leaf1, leaf2, name in CLADE_LCA:
    # 'clade' type needs an internal (LCA) node; kept the leaf1==leaf2 'branch' type
    # fallback (used previously, when Lemurs was a single leaf) in case a future
    # species change ever collapses a clade back down to one tip.
    if leaf1 == leaf2:
        data_lines.append(f"{leaf1} branch {CLADE_COLORS[name]} normal 1.3")
    else:
        data_lines.append(f"{leaf1}|{leaf2} clade {CLADE_COLORS[name]} normal 1.3")
for taxon in ALL_TAXA:
    data_lines.append(f"{taxon} label {CLADE_COLORS[taxon_group[taxon]]}")

out = """TREE_COLORS
#Colors both tree branches AND leaf labels by major clade (Apes/Old World Monkeys/New World Monkeys/
#Lemurs), matching Master_Comparison_Table.xlsx 'Group' column and the project-wide
#4-clade color scheme. TREE_COLORS is a first-class tree annotation (not a
#DATASET_* ring), so branch color and label color live in one file -- supersedes the
#earlier DATASET_STYLE branch-only file. No colored strip and no bracket (bracket
#labels were tried and dropped as too visually distracting).

SEPARATOR SPACE

DATA
""" + '\n'.join(data_lines) + '\n'

with open('/Users/lss0021/Documents/Primate_Maps/Figure_1/iTOL_datasets/clade_colors_tree.txt', 'w') as f:
    f.write(out)

print("Wrote clade_colors_tree.txt:", len(data_lines), "rows",
      f"({len(CLADE_LCA)} clade branch rows + {len(ALL_TAXA)} leaf label rows)")
