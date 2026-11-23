"""d65: print the planar developments found by d14_reality.py (reads d14_reality.json).
Run: python3 -B develop_planar.py
"""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import d14_reality as R
from hurwitz import plain_orbit, decode, cycles
from involution_flag import reflections, edge_maps, step, EDGES
rep = json.load(open(HERE / (sys.argv[1] if len(sys.argv) > 1 else 'd14_reality.json')))['orbits']
for o in rep:
    if 'planar' not in str(o['reflection_status']): continue
    t0 = tuple(tuple(g) for g in o['rep'])
    for which, tt0 in (('t', t0),):
        for enc in sorted(plain_orbit(tt0)):
            tt, _ = decode(enc, len(t0[0]), False)
            for phi in reflections(tt):
                if R.classify(tt, phi) != 'planar': continue
                E = edge_maps(tt); pos={0:(0,0)}; q=[0]
                for i in q:
                    for e in EDGES:
                        if E[e][i]==phi[i]: continue
                        j=phi[E[e][i]]
                        if j not in pos: pos[j]=step(pos[i],e); q.append(j)
                xs=[p[0] for p in pos.values()]; ys=[p[1] for p in pos.values()]
                print(o['order'], o['relations'], 'tuple', tt, 'phi', phi)
                for y in range(max(ys), min(ys)-1, -1):
                    print(''.join('#' if (x,y) in pos.values() else '.' for x in range(min(xs), max(xs)+1)))
                print('cells', sorted(pos.values()))
