"""d164 attack on the stacked-hall theorem of parallel-mouth-combs.md.

Ten explicit named rooms at the edges of the hypotheses. For each room every pair of distinct
lattice / half-lattice interior marks (with at least one mark outside the open hall strip) gets the
note's shot family. Pairs where the whole family fails get a direct exact search inside that room
only: every primitive direction (p,q) with max(|p|,|q|) <= 60, at most 40 reflections, plus the
four axis directions. No room search.

Exact integer arithmetic: coordinates are doubled, so marks are integer points and walls lie on
even lines. polygon(), interior(), half_points() and the Fraction tracer trace() are copied from
d162-review-combs/checks.py (itself from d161); trace() cross-checks the integer stepper and
re-checks every dark candidate.
Run: python3 -B attack.py > attack.log
"""
import time
from fractions import Fraction as F
from itertools import combinations
from math import floor, gcd
from collections import Counter

T0 = time.process_time()
BUDGET = 540.0  # CPU seconds


def log(*a):
    print(*a, flush=True)


# ------------------------------------------------------------------ copied from d162
def cells_rect(a, b, c, d):
    return {(x, y) for x in range(a, b) for y in range(c, d)}


def polygon(cells):
    E = {}
    for x, y in cells:
        if (x, y - 1) not in cells: E[(x, y)] = (x + 1, y)
        if (x + 1, y) not in cells: E[(x + 1, y)] = (x + 1, y + 1)
        if (x, y + 1) not in cells: E[(x + 1, y + 1)] = (x, y + 1)
        if (x - 1, y) not in cells: E[(x, y + 1)] = (x, y)
    s = min(E)
    pts, p = [s], E[s]
    while p != s:
        pts.append(p); p = E[p]
    n = len(pts)
    V = []
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        if (b[0] - a[0], b[1] - a[1]) != (c[0] - b[0], c[1] - b[1]):
            V.append(b)
    assert len(E) == n, "not strictly simple"
    return V


def trace(P, A, B, maxrefl=10**6):
    n = len(P)
    hw = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][1] == P[(i + 1) % n][1]]
    vw = [(P[i], P[(i + 1) % n]) for i in range(n) if P[i][0] == P[(i + 1) % n][0]]
    V = {(F(a), F(b)) for a, b in P}
    X, Y = F(A[0]), F(A[1])
    vx, vy = F(B[0]) - X, F(B[1]) - Y
    tau, contacts = F(1), []
    for _ in range(maxrefl):
        best = None
        if vx:
            for a, b in vw:
                t = (a[0] - X) / vx
                if t > 0 and (best is None or t < best[0]) and min(a[1], b[1]) <= Y + vy * t <= max(a[1], b[1]):
                    best = (t, 'v')
        if vy:
            for a, b in hw:
                t = (a[1] - Y) / vy
                if t > 0 and (best is None or t < best[0]) and min(a[0], b[0]) <= X + vx * t <= max(a[0], b[0]):
                    best = (t, 'h')
        if best is None or best[0] > tau:
            return 'end', (X + vx * tau, Y + vy * tau), contacts
        t, kind = best
        X, Y = X + vx * t, Y + vy * t
        if best[0] == tau:
            return 'wall-end', (X, Y), contacts
        tau -= t
        if (X, Y) in V:
            return 'corner', (X, Y), contacts
        contacts.append(((X, Y), kind))
        if kind == 'v': vx = -vx
        else: vy = -vy
    return 'limit', (X, Y), contacts


def interior(cells, p):
    xs = [int(p[0]) - 1, int(p[0])] if F(p[0]).denominator == 1 else [floor(p[0])]
    ys = [int(p[1]) - 1, int(p[1])] if F(p[1]).denominator == 1 else [floor(p[1])]
    return all((i, j) in cells for i in xs for j in ys)


def half_points(cells):
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    return [(F(i, 2), F(j, 2)) for i in range(2 * min(xs), 2 * max(xs) + 3)
            for j in range(2 * min(ys), 2 * max(ys) + 3) if interior(cells, (F(i, 2), F(j, 2)))]


def fr(p):
    return f"({p[0]},{p[1]})"


# ------------------------------------------------------------------ rooms
class Room:
    """Hall [0,A]x[0,c]; top rects (l,r,b,t) with b>=c; bottom rects with t<=0."""

    def __init__(self, name, A, c, top, bot=()):
        self.name, self.A, self.c, self.top, self.bot = name, A, c, list(top), list(bot)
        cl = cells_rect(0, A, 0, c)
        for l, r, b, t in self.top + self.bot:
            cl |= cells_rect(l, r, b, t)
        self.cells, self.P = cl, polygon(cl)
        self.ratio_top = max([F(8 * A * (t - c), c * (r - l)) for l, r, b, t in self.top] or [0])
        self.ratio_bot = max([F(8 * A * (0 - b), c * (r - l)) for l, r, b, t in self.bot] or [0])

    def bank(self, p):
        return 'top' if p[1] > self.c else 'bot' if p[1] < 0 else 'hall'

    def rect_of(self, p):
        if p[1] > self.c:
            for R in self.top:
                l, r, b, t = R
                if l < p[0] < r and b <= p[1] < t:
                    return R
        else:
            best = None
            for R in self.bot:
                l, r, b, t = R
                if l < p[0] < r and b < p[1] <= t and (best is None or R[2] < best[2]):
                    best = R
            if best: return best
        raise AssertionError(p)

    def signs(self, p):
        if self.bank(p) == 'hall':
            return (1, -1)
        l, r, b, t = self.rect_of(p)
        dr, dl = r - p[0], p[0] - l
        return (1, -1) if dr == dl else ((1,) if dr > dl else (-1,))

    def mouth(self, p):  # open mouth containing a seam mark, or None
        for l, r, b, t in self.top:
            if b == self.c and p[1] == self.c and l < p[0] < r: return ('t', l)
        for l, r, b, t in self.bot:
            if t == 0 and p[1] == 0 and l < p[0] < r: return ('b', l)
        return None


def zigzag():
    rs, l, r = [], 0, 8
    for k in range(8):
        rs.append((l, r, 9 + k, 10 + k))
        if k % 2 == 0: l += 1
        else: r -= 1
    return rs


DB55 = Room("D3 DB55 (y shifted by -2): hall [0,13]x[0,1], banks [0,5],[8,13] depth 2 both sides", 13, 1,
            [(0, 5, 1, 3), (8, 13, 1, 3)], [(0, 5, -2, 0), (8, 13, -2, 0)])
assert {(x, y + 2) for x, y in DB55.cells} == cells_rect(0, 5, 0, 5) | cells_rect(5, 8, 2, 3) | cells_rect(8, 13, 0, 5)

ROOMS = [
    Room("A2 2x bound: A=5,c=10, tooth [1,3]x[10,11]", 5, 10, [(1, 3, 10, 11)]),
    Room("A4 4x bound: A=5,c=5, tooth [1,3]x[5,6]", 5, 5, [(1, 3, 5, 6)]),
    Room("A8 8x bound: A=5,c=5, tooth [1,3]x[5,7]", 5, 5, [(1, 3, 5, 7)]),
    Room("AT narrow tall arm: A=5,c=3, arm [1,2]x[3,9] (80x)", 5, 3, [(1, 2, 3, 9)]),
    Room("B overhang: A=6,c=32, [1,3]x[32,33] > child [2,5]x[33,34] (metric holds)", 6, 32,
         [(1, 3, 32, 33), (2, 5, 33, 34)]),
    Room("C flush: A=5,c=40, [1,4]x[40,41] > child [2,4]x[41,42] flush right (metric holds)", 5, 40,
         [(1, 4, 40, 41), (2, 4, 41, 42)]),
    Room("D1 two-sided stacked: A=5,c=20, roof [1,3]x[20,21], floor [1,3]x[-1,0]", 5, 20,
         [(1, 3, 20, 21)], [(1, 3, -1, 0)]),
    Room("D2 two-sided offset: A=6,c=24, roof [1,3]x[24,25], floor [3,5]x[-1,0]", 6, 24,
         [(1, 3, 24, 25)], [(3, 5, -1, 0)]),
    DB55,
    Room("E deep: A=9,c=9, 8 nested levels, zigzag flush, unit heights", 9, 9, zigzag()),
]


# ------------------------------------------------------------------ integer stepper
def walk(cells, S2, p, q, maxrefl, mstop=None, targets=None, found=None, c=None, hall_only=False):
    """Billiard from doubled point S2 in primitive direction (p,q), p,q != 0.
    mstop: return doubled physical point at unfolded time mstop (None if the ray stops first).
    targets/found: record first visit of each target point, with reflection categories so far."""
    sx, sy = S2
    sp = 1 if p > 0 else -1; sq = 1 if q > 0 else -1
    ap, aq = abs(p), abs(q)
    i = sx // 2 if (sx & 1 or sp > 0) else sx // 2 - 1
    j = sy // 2 if (sy & 1 or sq > 0) else sy // 2 - 1
    I, J = i, j
    dx = dy = 1; ox = oy = 0
    m, refl = 1, 0
    cats = []
    while True:
        Xb = 2 * (I + 1) if sp > 0 else 2 * I
        Yb = 2 * (J + 1) if sq > 0 else 2 * J
        nx = abs(Xb - sx); ny = abs(Yb - sy)
        cmp = nx * aq - ny * ap
        if cmp <= 0: num, den = nx, ap
        else: num, den = ny, aq
        while m * den <= num:
            P = (dx * (sx + m * p) + ox, dy * (sy + m * q) + oy)
            if mstop is not None:
                if m == mstop: return P
            elif P in targets and P not in found:
                found[P] = ((p, q), tuple(cats))
            m += 1
        ex = dx * sp; ey = dy * sq
        if cmp < 0:
            if (i + ex, j) in cells: i += ex
            else:
                w = 2 * (i + 1) if ex > 0 else 2 * i
                ox = 2 * w - ox; dx = -dx; refl += 1
                if c is not None:
                    cats.append(vcat(j, c))
                    if hall_only and cats[-1][:3] in ('arm', 'ban'): return None
            I += sp
        elif cmp > 0:
            if (i, j + ey) in cells: j += ey
            else:
                w = 2 * (j + 1) if ey > 0 else 2 * j
                oy = 2 * w - oy; dy = -dy; refl += 1
                if c is not None:
                    cats.append(hcat(w // 2, ey, c))
                    if hall_only and cats[-1][:3] in ('arm', 'ban'): return None
            J += sq
        else:
            c1 = (i + ex, j) in cells; c2 = (i, j + ey) in cells; c3 = (i + ex, j + ey) in cells
            if c1 and c2 and c3:
                i += ex; j += ey
            elif c1 and not c2 and not c3:
                w = 2 * (j + 1) if ey > 0 else 2 * j
                i += ex; oy = 2 * w - oy; dy = -dy; refl += 1
                if c is not None:
                    cats.append(hcat(w // 2, ey, c))
                    if hall_only and cats[-1][:3] in ('arm', 'ban'): return None
            elif c2 and not c1 and not c3:
                w = 2 * (i + 1) if ex > 0 else 2 * i
                j += ey; ox = 2 * w - ox; dx = -dx; refl += 1
                if c is not None:
                    cats.append(vcat(j, c))
                    if hall_only and cats[-1][:3] in ('arm', 'ban'): return None
            else:
                return None  # vertex
            I += sp; J += sq
        if refl > maxrefl:
            return None


def vcat(j, c):
    return 'arm-side' if j >= c else 'bank-side' if j < 0 else 'hall-side'


def hcat(yw, ey, c):
    if yw == 0 and ey < 0: return 'floor'
    if yw == c and ey > 0: return 'roof'
    return 'arm-horiz' if yw > c else 'bank-horiz'


def d2(p):
    return (int(2 * p[0]), int(2 * p[1]))


def axis_clear(room, S, T):
    if S[0] != T[0] and S[1] != T[1]: return False
    n = int(2 * max(abs(T[0] - S[0]), abs(T[1] - S[1])))
    return all(interior(room.cells, (S[0] + (T[0] - S[0]) * k / n, S[1] + (T[1] - S[1]) * k / n)) for k in range(1, n))


def shot_ok(room, S, B, T):
    """Does the straight-line development S->B land on T?"""
    vx, vy = int(2 * (B[0] - S[0])), int(2 * (B[1] - S[1]))
    if vx == 0 or vy == 0:
        return (B == T) and axis_clear(room, S, T)
    g = gcd(abs(vx), abs(vy))
    return walk(room.cells, d2(S), vx // g, vy // g, 10**9, mstop=g) == d2(T)


# ------------------------------------------------------------------ the note's shot family
def family(room, S, T):
    """List of (label, B). Labels: direct, chosen, other (floor turn), roofturn, traverse."""
    A, c = room.A, room.c
    bs, bt = room.bank(S), room.bank(T)
    out = []
    if bs == 'hall' and bt == 'hall':
        ms, mt = room.mouth(S), room.mouth(T)
        same_seam_diff = (S[1] == T[1] and S[1] in (0, c) and ms != mt)
        if not same_seam_diff:
            return [('direct', T)]

    def legs(D, sgnS, sgnT):
        for ss in sgnS:
            for dt in sgnT:
                E = (-dt * T[0] - ss * S[0]) % (2 * A) or 2 * A
                yield ss, E

    two = bool(room.bot)
    # floor turn (one-sided theorem); in two-sided rooms only for top/hall pairs
    if not (two and 'bot' in (bs, bt)) and S[1] + T[1] > 0:
        D = S[1] + T[1]; f = S[1] / D
        for ss, E in legs(D, room.signs(S), room.signs(T)):
            cands = [E, E + 2 * A]
            corner = [((ss * S[0] + f * Ee) % A) == 0 for Ee in cands]
            if all(corner): continue
            pick = 0 if not corner[0] else 1
            for k, Ee in enumerate(cands):
                if corner[k]: continue
                out.append(('chosen' if k == pick else 'other', (S[0] + ss * Ee, -T[1])))
    if two:
        if not ('top' in (bs, bt)) and 2 * c - S[1] - T[1] > 0:  # roof turn for bottom/hall pairs (mirror of the floor turn)
            D = 2 * c - S[1] - T[1]; f = (c - S[1]) / D
            for ss, E in legs(D, room.signs(S), room.signs(T)):
                for Ee in (E, E + 2 * A):
                    if ((ss * S[0] + f * Ee) % A) != 0:
                        out.append(('roofturn', (S[0] + ss * Ee, 2 * c - T[1])))
        if {bs, bt} != {'hall'} and not (bs == bt):  # opposite banks or bank-hall: direct traversal
            for ss, E in legs(abs(T[1] - S[1]), room.signs(S), room.signs(T)):
                for Ee in (E, E + 2 * A):
                    out.append(('traverse', (S[0] + ss * Ee, T[1])))
    return out


# ------------------------------------------------------------------ cross-check of the stepper
def crosscheck(room, n=1500):
    pts = half_points(room.cells)
    bad = cnt = 0
    k = 0
    for S, T in combinations(pts, 2):
        k += 1
        if k % 7: continue
        for lab, B in family(room, S, T)[:2]:
            if B == T and (S[0] == T[0] or S[1] == T[1]): continue
            ev, end, con = trace(room.P, S, B)
            a = ev == 'end' and end == T
            b = shot_ok(room, S, B, T)
            cnt += 1; bad += a != b
            if cnt >= n: return cnt, bad
    return cnt, bad


# ------------------------------------------------------------------ lit search
DIRS = sorted({(p // gcd(abs(p), abs(q)), q // gcd(abs(p), abs(q)))
               for p in range(-60, 61) for q in range(-60, 61) if p and q},
              key=lambda d: (max(abs(d[0]), abs(d[1])), abs(d[0]) + abs(d[1]), d))


def search_from(room, S, targets, hall_only=False):
    """targets: set of doubled points. Returns found dict target -> (dir, cats)."""
    found = {}
    for T2 in targets:
        T = (F(T2[0], 2), F(T2[1], 2))
        if axis_clear(room, S, T):
            found[T2] = ('axis', ())
    if len(found) == len(targets): return found
    S2 = d2(S)
    for p, q in DIRS:
        walk(room.cells, S2, p, q, 40, targets=targets, found=found, c=room.c, hall_only=hall_only)
        if len(found) == len(targets): break
    return found


def exact_dark_check(room, S, T):
    """Independent Fraction re-check: does any direction (height<=60, <=40 reflections) pass T?"""
    for p, q in DIRS:
        L = 10**4
        ev, end, con = trace(room.P, S, (S[0] + L * p, S[1] + L * q), maxrefl=41)
        pts = [S] + [c_[0] for c_ in con[:40]] + ([end] if len(con) <= 40 else [con[40][0]])
        for a, b in zip(pts, pts[1:]):
            if (b[0] - a[0]) * (T[1] - a[1]) == (b[1] - a[1]) * (T[0] - a[0]) and \
               min(a[0], b[0]) <= T[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= T[1] <= max(a[1], b[1]) and T != a:
                return (p, q)
    for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if axis_clear(room, S, T): return d
    return None


def coarse(cats):
    if not cats: return 'straight'
    if any(k.startswith('arm') or k.startswith('bank') for k in cats): return 'uses attachment walls'
    nf = cats.count('floor') + cats.count('roof')
    return 'hall sides only' if nf == 0 else f'hall walls only, {nf} floor/roof'


def sig(cats):
    if not cats: return 'straight'
    C = Counter(cats)
    return '+'.join(f"{k}x{C[k]}" for k in sorted(C))


# ------------------------------------------------------------------ main
log("# d164 attack on stacked halls (parallel-mouth-combs.md)")
cnt, bad = crosscheck(ROOMS[0]); log(f"stepper vs d162 Fraction tracer, room A2: {cnt} shots, disagreements {bad}")
cnt, bad = crosscheck(DB55); log(f"stepper vs d162 Fraction tracer, DB55: {cnt} shots, disagreements {bad}")
# search consistency: on A4 every pair the family lights must also be found by the search
r4 = ROOMS[1]; pts4 = half_points(r4.cells); miss = tot = 0
for S in [p for p in pts4 if r4.bank(p) == 'top']:
    tg = set()
    for T in pts4:
        if T == S: continue
        for lab, B in family(r4, S, T):
            vx, vy = int(2 * (B[0] - S[0])), int(2 * (B[1] - S[1]))
            g = gcd(abs(vx), abs(vy))
            if vx and vy and max(abs(vx), abs(vy)) // g <= 60 and shot_ok(r4, S, B, T):
                ev, end, con = trace(r4.P, S, B)
                if len(con) <= 40: tg.add(d2(T)); break
    fnd = search_from(r4, S, tg); tot += len(tg); miss += len(tg) - len(fnd)
log(f"search consistency on A4: {tot} family-lit pairs within bounds, missed by search {miss}")
log(f"search directions: {len(DIRS)} primitive non-axis (height <= 60) + 4 axis; <= 40 reflections\n")

summary = []
first_fail = None
for room in ROOMS:
    t0 = time.process_time()
    pts = half_points(room.cells)
    out_pts = [p for p in pts if room.bank(p) != 'hall' or p[1] in (0, room.c)]
    hall_open = [p for p in pts if 0 < p[1] < room.c]
    pairs = [(S, T) for S in out_pts for T in hall_open] + list(combinations(out_pts, 2))
    chosen_fail, fam_fail = [], []
    lab_stats = Counter()
    for S, T in pairs:
        fam = family(room, S, T)
        okc = okf = False
        for lab, B in fam:
            ok = shot_ok(room, S, B, T)
            lab_stats[(lab, ok)] += 1
            if ok:
                okf = True
                if lab in ('chosen', 'direct'): okc = True
        if not okc and room.bot == [] : chosen_fail.append((S, T))
        if not okf: fam_fail.append((S, T))
    nW = len(room.P)
    log(f"## {room.name}")
    log(f"   W={nW}, max 8Ah/(cu): top {room.ratio_top}, bottom {room.ratio_bot}; marks {len(pts)}, "
        f"pairs tested {len(pairs)} (open-hall pairs are convex chords, not traced)")
    log(f"   shots traced [label: ok/fail]: " + ", ".join(f"{l}: {lab_stats[(l, True)]}/{lab_stats[(l, False)]}"
                                                     for l in ('direct', 'chosen', 'other', 'roofturn', 'traverse')
                                                     if lab_stats[(l, True)] + lab_stats[(l, False)]))
    if not room.bot:
        log(f"   pairs where the note's chosen shot fails for every allowed sign: {len(chosen_fail)}")
    log(f"   pairs where the whole family fails: {len(fam_fail)}"
        + (f"; e.g. {[(fr(a), fr(b)) for a, b in fam_fail[:3]]}" if fam_fail else ""))
    if fam_fail and first_fail is None: first_fail = room.name
    # lit search on family failures, greedy by endpoint
    lit = {}; dark = []; unres = []
    if fam_fail:
        rem = {}
        for S, T in fam_fail:
            rem.setdefault(S, set()).add(T); rem.setdefault(T, set()).add(S)
        while rem:
            if time.process_time() - T0 > BUDGET:
                unres = sorted({tuple(sorted((a, b))) for a in rem for b in rem[a]}); break
            S = max(rem, key=lambda k: (len(rem[k]), k))
            tg = {d2(T) for T in rem[S]}
            found = search_from(room, S, tg)
            for T in list(rem[S]):
                key = tuple(sorted((S, T)))
                if d2(T) in found: lit[key] = found[d2(T)]
                else: dark.append(key)
                rem[T].discard(S)
                if not rem[T]: del rem[T]
            del rem[S]
        mech = Counter(sig(v[1]) for v in lit.values())
        hts = Counter(max(abs(v[0][0]), abs(v[0][1])) if v[0] != 'axis' else 0 for v in lit.values())
        log(f"   lit by search: {len(lit)}/{len(fam_fail)}; max direction height used {max(hts) if hts else '-'}; "
            f"max reflections {max((len(v[1]) for v in lit.values()), default=0)}")
        log(f"   mechanisms (reflection multiset of first path found): {dict(mech.most_common(6))}")
        need = [k for k, v in lit.items() if coarse(v[1]) == 'uses attachment walls']
        bysrc = {}
        for a, b in need: bysrc.setdefault(a, set()).add(d2(b))
        still, hc, ex_need = 0, Counter(), None
        for a, tg in sorted(bysrc.items()):
            fh = search_from(room, a, tg, hall_only=True)
            still += len(tg) - len(fh)
            hc.update(coarse(v[1]) for v in fh.values())
            if ex_need is None and len(fh) < len(tg):
                b2 = min(tg - set(fh)); b = (F(b2[0], 2), F(b2[1], 2))
                ex_need = (a, b, lit[tuple(sorted((a, b)))])
        log(f"   pairs whose first path uses attachment walls: {len(need)}; of these, no hall-walls-only path "
            f"(same bounds): {still}; hall-only paths found: {dict(hc.most_common(4))}")
        if ex_need:
            log(f"      needs attachment wall, e.g. {fr(ex_need[0])}-{fr(ex_need[1])}: dir {ex_need[2][0]}, "
                f"reflections {list(ex_need[2][1])}")
        log(f"   coarse: {dict(Counter(coarse(v[1]) for v in lit.values()).most_common())}")
        ex = sorted(lit.items())[:2]
        for (a, b), v in ex:
            log(f"      e.g. {fr(a)}-{fr(b)}: dir {v[0]}, reflections {list(v[1])}")
        if dark:
            log(f"   NO PATH within bounds: {len(dark)} pairs: {[(fr(a), fr(b)) for a, b in dark[:6]]}")
            for a, b in dark[:3]:
                r = exact_dark_check(room, a, b)
                log(f"      Fraction re-check {fr(a)}-{fr(b)}: {'lit by ' + str(r) if r else 'still no path'}")
        if unres:
            log(f"   UNRESOLVED (budget): {len(unres)} pairs")
    log(f"   CPU {time.process_time() - t0:.1f}s\n")
    summary.append((room.name.split(':')[0], nW, len(pairs), len(chosen_fail) if not room.bot else '-',
                    len(fam_fail), len(lit), len(dark), len(unres)))

log("# Summary: room, W, pairs, chosen-shot fails, family fails, lit by search, no path, unresolved")
for s in summary:
    log("   " + " | ".join(str(x) for x in s))
log(f"first room where the shot family fails: {first_fail}")
log(f"\nCPU {time.process_time() - T0:.1f}s")
