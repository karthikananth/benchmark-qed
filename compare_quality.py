"""Compare LGR vs GRZ search quality."""
import json, re

with open(r'C:\Users\kaanan\Documents\AIFSP\Bookshelf\eval\benchmark-qed\lgr_search_result_run2.json', encoding='utf-8') as f:
    lgr = json.load(f)
with open(r'C:\Users\kaanan\Documents\AIFSP\Bookshelf\eval\benchmark-qed\grz_search_result_run3.json', encoding='utf-8') as f:
    grz = json.load(f)

lgr_text = lgr['text']
grz_text = grz['response']

# Section headers
lgr_sections = [l.strip() for l in lgr_text.split('\n') if l.strip().startswith('#')]
grz_sections = [l.strip() for l in grz_text.split('\n') if l.strip().startswith('#')]

print("=== LGR SECTIONS ===")
for s in lgr_sections: print(f"  {s}")
print(f"\n=== GRZ SECTIONS ===")
for s in grz_sections: print(f"  {s}")

# Key term frequency
terms = ['IC50', 'EC50', 'hERG', 'ATRA', 'ATO', 'OXS007417', 'autophagy', 'SAR',
         'solubility', 'permeability', 'metabolic stability', 'CD11b', 'PML', 'APL',
         'differentiation', 'potency', 'selectivity', 'ADMET', 'scaffold', 'tubulin']

print(f"\n{'=== KEY TERM FREQUENCY ===':}")
print(f"{'Term':<22} {'LGR':>5} {'GRZ':>5}  Winner")
print("-" * 45)
for t in terms:
    lc = lgr_text.lower().count(t.lower())
    gc = grz_text.lower().count(t.lower())
    winner = ""
    if lc > gc * 1.5 and lc > 1: winner = "LGR"
    elif gc > lc * 1.5 and gc > 1: winner = "GRZ"
    print(f"{t:<22} {lc:>5} {gc:>5}  {winner}")

# Quantitative data points
lgr_numbers = re.findall(r'\d+\.?\d*\s*(?:µM|nM|mg/kg|%)', lgr_text)
grz_numbers = re.findall(r'\d+\.?\d*\s*(?:µM|nM|mg/kg|%)', grz_text)
print(f"\n=== QUANTITATIVE DATA POINTS ===")
print(f"LGR: {len(lgr_numbers)} numeric values with units")
print(f"GRZ: {len(grz_numbers)} numeric values with units")
print(f"  LGR examples: {lgr_numbers[:8]}")
print(f"  GRZ examples: {grz_numbers[:8]}")

# Compounds mentioned
compounds = ['OXS007417', 'OXS000675', 'OXS008474', 'OXS008255', 'OXS007570',
             'OXS007002', 'JAG21', 'TH1579', 'valproic acid', 'VPA', 'lithium',
             'chloroquine', 'tranylcypromine', 'indazole']
print(f"\n=== SPECIFIC COMPOUNDS/AGENTS MENTIONED ===")
lgr_compounds = [c for c in compounds if c.lower() in lgr_text.lower()]
grz_compounds = [c for c in compounds if c.lower() in grz_text.lower()]
print(f"LGR ({len(lgr_compounds)}): {', '.join(lgr_compounds)}")
print(f"GRZ ({len(grz_compounds)}): {', '.join(grz_compounds)}")

# Data gaps acknowledgment
print(f"\n=== HONESTY / DATA GAPS ===")
lgr_gaps = lgr_text.lower().count("not provide") + lgr_text.lower().count("not present") + lgr_text.lower().count("not supported")
grz_gaps = grz_text.lower().count("not provide") + grz_text.lower().count("not present") + grz_text.lower().count("do not include") + grz_text.lower().count("cannot reproduce")
print(f"LGR gap acknowledgments: {lgr_gaps}")
print(f"GRZ gap acknowledgments: {grz_gaps}")

# Actionable design strategies
print(f"\n=== ACTIONABLE DESIGN STRATEGIES ===")
lgr_strategies = [l.strip() for l in lgr_text.split('\n') if 'Strategy' in l and l.strip().startswith('#')]
grz_strategies = [l.strip() for l in grz_text.split('\n') if 'strategy' in l.lower() or 'design' in l.lower() and l.strip().startswith('#')]
print(f"LGR named strategies: {len(lgr_strategies)}")
for s in lgr_strategies: print(f"  {s}")
grz_design = [l.strip() for l in grz_text.split('\n') if l.strip().startswith('#') and ('design' in l.lower() or 'strategy' in l.lower())]
print(f"GRZ design sections: {len(grz_design)}")
for s in grz_design: print(f"  {s}")
