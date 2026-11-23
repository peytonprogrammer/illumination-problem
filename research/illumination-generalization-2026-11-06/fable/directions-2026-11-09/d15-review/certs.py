"""Cross-check of every r <= 2 certificate of d15-small-r/lemmas.py.

For each order type and each pair of position types:
1. Ask the author's certify_pair for its certificate.
2. Build a representative room (unit gaps) and representative points.
3. Find, with the review code rv.py, every lemma instance whose hypotheses
   hold. The review code is written from the lemma statements.
4. Require that the author's certificate names an instance the review code
   also finds (same lemma, same door, same flat end, same roles).
5. Trace the prescribed paths of every instance.

Usage: python3 -B certs.py [dump]
"""
import os
import random
import sys
from collections import Counter
from fractions import Fraction as Fr

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
AUTH = os.path.join(HERE, "..", "d15-small-r")
sys.path.insert(0, AUTH)
sys.path.insert(0, HERE)
import lemmas as AL            # noqa: E402  (author's code, read only)
import rv                      # noqa: E402

Q = rv.field(2)


def show(ot):
    return "/".join("".join("#" if ot.ins(i, j) else "." for i in range(ot.nx)) for j in reversed(range(ot.ny)))


def auth_key(c, R):
    co = R.coord
    lem = c['lem']
    if lem == 'A':
        return ('A',)
    if lem == 'A2':
        ax, i = c['r2']
        return ('A2', ax, co[ax][i])
    if lem == 'B':
        ax, ci, ei = c['p2']
        ay, d = c['cons'][0][0], c['cons'][0][1]
        return ('B', c['swap'], ax, co[ax][ci], co[ax][ei], co[ay][d])
    if lem == 'B2':
        al, F, E = c['p2']
        perp, opp = c['r2']
        dp = c['cons'][0][2]
        return ('B2', c['swap'], al, co[al][F], co[al][E], co[perp][opp], co[perp][dp])
    if lem == 'C':
        al1, F1, E1 = c['p1']
        al2, F2, E2 = c['p2']
        c1, c2 = c['cons']
        d1 = co[c1[0]][c1[1]]
        if c['form'] == 'same':
            perp, opp = c['r2']
            d2 = co[c2[0]][c2[2]]
            oppv = co[perp][opp]
        else:
            d2 = co[c2[0]][c2[1]]
            oppv = None
        return ('C', c['form'], (al1, co[al1][F1], co[al1][E1], d1), (al2, co[al2][F2], co[al2][E2], d2), oppv)
    if lem == 'D':
        return ('D',)
    raise ValueError(lem)


def rep(X, frac):
    """Representative value for a doubled coordinate in a unit-gap room."""
    return Q(X // 2) if X % 2 == 0 else Q(Fr(X // 2) + frac)


def main():
    dump = len(sys.argv) > 1
    rng = random.Random(1)
    tot = Counter()
    problems = []
    for r in (0, 1, 2):
        for line in open(os.path.join(AUTH, f"types_r{r}.txt")):
            nx, ny, W, mask = map(int, line.split())
            ot = AL.OT.from_mask(nx, ny, mask)
            R = rv.Room(nx, ny, ot.cells, [Q(i) for i in range(nx + 1)], [Q(j) for j in range(ny + 1)])
            assert len(R.vertices()) == W == len(R.walls())
            pts = ot.interior_types()
            cache = {P: AL.arm_objects(ot, P) for P in pts}
            cnt = Counter()
            for a in range(len(pts)):
                for b in range(a, len(pts)):
                    St, Tt = pts[a], pts[b]
                    if St == Tt:
                        if St[0] % 2 == 0 and St[1] % 2 == 0:
                            continue
                        c = dict(lem='A', swap=0)
                        S = (rep(St[0], Fr(1, 3)), rep(St[1], Fr(2, 5)))
                        T = (rep(Tt[0], Fr(3, 4)), rep(Tt[1], Fr(4, 7)))
                    else:
                        c = AL.certify_pair(ot, St, Tt, cache)
                        # generic representatives: different fractions for S and T
                        S = (rep(St[0], Fr(1, 3)), rep(St[1], Fr(2, 5)))
                        T = (rep(Tt[0], Fr(3, 7)), rep(Tt[1], Fr(5, 11)))
                    assert R.pt(S)[2:] == St and R.pt(T)[2:] == Tt
                    assert R.interior(S) and R.interior(T)
                    if c is None:
                        problems.append((show(ot), St, Tt, 'author has no certificate'))
                        continue
                    ak = auth_key(c, R)
                    name = c['lem'] + ('-' + c['form'] if 'form' in c else '')
                    cnt[name] += 1
                    tot[name] += 1
                    insts = rv.all_instances(R, S, T, rng)
                    keys = [i['key'] for i in insts]
                    if ak not in keys:
                        problems.append((show(ot), St, Tt, 'author certificate not confirmed', ak,
                                         sorted({k[0] for k in keys if k})))
                    for inst in insts:
                        v, det = rv.evaluate(R, inst, rng)
                        tot['instances traced ' + inst['lem']] += 1
                        if v != 'ok':
                            problems.append((show(ot), St, Tt, 'path failure', inst['key'], v, det))
                    if dump:
                        mine = sorted({(i['lem'] + ('-' + i['form'] if 'form' in i else '')) for i in insts})
                        print(f"{show(ot):14s} S{St} T{Tt} author={name:7s} key={ak} mine={mine}")
            print(f"r={r} {nx}x{ny} {show(ot):14s} pairs {sum(cnt.values())} {dict(cnt)}")
    print("totals", dict(tot))
    print("problems", len(problems))
    for p in problems:
        print("  ", p)


if __name__ == "__main__":
    main()
