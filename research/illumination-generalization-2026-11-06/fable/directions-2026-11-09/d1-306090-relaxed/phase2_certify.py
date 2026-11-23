"""Certify fold-family rooms (phase2-fold-*.json 'best' and 'others').

For each room Q = B u s1 B (u s2 B):
  1. check_room.analyze: simple polygon, walls, interior A points, transparent C points.
  2. Shooter: every ordered pair of interior A points, all A-lattice targets up to --bound.
  3. mirror_exact: the 12 mirror directions from S, decided exactly (any length).
  4. Fold conditions for the written proof (README, phase 2):
     a. B is C-clean; f(S), f(T) are A points of B.
     b. Copies meet only along their seam lines (checked when the room was built).
     c. Every non-corner point p of Q whose image is a corner of B lies in exactly
        two copies, each with a 90-degree angle there (seam-endpoint reversal).
"""
import json, sys, glob, itertools
from check_room import analyze, label
from phase2_shoot import find_paths, mirror_exact
from phase2_fold import refl

UNIT = {'A': 30, 'B': 60, 'C': 90}


def angles(tiles):
    cnt = {}
    for t in tiles:
        for p in t: cnt[p] = cnt.get(p, 0) + 1
    return {p: c * UNIT[label(p)] for p, c in cnt.items()}


def fold_conditions(rec, l1):
    base = [tuple(map(tuple, t)) for t in rec['base']]; d1 = (1, 0) if l1 == 'edge' else (0, 1)
    maps = [lambda q: q, lambda q: refl(q, (0, 0), d1)]
    if rec.get('l2'):
        T, d2 = tuple(rec['T']), tuple(rec['l2']); maps.append(lambda q, T=T, d2=d2: refl(q, T, d2))
    angB = angles(base)
    binfo, _ = analyze(base)
    bcorner = {tuple(c['p']) for c in binfo['corners']}
    cclean = all(a in (90, 270) for p, a in angB.items() if label(p) == 'C')
    Q = [tuple(map(tuple, t)) for t in rec['Q']]; angQ = angles(Q)
    qinfo, _ = analyze(Q); qcorner = {tuple(c['p']) for c in qinfo['corners']}
    bad = []; reversal_points = []
    for p, a in angQ.items():
        if p in qcorner: continue
        # copy k = g_k(B) with g_k an involution, so p lies in copy k iff g_k(p) is a vertex of B
        inside = [(k, g(p)) for k, g in enumerate(maps) if g(p) in angB]
        corner_images = [(k, q) for k, q in inside if q in bcorner]
        if not corner_images: continue
        if len(inside) == 2 and all(angB[q] == 90 for _, q in inside): reversal_points.append(p)
        else: bad.append(dict(p=p, copies=inside))
    return dict(base_walls=binfo['walls'], base_C_clean=cclean,
                fS_label=label((0, 0)), fT_label=label(tuple(rec['T'])),
                reversal_points=[list(p) for p in reversal_points], violations=bad, PASS=cclean and not bad)


def certify(rec, l1, bound):
    Q = [tuple(map(tuple, t)) for t in rec['Q']]
    info, corners = analyze(Q)
    pairs = {}
    for S, T in itertools.permutations([tuple(p) for p in info['interior_A']], 2):
        paths, shots = find_paths(S, T, corners, bound, 1)
        pairs[f'{list(S)}->{list(T)}'] = dict(lit=bool(paths), shots=shots,
                                              witness=[[str(c) for c in q] for q in paths[0]['path']] if paths else None)
    T = tuple(rec['T'])
    return dict(WQ=info['walls'], tiles=info['tiles'], interior_A=info['interior_A'], transparent_C=info['transparent_C'],
                angle_histogram=info['angle_histogram'], corners=info['corners'],
                pairs=pairs, mirror_S_to_T=mirror_exact((0, 0), T, corners), fold=fold_conditions(rec, l1))


if __name__ == '__main__':
    bound = int(sys.argv[1]) if len(sys.argv) > 1 else 40; wmax = int(sys.argv[2]) if len(sys.argv) > 2 else 99; out = {}
    jobs = []
    for f in sorted(glob.glob('phase2-fold-*.json')):
        r = json.load(open(f))
        jobs += [(f'{f}#{n}', rec, r['l1']) for n, rec in enumerate([r['best']] + r.get('others', []) if r.get('best') else [])]
    for f in sorted(glob.glob('phase2-fold2-T*.json')):  # direct F3 model: one room per file, l1 = x-axis
        r = json.load(open(f))
        if r.get('rec') and r['WQ'] <= wmax: jobs.append((f, r['rec'], 'edge'))
    for f, rec, l1 in jobs:
        c = certify(rec, l1, bound); out[f] = c
        print(f, c['WQ'], 'lit pairs:', sum(v['lit'] for v in c['pairs'].values()), '/', len(c['pairs']),
              'mirror:', sorted({m['result'] for m in c['mirror_S_to_T']}), 'fold:', c['fold']['PASS'], flush=True)
    json.dump(out, open('phase2-certify.json', 'w'), indent=1, default=str)
