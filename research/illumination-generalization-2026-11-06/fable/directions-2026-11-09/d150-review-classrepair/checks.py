"""Independent checks for class-repair.2026-11-22-0100.md (d150 review).

Two independent implementations are compared throughout:
  * walk(): a cell-level billiard tracer (adapted from d148) that also records which unfolded
    horizontal cylinder each leg lies in and which open rim arc each seam crossing uses;
  * propagate(): the note's abstract forward propagation in cylinder coordinates
    (circumferences, rim stops, chart translations), with no reference to cells.
Named rooms only (DB55; DB55 transposed for vertical-class rows).  No room search, no network.
Run: python3 -B checks.py
"""
import sys, time, random
from bisect import bisect_left
from collections import Counter
from fractions import Fraction
from itertools import product, combinations
from math import gcd, lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd10-mechanisms'))
import roomtools as rt  # noqa: E402

T0 = time.process_time()
log = []
def out(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True); log.append(s)

INF = 10**9
def v2(n):
    if n == 0: return INF
    n = abs(n); k = 0
    while n % 2 == 0: n //= 2; k += 1
    return k

def v2q(f):
    f = Fraction(f); return v2(f.numerator) - v2(f.denominator)

def qlcm(fr):
    """Positive generator of the intersection of the groups f*Z."""
    fr = [Fraction(f) for f in fr]
    num = lcm(*[f.numerator for f in fr]); den = gcd(*[f.denominator for f in fr])
    return Fraction(num, den)

def klass(U, h):
    """Primitive parity of (U,h) relative to the frame: 'core' = (1,0) mod 2, else 'other'."""
    return 'core' if v2(U) < v2(h) else 'other'

def phys_class(p, q):
    g = gcd(p, q); p, q = p // g, q // g
    return {(1, 0): 'b', (1, 1): 'c', (0, 1): 'd'}[(p % 2, q % 2)]

def rect(a, b, c, d):
    return set(product(range(a, b), range(c, d)))

DB55 = rect(0, 5, 0, 5) | rect(5, 8, 2, 3) | rect(8, 13, 0, 5)

# ---------------------------------------------------------------- horizontal cylinder geometry
class Geo:
    def __init__(self, cells):
        self.cells = cells
        rows = {}
        for (x, y) in cells: rows.setdefault(y, []).append(x)
        ivs = {}
        for y, xs in rows.items():
            xs.sort(); a = xs[0]
            for i, x in enumerate(xs):
                if i + 1 == len(xs) or xs[i + 1] != x + 1:
                    ivs[(a, x + 1, y)] = None
                    if i + 1 < len(xs): a = xs[i + 1]
        # merge identical intervals in consecutive rows (no corner on the level between them)
        self.strips = []; self.sof = {}
        for (a, b, y) in sorted(ivs, key=lambda t: (t[2], t[0])):
            if (a, b, y - 1) in ivs:
                sid = self.sof[(a, y - 1)]
                A, B, Y0, Y1 = self.strips[sid]; self.strips[sid] = (A, B, Y0, y + 1)
            else:
                sid = len(self.strips); self.strips.append((a, b, y, y + 1))
            for x in range(a, b): self.sof[(x, y)] = sid
        self.stops2 = {}; self.nxt = {}
        for sid, (a, b, y0, y1) in enumerate(self.strips):
            C = 2 * (b - a)
            for dy in (1, -1):
                lev = y1 if dy > 0 else y0
                st = set()
                for x in range(a, b + 1):
                    if self.nc((x, lev)) in (1, 3):
                        st.add(2 * (x - a) % (2 * C)); st.add((2 * C - 2 * (x - a)) % (2 * C))
                self.stops2[(sid, dy)] = sorted(st)
                assert st, ('rim without stop', sid, dy)
                for i in range(a, b):
                    beyond = (i, y1) if dy > 0 else (i, y0 - 1)
                    nb = (self.sof[beyond], dy) if beyond in cells else (sid, -dy)
                    for ex in (1, -1):
                        key = ((sid, dy), self.arc((sid, dy), 2 * i + 1, ex))
                        assert self.nxt.setdefault(key, nb) == nb, 'gluing not constant on an arc'

    def nc(self, p):
        x, y = p
        return sum(c in self.cells for c in ((x-1, y-1), (x, y-1), (x-1, y), (x, y)))

    def C(self, cyl):
        a, b, _, _ = self.strips[cyl[0]]; return 2 * (b - a)

    def theta2(self, cyl, x2, ex):
        a = self.strips[cyl[0]][0]; C = self.C(cyl)
        return (x2 - 2 * a) % (2 * C) if ex > 0 else (2 * C - (x2 - 2 * a)) % (2 * C)

    def arc(self, cyl, x2, ex):
        st = self.stops2[cyl]; t = self.theta2(cyl, x2, ex)
        assert t not in st, 'crossing at a stop'
        return bisect_left(st, t) % len(st)

    def exit_level(self, cyl):
        _, _, y0, y1 = self.strips[cyl[0]]; return y1 if cyl[1] > 0 else y0

    def entry_level(self, cyl):
        _, _, y0, y1 = self.strips[cyl[0]]; return y0 if cyl[1] > 0 else y1

# ---------------------------------------------------------------- cell-level tracer with chain recording
def pattern(p, q):
    ev = [(Fraction(k, p), 'V') for k in range(1, p)] + [(Fraction(l, q), 'H') for l in range(1, q)]
    return [c for _, c in sorted(ev)]

_pat = {}
def walk(G, S, U, h, ex0, dy0, nsteps):
    """Unfolded velocity (U,h), h>0, from the lift of S in x-copy ex0 with initial physical vy sign dy0.
    Yields after each primitive lattice step: (k, P, blocked, seams, cyl, ex)."""
    cells, sof = G.cells, G.sof
    g0 = gcd(abs(U), h); p, q = abs(U) // g0, h // g0
    su = (U > 0) - (U < 0)
    seams = []
    if p == 0:
        x, P, dy, ex = S[0], S, dy0, ex0
        cyl = None
        for k in range(1, nsteps + 1):
            for _ in range(2):
                r = P[1] if dy > 0 else P[1] - 1
                cand = [c for c in ((x - 1, r), (x, r)) if c in cells]
                if cand: break
                seams.append((cyl, G.arc(cyl, 2 * x, ex))); dy = -dy; cyl = (cyl[0], dy)
            s = sof[cand[0]]
            if cyl is None: cyl = (s, dy)
            elif s != cyl[0]:
                seams.append((cyl, G.arc(cyl, 2 * x, ex))); cyl = (s, dy)
            P = (x, P[1] + dy)
            if G.nc(P) in (1, 3):
                yield (k, P, True, seams, cyl, ex); return
            yield (k, P, False, seams, cyl, ex)
        return
    if (p, q) not in _pat: _pat[(p, q)] = pattern(p, q)
    pat = _pat[(p, q)]
    dx, dy = ex0 * su, dy0
    cell = (S[0] - (dx < 0), S[1] - (dy < 0)); assert cell in cells
    cyl = (sof[cell], dy)
    for k in range(1, nsteps + 1):
        for c in pat:
            if c == 'V':
                nb = (cell[0] + dx, cell[1])
                if nb in cells: cell = nb
                else: dx = -dx
            else:
                nb = (cell[0], cell[1] + dy)
                if nb in cells:
                    if sof[nb] != cyl[0]:
                        seams.append((cyl, G.arc(cyl, 2 * cell[0] + 1, dx * su))); cyl = (sof[nb], dy)
                    cell = nb
                else:
                    seams.append((cyl, G.arc(cyl, 2 * cell[0] + 1, dx * su))); dy = -dy; cyl = (cyl[0], dy)
        P = (cell[0] + (dx > 0), cell[1] + (dy > 0))
        if G.nc(P) in (1, 3):
            yield (k, P, True, seams, cyl, dx * su); return
        yield (k, P, False, seams, cyl, dx * su)
        if k == nsteps: return
        diag, hor, ver = (cell[0] + dx, cell[1] + dy), (cell[0] + dx, cell[1]), (cell[0], cell[1] + dy)
        ex = dx * su
        if diag in cells:
            if sof[diag] != cyl[0]:
                seams.append((cyl, G.arc(cyl, 2 * P[0], ex))); cyl = (sof[diag], dy)
            cell = diag
        elif hor in cells:   # smooth point on a horizontal wall
            seams.append((cyl, G.arc(cyl, 2 * P[0], ex))); dy = -dy; cell = hor; cyl = (cyl[0], dy)
        elif ver in cells:   # smooth point on a vertical wall
            if sof[ver] != cyl[0]:
                seams.append((cyl, G.arc(cyl, 2 * P[0], ex))); cyl = (sof[ver], dy)
            dx = -dx; cell = ver
        else:
            raise RuntimeError(P)

def chain_of(G, S, T, seams, cyl_end, ex_end, ex0, dy0, U):
    """Chain data of a shot: start cylinder, seams, final cylinder, endpoint charts, leg heights."""
    start = seams[0][0] if seams else cyl_end
    cyls = [s[0] for s in seams] + [cyl_end]
    H = []
    for i, c in enumerate(cyls):
        lo = S[1] if i == 0 else G.entry_level(c)
        hi = T[1] if i == len(cyls) - 1 else G.exit_level(c)
        H.append(abs(hi - lo))
    return dict(start=start, seams=tuple(seams), end=cyl_end, ex0=ex0, dy0=dy0, exT=ex_end,
                H=tuple(H), C=tuple(G.C(c) for c in cyls), cyls=tuple(cyls))

def shoot(G, S, T, U, h, ex0, dy0):
    """Physical legal arrival at T after unfolded displacement (U,h) exactly.  Returns chain or None."""
    g0 = gcd(abs(U), h)
    last = None
    for k, P, blk, seams, cyl, ex in walk(G, S, U, h, ex0, dy0, g0):
        if blk: return None
        last = (P, seams, cyl, ex)
    P, seams, cyl, ex = last
    if P != T: return None
    return chain_of(G, S, T, list(seams), cyl, ex, ex0, dy0, U)

def propagate(G, ch, S, T, U, h):
    """The note's forward propagation for slope s=U/h on the prescribed chain, cylinder coordinates only.
    Coordinates are scaled by h so everything is an integer."""
    cyl = ch['start']
    if cyl[1] != ch['dy0']: return False
    Th = h * G.theta2(cyl, 2 * S[0], ch['ex0']) // 2
    for i, (c, arc) in enumerate(ch['seams']):
        assert c == cyl
        Ch = h * G.C(cyl)
        Th = (Th + U * ch['H'][i]) % Ch
        st = [h * s // 2 for s in G.stops2[cyl]]
        if Th in st: REASON['stop'] += 1; return False
        if bisect_left(st, Th) % len(st) != arc: REASON['arc'] += 1; return False
        a = G.strips[cyl[0]][0]; L = G.C(cyl) // 2
        hx = h * a + Th if Th <= h * L else h * a + Ch - Th
        ex = 1 if Th <= h * L else -1
        cyl = G.nxt[(cyl, arc)]
        a2 = G.strips[cyl[0]][0]; C2h = h * G.C(cyl)
        Th = (hx - h * a2) % C2h if ex > 0 else (C2h - (hx - h * a2)) % C2h
    if cyl != ch['end']: return False
    Ch = h * G.C(cyl)
    ok = (Th + U * ch['H'][-1]) % Ch == (h * G.theta2(cyl, 2 * T[0], ch['exT']) // 2) % Ch
    REASON['pass' if ok else 'terminal'] += 1
    return ok
    return (Th + U * ch['H'][-1]) % Ch == (h * G.theta2(cyl, 2 * T[0], ch['exT']) // 2) % Ch

REASON = Counter()
def same(ch1, ch2):
    k = ('start', 'seams', 'end', 'ex0', 'dy0', 'exT')
    return ch2 is not None and all(ch1[x] == ch2[x] for x in k)

def legal_shots(G, S, T, B, Hmax, want_q_odd=None):
    """All legal arrivals at T from S with primitive (|p|<=B, 1<=q<=min(B,Hmax)) and transverse travel <= Hmax.
    want_q_odd: True -> other class only (q odd), False -> core class only (q even), None -> all."""
    shots = []
    for p in range(-B, B + 1):
        for q in range(1, min(B, Hmax) + 1):
            if gcd(p, q) != 1: continue
            if want_q_odd is not None and (q % 2 == 1) != want_q_odd: continue
            for dy0 in (1, -1):
                for k, P, blk, seams, cyl, ex in walk(G, S, p, q, 1, dy0, Hmax // q):
                    if blk: break
                    if P == T:
                        shots.append((p * k, q * k, chain_of(G, S, T, list(seams), cyl, ex, 1, dy0, p * k)))
    return shots

# ================================================================ 0. tracer cross-check against d148's tracer
out('== 0. tracer and cylinder model sanity')
G = Geo(DB55)
out('DB55 horizontal strips (a,b,y0,y1):', G.strips)
out('  heights/circumferences:', [(y1 - y0, 2 * (b - a)) for a, b, y0, y1 in G.strips])
sys.path.insert(0, str(HERE.parent / 'd148-review-delinv'))
src = (HERE.parent / 'd148-review-delinv' / 'checks.py').read_text()
ns = {'product': product, 'gcd': gcd, 'rt': rt, 'Counter': Counter, 'combinations': combinations, 'lcm': lcm}
exec(compile(src.split('# ---------------------------------------------------------------- algebra')[0]
             .split("T0 = time.process_time()")[1], 'd148', 'exec'), ns)
d148_trace = ns['trace']
mism = 0; ndir = 0
for p in range(-7, 8):
    for q in range(1, 8):
        if gcd(p, q) != 1: continue
        for S_ in ((2, 2), (1, 1), (11, 3)):
            for dy0 in (1, -1):
                ndir += 1
                mine = []
                for k, P, blk, *_ in walk(G, S_, p, q, 1, dy0, 200):
                    if blk: break
                    mine.append(P)
                ref = d148_trace(DB55, S_, (1 if p >= 0 else -1), dy0, p if p else 0, q)
                n = min(len(mine), len(ref))
                if mine[:n] != ref[:n] or (len(mine) < 200 and len(mine) != len(ref)): mism += 1
out('walk vs d148 trace, lattice-point sequences:', ndir, 'rays,', mism, 'mismatches')

# ================================================================ 1. arithmetic of the fixed-crossing criterion
out('\n== 1a. fixed-crossing criterion, pure arithmetic (exhaustive small cases)')
bad = 0; cases = 0; nonint = 0
for n, HR, CR in ((1, 16, 24), (2, 8, 12), (3, 4, 8)):
    for Hs in product(range(1, HR + 1), repeat=n):
        for Cs in product(range(1, CR + 1), repeat=n):
            h = sum(Hs); b = v2(h)
            P = qlcm([Fraction(C, H) for C, H in zip(Cs, Hs)])
            if (P * h).denominator != 1: nonint += 1
            crit = all(v2(H) > v2(C) for H, C in zip(Hs, Cs))
            assert (v2q(P) < 0) == crit
            for u in range(-h, h + 1):
                if v2(u) < b: continue           # seed must not be in the core class
                cases += 1
                exists = any(v2(u + j * P * h) < b for j in range(1, 9))
                bad += exists != crit
out('cases', cases, 'iff failures', bad, '| P*h non-integral', nonint)

# ================================================================ 2. DB55 claim
S, T = (2, 2), (10, 2)
out('\n== 2. DB55, S=(2,2), T=(10,2): horizontal frame, horizontal core class')
strip = [i for i, s in enumerate(G.strips) if s == (0, 13, 2, 3)]
out('strip 2<y<3 spans x in [0,13]:', bool(strip), '| C =', G.C((strip[0], 1)), 'H =', 1,
    '| stops on y=2 and y=3 (2*theta):', G.stops2[(strip[0], -1)], G.stops2[(strip[0], 1)])
interior_levels = [(x, y) for x in range(0, 14) for y in (2, 3) if G.nc((x, y)) in (1, 3)]
out('corners on the two boundary levels:', interior_levels)
B, HMAX = 30, 40
seeds = legal_shots(G, S, T, B, HMAX, want_q_odd=True)
core = legal_shots(G, S, T, B, HMAX, want_q_odd=False)
out(f'legal S->T shots with |p|<={B}, transverse travel h<={HMAX}: other class', len(seeds), '| core class', len(core))
out('  physical classes of the other-class seeds:', dict(Counter(phys_class(U, h) for U, h, _ in seeds)))
hasleg = sum(any(c[0] == strip[0] and H == 1 for c, H in zip(ch['cyls'], ch['H'])) for _, _, ch in seeds)
hsum = sum(sum(ch['H']) == h for _, h, ch in seeds)
vP = Counter(); shift_ok = Counter()
for U, h, ch in seeds:
    P = qlcm([Fraction(C, H) for C, H in zip(ch['C'], ch['H'])])
    vP[v2q(P)] += 1
    for j in (1, -1):
        U2 = U + j * int(P * h)
        ch2 = shoot(G, S, T, U2, h, ch['ex0'], ch['dy0'])
        shift_ok[(same(ch, ch2), klass(U2, h))] += 1
out('  seeds with sum(H_i)=h:', hsum, '/', len(seeds), '| seeds with a strip leg H=1, C=26:', hasleg, '/', len(seeds))
out('  v2(P) over seeds:', dict(vP), '(criterion needs v2(P)<0)')
out('  shifts U -> U +- P*h traced physically: (same chain & legal, class)', dict(shift_ok))
hasleg_core = sum(any(c[0] == strip[0] for c in ch['cyls']) for _, _, ch in core)
out('  core-class shots also using the strip:', hasleg_core, '/', len(core))
# direction (3,2)
w32 = [(U, h, ch) for U, h, ch in core if (U, h) == (48, 32) or (U, h) == (-48, 32)]
U, h, ch = w32[0]
P32 = qlcm([Fraction(C, H) for C, H in zip(ch['C'], ch['H'])])
out('(3,2) shot: displacement', (U, h), 'frame class', klass(U, h), '| legs (strip, H, C):',
    [(c[0], H, C) for c, H, C in zip(ch['cyls'], ch['H'], ch['C'])])
out('  P =', P32, 'v2(P) =', v2q(P32), '| strip legs with H=1:', sum(c[0] == strip[0] and H == 1 for c, H in zip(ch['cyls'], ch['H'])))

# ================================================================ 3. sliding test on prescribed chains
def sweep(G, S, T, ch, U0, h, label, maxres=4000, window=300):
    g = gcd(*ch['C']); P = qlcm([Fraction(C, H) for C, H in zip(ch['C'], ch['H'])])
    Ph = int(P * h); b = v2(h)
    per = Ph // g
    joint = lcm(per, 2 ** b // gcd(g, 2 ** b))
    out(f'{label}: h={h}, b={b}, g={g}, P={P}, Ph={Ph}, period in m={per}, joint period={joint}, legs={len(ch["H"])}')
    nres = min(joint, maxres)
    m0 = -(nres // 2)
    res = {}
    agree = Counter(); REASON.clear(); stopblk = Counter()
    for m in range(m0, m0 + nres):
        Uc = U0 + m * g
        a = propagate(G, ch, S, T, Uc, h)
        phys = shoot(G, S, T, Uc, h, ch['ex0'], ch['dy0'])
        ph = same(ch, phys)
        agree[(a, ph)] += 1
        if REASON['stop']: stopblk[phys is None] += 1; REASON['stop'] = 0; REASON['stopped'] += 1
        res[m] = a
        if a: res.setdefault('pass', []).append(Uc)
    passes = res.get('pass', [])
    out('  passing (U,h) with class:', [((x, h), phys_class(x, h)) for x in passes])
    out('  residues tested', nres, '| (test, physics-same-chain) counts', dict(agree))
    out('  test outcomes: hit a seam endpoint (stop)', REASON['stopped'], '| wrong arc', REASON['arc'],
        '| wrong terminal coordinate', REASON['terminal'], '| pass', REASON['pass'],
        '| stop-hit residues physically blocked:', stopblk[True], 'of', sum(stopblk.values()))
    out('  passing slopes', len(passes), 'by frame class:', dict(Counter(klass(x, h) for x in passes)),
        '| witness passes:', propagate(G, ch, S, T, U0, h))
    if nres == joint:
        periodic = all(propagate(G, ch, S, T, U0 + (m + per) * g, h) == res[m] for m in range(m0, m0 + min(nres, 400)))
        out('  periodic with period Ph/g on first 400 residues:', periodic)
    # necessity of the congruence U = U0 mod g: no physical same-chain arrival off the coset
    off = [Uc for Uc in range(U0 - window, U0 + window + 1)
           if (Uc - U0) % g and same(ch, shoot(G, S, T, Uc, h, ch['ex0'], ch['dy0']))]
    out(f'  same-chain physical arrivals with U != U0 mod g in |U-U0|<={window}:', len(off))
    # other physical arrivals at T on the coset using a different chain (allowed, not a contradiction)
    return passes

out('\n== 3a. sliding test, DB55 (3,2) chain')
sweep(G, S, T, ch, U, h, 'DB55 (3,2)')
# other-class chains: can sliding reach the core class?  If v2(h) <= v2(g) the coset U0+gZ has fixed class.
out('\n== 3b. sliding test on other-class seed chains')
rigid = sum(v2(h_) <= v2(gcd(*c_['C'])) for _, h_, c_ in seeds)
out('  seeds whose chain is class-rigid because v2(h) <= v2(g):', rigid, '/', len(seeds))
seen = set(); cnt = Counter()
for U_, h_, ch_ in sorted(seeds, key=lambda t: (t[1], abs(t[0]))):
    if v2(h_) <= v2(gcd(*ch_['C'])): continue
    key = (ch_['start'], ch_['seams'], ch_['end'], ch_['ex0'], ch_['exT'])
    if key in seen: continue
    seen.add(key)
    ps = sweep(G, S, T, ch_, U_, h_, f'  seed {(U_, h_)} class {phys_class(U_, h_)}', maxres=1500, window=60)
    cnt['chains'] += 1; cnt['with core residue'] += any(klass(x, h_) == 'core' for x in ps)
    if cnt['chains'] == 4: break
out(' ', dict(cnt))

# ================================================================ 3c. a d148 lost row
out('\n== 3c. a d148 lost row (pencil-relaxed, no legal pencil), DB55')
exec(compile(src.split('# ---------------------------------------------------------------- algebra: own pencil evaluation')[1]
             .split('log = []')[0], 'd148alg', 'exec'), ns)
ns['ROOMS'] = {'DB55': DB55}
ns['interior_pts'] = lambda cells, origin: sorted(x for x in rt.lattice_points(cells)
                                                if G.nc(x) == 4 and (x[0] % 2, x[1] % 2) == origin)
Setup, PENCILS = ns['Setup'], ns['PENCILS']
lost = []
for origin in product(range(2), repeat=2):
    st = Setup('DB55', origin)
    for S_, T_ in combinations(st.pts, 2):
        for d in (1, 3):
            pens = PENCILS[d]
            rel = any(st.connected(d, pn, j, S_, T_, False) for pn in pens for j in range(st.order[pn]))
            leg = any(st.connected(d, pn, j, S_, T_, True) for pn in pens for j in range(st.order[pn]))
            if rel and not leg: lost.append((d, S_, T_))
out('DB55 lost rows in classes b/d (d148 total is 64):', len(lost), '| first few:', lost[:6])
out('  classes of the lost rows:', dict(Counter(r[0] for r in lost)), '(1 = horizontal b)')
S3, T3 = (2, 2), (10, 4)
assert (1, S3, T3) in lost
GT, S3t, T3t = G, S3, T3
out(f'chosen row: class b, S={S3}, T={T3} (T inside the open cylinder 3<y<5); physical frame')
coreT = legal_shots(GT, S3t, T3t, 15, 40, want_q_odd=False)
U3, h3, ch3 = min(coreT, key=lambda t: (t[1], abs(t[0])))
out('  lowest core-class witness:', (U3, h3), 
    '| legs (H,C):', list(zip(ch3['H'], ch3['C'])))
sweep(GT, S3t, T3t, ch3, U3, h3, 'lost-row witness chain')
seedsT = legal_shots(GT, S3t, T3t, 15, 40, want_q_odd=True)
vPT = Counter(v2q(qlcm([Fraction(C, H) for C, H in zip(c['C'], c['H'])])) for _, _, c in seedsT)
out('  fixed-crossing criterion on its other-class seeds (|p|<=15, h<=40):', len(seedsT), 'seeds, v2(P) counts', dict(vPT))

out('\nCPU seconds', round(time.process_time() - T0, 1))
(HERE / 'checks.log').write_text('\n'.join(log) + '\n')
