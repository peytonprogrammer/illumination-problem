"""D112 top priority: the L > 4d whole-room theorem for rectangular dumbbells.

Implements the note's monotone-jump construction literally and traces every
constructed path exactly on the full polygon (own tracer chamber.shoot_room, and
d110's geom.shoot as an independent cross-check).

Usage: python3 -B linear.py
"""
import sys, random
from fractions import Fraction as F
from pathlib import Path
from chamber import shoot_room, Irregular
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd110-review-length'))
sys.path.insert(0, str(HERE.parent / 'd109-check-dbas'))
from geom import room, shoot as shoot110
import path as P109
from room import cells as cells109


JUMPS = []


class Leg:
    """First-hit phase of one leg, in the ray's own tracing direction (note's f)."""

    def __init__(self, x, y, D, w):
        self.x, self.D, self.w = F(x), F(D), F(w)
        y = F(y)
        if y < 0:
            self.kind, self.h, self.eps = 'below', -y, 1
        elif y > w:
            self.kind, self.h, self.eps = 'above', y - w, -1
        else:
            self.kind, self.h, self.y = 'door', None, y
            self.eps = 1 if y <= w / 2 else -1

    def A(self, j):
        return self.x + 2 * self.D * j

    def index(self, s):
        """First j with s*A_j > h; None at a lip hit."""
        if self.kind == 'door':
            return 0
        j = max(0, int((self.h / s - self.x) / (2 * self.D)) - 1)
        while s * self.A(j) <= self.h:
            if s * self.A(j) == self.h:
                return None
            j += 1
        return j

    def affine(self, j):
        """f = c + s*A on the branch with index j."""
        if self.kind == 'door':
            return self.eps * self.y, self.x
        c = -self.h if self.kind == 'below' else -self.w - self.h
        return c, self.A(j)

    def f0(self):
        return {'below': F(0), 'above': -self.w, 'door': None}[self.kind] if self.kind != 'door' else self.eps * self.y

    def thresholds(self, s0, s1):
        if self.kind == 'door':
            return []
        out, j = [], 0
        while True:
            t = self.h / self.A(j)
            if t <= s0:
                break
            if t < s1:
                out.append(t)
            j += 1
        return out


def construct(L, w, l1, l2, d):
    """Return a root slope s of F = M on an open interval, following the note."""
    B = l1.f0() + l2.f0()
    M = (B // (2 * w) + 1) * (2 * w)          # smallest multiple of 2w strictly above B
    s1 = w / (2 * d) * F(999999, 1000000)
    s0 = (M - B) / (2 * (L + 4 * d))
    while l1.index(s0) is None or l2.index(s0) is None:
        s0 /= 2
    while l1.index(s1) is None or l2.index(s1) is None:
        s1 = (s1 + w / (2 * d)) / 2
    def Fv(s):
        c1, a1 = l1.affine(l1.index(s)); c2, a2 = l2.affine(l2.index(s))
        return L * s + c1 + a1 * s + c2 + a2 * s
    assert Fv(s0) < M < Fv(s1), (Fv(s0), M, Fv(s1))
    cuts = sorted(set([s0, s1] + l1.thresholds(s0, s1) + l2.thresholds(s0, s1)))
    gap = min(b - a for a, b in zip(cuts, cuts[1:])) / 4
    def branch_at(t, side):  # value at t of the affine branch just left/right of t
        u = t + side * gap
        c1, a1 = l1.affine(l1.index(u)); c2, a2 = l2.affine(l2.index(u))
        return L * t + c1 + a1 * t + c2 + a2 * t
    for t in cuts[1:-1]:  # right limit strictly below left limit at every threshold
        JUMPS.append(branch_at(t, 1) < branch_at(t, -1))
    jumps_down = 0
    for lo, hi in zip(cuts, cuts[1:]):
        mid = (lo + hi) / 2
        j1, j2 = l1.index(mid), l2.index(mid)
        c1, a1 = l1.affine(j1); c2, a2 = l2.affine(j2)
        slope = L + a1 + a2
        root = (M - c1 - c2) / slope
        if lo < root < hi:
            return root, M, len(cuts) - 2
    raise AssertionError("no root found on any open interval")


def velocity(leg, s, hx):
    return (F(hx), leg.eps * s)


def run_pair(name, L, S, T, R, xcheck=True):
    w, p = F(R['w']), F(R['p'])
    d1, d2 = F(R['d1']), F(R['d2'])
    d = max(d1, d2)
    lS = Leg(d1 - F(S[0]), F(S[1]) - p, d1, w)
    lT = Leg(F(T[0]) - (d1 + L), F(T[1]) - p, d2, w)
    s, M, nthr = construct(F(L), w, lS, lT, d)
    v = velocity(lS, s, 1)
    hits = shoot_room(R['V'], S, v, T)
    ok110 = True
    if xcheck:
        hits2 = shoot110(R['V'], S, v, T)
        ok110 = [q for _, q in hits2] == [q for _, q in hits]
    return s, M, nthr, len(hits), ok110


def lattice_pairs(R):
    L, d1, d2 = R['L'], R['d1'], R['d2']
    A = [(x, y) for x in range(1, d1) for y in range(R['b1'] + 1, R['b1'] + R['h1'])]
    B = [(d1 + L + x, y) for x in range(1, d2) for y in range(R['b2'] + 1, R['b2'] + R['h2'])]
    return [(a, b) for a in A for b in B]


def main():
    print("== the two DBas paths at L = 21 printed in the note ==")
    R = room('DBas', 21)
    S, T = (F(1), F(3)), (F(27), F(3))
    lS = Leg(4, 2, 5, 1); lT = Leg(1, 2, 4, 1)
    s = F(1, 13)
    print("indices", lS.index(s), lS.A(lS.index(s)), lT.index(s), lT.A(lT.index(s)))
    c1, a1 = lS.affine(lS.index(s)); c2, a2 = lT.affine(lT.index(s))
    print("F(1/13) =", 21 * s + c1 + a1 * s + c2 + a2 * s)
    for tag, v, tgt in (("S->T", (13, -1), T), ("S->(6,3/2)", (10, -3), (F(6), F(3, 2)))):
        h = shoot_room(R['V'], S, v, tgt)
        h110 = shoot110(R['V'], S, v, tgt)
        h109 = P109.shoot(cells109(21), S, (F(v[0]), F(v[1])), tgt, 10000)
        doors = []
        pts = [S] + [q for _, q in h] + [tgt]
        for a, b in zip(pts, pts[1:]):
            for X in (5, 26):
                if min(a[0], b[0]) < X < max(a[0], b[0]):
                    doors.append((X, a[1] + (X - a[0]) * (b[1] - a[1]) / (b[0] - a[0])))
        print(f"  {tag} v={v}: own {len(h)} hits, d110 {len(h110)}, d109 {len(h109)} events; door crossings {doors}")

    print("\n== constructed witnesses for all cross-chamber lattice pairs plus real pairs ==")
    rnd = random.Random(112)
    plan = [('DBas', 21), ('DB55', 21), ('DBw2', 21), ('DB55', 25), ('DB55', 30), ('DB55', 35),
            ('DBas', 22), ('DBw2', 40), ('DB55', 105)]
    for name, L in plan:
        R = room(name, L)
        pairs = lattice_pairs(R)
        # real marks: random rationals with large denominators, incl. near door lips
        for _ in range(40):
            a = (F(rnd.randrange(1, 1000 * R['d1']), 1000) + F(1, 7919),
                 R['b1'] + F(rnd.randrange(1, 1000 * R['h1']), 1000) + F(1, 7907))
            b = (R['d1'] + L + F(rnd.randrange(1, 1000 * R['d2']), 1000) + F(1, 7901),
                 R['b2'] + F(rnd.randrange(1, 1000 * R['h2']), 1000) + F(1, 7883))
            pairs.append((a, b))
        for lip in (R['p'], R['p'] + R['w']):  # marks 1/10007 off a lip level, both sides
            for e in (F(1, 10007), -F(1, 10007)):
                pairs.append(((F(R['d1']) - F(1, 9973), lip + e), (F(R['d1'] + L) + F(1, 9967), lip - e)))
        nok = n110 = 0; maxthr = 0; maxhits = 0
        for S, T in pairs:
            s, M, nthr, nh, ok = run_pair(name, L, S, T, R)
            nok += 1; n110 += ok
            maxthr = max(maxthr, nthr); maxhits = max(maxhits, nh)
        print(f"{name} L={L} (4d={4*max(R['d1'],R['d2'])}): {nok}/{len(pairs)} pairs reach T "
              f"(d110 tracer agrees on {n110}); max thresholds crossed {maxthr}, max wall hits {maxhits}")


def below_threshold():
    print("\n== outside the theorem: DB55 and DBas at L <= 4d (construction only, no claim) ==")
    for name in ('DB55', 'DBas'):
        fails = []
        for L in range(1, 21):
            R = room(name, L)
            bad = 0
            for S, T in lattice_pairs(R):
                try:
                    run_pair(name, L, S, T, R, xcheck=False)
                except AssertionError:
                    bad += 1
            fails.append((L, bad))
        print(name, "pairs where the construction has no start/end bracket or no root:", fails)


def chamber_to_corridor():
    print("\n== chamber mark to corridor point, every length (note's progression choice of A) ==")
    rnd = random.Random(7)
    for name in ('DBas', 'DB55', 'DBw2'):
        tot = ok = 0
        for L in (1, 2, 3, 5, 21):
            R = room(name, L)
            w, p, d1 = F(R['w']), F(R['p']), F(R['d1'])
            for _ in range(60):
                S = (F(rnd.randrange(1, 1000 * R["d1"]), 1000) + F(1, 7919),
                     R['b1'] + F(rnd.randrange(1, 1000 * R['h1']), 1000) + F(1, 7907))
                z = F(rnd.randrange(0, 1000 * L + 1), 1000)
                t = F(rnd.randrange(1, 1000 * R['w']), 1000) + F(1, 7901)
                Tpt = (d1 + z, p + t)
                y = S[1] - p; x = d1 - S[0]
                if 0 <= y <= w:
                    v = (Tpt[0] - S[0], Tpt[1] - S[1])
                else:
                    above = y > w
                    hh = y - w if above else -y
                    tt = w - t if above else t
                    lo = hh * z / tt; hi = lo + 2 * d1 * (1 + hh / tt)
                    j = 0
                    while x + 2 * d1 * j <= lo:
                        j += 1
                    A = x + 2 * d1 * j
                    assert A < hi
                    s = (hh + tt) / (A + z)
                    v = (F(1), -s if above else s)
                tot += 1
                try:
                    shoot_room(R['V'], S, v, Tpt); ok += 1
                except Irregular as e:
                    print("  FAIL", name, L, S, Tpt, e)
        print(f"  {name}: {ok}/{tot} chamber-to-corridor pairs reach the target (L in 1,2,3,5,21)")


if __name__ == '__main__':
    main()
    print(f"\nthresholds checked: {len(JUMPS)}, all downward: {all(JUMPS)}")
    chamber_to_corridor()
    below_threshold()
