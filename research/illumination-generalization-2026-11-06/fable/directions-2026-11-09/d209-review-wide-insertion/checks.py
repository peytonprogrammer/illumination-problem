"""D209 referee checks: wide insertion and terminal-cap collar lemma.

Exact rational billiard tracer (fractions.Fraction). Only the named rooms
(rank 11 and rank 18 of the a21 archive) plus one hand-built probe room for
the lemma. Run: nice -n 10 python3 -B checks.py
"""
from fractions import Fraction as F
from math import gcd, lcm
import random, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
A21 = HERE.parent / "seed-profile-a21"
DIRS = [(x, s - x) for s in range(1, 41) for x in range(s, -1, -1) if gcd(x, s - x) == 1]
T0 = time.process_time()


# ---------------------------------------------------------------- geometry
def cells_of(rows):
    return {(x, y) for y, r in enumerate(rows) for x in range(r.bit_length()) if r >> x & 1}


def marks_of(rows):
    c = cells_of(rows)
    return sorted([(x, y) for x, y in c if {(x - 1, y), (x, y - 1), (x - 1, y - 1)} <= c],
                  key=lambda p: (p[1], p[0]))


def segments(rows):
    """Maximal wall segments: ('v', k, lo, hi) for x=k, ('h', k, lo, hi) for y=k."""
    c = cells_of(rows)
    vu, hu = set(), set()
    for x, y in c:
        if (x - 1, y) not in c: vu.add((x, y))
        if (x + 1, y) not in c: vu.add((x + 1, y))
        if (x, y - 1) not in c: hu.add((y, x))
        if (x, y + 1) not in c: hu.add((y + 1, x))
    segs = []
    for kind, units in (('v', vu), ('h', hu)):
        for k, lo in sorted(units):
            if (k, lo - 1) in units: continue
            hi = lo
            while (k, hi) in units: hi += 1
            segs.append((kind, k, lo, hi))
    return segs


class Room:
    def __init__(self, rows, zone=None):
        self.rows = rows
        self.segs = segments(rows)
        self.corners = {(F(s[1]), F(e)) if s[0] == 'v' else (F(e), F(s[1]))
                        for s in self.segs for e in (s[2], s[3])}
        self.zone = zone  # (a, w, zlo, zhi): open fast rectangle with full side walls

    def trace(self, S, v, tmax, T=None, watch=None):
        """Trace from S with velocity v for time tmax.
        Returns dict(ok, corner, hitT (time or None), refl, events) where
        events records floor hits and downward crossings of y=watch."""
        px, py = F(S[0]), F(S[1]); vx, vy = F(v[0]), F(v[1]); t = F(0)
        Tx, Ty = (F(T[0]), F(T[1])) if T else (None, None)
        out = dict(corner=None, hitT=None, refl=0, floor=[], cross=[])
        while t < tmax:
            rem = tmax - t
            z = self.zone
            if z and vy and z[2] < py < z[3] and z[0] <= px <= z[0] + z[1]:
                a, w = z[0], z[1]
                te = ((z[3] if vy > 0 else z[2]) - py) / vy
                te = min(te, rem)
                if T and out['hitT'] is None and z[2] <= Ty <= z[3]:
                    ts = (Ty - py) / vy
                    if 0 <= ts <= te and self._fold(px, vx, ts, a, w)[0] == Tx:
                        out['hitT'] = t + ts
                nx, nvx, nb = self._fold(px, vx, te, a, w)
                out['refl'] += nb
                px, py, vx, t = nx, py + vy * te, nvx, t + te
                continue
            best, hit = rem, None
            for kind, k, lo, hi in self.segs:
                if kind == 'v':
                    if not vx: continue
                    s = (k - px) / vx
                    if 0 < s <= best:
                        yy = py + vy * s
                        if lo <= yy <= hi:
                            if s < best or hit is None: best, hit = s, (kind, k, lo, hi, yy)
                else:
                    if not vy: continue
                    s = (k - py) / vy
                    if 0 < s <= best:
                        xx = px + vx * s
                        if lo <= xx <= hi:
                            if s < best or hit is None: best, hit = s, (kind, k, lo, hi, xx)
            # target on this leg
            if T and out['hitT'] is None:
                if vx:
                    s = (Tx - px) / vx
                    if 0 <= s <= best and py + vy * s == Ty: out['hitT'] = t + s
            if watch is not None and vy < 0 and py > watch >= py + vy * best and \
                    not (py + vy * best == watch and hit is not None and hit[0] == 'h'):
                s = (watch - py) / vy
                out['cross'].append((t + s, px + vx * s))
            nx, ny = px + vx * best, py + vy * best
            t += best
            if hit is None:
                px, py = nx, ny; break
            if (nx, ny) in self.corners:
                out['corner'] = (nx, ny, t); return out
            out['refl'] += 1
            if hit[0] == 'v': vx = -vx
            else:
                vy = -vy
                if hit[1] == 0: out['floor'].append((t, nx))
            px, py = nx, ny
        out['end'] = (px, py); out['vel'] = (vx, vy)
        return out

    @staticmethod
    def _fold(px, vx, te, a, w):
        U = (px - a) if vx > 0 else 2 * w - (px - a)
        U1 = U + abs(vx) * te
        nb = int(U1 // w) - int(U // w)
        r = U1 % (2 * w)
        if r < w: return a + r, abs(vx), nb
        return a + 2 * w - r, -abs(vx), nb


def inserted(rows, j, E):
    return rows[:j + 1] + [rows[j]] * E + rows[j + 1:]


def decode(word):
    p, q = DIRS[word & 511]; sh = word >> 9 & 3
    p *= 1 - 2 * (sh & 1); q *= 1 - 2 * (sh >> 1)
    return p, q, word >> 11 & 127, word >> 18


def archive(shard, room):
    raw = subprocess.check_output([str(A21 / 'extract'), str(A21 / 'a21' / f'{shard}.bin'), str(room)],
                                  text=True).splitlines()
    rows = list(map(int, raw[0].split()))
    marks = marks_of(rows)
    words = list(map(int, raw[1].split()))
    pairs = {}
    k = 0
    for i in range(len(marks)):
        for jj in range(i + 1, len(marks)):
            pairs[marks[i], marks[jj]] = decode(words[k]); k += 1
    assert k == len(words)
    return rows, marks, pairs


def sh(m, E, cut_y):
    return (m[0], m[1] + E) if m[1] > cut_y else m


# ---------------------------------------------------------------- checks
def check_room(name, shard, room, a, w, H0, mouth, E, n_new_sample, claimed):
    print(f"\n===== {name}: shard {shard} room {room}, E={E}")
    rows, marks, pairs = archive(shard, room)
    print("rows", rows, "marks", marks)
    base = Room(rows)
    cut = F(3, 2)
    # 1. base replay periods
    periods = []
    for (S, T), (p, q, m, b) in pairs.items():
        r = base.trace(S, (p, q), F(m), T)
        assert r['corner'] is None and r['end'] == (T[0], T[1]), (S, T, r)
        # count crossings of the cut via a re-trace that records points
        cr = count_crossings(base, S, (p, q), F(m), cut)
        per = 2 * w * abs(q) // gcd(abs(p), 2 * w * abs(q)) if cr else None
        if cr: periods.append(per)
        print(f"  seed {S}->{T} dir ({p},{q}) m={m} b={b} crossings={cr} period={per}")
    P = lcm(*periods)
    print("  periods", periods, "P =", P, "(claimed", claimed['P'], ")")
    assert P == claimed['P']
    # entrance itineraries: reverse seed from lower mark to each upper mark
    lower = [mk for mk in marks if mk[1] < H0]
    upper = [mk for mk in marks if mk[1] > H0]
    assert len(lower) == 1
    L0 = lower[0]
    itin = {}
    for U in upper:
        p, q, m, b = pairs[L0, U]
        fw = base.trace(L0, (p, q), F(m), U)
        p, q = -fw['vel'][0], -fw['vel'][1]  # reversed seed starts with the negated final velocity
        r = base.trace(U, (p, q), F(m), L0, watch=H0)
        assert r['corner'] is None and r['end'] == L0
        ent = [c for c in r['cross'] if mouth[0] < c[1] < mouth[1]]
        tfirst, xfirst = ent[0]
        D = abs(q) * tfirst
        g = gcd(int(p), int(q)); u, v = abs(int(p)) // g, abs(int(q)) // g
        assert D.denominator == 1
        itin[U] = (F(p), F(q), F(u, v), u, v, int(D))
        print(f"  upper {U}: reversed dir ({p},{q}) s0={u}/{v}, D={D} (bound m|q|={m*abs(q)}), (2v-1)D={(2*v-1)*int(D)}, E+3={E+3}")
    # enlarged room
    big = inserted(rows, 1, E)
    zone = (a, w, 1, E + 1)
    R = Room(big, zone)
    Hn = H0 + E
    newm = [(x, y) for x in range(a + 1, a + w) for y in range(2, 2 + E)]
    allm = marks_of(big)
    ret = [sh(mk, E, cut) for mk in marks]
    assert sorted(allm) == sorted(ret + newm), "new-mark count mismatch"
    print(f"  marks after insertion: {len(allm)} = {len(marks)} retained + {len(newm)} new (E(w-1)={E*(w-1)})")
    # 2. retained pairs by replay
    for (S, T), (p, q, m, b) in pairs.items():
        cr = count_crossings(base, S, (p, q), F(m), cut)
        tm = F(m) + (F(cr * E, abs(q)) if cr else 0)
        S2, T2 = sh(S, E, cut), sh(T, E, cut)
        r = R.trace(S2, (p, q), tm, T2)
        ok = r['corner'] is None and r['end'] == (T2[0], T2[1])
        print(f"  replay {S2}->{T2}: legal={r['corner'] is None} endpoint_ok={ok} refl={r['refl']}")
        assert ok
    # new-new and new-lower: direct segments in the convex cap rectangle (checked symbolically)
    for N in newm:
        assert a < N[0] < a + w and 0 < N[1] < Hn
    assert a < L0[0] < a + w and 0 < L0[1] < Hn
    rngd = random.Random(1)
    direct = [(L0, N) for N in newm] + [tuple(rngd.sample(newm, 2)) for _ in range(100)]
    nd = 0
    for S, T in direct:
        r = R.trace(S, (T[0] - S[0], T[1] - S[1]), F(1), T)
        assert r['corner'] is None and r['end'] == T and r['refl'] == 0, (S, T, r)
        nd += 1
    print(f"  direct segments traced (lower-new and new-new): {nd}, all legal with 0 reflections")
    # 3/4. new-to-upper pairs by the collar construction
    rng = random.Random(209)
    sample = newm if n_new_sample is None else sorted(set(
        [newm[0], newm[-1]] + rng.sample(newm, min(n_new_sample, len(newm)))))
    stats = dict(pairs=0, ok=0, persist_fail=0, window=0, hits=0, floorcorner=0, minlegal=10**9)
    for U in upper:
        U2 = sh(U, E, cut)
        sx, sy, s0, u, v, D = itin[U]
        for N in sample:
            L = D + Hn + N[1]
            Fl = D + Hn
            lo = (u * L * D - L) // (v * D) + 1  # integers n with |n/L - u/v| < 1/(vD), n > 0
            ns = [n for n in range(max(1, lo - 2), (u * L * D + L) // (v * D) + 3)
                  if abs(F(n, L) - s0) < F(1, v * D) and n > 0]
            legal = 0
            for n in ns:
                vel = (n if sx > 0 else -n, -L if sy < 0 else L)
                r = R.trace(U2, vel, F(1), N, watch=Hn)
                stats['window'] += 1
                ent = [c for c in r['cross'] if mouth[0] < c[1] < mouth[1]]
                # persistence: first downward crossing of y=Hn is through the mouth at axial D
                first = r['cross'][0] if r['cross'] else None
                if r['corner'] is not None and (first is None or r['corner'][2] < first[0]):
                    stats['persist_fail'] += 1
                    print("   PERSIST FAIL corner", U2, N, n, L, r['corner']); continue
                if first is None or not ent or first != ent[0] or first[0] * L != D:
                    stats['persist_fail'] += 1
                    print("   PERSIST FAIL", U2, N, n, L, first, D); continue
                reached = r['corner'] is None and r['end'] == (N[0], N[1])
                if reached:
                    stats['hits'] += 1; legal += 1
                elif r['corner'] is not None and r['corner'][1] == 0:
                    # floor corner with a target image (end would be target)
                    stats['floorcorner'] += 1
            stats['pairs'] += 1
            stats['ok'] += legal > 0
            stats['minlegal'] = min(stats['minlegal'], legal)
            if legal == 0: print("   NO LEGAL SLOPE", U2, N, L, len(ns))
    print("  collar stats", stats, f"cpu {time.process_time()-T0:.1f}s")
    return R, itin


def count_crossings(room, S, v, tm, cut):
    """Number of crossings of y=cut by the exact trace (re-traced leg by leg)."""
    px, py = F(S[0]), F(S[1]); vx, vy = F(v[0]), F(v[1]); t = F(0); n = 0
    side = (py > cut) - (py < cut)
    while t < tm:
        best, hit = tm - t, None
        for kind, k, lo, hi in room.segs:
            if kind == 'v' and vx:
                s = (k - px) / vx
                if 0 < s <= best and lo <= py + vy * s <= hi: best, hit = s, 'v'
            if kind == 'h' and vy:
                s = (k - py) / vy
                if 0 < s <= best and lo <= px + vx * s <= hi: best, hit = s, 'h'
        ny = py + vy * best
        nside = (ny > cut) - (ny < cut)
        if nside and nside != side: n += 1; side = nside
        px, py, t = px + vx * best, ny, t + best
        if hit == 'v': vx = -vx
        elif hit == 'h': vy = -vy
    return n


def explicit_example():
    print("\n===== rank 11 explicit example: E=80, (3,86) -> (1,2), slope 211/44 (initial signs of the reversed seed: -x, -y)")
    rows, marks, pairs = archive(48, 1156563)
    R = Room(inserted(rows, 1, 80), (0, 2, 1, 81))
    r = R.trace((3, 86), (-422, -88), F(1), (1, 2), watch=82)
    print("  corner", r['corner'], "end", r['end'], "hitT", r['hitT'], "first entry", r['cross'][:1],
          "floor", r['floor'], "refl", r['refl'])
    assert r['corner'] is None and r['end'] == (1, 2)
    print("  D =", r['cross'][0][0] * 88, " |211/44-24/5| =", abs(F(211, 44) - F(24, 5)), "< 1/20:",
          abs(F(211, 44) - F(24, 5)) < F(1, 20))
    print("  replay period of (211,44) at w=2:", 4 * 44 // gcd(211, 4 * 44))


def probe_room():
    """Hand-built probe for the general lemma: cap width w=3, off-center targets,
    mouth (0,1) at y=2. Upper marks use hand-chosen entry directions. Check every E up to 30 and every new target; compare with the 4w criterion."""
    print("\n===== probe room: rows [7,7,1,15,15], cut y=3/2, w=3")
    rows = [7, 7, 1, 15, 15]
    base = Room(rows)
    print("  marks", marks_of(rows))
    # hand-chosen entry seeds (direction, from upper mark): checked legal by trace
    seeds = {(1, 4): (-1, -3), (2, 4): (-2, -3), (3, 4): (-3, -2)}
    res = []
    for U, (p, q) in seeds.items():
        r = base.trace(U, (p, q), F(10), watch=2)
        ent = [c for c in r['cross'] if 0 < c[1] < 1]
        if r['corner'] is not None and (not r['cross'] or r['corner'][2] < r['cross'][0][0]):
            print("  seed", U, (p, q), "hits corner first", r['corner']); continue
        if not r['cross'] or not ent or r['cross'][0] != ent[0]:
            print("  seed", U, (p, q), "no first entry via mouth", r['cross'][:2]); continue
        g = gcd(p, q); u, v = abs(p) // g, abs(q) // g
        D = int(ent[0][0] * abs(q))
        print(f"  entry seed {U} dir ({p},{q}) s0={u}/{v} D={D}")
        for E in range(1, 31):
            R = Room(inserted(rows, 1, E), (0, 3, 1, E + 1))
            Hn = 2 + E
            for N in [(x, y) for x in (1, 2) for y in range(2, 2 + E)]:
                L = D + Hn + N[1]
                crit = F(2 * L, v * D) > 12
                legal = 0; fails = 0
                for n in range(1, 4 * L):
                    if not (abs(F(n, L) - F(u, v)) < F(1, v * D)): continue
                    rr = R.trace((U[0], U[1] + E), (n if p > 0 else -n, -L if q < 0 else L), F(1), N, watch=Hn)
                    first = rr['cross'][0] if rr['cross'] else None
                    if first is None or first[0] * L != D or not (0 < first[1] < 1) or \
                       (rr['corner'] is not None and rr['corner'][2] < first[0]):
                        fails += 1
                    if rr['corner'] is None and rr['end'] == N: legal += 1
                res.append((U, E, N, crit, legal, fails))
    bad = [x for x in res if x[3] and x[4] == 0]
    pf = [x for x in res if x[5]]
    print(f"  probe cases {len(res)}, criterion-true {sum(x[3] for x in res)}, "
          f"criterion-true without legal slope {len(bad)}, persistence failures {len(pf)}")
    below = [x for x in res if not x[3]]
    print(f"  criterion-false cases {len(below)}, of which still lit by window {sum(x[4] > 0 for x in below)}")
    for x in bad[:5] + pf[:5]: print("   ", x)


if __name__ == '__main__':
    explicit_example()
    check_room("rank 11", 48, 1156563, a=0, w=2, H0=2, mouth=(0, 1), E=80, n_new_sample=None,
               claimed=dict(P=80))
    check_room("rank 11 (k=2)", 48, 1156563, a=0, w=2, H0=2, mouth=(0, 1), E=160, n_new_sample=40,
               claimed=dict(P=80))
    check_room("rank 18", 21, 4136869, a=1, w=2, H0=2, mouth=(2, 3), E=1440, n_new_sample=60,
               claimed=dict(P=1440))
    probe_room()
    print(f"\nTOTAL CPU {time.process_time()-T0:.1f}s")
