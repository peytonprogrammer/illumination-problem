import sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd6-hurwitz-census'))
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
import d4_monodromy as d4
import unified_test as UT
for n in [int(a) for a in sys.argv[1:]]:
    d=json.load(open(HERE/f'mine_n{n}.json'))
    for o in d['orbits']:
        t=tuple(tuple(g) for g in o['rep'])
        for xi in range(3):
            exc=[p for p in o['pairs'] if not p['lit_x'][xi] and not p['cert_x'][xi]]
            if not exc: continue
            parts=[p for p in d4.all_block_systems(list(t),n)]
            pil=[len(p) for p in parts if 1<len(p)<n and UT.is_pillowcase(UT.Factor(t,p))]
            print(n,'cts',o['cts'],'x=','bcd'[xi],'|G|',o['order'],'prim',o['primitive'],'pillow factors (blocks):',pil,
                  'plain',o['plain'],'marked',o['marked'],'q',o['q'],
                  'exc pairs',[(p['P'],p['Q'],'LIT' if p['lit'] else 'DARK',p['lit_x'],p['same_fibre_x'][xi]) for p in exc])
