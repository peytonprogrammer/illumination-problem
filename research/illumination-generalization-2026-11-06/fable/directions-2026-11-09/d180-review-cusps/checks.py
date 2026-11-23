"""d180 checks for l1-swap-cylinders.md and l1-marked-cusp-frequency.md
(snapshot d95-review-queue/snapshots/1906).

Named rooms only: DB55 stretch at p = 53 (d178/d179) and U2 (d69,
adjacent-cylinders.md).  Named mark pairs only.  No room, ray, direction or
word search.  The CRT check is an exhaustive check of an integer identity on
small (d, C, h), not a geometric search.

Models reused:
  * d146 `Double` (pillowcase cover Q -> B, front sheets, tau, g_ij), loaded
    from the definitions section of ../d146-review-exdescent/checks.py exactly
    as d178/d179 do.
  * trace() copied verbatim by exec from ../d175-review-windinglimits/checks.py
    (originally d170/d174): exact Fraction billiard tracer.
Run: python3 -B checks.py > checks.log
"""
from fractions import Fraction as Fr
from itertools import product
from math import gcd
from pathlib import Path
from decimal import Decimal, getcontext
import time

t0 = time.process_time()
HERE = Path(__file__).resolve().parent
src = (HERE.parent / 'd146-review-exdescent' / 'checks.py').read_text()
defs = src.split('# ' + '=' * 66 + ' 1')[0]
ns = {'__file__': str(HERE.parent / 'd146-review-exdescent' / 'checks.py')}
exec(compile(defs, 'd146-checks-defs', 'exec'), ns)
Double, rect = ns['Double'], ns['rect']

src175 = (HERE.parent / 'd175-review-windinglimits' / 'checks.py').read_text()
tr = src175[src175.index('def trace('):src175.index('def den(')]
ns2 = {'F': Fr}
exec(compile(tr, 'd175-trace', 'exec'), ns2)
trace = ns2['trace']

FAIL = []


def hdr(s):
    print('=' * 78); print(s); print('=' * 78)


def check(ok, msg):
    print(('  PASS ' if ok else '  FAIL ') + msg)
    if not ok:
        FAIL.append(msg)


# ============================================================ item 1
p = 53; L = p - 50; Dw = 10 + L
cells = rect(0, 5, 0, 5) | rect(5, 5 + L, 2, 3) | rect(5 + L, 10 + L, 0, 5)
Q = Dw and Double(cells)
n = Q.n
hdr(f'Item 1: DB55 p={p}, D={Dw}, n={n}; horizontal pair annuli in the band 2<y<3')


def to_front(s, i):
    return s if (s[0] + s[1] + s[2]) % 2 == 0 else Q.tau('V', i, s)


def pair_orbit_len(g, a, b):
    P0 = frozenset((a, b)); P = P0; k = 0
    while True:
        u, w = tuple(P); P = frozenset((g[u], g[w])); k += 1
        if P == P0:
            return k


cyc = {}
for site, g in Q.g.items():
    for c in Q.cycles(g):
        for i in c:
            cyc[(site, i)] = len(c)


def physical_corner(s, i, j):
    """Corner of square s on the vertical line of parity i, horizontal of parity j."""
    x, y, _ = s
    X = x if x % 2 == i else x + 1
    Y = y if y % 2 == j else y + 1
    return (X, Y)


# band coordinate u in [0, 2D): front copy c=0 x=u, back copy c=1 x=2D-1-u (unit squares)
def sq_at(k):  # k = integer unit index along the band, k mod 2D
    k %= 2 * Dw
    return (k, 2, 0) if k < Dw else (2 * Dw - 1 - k, 2, 1)


# sanity: walking the band by crossings reproduces sq_at, crossing line X applies tau('V', X%2)
s = sq_at(0); ok = True
for k in range(2 * Dw):
    nxt = sq_at(k + 1)
    # the line crossed: right side of a front square, left side of a back square
    X = s[0] + 1 if s[2] == 0 else s[0]
    if k == Dw - 1 or k == 2 * Dw - 1:  # wall bounce: same square, other copy
        X = s[0] + 1 if s[2] == 0 else s[0]
    t = Q.tau('V', X % 2, s)
    ok &= (t == nxt)
    s = nxt
check(ok, f'band parametrization: u-steps of 1 are tau crossings; band is one Q-cylinder of circumference {2 * Dw}')

res = {}
for j in range(1, Dw):
    # pair {(u),(u+2j)}: both unit squares project to the same base square (offset even)
    same_base = all((sum(sq_at(k)) % 2) == (sum(sq_at(k + 2 * j)) % 2) for k in range(2 * Dw))
    # circumference in Y: smallest m>0 (step 2 units) with {k+2m, k+2j+2m} = {k, k+2j} as unordered pairs
    m = next(m for m in range(1, 2 * Dw + 1)
             if {(2 * m) % (2 * Dw), (2 * m + 2 * j) % (2 * Dw)} == {0, (2 * j) % (2 * Dw)})
    circ = 2 * m
    rim = {0: [], 1: []}
    for k in range(2 * Dw):
        a, b = sq_at(k), sq_at(k + 2 * j)
        for i in (0, 1):
            for jj in (0, 1):  # jj = 0: rim y=2, jj = 1: rim y=3
                fa, fb = Q.idx[to_front(a, i)], Q.idx[to_front(b, i)]
                g = Q.g[(i, jj)]
                swap = g[fa] == fb and g[fb] == fa
                ang = pair_orbit_len(g, fa, fb)
                if swap:
                    ang = 1
                rim[jj].append(dict(k=k, Xa=physical_corner(a, i, jj), Xb=physical_corner(b, i, jj),
                                    ca=cyc[((i, jj), fa)], cb=cyc[((i, jj), fb)], swap=swap, ang=ang,
                                    Y=frozenset((fa, fb)), site=(i, jj)))
    res[j] = (same_base, circ, rim)

hj = list(range(1, (Dw - 1) // 2 + 1))
for j in hj:
    same_base, circ, rim = res[j]
    out = []
    for jj, nm in ((0, 'y=2'), (1, 'y=3')):
        sw = sorted({(e['Xa'], e['Xb']) for e in rim[jj] if e['swap']})
        mx = max(e['ang'] for e in rim[jj])
        refl = any(e['ca'] == 3 or e['cb'] == 3 for e in rim[jj])
        out.append((nm, sw, mx, refl))
    print(f'   j={j}: same base point {same_base}; circumference {circ}; height 1 (band); ' +
          '; '.join(f'rim {nm}: swap poles at physical {sw if sw else "none"}, max cone angle {mx}pi, '
                    f'reflex coordinate present {refl}' for nm, sw, mx, refl in out))
check(all(res[j][0] and res[j][1] == 2 * Dw for j in hj), f'j=1..{hj[-1]}: same base point, circumference {2 * Dw}')
check(all(max(e['ang'] for e in res[j][2][jj]) >= 3 for j in hj for jj in (0, 1)),
      'every rim of every j has a Y cone point of angle >= 3pi (maximal cylinder, height exactly 1)')
nopole = [j for j in hj if not any(e['swap'] for jj in (0, 1) for e in res[j][2][jj])]
both = [j for j in hj if all(any(e['swap'] for e in res[j][2][jj]) for jj in (0, 1))]
check(nopole == [1, 2, 3, 4, 5] and both == [6], f'no swap pole on either rim for j={nopole}; poles on both rims for j={both}')
# folding argument: pole positions should be x=j and x=D-j on the walls 5<x<D-5
for j in hj:
    for jj in (0, 1):
        for e in res[j][2][jj]:
            if e['Xa'] == e['Xb'] or (e['Xa'][0] in (j, Dw - j) and e['Xb'][0] == e['Xa'][0]):
                pass
    xs = sorted({e['Xa'][0] for jj in (0, 1) for e in res[j][2][jj] if e['Xa'] == e['Xb']})
    sw = sorted({e['Xa'][0] for jj in (0, 1) for e in res[j][2][jj] if e['swap']})
    print(f'   j={j}: physical x where the two coordinates fold to the same lattice point: {xs}; '
          f'of these, swap poles at x={sw}')
check(all(sorted({e['Xa'][0] for jj in (0, 1) for e in res[j][2][jj] if e['Xa'] == e['Xb']}) == sorted({j, Dw - j})
          for j in hj), 'folding positions are exactly x=j and x=D-j for every j')
# offsets j and D-j... in u the offset 2j and 2D-2j give the same annulus
check(all({res[j][2][0][k]['Y'] for k in range(len(res[j][2][0]))} ==
          {res[Dw - j][2][0][k]['Y'] for k in range(len(res[Dw - j][2][0]))} for j in hj),
      'offsets 2j and 2D-2j give the same annulus (j and D-j), so j=1..6 is the full list of even offsets')
check(len({frozenset(e['Y'] for e in res[j][2][0]) for j in hj}) == len(hj), 'the six annuli are distinct')
# compatible start (1,2),(3,2) front lifts on the j=1 rim y=2
S, T = (1, 2), (3, 2)
sS, sT = Q.qpoint(S, 0), Q.qpoint(T, 0)
site = (1, 0)
hit = [e for e in res[1][2][0] if e['site'] == site and e['Xa'] == S and e['Xb'] == T]
ok = bool(hit) and set(hit[0]['Y']) <= (set(sS) | set(sT)) and len(set(hit[0]['Y']) & set(sS)) == 1
check(ok, f'front lifts of S={S}, T={T} (Q-points {sorted(sS)}, {sorted(sT)}) form a Y-point on the j=1 rim y=2: '
          f'{sorted(hit[0]["Y"]) if hit else None}, cone angle {hit[0]["ang"] if hit else None}pi')
check((S[0] + S[1]) % 2 == (T[0] + T[1]) % 2, 'S and T have the same parity (both odd)')
st, pt, con = trace([(0, 0), (5, 0), (5, 2), (8, 2), (8, 0), (13, 0), (13, 5), (8, 5), (8, 3), (5, 3), (5, 5), (0, 5)], S, T)
check(st == 'end' and pt == (Fr(3), Fr(2)) and not con, 'S and T are directly visible (trace: no contact)')

hdr('Item 1b: CRT primitive-displacement claim, exhaustive for |d|<=30, 1<=C,h<=30')
bad = 0
for d in range(-30, 31):
    for C in range(1, 31):
        for h in range(1, 31):
            exists = any(gcd(d + k * C, h) == 1 for k in range(h + 1))
            if exists != (gcd(gcd(d, C), h) == 1):
                bad += 1
check(bad == 0, 'exists k with gcd(d+kC,h)=1  <=>  gcd(d,C,h)=1 (k ranges over one period 0..h)')

# ============================================================ item 3
hdr('Item 3: triangle step q|qx-p| < q/q\' <= 1 on named irrationals, 40 convergents each')
getcontext().prec = 120
named = {'sqrt2': Decimal(2).sqrt(), 'golden': (1 + Decimal(5).sqrt()) / 2, 'e': Decimal(1).exp(),
         'sqrt7-2': Decimal(7).sqrt() - 2}
for nm, x in named.items():
    a = []; y = x
    for _ in range(42):
        q0 = int(y); a.append(q0); y = 1 / (y - q0)
    P, Qd = [1, a[0]], [0, 1]
    for ak in a[1:]:
        P.append(ak * P[-1] + P[-2]); Qd.append(ak * Qd[-1] + Qd[-2])
    ok = True; worst = Decimal(0)
    for k in range(1, 41):
        pk, qk, qn = P[k], Qd[k], Qd[k + 1]
        area = qk * abs(qk * x - pk)
        ok &= gcd(pk, qk) == 1 and area < Decimal(qk) / qn <= 1
        worst = max(worst, area)
    check(ok, f'{nm}: all 40 convergents primitive with doubled area < q/q\' <= 1 (max area {float(worst):.4f})')

# ============================================================ item 4
hdr('Item 4: equal-depth (and unequal-depth) seam criterion, traced exactly')


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def seam_chords(o1, o2, l, C1, C2, x1, x2, h1, h2, kmax=6):
    """All u in (0,l) and travels t1 with h2(o1+u-x1+iC1) = h1(x2-o2-u+jC2)."""
    g = gcd(h1 * C2, h2 * C1)
    r = h1 * (x2 - o2) + h2 * (x1 - o1)
    out = []
    for k in range(-kmax * (h1 + h2) * l, kmax * (h1 + h2) * l + 1):
        u = Fr(r + k * g, h1 + h2)
        if 0 < u < l:
            R = (h1 + h2) * u - r  # = h1 j C2 - h2 i C1
            gg, A, B = egcd(h1 * C2, h2 * C1)
            assert R % gg == 0
            j, i = A * (R // gg), -B * (R // gg)
            assert h1 * j * C2 - h2 * i * C1 == R
            t1 = o1 + u - x1 + i * C1
            out.append((u, t1))
    return g, r, sorted(set(out))


DB = [(0, 0), (5, 0), (5, 2), (8, 2), (8, 0), (13, 0), (13, 5), (8, 5), (8, 3), (5, 3), (5, 5), (0, 5)]
U2 = [(0, 0), (9, 0), (9, 7), (5, 7), (5, 5), (7, 5), (7, 2), (2, 2), (2, 9), (0, 9)]


def run(room, nm, S, T, lifts, o1, o2s, l, C1, C2, h1, h2, x1, phys):
    for lift, (x2, o2) in lifts.items():
        g, r, sols = seam_chords(o1, o2, l, C1, C2, x1, x2, h1, h2)
        crit = f'{h1 + h2}u = {r} mod {g}, u in (0,{l})'
        suff = (h1 + h2) * l > g
        if not sols:
            print(f'   {nm} S={S} T={T} [{lift}]: {crit}: no solution (sufficient bound {(h1 + h2) * l}>{g}: {suff})')
            continue
        for u, t1 in sols[:2]:
            first = phys(t1)
            mid = (S[0] + first[0], S[1] + first[1])
            end = (S[0] + first[0] * Fr(h1 + h2, h1), S[1] + first[1] * Fr(h1 + h2, h1))
            st1, p1, c1 = trace(room, S, mid)
            st2, p2, c2 = trace(room, S, end)
            check(st2 in ('end', 'wall-end') and p2 == tuple(map(Fr, T)) and st1 in ('end', 'wall-end'),
                  f'{nm} S={S} T={T} [{lift}]: {crit} -> u={u}, travel {t1}; seam point {tuple(map(str, p1))}; '
                  f'exact trace ends at {tuple(map(str, p2))} ({st2}, {len(c2)} reflections); '
                  f'sufficient bound {(h1 + h2) * l}>{g}: {suff}')


# --- DB55 p=53, vertical cylinder of the left chamber 0<x<5: longitudinal s (front s=y, back s=10-y),
# transverse x.  Rim x=5 is self-glued along the wall 3<y<5: side-1 occurrence s=3+u (front), paired
# occurrence s=7-u (back); common orientation on side 2 uses s~=-s, so o2=-7 and x2=-s_T.
print('   DB55: vertical left-chamber cylinder, C=10, height 5; open wall edge x=5, 3<y<5 (l=2), self-glued')
for S, T in (((4, 1), (4, 4)), ((4, 1), (4, 2)), ((4, 1), (4, 3))):
    lifts = {'T front s=%d' % T[1]: (-T[1], -7), 'T back s=%d' % (10 - T[1]): (-(10 - T[1]), -7)}
    run(DB, 'DB55', S, T, lifts, 3, None, 2, 10, 10, 1, 1, S[1], lambda t: (1, t))
print('   DB55 same cylinder, lower wall edge x=5, 0<y<2 (l=2): side-1 s=u, paired s=10-u -> o1=0, o2=-10')
S, T = (4, 1), (4, 4)
lifts = {'T front s=4': (-4, -10), 'T back s=6': (-6, -10)}
run(DB, 'DB55', S, T, lifts, 0, None, 2, 10, 10, 1, 1, S[1], lambda t: (1, t))
print('   DB55 self-glued edges have a second side assignment: S-side on the back occurrence.')
print('   upper wall edge, S-side s=5+u (back), paired s=5-u (front) -> o1=5, o2=-5')
S, T = (4, 1), (4, 4)
run(DB, 'DB55', S, T, {'T front s=4': (-4, -5), 'T back s=6': (-6, -5)}, 5, None, 2, 10, 10, 1, 1, S[1],
    lambda t: (1, t))
print('   lower wall edge, S-side s=8+u (back), paired s=2-u (front) -> o1=8, o2=-2')
run(DB, 'DB55', S, T, {'T front s=4': (-4, -2), 'T back s=6': (-6, -2)}, 8, None, 2, 10, 10, 1, 1, S[1],
    lambda t: (1, t))
print('   DB55 unequal depths (adjacent-cylinders.md general form): S=(4,1) depth 1, T=(3,4) depth 2, edge 3<y<5')
S, T = (4, 1), (3, 4)
lifts = {'T front s=4': (-4, -7), 'T back s=6': (-6, -7)}
run(DB, 'DB55', S, T, lifts, 3, None, 2, 10, 10, 1, 2, S[1], lambda t: (1, t))

# --- U2 horizontal: bar 0<y<2 (C1=18: front s=x, back s=18-x) below, left arm 0<x<2, 2<y<9 (C2=4:
# front s=x, back s=4-x) above.  Their shared open edge runs from the reflex corner (2,2) on the back,
# through the regular wall point (0,2), to (2,2) on the front: length l=4, o1=16, o2=2 (both increase).
print('   U2: bar cylinder C=18 below, left-arm cylinder C=4 above, shared open edge l=4 through (0,2)')
for S, T, h2 in (((7, 1), (1, 3), 1), ((5, 1), (1, 3), 1), ((5, 1), (1, 4), 2)):
    lifts = {'T front s=1': (T[0], 2), 'T back s=3': (4 - T[0], 2)}
    run(U2, 'U2', S, T, lifts, 16, None, 4, 18, 4, 1, h2, S[0], lambda t: (t, 1))
    # S back lift too: x1 = 18 - S[0], physical direction (-t, 1)
    run(U2, 'U2(S back)', S, T, lifts, 16, None, 4, 18, 4, 1, h2, 18 - S[0], lambda t: (-t, 1))

print(f'\nfailures: {len(FAIL)}')
for f in FAIL:
    print('   ', f)
print(f'CPU seconds: {time.process_time() - t0:.2f}')
