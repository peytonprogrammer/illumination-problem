"""d224 referee checks: seam parity and the band multi-twist.

Rooms: the d223 hand-made axial room P (area 22, 8 reflexes) and one more hand-made axial
room R2 (area 22, 4 reflexes) whose bands have height 2, so lattice marks can sit strictly inside
a band. Exact rational billiard traces along hand-chosen directions and their sheared images only.
The only loops over marks run over the interior lattice points of these two named rooms, and the
only loop over lambda runs over one period of the band arithmetic.
No room enumeration, no ray/direction/word/room-size search, no network.
Run: nice -n 10 python3 -B checks.py > checks.log
"""
import time
from fractions import Fraction as Fr
from math import floor, ceil, gcd

T0 = time.process_time()
FAIL = []


def check(cond, msg):
    print(('PASS ' if cond else 'FAIL ') + msg, flush=True)
    if not cond:
        FAIL.append(msg)


def lcm(*a):
    r = 1
    for x in a:
        r = r * x // gcd(r, x)
    return r


# ------------------------------------------------------------------ rooms (axis x = 0)
def room_data(cells):
    pts = set()
    for (x, y) in cells:
        for dx in (0, 1):
            for dy in (0, 1):
                pts.add((x + dx, y + dy))
    info = {}
    for (X, Y) in pts:
        pres = [c in cells for c in ((X - 1, Y - 1), (X, Y - 1), (X - 1, Y), (X, Y))]
        k = sum(pres)
        if k == 4:
            kind = 'interior'
        elif k == 3:
            kind = 'reflex'
        elif k == 1:
            kind = 'convex'
        else:
            kind = 'pinch' if pres in ([True, False, False, True], [False, True, True, False]) else 'smooth'
        info[(X, Y)] = kind
    return info


def mirror(cells):
    return {(-1 - x, y) for (x, y) in cells}


H1 = {(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2), (0, 3), (1, 3), (2, 1), (2, 3), (0, 4)}  # d223
H2 = {(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (0, 3), (1, 3), (0, 4), (1, 4)}  # new
ROOMS = {}
for name, H in (('P(d223)', H1), ('R2', H2)):
    Pc = H | mirror(H)
    info = room_data(Pc)
    infoH = room_data(H)
    r = sum(1 for k in info.values() if k == 'reflex')
    walls = sum(1 for k in info.values() if k in ('reflex', 'convex'))
    seam_ends = sorted(p for p, k in info.items() if p[0] == 0 and k != 'interior')
    ok = (len(Pc) == 22 and not any(k == 'pinch' for k in info.values())
          and len(seam_ends) == 2 and all(info[p] == 'smooth' for p in seam_ends)
          and all(infoH[p] == 'convex' for p in seam_ends))
    print(f'     {name}: area {len(Pc)}, reflexes {r}, walls {walls}, seam ends {seam_ends}')
    check(ok, f'{name}: area 22, no pinch, axis meets boundary at two smooth points that are convex corners of H')
    ROOMS[name] = dict(P=Pc, H=H, info=info, infoH=infoH, E=seam_ends)


# ------------------------------------------------------------------ bands (horizontal cylinders of Q)
def bands(cells):
    """maximal runs of rows with the same slice interval [a,b]; returns (y0,y1,a,b)."""
    rows = {}
    for (x, y) in cells:
        rows.setdefault(y, set()).add(x)
    ivs = {}
    for y, xs in rows.items():
        xs = sorted(xs)
        cur = [xs[0], xs[0]]
        out = []
        for x in xs[1:]:
            if x == cur[1] + 1:
                cur[1] = x
            else:
                out.append((cur[0], cur[1] + 1))
                cur = [x, x]
        out.append((cur[0], cur[1] + 1))
        ivs[y] = out
    res = []
    for y in sorted(ivs):
        for iv in ivs[y]:
            # extend an existing band ending at y with the same interval
            for k, (y0, y1, a, b) in enumerate(res):
                if y1 == y and (a, b) == iv:
                    res[k] = (y0, y + 1, a, b)
                    break
            else:
                res.append((y, y + 1, iv[0], iv[1]))
    return res


def band_of(B, x, y):
    for (y0, y1, a, b) in B:
        if y0 < y < y1 and a <= x <= b:
            return (y0, y1, a, b)
    return None


def phi(B, lam, x, y, sheet):
    """the multi-twist (xi,d) -> (xi + lam d mod 2W, d) on Q, in physical coords + sheet."""
    bd = band_of(B, x, y)
    if bd is None:
        return (x, y, sheet)
    y0, y1, a, b = bd
    W = b - a
    d = y - y0
    xi = (x - a) if sheet == 0 else (W + b - x)
    xi2 = (xi + lam * d) % (2 * W)
    if xi2 <= W:
        return (a + xi2, y, 0)
    return (b - (xi2 - W), y, 1)


# ------------------------------------------------------------------ exact tracer
def trace(cells, start, vel, targets=(), stop_time=None, max_steps=20000, axis=0):
    """Exact billiard in the union of unit cells.  Returns dict(kind, pt, time, sheet, events, axis_cross,
    seam_walls).  kind: 'hit' (first target), 'time' (stop_time reached), 'stop' (corner/outside)."""
    info = room_data(cells)
    px, py = Fr(start[0]), Fr(start[1])
    vx, vy = Fr(vel[0]), Fr(vel[1])
    t = Fr(0)
    sheet = 0
    ev = []
    cross = 0
    seamw = 0
    tg = [(Fr(a), Fr(b)) for (a, b) in targets]
    for _ in range(max_steps):
        tx = ty = None
        if vx != 0:
            nx_ = (floor(px) + 1) if vx > 0 else (ceil(px) - 1)
            tx = (nx_ - px) / vx
        if vy != 0:
            ny_ = (floor(py) + 1) if vy > 0 else (ceil(py) - 1)
            ty = (ny_ - py) / vy
        dt = min(s for s in (tx, ty) if s is not None)
        best = None
        for (a, b) in tg:
            tau = (a - px) / vx if vx != 0 else ((b - py) / vy if vy != 0 else None)
            if tau is None or not (0 < tau <= dt):
                continue
            if px + vx * tau == a and py + vy * tau == b and (best is None or tau < best[0]):
                best = (tau, (a, b))
        if best is not None:
            return dict(kind='hit', pt=best[1], time=t + best[0], sheet=sheet, events=ev, axis_cross=cross,
                        seam_walls=seamw)
        if stop_time is not None and t + dt >= stop_time:
            tau = stop_time - t
            return dict(kind='time', pt=(px + vx * tau, py + vy * tau), time=stop_time, sheet=sheet, events=ev,
                        axis_cross=cross, seam_walls=seamw)
        px, py, t = px + vx * dt, py + vy * dt, t + dt
        if px.denominator == 1 and py.denominator == 1:
            P = (int(px), int(py))
            kind = info.get(P, 'outside')
            if kind == 'interior':
                ev.append(('pass', P))
                if P[0] == axis:
                    cross += 1
                continue
            if kind == 'smooth':
                cs = [(P[0] - 1, P[1] - 1), (P[0], P[1] - 1), (P[0] - 1, P[1]), (P[0], P[1])]
                pres = [c in cells for c in cs]
                if pres in ([True, True, False, False], [False, False, True, True]):
                    vy = -vy
                else:
                    vx = -vx
                    if P[0] == axis:
                        seamw += 1
                sheet ^= 1
                ev.append(('wall-lattice', P))
                continue
            return dict(kind='stop', pt=P, why=kind, time=t, sheet=sheet, events=ev, axis_cross=cross,
                        seam_walls=seamw)
        if px.denominator == 1 and dt == tx:
            x0 = int(px)
            yc = floor(py)
            nxt = (x0, yc) if vx > 0 else (x0 - 1, yc)
            if nxt not in cells:
                vx = -vx
                sheet ^= 1
                ev.append(('wall', (px, py)))
                if x0 == axis:
                    seamw += 1
            elif x0 == axis:
                cross += 1
        else:
            y0 = int(py)
            xc = floor(px)
            nxt = (xc, y0) if vy > 0 else (xc, y0 - 1)
            if nxt not in cells:
                vy = -vy
                sheet ^= 1
                ev.append(('wall', (px, py)))
    return dict(kind='stop', why='max', pt=None, time=t, sheet=sheet, events=ev, axis_cross=cross, seam_walls=seamw)


def sig(p):
    return (-p[0], p[1])


def legal(res, E):
    """reached a target without stopping and without visiting a seam end."""
    return res['kind'] == 'hit' and not any(p in E for _, p in res['events'] if isinstance(p, tuple)
                                             and all(isinstance(c, int) for c in p))


def shear_test(name, S, T, vel, lam, K=9):
    """trace S->{T,sigma T} in P; apply the shear; check image ray, H parity and pointwise phi."""
    R = ROOMS[name]
    P, H, E = R['P'], R['H'], R['E']
    B = bands(P)
    S = (Fr(S[0]), Fr(S[1]))
    T = (Fr(T[0]), Fr(T[1]))
    o = trace(P, S, vel, [T, sig(T)])
    vel2 = (vel[0] + lam * vel[1], vel[1])
    im = trace(P, S, vel2, [T, sig(T)])
    oH = trace(H, S, vel, [T])
    imH = trace(H, S, vel2, [T])
    show = lambda p: '(' + ', '.join(str(c) for c in p) + ')'
    print(f'     [{name}] S={show(S)} T={show(T)} lambda={lam}')
    print(f'       original vel {vel}: {o["kind"]} {show(o["pt"]) if o["pt"] else o.get("why")}, '
          f'axis crossings {o["axis_cross"]}, walls {sum(1 for e in o["events"] if e[0] != "pass")}; '
          f'H: {oH["kind"]}, seam contacts {oH["seam_walls"]}')
    print(f'       image    vel {vel2}: {im["kind"]} {show(im["pt"]) if im["pt"] else im.get("why")}, '
          f'axis crossings {im["axis_cross"]}, walls {sum(1 for e in im["events"] if e[0] != "pass")}; '
          f'H: {imH["kind"]}, seam contacts {imH["seam_walls"]}')
    ok = legal(o, E) and legal(im, E) and oH['kind'] == 'hit' and imH['kind'] == 'hit'
    # physical image of the endpoint and of sampled interior points
    ex = phi(B, lam, o['pt'][0], o['pt'][1], o['sheet'])
    ok_end = ok and (im['pt'], im['sheet']) == ((ex[0], ex[1]), ex[2])
    pw = True
    for k in range(1, K + 1):
        tk = o['time'] * Fr(3 * k - 1, 3 * K + 2)
        a = trace(P, S, vel, stop_time=tk)
        b = trace(P, S, vel2, stop_time=tk)
        fa = phi(B, lam, a['pt'][0], a['pt'][1], a['sheet'])
        bd = band_of(B, fa[0], fa[1])
        on_vwall = bd is not None and fa[0] in (bd[2], bd[3])  # sheet label is ambiguous on a vertical wall
        same = (fa[0], fa[1]) == b['pt'] and (fa[2] == b['sheet'] or on_vwall)
        pw = pw and a['kind'] == 'time' and b['kind'] == 'time' and same
    return dict(o=o, im=im, oH=oH, imH=imH, ok=ok, ok_end=ok_end, pw=pw, T=T)


# ================================================================== claim 3: geometry of the twist
print('== Claim 3: band multi-twist')
for name in ROOMS:
    B = bands(ROOMS[name]['P'])
    print(f'     {name} bands (y0,y1,a,b): {B}')
    check(all(a + b == 0 for (_, _, a, b) in B), f'{name}: every slice interval is centered on the axis x=0')
    # translation by W (half circumference) sends front x to rear -x, i.e. to a lift of sigma
    good = True
    for (y0, y1, a, b) in B:
        W = b - a
        for xn in range(4 * W + 1):
            x = a + Fr(xn, 4)
            for sh in (0, 1):
                y = Fr(y0) + Fr(1, 2) if y1 - y0 == 1 else Fr(y0) + Fr(1, 3)
                d = y - y0
                lam = W / d  # lam*d = W exactly
                X, Y, s2 = phi([(y0, y1, a, b)], lam, x, y, sh)
                good = good and X == -x and (s2 != sh or x in (a, b))
    check(good, f'{name}: translation by W (not 2W) maps each lift (x, sheet) to (-x, other sheet)')
    # a non-centered interval: the same translation is the reflection about (a+b)/2, not sigma
    a, b = 0, 4
    X, _, _ = phi([(0, 1, a, b)], 8, Fr(1), Fr(1, 2), 0)
    check(X == a + b - 1 and X != -1, f'{name}: on a non-centered interval the half turn gives a+b-x, not sigma x')
    # band maps fix boundary circles: lam*h = 0 mod 2W
    L = lcm(*[2 * (b - a) // gcd(2 * (b - a), y1 - y0) for (y0, y1, a, b) in B])
    fixed = all(phi(B, L, a + Fr(k, 3), Fr(y), sh)[:2] == (a + Fr(k, 3), Fr(y))
                for (y0, y1, a, b) in B for y in (y0, y1) for k in range(3 * (b - a) + 1) for sh in (0, 1))
    top = all(((a + Fr(k, 3) - a + L * (y1 - y0)) % (2 * (b - a))) == (Fr(k, 3) % (2 * (b - a)))
              for (y0, y1, a, b) in B for k in range(3 * (b - a)))
    corners = [p for p, k in ROOMS[name]['info'].items() if k in ('convex', 'reflex')] + ROOMS[name]['E']
    cfix = all(band_of(B, Fr(p[0]), Fr(p[1])) is None for p in corners)
    check(fixed and top and cfix, f'{name}: L={L}; the shear is the identity on every band boundary; '
                                  f'all {len(corners)} corners and seam ends lie on band boundaries')

# lattice marks strictly inside a band
for name in ROOMS:
    info = ROOMS[name]['info']
    B = bands(ROOMS[name]['P'])
    marks = sorted(p for p, k in info.items() if k == 'interior' and p[0] != 0)
    inside = [p for p in marks if band_of(B, p[0], p[1]) is not None]
    print(f'     {name}: off-axis interior lattice marks {len(marks)}, strictly inside a band {inside}')
    ROOMS[name]['marks'] = marks
check(ROOMS['P(d223)']['marks'] and not [p for p in ROOMS['P(d223)']['marks']
                                         if band_of(bands(ROOMS['P(d223)']['P']), p[0], p[1])],
      'd223 room: every band has height 1, so every lattice mark is on a band boundary (test vacuous)')

# ------------------------------------------------------------------ exact sheared rays
print('-- d223 room, control: lattice marks are fixed, parity does not change')
r = shear_test('P(d223)', (1, 1), (1, 3), (-1, 1), 24)
check(r['ok'] and r['o']['pt'] == r['im']['pt'] == sig(r['T']) and r['ok_end'] and r['pw'],
      'd223: shear lambda=24 of the d223 ray S=(1,1)->sigma T=(-1,3) is legal and still reaches sigma T')

print('-- d223 room, rational targets strictly inside the row-1 band (W=6)')
for (T, vel, lam) in (((Fr(1, 2), Fr(5, 4)), (-2, 1), 24), ((Fr(1, 2), Fr(25, 16)), (8, 1), 96)):
    d = T[1] - 1
    check((lam * d) % 12 == 6 and lam % 24 == 0, f'lambda={lam}: multiple of L=24 and lambda*d = W mod 2W (d={d})')
    r = shear_test('P(d223)', (1, 1), T, vel, lam)
    check(r['ok'] and r['o']['pt'] == r['T'] and r['im']['pt'] == sig(r['T'])
          and r['oH']['seam_walls'] % 2 == 0 and r['imH']['seam_walls'] % 2 == 1,
          f'd223 T={T}: original reaches T (even), image is legal, reaches sigma T, H-parity odd')
    check(r['ok_end'] and r['pw'], 'image endpoint and 9 sampled points equal phi(original) in Q (exact)')

print('-- R2, lattice marks: S=(1,1) in band [0,2] (W=6), T=(1,4) in band [3,5] (W=4)')
B2 = bands(ROOMS['R2']['P'])
r = shear_test('R2', (1, 1), (1, 4), (-2, 3), 12)
check(r['ok'] and r['o']['pt'] == sig(r['T']) and r['im']['pt'] == r['T']
      and r['oH']['seam_walls'] % 2 == 1 and r['imH']['seam_walls'] % 2 == 0,
      'R2: direct ray S->sigma T (odd); shear lambda=12 gives a legal ray S->T (even) in P and in H')
check(r['ok_end'] and r['pw'], 'R2: image endpoint and 9 sampled points across three bands equal phi(original)')
r = shear_test('R2', (1, 1), (1, 4), (-2, 3), -12)
check(r['ok'] and r['im']['pt'] == r['T'] and r['pw'], 'R2: the inverse twist lambda=-12 also works')


# ------------------------------------------------------------------ divisibility test vs brute force
def band_data(B, p):
    bd = band_of(B, p[0], p[1])
    if bd is None:
        return None
    y0, y1, a, b = bd
    return (b - a, p[1] - y0, a, b)


def phys(B, lam, p, sheet):
    X, Y, s = phi(B, lam, Fr(p[0]), Fr(p[1]), sheet)
    return (X, Y)


print('-- divisibility test gcd(L_s d_t, 2W_t) | W_t versus brute force over one lambda period')
for name in ROOMS:
    B = bands(ROOMS[name]['P'])
    L = lcm(*[2 * (b - a) // gcd(2 * (b - a), y1 - y0) for (y0, y1, a, b) in B])
    M = lcm(*[2 * (b - a) for (_, _, a, b) in B]) * L
    marks = ROOMS[name]['marks']
    npair = mism = note_pass = gen_pass = rev_pass = 0
    passing, gen_only = [], []
    for S in marks:
        for T in marks:
            if T in (S, sig(S)):
                continue
            npair += 1
            sd, td = band_data(B, S), band_data(B, T)
            # note's test
            if td is None:
                pred = False
            else:
                Wt, dt_, _, _ = td
                Ls = L if sd is None else lcm(L, 2 * sd[0] // gcd(2 * sd[0], sd[1]))
                pred = Wt % gcd(Ls * dt_, 2 * Wt) == 0
            brute = any(phys(B, lam, S, 0) == S and phys(B, lam, S, 1) == S
                        and phys(B, lam, T, 0) == sig(T) and phys(B, lam, T, 1) == sig(T)
                        for lam in range(0, M, L))
            mism += pred != brute
            note_pass += pred
            if pred:
                passing.append((S, T))
            # generalized: start lift either sheet, S only physically fixed or swapped, exactly one swap
            gen = False
            for lam in range(0, M, L):
                for sh in (0, 1):
                    s_im = phys(B, lam, S, sh)
                    for tsh in (0, 1):
                        t_im = phys(B, lam, T, tsh)
                        if s_im in (S, sig(S)) and t_im in (T, sig(T)) and ((s_im == S) != (t_im == T)):
                            gen = True
            gen_pass += gen
            if gen and not pred:
                gen_only.append((S, T))
    print(f'     {name}: L={L}, ordered off-axis pairs in distinct orbits {npair}; note test passes {note_pass}; '
          f'generalized horizontal-twist condition passes {gen_pass}')
    print(f'       note-test pairs: {passing}')
    print(f'       pairs passing only the generalized condition: {gen_only}')
    check(mism == 0, f'{name}: note divisibility test equals brute force in all {npair} ordered pairs')
    check(gen_pass >= note_pass, f'{name}: generalized condition contains the note test')

# ================================================================== claim 4: seam-end partner
print('== Claim 4: path through a smooth seam end (R2, E=(0,5))')
P2, E2 = ROOMS['R2']['P'], ROOMS['R2']['E']
res = trace(P2, (1, 1), (-1, 4), [(-1, 1)])
print(f'     T=(1,1) vel (-1,4): {res["kind"]} {res["pt"]}; events {res["events"]}')
check(res['kind'] == 'hit' and res['pt'] == (-1, 1) and ('wall-lattice', (0, 5)) in res['events'],
      'partner: T -> seam end E (transverse) -> sigma T is legal; reflection at E is diag(1,-1) = -D sigma')
res = trace(P2, (2, 1), (-1, 4), [(-1, 1)])
seq = [e for e in res['events']]
print(f'     known ray extended: S=(2,1) vel (-1,4): {res["kind"]} {res["pt"]}; events {seq}')
passT = ('pass', (1, 1)) in seq and ('wall-lattice', (0, 5)) in seq
check(res['kind'] == 'hit' and res['pt'] == (-1, 1) and passT and
      seq.index(('pass', (1, 1))) < seq.index(('wall-lattice', (0, 5))),
      'extension: one straight itinerary S=(2,1) -> T=(1,1) -> E -> sigma T, lights both T and sigma T')
resH = trace(ROOMS['R2']['H'], (2, 1), (-1, 4), [(Fr(-1), Fr(1))])
check(resH['kind'] == 'stop' and resH['why'] == 'convex', 'the extended itinerary stops at the convex seam end in H')

# ================================================================== claim 1: seam character on N
print('== Claim 1: seam parity')
for name, (S, vel, tgt) in (('P(d223)', ((1, 1), (-1, 1), (1, 3))), ('R2', ((1, 1), (-2, 3), (1, 4)))):
    R = ROOMS[name]
    a = trace(R['H'], S, vel, [tgt])
    b = trace(R['P'], S, vel, [tgt, sig(tgt)])
    check(a['kind'] == b['kind'] == 'hit' and (b['pt'] == tgt) == (a['seam_walls'] % 2 == 0)
          and a['seam_walls'] == b['axis_cross'],
          f'{name}: H seam contacts ({a["seam_walls"]}) = P axis crossings; even <-> T, odd <-> sigma T')
# seam-adjacent horizontal cylinder of H: its core leaf in N crosses beta once (odd character)
for name in ROOMS:
    BH = bands(ROOMS[name]['H'])
    odd = [bd for bd in BH if bd[2] == 0]
    check(all(bd[2] == 0 for bd in BH), f'{name}: every horizontal cylinder of H touches the seam, '
                                         f'so its core crosses beta once in N (odd character)')

print(f'CPU {time.process_time() - T0:.1f}s')
print(f'FAILURES: {len(FAIL)}' + (' -- ' + '; '.join(FAIL) if FAIL else ''))
