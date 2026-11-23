"""D140 checks for half-turn-fibers snapshot. Own code, exact integer arithmetic.

Square-tiled surface: squares 0..n-1, h = right neighbour, v = top neighbour.
Half-lattice points: C(i) centre, R(i) midpoint of right edge of i, T(i) midpoint
of top edge of i, vertices = union-find classes of corners (i, 'BL'|'BR'|'TL'|'TR').
Run: python3 -B checks.py > checks.log
"""
import os, subprocess, sys
from math import gcd

def inv(p):
    q = [0] * len(p)
    for i, x in enumerate(p):
        q[x] = i
    return q

def comp(a, b):  # a after b
    return [a[b[i]] for i in range(len(b))]

def cycles(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i not in seen:
            c, j = [], i
            while j not in seen:
                seen.add(j); c.append(j); j = p[j]
            out.append(tuple(c))
    return out

class Surf:
    def __init__(self, h, v):
        self.n = n = len(h)
        self.h, self.v, self.hi, self.vi = h, v, inv(h), inv(v)
        par = {}
        def f(x):
            par.setdefault(x, x)
            while par[x] != x:
                par[x] = par[par[x]]; x = par[x]
            return x
        def u(a, b):
            par[f(a)] = f(b)
        for i in range(n):
            u((i, 'BR'), (h[i], 'BL')); u((i, 'TR'), (h[i], 'TL'))
            u((i, 'TL'), (v[i], 'BL')); u((i, 'TR'), (v[i], 'BR'))
        self.vc = {}
        roots = {}
        for i in range(n):
            for c in ('BL', 'BR', 'TL', 'TR'):
                r = f((i, c)); roots.setdefault(r, len(roots)); self.vc[(i, c)] = roots[r]
        self.nv = len(roots)
        cnt = [0] * self.nv
        for k in self.vc.values():
            cnt[k] += 1
        self.angle = [c // 4 for c in cnt]  # cone angle in units of 2*pi
        self.genus = (2 - (self.nv - n)) // 2

    def connected(self):
        seen, st = {0}, [0]
        while st:
            i = st.pop()
            for j in (self.h[i], self.v[i], self.hi[i], self.vi[i]):
                if j not in seen:
                    seen.add(j); st.append(j)
        return len(seen) == self.n

    def period_index(self):
        """Index of the absolute period lattice in Z^2 (0 if rank < 2)."""
        pos = {0: (0, 0)}; st = [0]; vecs = []
        while st:
            i = st.pop()
            for j, d in ((self.h[i], (1, 0)), (self.v[i], (0, 1))):
                q = (pos[i][0] + d[0], pos[i][1] + d[1])
                if j not in pos:
                    pos[j] = q; st.append(j)
                else:
                    vecs.append((q[0] - pos[j][0], q[1] - pos[j][1]))
        for i in range(self.n):  # include edges seen from the other side
            for j, d in ((self.h[i], (1, 0)), (self.v[i], (0, 1))):
                vecs.append((pos[i][0] + d[0] - pos[j][0], pos[i][1] + d[1] - pos[j][1]))
        g = 0
        for a in vecs:
            for b in vecs:
                g = gcd(g, abs(a[0] * b[1] - a[1] * b[0]))
        return g

    def trace(self, start, a, b, bad):
        """Straight segment from centre of `start` with displacement (a,b) in Z^2.
        bad(kind, idx) -> True if forbidden. Cone points are always illegal.
        Returns (end_square, first_illegal or None, midpoint_label)."""
        h, v, hi, vi = self.h, self.v, self.hi, self.vi
        A, B = abs(a), abs(b); sa = (a > 0) - (a < 0); sb = (b > 0) - (b < 0)
        c = start; i = j = 1; hit = None; mid = None
        # doubled coords X = 1 + 2 a u, events u = i/(2A) and j/(2B)
        while True:
            ti = (i, 2 * A) if A and i <= 2 * A else None
            tj = (j, 2 * B) if B and j <= 2 * B else None
            if ti is None and tj is None:
                break
            if ti and tj:
                cmpv = i * 2 * B - j * 2 * A
            else:
                cmpv = -1 if ti else 1
            xi = cmpv <= 0; yj = cmpv >= 0
            if xi and yj and i == 2 * A and j == 2 * B:
                break  # endpoint u = 1
            if xi and not tj and i == 2 * A:
                break
            if yj and not ti and j == 2 * B:
                break
            X = 1 + sa * i if xi else None
            Y = 1 + sb * j if yj else None
            if not B:
                Y = 1
            if not A:
                X = 1
            is_mid = (xi and A and 2 * i == 2 * A) or (yj and B and 2 * j == 2 * B)
            if X is not None and Y is not None:
                xe, ye = X % 2 == 0, Y % 2 == 0
                if not xe and not ye:
                    lab = ('C', c)
                elif xe and not ye:
                    lab = ('R', c) if sa > 0 else ('R', hi[c])
                elif ye and not xe:
                    lab = ('T', c) if sb > 0 else ('T', vi[c])
                else:
                    corner = ('T' if sb > 0 else 'B') + ('R' if sa > 0 else 'L')
                    lab = ('V', self.vc[(c, corner)])
                if is_mid and mid is None:
                    mid = lab
                if hit is None and (bad(*lab) or (lab[0] == 'V' and self.angle[lab[1]] != 1)):
                    hit = lab
            elif is_mid and mid is None:
                mid = ('generic', None)
            # update square on grid-line crossings
            if xi and A and (1 + sa * i) % 2 == 0 and yj and B and (1 + sb * j) % 2 == 0:
                if self.angle[self.vc[(c, ('T' if sb > 0 else 'B') + ('R' if sa > 0 else 'L'))]] != 1:
                    return None, hit, mid  # through a cone point: no continuation
                c1 = (v if sb > 0 else vi)[(h if sa > 0 else hi)[c]]
                c2 = (h if sa > 0 else hi)[(v if sb > 0 else vi)[c]]
                assert c1 == c2
                c = c1
            else:
                if xi and A and (1 + sa * i) % 2 == 0:
                    c = h[c] if sa > 0 else hi[c]
                if yj and B and (1 + sb * j) % 2 == 0:
                    c = v[c] if sb > 0 else vi[c]
            if xi: i += 1
            if yj: j += 1
        return c, hit, mid

def base(p):
    h = [(i + 1) % p for i in range(p)]
    v = list(range(p)); v[0], v[1] = 1, 0
    return h, v

def conj_solutions(h, v, th, tv):
    """All sigma with sigma h sigma^-1 = th and sigma v sigma^-1 = tv (sigma fixed by sigma(0), h transitive cycle)."""
    n = len(h); out = []
    for s0 in range(n):
        s = [None] * n; s[0] = s0; i = 0
        for _ in range(n - 1):
            s[h[i]] = th[s[i]]; i = h[i]
        if sorted(s) == list(range(n)) and comp(s, v) == comp(tv, s) and comp(s, h) == comp(th, s):
            out.append(s)
    return out

def point_maps(S, sig, kind):
    """Image map on half-lattice points for an automorphism permuting squares by sig.
    kind: 'rot' derivative -I, 'rx' diag(-1,1), 'ry' diag(1,-1)."""
    hi, vi = S.hi, S.vi
    cm = {'rot': {'BL': 'TR', 'BR': 'TL', 'TL': 'BR', 'TR': 'BL'},
          'rx': {'BL': 'BR', 'BR': 'BL', 'TL': 'TR', 'TR': 'TL'},
          'ry': {'BL': 'TL', 'TL': 'BL', 'BR': 'TR', 'TR': 'BR'}}[kind]
    def m(kd, i):
        if kd == 'C': return ('C', sig[i])
        if kd == 'R': return ('R', hi[sig[i]]) if kind in ('rot', 'rx') else ('R', sig[i])
        if kd == 'T': return ('T', vi[sig[i]]) if kind in ('rot', 'ry') else ('T', sig[i])
        # vertex: pick a representative corner
        for (sq, cn), k in S.vc.items():
            if k == i:
                return ('V', S.vc[(sig[sq], cm[cn])])
    return m

def all_points(S):
    pts = [('C', i) for i in range(S.n)] + [('R', i) for i in range(S.n)] + [('T', i) for i in range(S.n)]
    return pts + [('V', k) for k in range(S.nv)]

def block_systems(gens, n):
    def minimal(j):
        par = list(range(n))
        def f(x):
            while par[x] != x:
                par[x] = par[par[x]]; x = par[x]
            return x
        par[f(j)] = f(0); queue = [(0, j)]
        while queue:
            a, b = queue.pop()
            for g in gens:
                ra, rb = f(g[a]), f(g[b])
                if ra != rb:
                    par[ra] = rb; queue.append((g[a], g[b]))
        return tuple(f(x) for x in range(n))
    def canon(lab):
        m = {}; return tuple(m.setdefault(x, len(m)) for x in lab)
    systems = {canon(minimal(j)) for j in range(1, n)}
    changed = True
    while changed:
        changed = False
        for s in list(systems):
            for t in list(systems):
                par = list(range(n))
                def f(x):
                    while par[x] != x:
                        par[x] = par[par[x]]; x = par[x]
                    return x
                for lab in (s, t):
                    first = {}
                    for x, l in enumerate(lab):
                        if l in first: par[f(x)] = f(first[l])
                        else: first[l] = x
                j = canon(tuple(f(x) for x in range(n)))
                if j not in systems:
                    systems.add(j); changed = True
    return sorted(systems, key=lambda s: -len(set(s)))

def darkness(S, srcs, tgts, bad, N):
    """Enumerate all integer displacements with max(|a|,|b|) <= N from each source centre."""
    tg = set(tgts); legal_to_tgt = 0; to_tgt = 0; mid_bad = 0; legal_other = set(); nseg = 0
    for s in srcs:
        for a in range(-N, N + 1):
            for b in range(-N, N + 1):
                if a == 0 and b == 0: continue
                end, hit, mid = S.trace(s, a, b, bad)
                nseg += 1
                if end is None:
                    continue
                if end in tg:
                    to_tgt += 1
                    if hit is None: legal_to_tgt += 1
                    if mid is not None and mid[0] != 'generic' and bad(*mid): mid_bad += 1
                elif hit is None and not bad('C', end):
                    legal_other.add((s, end))
    return nseg, to_tgt, legal_to_tgt, mid_bad, len(legal_other)

def slow_trace(S, s, a, b, bad):
    """Independent cross-check: sample every multiple of 1/(4AB) with Fractions."""
    from fractions import Fraction as Fr
    A, B = abs(a), abs(b); D = 4 * max(A, 1) * max(B, 1); c = s; hit = None
    for k in range(1, D + 1):
        u = Fr(k, D); x = Fr(1, 2) + a * u; y = Fr(1, 2) + b * u
        cx, cy = x.denominator == 1, y.denominator == 1
        if k < D and (2 * x).denominator == 1 and (2 * y).denominator == 1:
            if not cx and not cy: lab = ('C', c)
            elif cx and not cy: lab = ('R', c) if a > 0 else ('R', S.hi[c])
            elif cy and not cx: lab = ('T', c) if b > 0 else ('T', S.vi[c])
            else: lab = ('V', S.vc[(c, ('T' if b > 0 else 'B') + ('R' if a > 0 else 'L'))])
            cone = lab[0] == 'V' and S.angle[lab[1]] != 1
            if hit is None and (bad(*lab) or cone): hit = lab
            if cone: return None, hit
        if cx and cy: c = (S.v if b > 0 else S.vi)[(S.h if a > 0 else S.hi)[c]]
        elif cx: c = (S.h if a > 0 else S.hi)[c]
        elif cy: c = (S.v if b > 0 else S.vi)[c]
    return c, hit

def main():
    print("== Part A: genus-2 prime-degree examples ==")
    for p, N in ((7, 60), (11, 50)):
        h, v = base(p); S = Surf(h, v)
        comm = comp(comp(S.vi, S.hi), comp(v, h))
        print(f"\np={p}: h=(0 1 ... {p-1}), v=(0 1)")
        print(" connected:", S.connected(), " genus:", S.genus, " cone angles (2pi units) by vertex:", S.angle)
        print(" commutator v^-1 h^-1 v h nontrivial cycles:", [c for c in cycles(comm) if len(c) > 1])
        ok = True; x = v
        for k in range(p - 1):  # h^k v h^-k = (k, k+1)
            t = list(range(p)); t[k], t[k + 1] = k + 1, k
            ok &= (x == t); x = comp(comp(h, x), S.hi)
        print(" h^k v h^-k = (k k+1) for k=0..p-2 (so group = S_p):", ok)
        print(" absolute period lattice index in Z^2:", S.period_index())
        sig = conj_solutions(h, v, S.hi, S.vi)
        print(" sigma with sigma h sigma^-1 = h^-1, sigma v sigma^-1 = v^-1:", sig)
        sig = sig[0]; print(" sigma^2 = id:", comp(sig, sig) == list(range(p)))
        iota = point_maps(S, sig, 'rot')
        fixed = [q for q in all_points(S) if iota(*q) == q]
        zero = [k for k in range(S.nv) if S.angle[k] != 1]
        print(" iota-fixed half-lattice points:", fixed, " count:", len(fixed), " zero vertex:", zero)
        print(" RH quotient genus: 2g-2 = 2(2g'-2)+#fix ->", (2 * S.genus - 2 - len(fixed)) // 4 + 1)
        # check iota is an involution on all points
        print(" iota involutive on half-lattice points:", all(iota(*iota(*q)) == q for q in all_points(S)))
        # reflections
        rx = conj_solutions(h, v, S.hi, v); ry = [t for t in [list(range(p))] if comp(t, v) == comp(S.vi, t)]
        print(" reflection square maps: r_x candidates", rx, " r_y = identity valid:", bool(ry))
        RX = point_maps(S, rx[0], 'rx'); RY = point_maps(S, list(range(p)), 'ry')
        for q in fixed:
            print(f"   fixed {q}: fixed by r_x {RX(*q)==q}, by r_y {RY(*q)==q}")
        interior = [q for q in fixed if RX(*q) != q and RY(*q) != q]
        print(" iota-fixed points on no mirror (interior pi-cone points of X/D2):", interior)
        F = set(fixed)
        bad = lambda kd, i: (kd, i) in F
        srcs = [i for i in range(p) if sig[i] != i]
        mism = sum(S.trace(s, a, b, bad)[:2] != slow_trace(S, s, a, b, bad)
                   for s in range(p) for a in range(-8, 9) for b in range(-8, 9) if a or b)
        print(" fast vs independent slow tracer, all starts, |a|,|b|<=8: mismatches", mism)
        for s in srcs:
            nseg, to_t, legal, midbad, other = darkness(S, [s], [sig[s]], bad, N)
            print(f"  x=C({s}) y=C({sig[s]}): segments {nseg}, reach y {to_t}, legal to y {legal},"
                  f" midpoint forbidden {midbad}, legal (x,other centre) pairs {other}")

    print("\n== Part B: degree-8p genus-9 cyclic cover (p=7) ==")
    for p, N in ((7, 30),):
        h, v = base(p); S = Surf(h, v); n = 8 * p
        sig = conj_solutions(h, v, S.hi, S.vi)[0]
        iota = point_maps(S, sig, 'rot'); F = {q for q in all_points(S) if iota(*q) == q}
        # chi = algebraic intersection with the closed vertical edge on the left of square 2
        a = [0] * p; a[S.hi[2]] = 1
        H = [0] * n; V = [0] * n
        for k in range(8):
            for i in range(p):
                H[i + p * k] = h[i] + p * ((k + a[i]) % 8)
                V[i + p * k] = v[i] + p * k
        T = Surf(H, V)
        print(f"p={p}: degree {n}, connected {T.connected()}, genus {T.genus}, cone angles {sorted(T.angle, reverse=True)[:10]}...")
        print(" lifts of zero:", sum(1 for x in T.angle if x == 3), " period lattice index:", T.period_index())
        proj_v = {}
        for (sq, cn), k in T.vc.items():
            proj_v.setdefault(k, S.vc[(sq % p, cn)])
        def badT(kd, i):
            return (kd, proj_v[i]) in F if kd == 'V' else (kd, i % p) in F
        nF = sum(1 for q in all_points(T) if badT(*q))
        print(" forbidden points upstairs:", nF)
        srcs0 = [i for i in range(p) if sig[i] != i]
        s = srcs0[0]; srcs = [s + p * k for k in range(8)]; tgts = [sig[s] + p * k for k in range(8)]
        nseg, to_t, legal, midbad, other = darkness(T, srcs, tgts, badT, N)
        print(f"  8 lifts of C({s}) -> 8 lifts of C({sig[s]}): segments {nseg}, reach a target {to_t}, legal {legal},"
              f" midpoint forbidden {midbad}, legal (source, other centre) pairs {other}")
        bs = block_systems([H, V], n)
        print(" block systems of upstairs monodromy (number of blocks, block size):",
              [(len(set(s_)), n // len(set(s_))) for s_ in bs])
        print(" nontrivial systems with fewer than p blocks:",
              [len(set(s_)) for s_ in bs if 1 < len(set(s_)) < p])

    print("\n== Part C: R22 block claim (re-run of d93 systems.py, read-only) ==")
    d93 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'd93-review-blocks', 'systems.py')
    out = subprocess.run([sys.executable, '-B', d93, 'R22-base'], capture_output=True, text=True)
    for line in out.stdout.splitlines():
        print(" ", line)
    if out.returncode:
        print(" d93 systems.py failed:", out.stderr[-500:])

if __name__ == '__main__':
    main()
