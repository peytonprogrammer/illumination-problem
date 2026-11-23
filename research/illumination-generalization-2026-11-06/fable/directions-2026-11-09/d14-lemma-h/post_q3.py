"""Counts from post_summary.json split by q = 2 and q >= 3 (Lemma H is vacuous at q = 2).

Run: python3 -B post_q3.py   (after post.py)
"""
import json
from collections import Counter
from math import factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
d = json.loads((HERE / 'post_summary.json').read_text())
tot = Counter()
for n, recs in sorted(d.items(), key=lambda kv: int(kv[0])):
    for fam in ('AN', 'PRIM'):
        rs = [r for r in recs if fam in r['fam']]
        for lab, sel in (('q=2', [r for r in rs if r['q'] == 2]), ('q>=3', [r for r in rs if r['q'] >= 3])):
            c = Counter()
            c['orbits'] = len(sel)
            c['M transitive'] = sum(r['M_orb'][0] == 1 for r in sel)
            c['M primitive'] = sum(r['M_prim'] for r in sel)
            c['M 2-homogeneous'] = sum(r['M_orb'][1] == 1 for r in sel)
            c['M = S_q'] = sum(r['M'] == factorial(r['q']) for r in sel)
            c['M has transposition or 3-cycle'] = sum(r['M_small'] for r in sel)
            c['Nbar = 1'] = sum(r['Nbar'] == 1 for r in sel)
            c['Nbar transitive'] = sum(r['Nbar_orb'][0] == 1 for r in sel)
            c['Nbar 2-homogeneous'] = sum(r['Nbar_orb'][1] == 1 for r in sel)
            c['Nbar = M'] = sum(r['Nbar'] == r['M'] for r in sel)
            c['transposition graph of Nbar connected'] = sum(r['tgraph'] for r in sel)
            c['single cusp loop is a transposition or 3-cycle'] = sum(r['single'] for r in sel)
            c['genus 0'] = sum(r['genus'] == 0 for r in sel)
            c['some state has a link'] = sum(r['link_any'] > 0 for r in sel)
            c['base state has a link'] = sum(r['base_link'] for r in sel)
            print(n, fam, lab, dict(c))
            for k, v in c.items():
                tot[(fam, lab, k)] += v
print('TOTAL n = 4..10')
for k, v in tot.items():
    print('  ', k, v)
