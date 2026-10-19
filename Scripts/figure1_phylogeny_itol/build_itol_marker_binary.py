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

ALL_TAXA = ['Alouatta_caraya','Callithrix_jacchus','Cebuella_pygmaea','Cebus_capucinus',
    'Chlorocebus_sabaeus','Daubentonia_madagascariensis','Eulemur_fulvus',
    'Eulemur_fulvus_albocollaris','Eulemur_fulvus_collaris','Gorilla_gorilla_gorilla',
    'Hylobates_lar','Lemur_catta','Macaca_fuscata','Macaca_mulatta','Macaca_nemestrina',
    'Macaca_nigra','Mandrillus_sphinx','Miopithecus_talapoin','Nomascus_leucogenys',
    'Pan_paniscus','Pan_troglodytes_ellioti','Pan_troglodytes_verus','Papio_anubis',
    'Papio_hamadryas','Papio_papio','Plecturocebus_cupreus','Saguinus_oedipus',
    'Sapajus_cay','Sapajus_libidinosus','Sapajus_nigritus']

# Ordered by chronology of the underlying technology, oldest to newest --
# Chiasma count (classical cytology, pre-1990s) -> MLH1 foci
# (immunofluorescence cytology, late 1990s on) -> Microsatellite (linkage mapping,
# 1990s-2000s) -> Short-read WGS (Illumina-era pedigree/LD studies) -> Long-read WGS
# (PacBio/ONT haplotype-switching studies, most recent). Renamed from the central
# table's own 'WGS' / 'Haplotype switching' to make this chronology
# explicit in the label text itself.
MARKERS = ['Chiasma count', 'MLH1 foci', 'Microsatellite', 'Short-read WGS', 'Long-read WGS']

# Pulled from EVERY row in the central table regardless of metric, same "not tied to
# cM/Mb" approach used throughout this figure's datasets -- so e.g. Hylobates_lar/
# Macaca_nemestrina/Papio_papio (Porsborg long-read only, no cM/Mb or Gini) still get
# a marker here.
by_taxon_markers = {t: set() for t in ALL_TAXA}
for r in data_rows:
    species, marker = r[1], r[3]
    if species not in SPECIES_MAP or not marker:
        continue
    taxon = SPECIES_MAP[species]
    if marker in MARKERS:
        by_taxon_markers[taxon].add(marker)

missing = [t for t in ALL_TAXA if not by_taxon_markers[t]]
if missing:
    raise RuntimeError(f"No Marker Type value found for: {missing} -- these would need dropping")

# All black -- color was distracting and shape alone is
# sufficient to distinguish the 5 marker types.
MARKER_COLOR = {m: '#000000' for m in MARKERS}
MARKER_SHAPE = {
    'Chiasma count': '1',
    'MLH1 foci': '2',
    'Microsatellite': '3',
    'Short-read WGS': '4',
    'Long-read WGS': '5',
}

binary_lines = []
for taxon in ALL_TAXA:
    vals = ['1' if m in by_taxon_markers[taxon] else '-1' for m in MARKERS]
    binary_lines.append(f"{taxon}," + ','.join(vals))

out = f"""DATASET_BINARY
#Underlying MARKER TYPE per species (the central table's 'Marker Type' column, pulled
#from "Rate Estimates Summary.xlsx" > Species Survey sheet's 'Markers' column, plus
#the 9 species added via Dumont et al. 2017's cross-check) -- distinct from
#Method_binary.txt. Method describes the analytical approach (LD-based/pedigree/
#cytogenetic/testis); Marker Type describes the underlying raw data type it was built
#from (chiasma counts, MLH1 immunofluorescent foci, microsatellite loci, short-read
#WGS, or long-read haplotypes) -- e.g. both LD-based AND pedigree-based-WGS studies
#share the same Short-read WGS marker, decoupled here from which analytical method
#was applied to it. Ordered oldest-to-newest technology (see MARKERS comment above).
#Pulled from EVERY row in the central table (cM/Mb, Gini, and raw NCO/CO count rows
#alike), not just cM/Mb-relevant ones -- so this ring is deliberately NOT tied to
#Method_binary.txt's cM/Mb-scoped species coverage. All 30 current tree tips have >=1
#Marker Type value (confirmed by the build script) -- no species needs to be dropped.
#All black -- shape alone distinguishes marker type.
#1 = filled shape (present), -1 = omitted entirely (absent).
#SHOW_LABELS,1 displays the field labels (Chiasma count/MLH1 foci/Microsatellite/
#Short-read WGS/Long-read WGS) above the columns directly.

SEPARATOR COMMA

DATASET_LABEL,Marker type
COLOR,#000000

FIELD_SHAPES,{','.join(MARKER_SHAPE[m] for m in MARKERS)}
FIELD_LABELS,{','.join(MARKERS)}
FIELD_COLORS,{','.join(MARKER_COLOR[m] for m in MARKERS)}

DASHED_LINES,1
SHOW_LABELS,1

LEGEND_TITLE,Marker type
LEGEND_SHAPES,{','.join(MARKER_SHAPE[m] for m in MARKERS)}
LEGEND_COLORS,{','.join(MARKER_COLOR[m] for m in MARKERS)}
LEGEND_LABELS,{','.join(MARKERS)}

DATA
""" + '\n'.join(binary_lines) + '\n'

with open(os.path.join(ITOL_DIR, 'Marker_binary.txt'), 'w') as f:
    f.write(out)

print("Wrote Marker_binary.txt:", len(binary_lines), "species rows")
for t in ALL_TAXA:
    print(t, sorted(by_taxon_markers[t]))
