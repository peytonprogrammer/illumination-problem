"""D113 claims 1-2: the 20-wall BBBB room of general-gluing.md, exact first-door mismatch
around s0 = 43/33, exact traces, and a few named candidate paths. python3 -B jump.py"""
import sys
from fractions import Fraction as F
from pathlib import Path
from geo import rect, summary, shoot, first_cross, reach, Corner
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'd103-twenty-check'))
import tracer as T103

s0 = F(43, 33)


def cells(k=0):
    L = 4 + 66 * k
    return (rect(0, 5, 0, 4) | rect(1, 3, 4, 48) | rect(1, 3, -3, 0) | rect(5, 5 + L, 1, 2)
            | rect(5 + L, 9 + L, -1, 5)), L


def marks(k=0):
    return (F(2), F(47)), (F(10 + 66 * k), F(3))


def mismatch(V, L, S, T, s):
    """Exact first-door mismatch F = L s + f_A + f_B (own tracer, sealed by stopping at first crossing)."""
    rA, evA = shoot(V, S, (1, -s), first_cross(5)); rB, evB = shoot(V, T, (-1, -s), first_cross(5 + L))
    if rA is None or rB is None:
        raise Corner('no door crossing')
    (yA, sgA), (yB, sgB) = rA, rB
    fA = sgA * (yA - 1); fB = sgB * (yB - 1)
    return L * s + fA + fB, yA, sgA, yB, sgB, len(evA), len(evB)


def formulas(L, s):
    return (L * s + 42 * s - 56, L * s + 36 * s - 48)   # below / above branch (note: 46s-56, 40s-48 at L=4)


def main():
    C, L = cells(0); S, T = marks(0)
    info = summary(C); V = info['V']
    print('== room ==')
    for k in ('W', 'r', 'area', 'gcd_h', 'gcd_v', 'no_corner_only_class'):
        print(f'  {k} = {info[k]}')
    print('  reflex =', info['reflex'])
    print('  classes =', {c: v for c, v in sorted(info['classes'].items())})
    print('  S kind', T103.is_corner(C, 2, 47), 'T kind', T103.is_corner(C, 10, 3),
          'S,T parity', (2 % 2, 47 % 2), (10 % 2, 3 % 2))
    print('== exact slope s0 ==')
    try:
        shoot(V, S, (1, -s0), first_cross(5)); print('  no corner (unexpected)')
    except Corner as e:
        print('  source ray at s0 hits vertex', e.args[0])
    print('== one-sided mismatches (own tracer) vs formulas ==')
    bad = 0
    for e in [F(1, 10**k) for k in (2, 3, 4, 6, 9)] + [F(1, 200), F(1, 300)]:
        for side, s in (('below', s0 - e), ('above', s0 + e)):
            try:
                Fv, yA, sgA, yB, sgB, nA, nB = mismatch(V, L, S, T, s)
            except Corner as c:
                print(f'  {side} eps={e}: corner {c.args[0]}'); continue
            fb, fa = formulas(L, s)
            want = fb if side == 'below' else fa
            ok = Fv == want and 1 < yA < 2 and 1 < yB < 2
            bad += not ok
            print(f'  {side} eps={e}: F={float(Fv):.6f} formula_ok={Fv == want} yA={float(yA):.5f}{"+" if sgA>0 else "-"} '
                  f'yB={float(yB):.5f}{"+" if sgB>0 else "-"} bouncesA={nA} F-4={float(Fv-4):+.6f}')
    e = F(1, 10000)
    for s in (s0 - e, s0 + e):
        Fv, yA, *_ = mismatch(V, L, S, T, s)
        print(f'  s0{"-" if s < s0 else "+"}1/10000: yA={yA} F={Fv}')
    fb, fa = formulas(L, s0)
    print('  limits', fb, fa, ' required 4 =', F(132, 33), ' roots', F(60, 46), F(52, 40))
    # branch width: scan a fixed grid (not a witness search) to find where each formula stops holding
    print('== branch extent on grid step 1/3300 ==')
    for side, sg in (('below', -1), ('above', 1)):
        j = 1
        while True:
            s = s0 + sg * F(j, 3300)
            try:
                Fv = mismatch(V, L, S, T, s)[0]
            except Corner:
                break
            if Fv != (formulas(L, s)[0] if sg < 0 else formulas(L, s)[1]): break
            j += 1
        print(f'  {side}: formula holds for j=1..{j-1} (|s-s0|<= {j-1}/3300), fails/corner at j={j}')
    print('  formula mismatches in eps table:', bad)
    # d103 unfolded tracer cross-check of the source leg to the first door (independent code)
    print('== d103 cross-check: unfolded displacement to x-developed 41 / 35 ==')
    for s, dev in ((s0 - e, 41), (s0 + e, 35)):
        end = T103.trace(C, S, (F(dev), -s * dev))
        print(f'  s={"s0-e" if s < s0 else "s0+e"} dev={dev}: end={end} (expect x=5, y in (1,2))')

    print('== candidate full-room traces (claim 1, natural candidates only) ==')
    cands = [('root of below formula', F(30, 23)), ('root of above formula', F(13, 10)),
             ('below formula = 2', F(58, 46)), ('below formula = 6', F(62, 46)),
             ('above formula = 2', F(50, 40)), ('above formula = 6', F(54, 40))]
    for name, s in cands:
        for dy in (-1, 1):
            try:
                Fv = mismatch(V, L, S, T, s)[0] if dy < 0 else None
            except Corner as c:
                Fv = f'corner {c.args[0]}'
            res = confirm(C, V, S, T, (s.denominator, dy * s.numerator), 5000)
            print(f'  {name} s={s} dir=(+,{dy:+d}): true first-door F={Fv if not isinstance(Fv, F) else Fv} -> {res}')


def confirm(C, V, S, T, d, maxev):
    """Full trace to T with own tracer, then replay the developed displacement with d103."""
    try:
        r, ev = shoot(V, S, d, reach(T), maxev=maxev)
    except Corner as c:
        return f'corner {c.args[0]}'
    if not r:
        return f'no reach in {maxev} bounces'
    pts = [S] + [q for _, q in ev] + [T]
    dx = sum(abs(b[0] - a[0]) for a, b in zip(pts, pts[1:]))
    v = (F(d[0]) / abs(d[0]) * dx, F(d[1]) / abs(d[0]) * dx)
    end = T103.trace(C, S, v)
    hits = sum(1 for a, b in zip(pts, pts[1:]) if (a[0] - 5) * (b[0] - 5) < 0)
    return f'REACH after {len(ev)} bounces, {hits} crossings of x=5, d103 replay of v={v}: end={end} ok={end == T}'


def persistence():
    print('== claim 2: L = 4+66k ==')
    for k in (1, 3, 10, 30):
        C, L = cells(k); S, T = marks(k); info = summary(C); V = info['V']
        e = F(1, 10**6)
        Fm = mismatch(V, L, S, T, s0 - e)[0]; Fp = mismatch(V, L, S, T, s0 + e)[0]
        fb, fa = formulas(L, s0)
        req = 4 + 86 * k
        print(f'  k={k} L={L} W={info["W"]} r={info["r"]} BBBB-free={info["no_corner_only_class"]}: '
              f'limits {fb},{fa} required {req}; traced F(s0-+1e-6)-req = {float(Fm-req):+.6f}, {float(Fp-req):+.6f}')
        # neighbouring even values on the same branches: constructed slopes, then exact full trace
        for name, s in (('below = req-2', F(58 + 86 * k, 46 + 66 * k)), ('above = req+2', F(56 + 86 * k, 40 + 66 * k))):
            try:
                Fv = mismatch(V, L, S, T, s)[0]
            except Corner as c:
                Fv = f'corner {c.args[0]}'
            res = confirm(C, V, S, T, (s.denominator, -s.numerator), 20000)
            print(f'     {name}: s={s} (s-s0={float(s-s0):+.2e}) true F={Fv} -> full trace {res}')


if __name__ == '__main__':
    main(); persistence()
