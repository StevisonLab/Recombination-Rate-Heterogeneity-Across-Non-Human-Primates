#!/usr/bin/env python3
"""
Reproduces the two PRDM9-related Gini hypothesis tests described in
PRDM9_ZF_vs_Gini_Hypothesis_Test.txt and
Joseph2024_DefaultHotspots_vs_Gini_Hypothesis_Test.txt. Both are simple
Pearson correlations against this review's own Gini values; the data below
is transcribed directly from those two notes so the reported r/p values can
be checked independently. Requires scipy.
"""
from scipy.stats import pearsonr

# ---------------------------------------------------------------------------
# Hypothesis 1: PRDM9 zinc-finger array size vs. Gini
# ---------------------------------------------------------------------------
zf_gini_data = [
    # (species, ZF count, Gini, estimator)
    ("Chlorocebus sabaeus", 7.00, 0.9523, "LDhat"),
    ("Macaca mulatta", 8.00, 0.7944, "LDhat"),
    ("Nomascus leucogenys", 8.00, 0.8441, "LDhat"),
    ("Gorilla gorilla gorilla", 11.60, 0.8119, "LDhat"),
    ("Pan paniscus", 7.25, 0.8128, "LDhat"),
    ("Pan troglodytes", 15.56, 0.8210, "LDhat"),
    ("Callithrix jacchus", 10.00, 0.8068, "LDhat"),
    ("Papio anubis", 9.00, 0.7511, "pyrho"),
    ("Daubentonia madagascariensis", 7.00, 0.4509, "pyrho"),
]

print("=" * 70)
print("HYPOTHESIS 1: PRDM9 zinc-finger array size vs. Gini")
print("=" * 70)

zf_all = [(row[1], row[2]) for row in zf_gini_data]
r, p = pearsonr([x[0] for x in zf_all], [x[1] for x in zf_all])
print(f"All {len(zf_all)} species:          r = {r:.3f}  p = {p:.3f}")

zf_ldhat = [(row[1], row[2]) for row in zf_gini_data if row[3] == "LDhat"]
r, p = pearsonr([x[0] for x in zf_ldhat], [x[1] for x in zf_ldhat])
print(f"LDhat-only ({len(zf_ldhat)} species):     r = {r:.3f}  p = {p:.3f}")

# ---------------------------------------------------------------------------
# Hypothesis 2: Joseph et al. 2024 relrechot_KO (default-hotspot activity)
# vs. Gini
# ---------------------------------------------------------------------------
joseph_gini_data = [
    # (species, relrechot_KO, Gini, is_congener_substitution)
    ("Callithrix jacchus", 1.102, 0.8068, False),
    ("Macaca fascicularis (-> M. mulatta)", 1.193, 0.7944, True),
    ("Pan troglodytes", 1.210, 0.8210, False),
    ("Chlorocebus sabaeus", 1.422, 0.9523, False),
]

print()
print("=" * 70)
print("HYPOTHESIS 2: Joseph et al. 2024 default-hotspot activity vs. Gini")
print("=" * 70)

joseph_all = [(row[1], row[2]) for row in joseph_gini_data]
r, p = pearsonr([x[0] for x in joseph_all], [x[1] for x in joseph_all])
print(f"All {len(joseph_all)} species:          r = {r:.3f}  p = {p:.3f}")

joseph_exact = [(row[1], row[2]) for row in joseph_gini_data if not row[3]]
r, p = pearsonr([x[0] for x in joseph_exact], [x[1] for x in joseph_exact])
print(f"Exact species matches ({len(joseph_exact)}):  r = {r:.3f}  p = {p:.3f}")
