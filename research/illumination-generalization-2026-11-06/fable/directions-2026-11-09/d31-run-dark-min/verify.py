"""Verify the smallest glued rooms of found.json with two independent methods.

1. orbitc (d9, complete SL(2,Z)-orbit decider) on the pair.
2. The lattice-chain tracer of d30/mirror_check.py (its functions, loaded
   without running its P6 script part), all directions with |q|,|p| <= B.

usage: python3 verify.py WMAX B
"""
import sys, json, subprocess, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.dirname(HERE)
src = open(os.path.join(D, 'd30-rigidity-proof/mirror_check.py')).read()
ns = {}
exec(src[:src.index('ident = (lambda')], ns)
ORBITC = os.path.join(D, 'd9-census-w22/orbitc')

WMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 36
B = int(sys.argv[2]) if len(sys.argv) > 2 else 20


def orbitc(cells, S, T, cap=5_000_000):
    line = (f"{len(cells)} " + " ".join(f"{x} {y}" for x, y in sorted(cells))
            + f" | 2 {S[0]} {S[1]} {T[0]} {T[1]}")
    out = subprocess.run([ORBITC, str(cap)], input=line + "\n", capture_output=True,
                         text=True).stdout.split("\n")
    verdict = [ln.split()[-1] for ln in out[1:] if len(ln.split()) == 5]
    return out[0].strip(), verdict


rooms = [f for f in json.load(open(os.path.join(HERE, 'found.json'))) if f['W'] <= WMAX]
for f in rooms:
    cells = {tuple(c) for c in f['cells']}
    t, W, r = ns['stats'](cells)
    assert W == f['W']
    for S, T, pos in f['pairs'][:2]:
        S, T = tuple(S), tuple(T)
        assert t[S] == 'int' and t[T] == 'int'
        oc = orbitc(cells, S, T) if len(cells) <= 40 else ('area > 40', [])
        wit = ns['lit'](cells, t, S, T, B)
        print(f"W {W} r {r} area {len(cells)} d {f['d']} pair {S}-{T} run {pos}: "
              f"orbitc {oc[1]} [{oc[0]}]; trace |q|,|p|<={B}: {'no witness' if wit is None else wit}",
              flush=True)
