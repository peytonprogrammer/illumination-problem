"""Numerical attack on the r <= 2 theorem with real edge lengths and real points.

For each order type: random rooms (rational, sqrt 2, golden ratio, sqrt 3,
extreme aspect ratios), and for each room at least 50 point pairs biased
toward degenerate positions. For each pair:

1. Every lemma instance whose hypotheses hold (review code rv.py) is built
   and its prescribed candidate paths are traced in exact arithmetic.
2. The author's certificate for the pair's position types (lemmas.py) must
   name one of those instances, and that instance must give a legal path.
3. Extra pairs are engineered from Lemma B, B2, and C instances so that a
   family member passes exactly through a flat end, a door end, or the corner
   of Lemma B2.

Usage: python3 -B attack.py <type indices, comma separated> <rooms per type> <seed> <out prefix>
Type index 0..7 = line of types_r2.txt; 8 = L (r = 1); 9 = rectangle.

A trace stops at rv.MAXREF reflections and is then counted as skipped, never
as a success or a failure. To retry Lemma B certificates whose sampled
candidates all exceed that cap, set ATTACK_DEEP to a larger cap, for example
ATTACK_DEEP=200000.
"""
import json
import os
import random
import sys
import time
from collections import Counter
from fractions import Fraction as Fr

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
AUTH = os.path.join(HERE, "..", "d15-small-r")
sys.path.insert(0, AUTH)
sys.path.insert(0, HERE)
import lemmas as AL            # noqa: E402
import rv                      # noqa: E402
from certs import auth_key, show   # noqa: E402


def load_types():
    out = []
    for r in (2, 1, 0):
        for line in open(os.path.join(AUTH, f"types_r{r}.txt")):
            nx, ny, W, mask = map(int, line.split())
            out.append(AL.OT.from_mask(nx, ny, mask))
    return out


# ----------------------------------------------------------------- random reals
def rand_unit(Q, rng):
    """A field element strictly between 0 and 1."""
    c = rng.random()
    if c < 0.5:
        den = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 16, 97])
        return Q(Fr(rng.randint(1, den - 1), den))
    if c < 0.6:
        return Q(Fr(1, rng.choice([10 ** 3, 10 ** 6, 10 ** 9])))            # very near a line
    if c < 0.7:
        return Q(1) - Q(Fr(1, rng.choice([10 ** 3, 10 ** 6, 10 ** 9])))
    k = rng.randint(1, 30)
    v = Q(0, k)                                                              # k * sqrt(D)
    v = v - v.floor()
    if rng.random() < 0.5:
        v = v * Fr(rng.randint(1, 5), 7) + Fr(1, 9)                          # mix with rationals
        v = v - v.floor()
        if v.sign() == 0:
            v = Q(Fr(1, 2))
    return v


def rand_gap(Q, rng, style):
    D = Q.D
    if style == 'int':
        return Q(rng.randint(1, 5))
    if style == 'rat':
        return Q(Fr(rng.randint(1, 40), rng.randint(1, 12)))
    # irrational
    if D == 5 and rng.random() < 0.7:
        phi = Q(Fr(1, 2), Fr(1, 2))
        return rng.choice([phi, phi * phi, phi.inv(), phi * phi * phi, Q(1), Q(0, 1)]) * \
            Fr(rng.randint(1, 6), rng.randint(1, 4))
    while True:
        v = Q(Fr(rng.randint(-6, 12), rng.randint(1, 5)), Fr(rng.randint(-4, 6), rng.randint(1, 5)))
        if v > Fr(1, 10) and v < 20:
            return v


def make_room(ot, rng):
    D = rng.choice([2, 2, 5, 5, 3])
    Q = rv.field(D)
    style = rng.choice(['int', 'rat', 'irr', 'irr', 'irr', 'mixed', 'mixed', 'extreme', 'extreme'])

    def gaps(n):
        out = []
        for _ in range(n):
            st = style
            if style == 'mixed':
                st = rng.choice(['rat', 'irr', 'int'])
            if style == 'extreme':
                st = rng.choice(['rat', 'irr'])
            out.append(rand_gap(Q, rng, st))
        return out
    gx, gy = gaps(ot.nx), gaps(ot.ny)
    if style == 'extreme':
        for arr in (gx, gy):
            for i in range(len(arr)):
                c = rng.random()
                if c < 0.3:
                    arr[i] = arr[i] * Fr(1, rng.choice([20, 50, 100]))
                elif c < 0.45:
                    arr[i] = arr[i] * rng.choice([10, 30])
    xs = [Q(0)]
    for g in gx:
        xs.append(xs[-1] + g)
    ys = [Q(0)]
    for g in gy:
        ys.append(ys[-1] + g)
    return rv.Room(ot.nx, ot.ny, ot.cells, xs, ys), Q, style, D


# ----------------------------------------------------------------- points
def rand_point(R, Q, rng, kind):
    cells = sorted(R.cells)
    i, j = rng.choice(cells)
    x = R.xs[i] + (R.xs[i + 1] - R.xs[i]) * rand_unit(Q, rng)
    y = R.ys[j] + (R.ys[j + 1] - R.ys[j]) * rand_unit(Q, rng)
    if kind == 'gridx':
        x = rng.choice(R.xs)
    elif kind == 'gridy':
        y = rng.choice(R.ys)
    elif kind == 'gridxy':
        x = rng.choice(R.xs)
        y = rng.choice(R.ys)
    elif kind == 'vline':
        V = R.vertices()
        v1, v2 = rng.sample(V, 2)
        t = Fr(rng.randint(-8, 16), 8)
        x = v1[0] + (v2[0] - v1[0]) * t
        y = v1[1] + (v2[1] - v1[1]) * t
    return (x, y)


def derived(R, Q, rng, S, kind):
    V = R.vertices()
    if kind == 'sym':                      # S + T = 2V
        v = rng.choice(V)
        return (2 * v[0] - S[0], 2 * v[1] - S[1])
    if kind == 'ray':                      # the direct segment grazes a vertex
        v = rng.choice(V)
        t = Fr(rng.randint(1, 24), 8)
        return (v[0] + (v[0] - S[0]) * t, v[1] + (v[1] - S[1]) * t)
    if kind == 'mirror':                   # mirror image of S in a grid line
        if rng.random() < 0.5:
            c = rng.choice(R.xs)
            return (2 * c - S[0], S[1])
        c = rng.choice(R.ys)
        return (S[0], 2 * c - S[1])
    if kind == 'samex':
        T = rand_point(R, Q, rng, 'cell')
        return (S[0], T[1])
    if kind == 'samey':
        T = rand_point(R, Q, rng, 'cell')
        return (T[0], S[1])
    if kind == 'fold':                     # an image of T lies on the ray from S through a grid point
        gp = (rng.choice(R.xs), rng.choice(R.ys))
        t = Fr(rng.randint(1, 40), 8)
        x = gp[0] + (gp[0] - S[0]) * t
        y = gp[1] + (gp[1] - S[1]) * t
        i, j = sorted(rng.sample(range(R.nx + 1), 2))
        x = rv.fold(x, R.xs[i], R.xs[j])
        i, j = sorted(rng.sample(range(R.ny + 1), 2))
        y = rv.fold(y, R.ys[i], R.ys[j])
        return (x, y)
    raise ValueError(kind)


def gen_pairs(R, Q, rng, npairs):
    kinds = ['cell'] * 4 + ['gridx', 'gridy', 'gridxy', 'vline', 'vline']
    base = []
    tries = 0
    while len(base) < 7 and tries < 2000:
        tries += 1
        P = rand_point(R, Q, rng, rng.choice(kinds))
        if R.interior(P) and P not in base:
            base.append(P)
    pairs = [('base', base[a], base[b]) for a in range(len(base)) for b in range(a + 1, len(base))]
    dk = ['sym', 'ray', 'ray', 'mirror', 'samex', 'samey', 'fold', 'fold', 'fold']
    tries = 0
    while len(pairs) < npairs and tries < 5000:
        tries += 1
        S = rng.choice(base) if rng.random() < 0.5 else rand_point(R, Q, rng, rng.choice(kinds))
        if not R.interior(S):
            continue
        k = rng.choice(dk)
        T = derived(R, Q, rng, S, k)
        if R.interior(T) and T != S:
            pairs.append((k, S, T))
    return pairs


# ----------------------------------------------------------------- engineered pairs
def engineered(R, Q, rng, inst):
    """New pairs (label, A, B) in the original frame for which a member of the
    family of this instance passes exactly through a special point."""
    g = inst['g']
    s, t = inst['a'], inst['b']
    geo = inst.get('geo')
    out = []
    lem = inst['lem']
    if lem == 'B':
        p, q, d = geo['p'], geo['q'], geo['d']
        lam = (d - s[1]) / (t[1] - s[1])
        for lab, x0 in (('B:flat-end', p), ('B:reflex-end', q)):
            xn = rv.fold(s[0] + (x0 - s[0]) / lam, p, q)
            out.append((lab, s, (xn, t[1])))
    elif lem == 'B2':
        gx0, gx1, gy0, w = geo['gx0'], geo['gx1'], geo['gy0'], geo['w']
        for near in (False, True):
            tx = gx0 - (gx0 - t[0]) * Fr(1, 1000) if near else t[0]
            XT = 2 * gx1 - tx
            yF = s[1] + (gy0 - s[1]) * (XT - s[0]) / (2 * gx1 - gx0 - s[0])
            out.append(('B2:flat-end' + ('-near' if near else ''), s, (tx, rv.fold(yF, gy0, gy0 + w))))
            if s[0] < gx1:
                yC = s[1] + (gy0 - s[1]) * (XT - s[0]) / (gx1 - s[0])
                out.append(('B2:corner' + ('-near' if near else ''), s, (tx, rv.fold(yC, gy0, gy0 + w))))
    elif lem == 'C' and inst['form'] in ('par', 'same', 'perp'):
        gx0, gx1, gy0, gy1 = geo['gx0'], geo['gx1'], geo['gy0'], geo['gy1']
        w1, w2, F2, E2 = geo['w1'], geo['w2'], geo['F2'], geo['E2']
        lo2, hi2 = (F2, E2) if F2 < E2 else (E2, F2)
        u = Fr(rng.randint(-15, 15), 16)
        form = inst['form']
        if form in ('par', 'same'):
            Lh = (gx1 - gx0) * (2 if form == 'same' else 1)
            lines = [('C:F1', gy0, (F2 + u * w2 - gy0) / Lh), ('C:F2', gy0 + u * w1, (F2 - gy0 - u * w1) / Lh)]
            if F2 != gy0:
                lines.append(('C:F1F2', gy0, (F2 - gy0) / Lh))
            for lab, a, kap in lines:
                sy = rv.fold(a - kap * (gx0 - s[0]), gy0, gy0 + w1)
                txu = (2 * gx1 - t[0]) if form == 'same' else t[0]
                ty = rv.fold(a + kap * (txu - gx0), lo2, hi2)
                out.append((lab + '-' + form, (s[0], sy), (t[0], ty)))
        else:
            H, L = gy1 - gy0, gx1 - gx0
            lines = [('C:F1F2', gy0, H / L)]
            b = gx1 + u * w2
            if b > gx0:
                lines.append(('C:F1', gy0, H / (b - gx0)))
            a = gy0 + u * w1
            lines.append(('C:F2', a, (gy1 - a) / L))
            for lab, a, kap in lines:
                sy = rv.fold(a - kap * (gx0 - s[0]), gy0, gy0 + w1)
                tx = rv.fold(gx0 + (t[1] - a) / kap, lo2, hi2)
                out.append((lab + '-perp', (s[0], sy), (tx, t[1])))
    res = []
    for lab, a, b in out:
        A, B = rv.tpoint_inv(g, a), rv.tpoint_inv(g, b)
        if R.interior(A) and R.interior(B) and A != B:
            res.append((lab, A, B))
    return res


# ----------------------------------------------------------------- main loop
def fl(P):
    return [float(P[0]), float(P[1])]


TRACER_CHECK = Counter()


def checked_tracer(room, S, D, T, maxref=None):
    """Integer tracer; about 2% of the calls are repeated with the Fraction
    tracer and compared."""
    res = rv.trace_fast(room, S, D, T, maxref)
    if res[0] != 'too-long' and res[1] <= 300 and CHECK_RNG.random() < 0.02:
        TRACER_CHECK['compared'] += 1
        if rv.trace(room, S, D, T, maxref) != res:
            TRACER_CHECK['DISAGREE'] += 1
    return res


CHECK_RNG = random.Random(4)
DEEP = int(os.environ.get('ATTACK_DEEP', '0'))      # reflection cap of the retry; 0 = no retry


def deep_retry(R, inst, stats):
    """Lemma B certificate whose sampled candidates all exceed rv.MAXREF:
    trace the shortest candidate of each sign with the cap DEEP."""
    Rg = R.tf(inst['g'])
    a, b = inst['a'], inst['b']
    wbox, hbox = float(Rg.xs[-1] - Rg.xs[0]), float(Rg.ys[-1] - Rg.ys[0])
    best = {}
    for lab, Dv in inst['cands']:
        est = abs(float(Dv[0])) / wbox + abs(float(Dv[1])) / hbox
        if lab[0] not in best or est < best[lab[0]][0]:
            best[lab[0]] = (est, Dv)
    res = [rv.trace_fast(Rg, a, Dv, b, DEEP) for (_, Dv) in best.values()]
    sts = [r[0] for r in res]
    if any(st not in ('ok', 'too-long') for st in sts):
        return 'B:candidate-invalid-in-deep-retry'
    if 'ok' not in sts:
        stats['deep retry: still over the cap'] += 1
        return 'skip'
    stats['deep retry: legal path traced'] += 1
    stats['deep retry: max reflections'] = max(stats['deep retry: max reflections'],
                                               max(r[1] for r in res if r[0] == 'ok'))
    return 'ok'
rv.TRACER[0] = checked_tracer


def run(tidx, nrooms, seed, prefix):
    types = load_types()
    ot = types[tidx]
    rng = random.Random(seed * 1000 + tidx)
    cert_cache = {}
    arm_cache = {P: AL.arm_objects(ot, P) for P in ot.interior_types()}
    stats = Counter()
    kinds = Counter()
    styles = Counter()
    failures = []
    maxref = 0
    t0 = time.time()

    def do_pair(R, label, S, T, eng):
        nonlocal maxref
        St, Tt = R.pt(S)[2:], R.pt(T)[2:]
        if St == Tt:
            ak = ('A',)
        else:
            if (St, Tt) not in cert_cache:
                cert_cache[(St, Tt)] = AL.certify_pair(ot, St, Tt, arm_cache)
            c = cert_cache[(St, Tt)]
            if c is None:
                failures.append(dict(kind='author-no-certificate', St=St, Tt=Tt))
                return []
            ak = auth_key(c, R)
        insts = rv.all_instances(R, S, T, rng)
        stats['pairs' + ('-engineered' if eng else '')] += 1
        kinds[label] += 1
        got = False
        for inst in insts:
            v, det = rv.evaluate(R, inst, rng, max_c_traces=(40 if eng else 6))
            name = inst['lem'] + ('-' + inst['form'] if 'form' in inst else '')
            stats['inst ' + name] += 1
            stats['traces'] += det.get('traces', 0)
            maxref = max(maxref, det.get('maxref', 0))
            if det.get('corner'):
                stats['B2 corner-case candidates (invalid, as the proof says)'] += det['corner']
            if det.get('one_sign_only'):
                stats['B2 instances where only one sign works'] += 1
            if det.get('capped'):
                stats['C sign pairs with capped search and no solution found'] += det['capped']
            stats['traces skipped (over the reflection cap)'] += det.get('skipped', 0)
            if v == 'skip':
                stats['instances undecided (reflection cap)'] += 1
            elif v != 'ok':
                failures.append(dict(kind='lemma-instance-failure', verdict=v, lem=name, label=label,
                                     key=repr(inst['key']), S=fl(S), T=fl(T), Sx=repr(S), Tx=repr(T),
                                     xs=repr(R.xs), ys=repr(R.ys), detail=repr(det)))
            if inst['key'] == ak and v == 'skip' and DEEP and inst['lem'] == 'B':
                v = deep_retry(R, inst, stats)
            if inst['key'] == ak:
                got = True
                stats['cert ' + name + (' undecided' if v == 'skip' else '')] += 1
                if v not in ('ok', 'skip'):
                    failures.append(dict(kind='CERTIFICATE-PATH-FAILURE', verdict=v, label=label,
                                         S=repr(S), T=repr(T), xs=repr(R.xs), ys=repr(R.ys)))
        if not got:
            failures.append(dict(kind='author-certificate-not-an-instance', ak=repr(ak), label=label,
                                 S=repr(S), T=repr(T), xs=repr(R.xs), ys=repr(R.ys)))
        return insts

    for rno in range(nrooms):
        R, Q, style, D = make_room(ot, rng)
        styles[f'{style}/sqrt{D}'] += 1
        pairs = gen_pairs(R, Q, rng, 52)
        eng_budget = {'B': 4, 'B2': 6, 'C': 9}
        for (label, S, T) in pairs:
            insts = do_pair(R, label, S, T, False)
            for inst in insts:
                lem = inst['lem']
                if lem in eng_budget and eng_budget[lem] > 0 and rng.random() < 0.5:
                    for (lab, A, B) in engineered(R, Q, rng, inst):
                        if eng_budget[lem] <= 0:
                            break
                        eng_budget[lem] -= 1
                        do_pair(R, lab, A, B, True)
        if rv.FLAGS:
            for f in rv.FLAGS:
                failures.append(dict(kind='flag', what=repr(f)))
            rv.FLAGS.clear()
        if (rno + 1) % 20 == 0:
            print(f"type {tidx} {show(ot)} rooms {rno + 1} pairs {stats['pairs']} "
                  f"eng {stats['pairs-engineered']} failures {len(failures)} "
                  f"t={time.time() - t0:.0f}s", flush=True)
    stats['C sign pairs solved by the bisection fallback'] = rv.CSTATS['bisect']
    stats['C sign pairs where the bisection fallback also failed'] = rv.CSTATS['bisect-failed']
    rv.CSTATS['bisect'] = rv.CSTATS['bisect-failed'] = 0
    res = dict(type=tidx, shape=show(ot), rooms=nrooms, seed=seed, stats=dict(stats), pair_kinds=dict(kinds),
               room_styles=dict(styles), max_reflections=maxref, failures=failures[:200],
               tracer_check=dict(TRACER_CHECK),
               n_failures=len(failures), seconds=round(time.time() - t0, 1))
    with open(f"{prefix}_type{tidx}.json", "w") as f:
        json.dump(res, f, indent=1)
    print("DONE", tidx, show(ot), json.dumps({k: v for k, v in res.items() if k != 'failures'}), flush=True)


if __name__ == "__main__":
    tl = [int(x) for x in sys.argv[1].split(",")]
    nrooms = int(sys.argv[2])
    seed = int(sys.argv[3])
    prefix = sys.argv[4]
    for t in tl:
        run(t, nrooms, seed, prefix)
