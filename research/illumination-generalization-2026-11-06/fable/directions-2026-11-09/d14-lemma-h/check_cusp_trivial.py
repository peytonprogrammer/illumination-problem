"""Independent check of the cusp-trivial orbits.

For an orbit, build the fully marked orbit (every regular a-point labelled) and the plain
orbit, and compare the cycle lengths of the three parabolic words
    T_b = s0^2,   T_d = s1^2,   T_bd = s0^2 s1^2   (conjugate to T_c^-1 in PMod(S_{0,4}))
on marked states and on their plain images.  All cusp loops act trivially on the regular
a-points exactly when every marked cycle has the length of its plain image (deck group
trivial).  The script also reports the number of marked states per plain state, which is
|M_t| when the deck group is trivial.  It does not use cusp.py.
"""
import json, sys
from collections import deque
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd6-hurwitz-census'))
from hurwitz import pure_move, canon_marked, canon_plain, initial_pt

LABELS = ('a', 'b', 'c', 'd')
WORDS = {'T_b': [(0, 1)], 'T_d': [(1, 1)], 'T_bd': [(0, 1), (1, 1)]}


def run(rep):
    t0 = tuple(tuple(g) for g in rep)
    n = len(t0[0])
    cid, plen = initial_pt(t0[0])
    pt0 = tuple(c if plen[c] == 2 else -1 for c in cid)
    root = min(c for c in cid if plen[c] == 2)

    def cm(t, pt):
        return canon_marked(t, pt, [i for i in range(n) if pt[i] == root])

    seen = {cm(t0, pt0): (t0, pt0)}
    dq = deque([(t0, pt0)])
    while dq:
        t, pt = dq.popleft()
        for (i, s) in ((0, 1), (0, -1), (1, 1), (1, -1)):
            t2, _, p2 = pure_move(t, LABELS, pt, i, s)
            c = cm(t2, p2)
            if c not in seen:
                seen[c] = (t2, p2)
                dq.append((t2, p2))
    plain = {canon_plain(t) for t, _ in seen.values()}
    out = {'marked': len(seen), 'plain': len(plain)}
    for name, word in WORDS.items():
        trivial = True
        for c0, (t, pt) in seen.items():
            p0 = canon_plain(t)
            lm = lp = None
            k = 0
            while lm is None:
                for (i, s) in word:
                    t, _, pt = pure_move(t, LABELS, pt, i, s)
                k += 1
                if lp is None and canon_plain(t) == p0:
                    lp = k
                if cm(t, pt) == c0:
                    lm = k
            if lm != lp:
                trivial = False
        out[name] = trivial
    return out


if __name__ == '__main__':
    reps = {
        'n5 a[2,2,1] b[2,2,1] c[3,1,1] d[3,1,1]': None,
        'n7 a[2,2,2,1] b[2,2,2,1] c[3,2,1,1] d[3,2,1,1]': None,
    }
    want = {5: [[2, 2, 1], [2, 2, 1], [3, 1, 1], [3, 1, 1]],
            7: [[2, 2, 2, 1], [2, 2, 2, 1], [3, 2, 1, 1], [3, 2, 1, 1]],
            8: [[3, 2, 2, 1], [2, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 2]]}
    for n, cts in want.items():
        d = json.loads((HERE / f'cusp_n{n}.json').read_text())
        for o in d['orbits']:
            if o['cts'] == cts and o['contains_An']:
                print(n, cts, 'plain', o['plain'], 'cusp.py: |N|', o['N_order'], '|M|', o['M_order'],
                      '->', run(o['rep']))
