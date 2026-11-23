"""Double-resonance instances (H and E both fail): try the viewer back-wall
families B, BE, then a bounded image enumeration on each fixed instance.
Usage: python3 -B double.py > logs/double.log"""
import time, resource, itertools
from fractions import Fraction as Fr
from build import config, DOOR
from door_geom import behind
from families import light, window_exists
from exact import trace
import tests_lib as TL
resource.setrlimit(resource.RLIMIT_CPU, (300, 300))
t0 = time.process_time()


def images(cs, v, depth, R, centre):
    out = {v}; fr = {v}
    for _ in range(depth):
        nf = set()
        for x in fr:
            for c in cs:
                y = 2 * c - x
                if abs(y - centre) <= R and y not in out: nf.add(y)
        out |= nf; fr = nf
    return out


def enum_lit(room, S, T, depth, R):
    X = images(room.xs, T[0], depth, R, S[0]); Y = images(room.ys, T[1], depth, R, S[1])
    cand = sorted(((x - S[0]) ** 2 + (y - S[1]) ** 2, x, y) for x in X for y in Y if x != S[0] and y != S[1])
    for i, (_, x, y) in enumerate(cand):
        ok, nref, why = trace(room, S, (x - S[0], y - S[1]), T, maxhits=400)
        if ok: return ('lit', nref, (x - S[0], y - S[1]), i + 1, len(cand))
    return ('no path found', None, None, len(cand), len(cand))


for mask, S, T in DOOR:
    for k in (4, 8):
        try:
            room, geo, info = TL.resonant(mask, S, T, k, 'double')
        except AssertionError:
            continue
        a, b, p, q, d, Sv, Tc = geo
        h, D, ell = Tc[1] - d, d - Sv[1], info['ell']
        if window_exists(geo, h, D) or window_exists(geo, 2 * ell - h, D):
            continue                                            # not a double failure
        o = config(mask, S, T)[7]
        A, B, P, Q, Dd = info['cfg']
        c0, kind = behind(o, A, B, info['V'])
        c = room.ys[c0 // 2]
        res = [f'{mask} {S} {T} k={k} back={kind}']
        for nm, fam in (('B', (h, D + 2 * (Sv[1] - c), -1)), ('BE', (2 * ell - h, D + 2 * (Sv[1] - c), -1))):
            st, nref, vec, tried = light(room, geo, fam)
            res.append(f'{nm}:{st}/{nref} win={window_exists(geo, fam[0], fam[1])} tried={tried}')
        r = enum_lit(room, Sv, Tc, 4, Fr(40))
        res.append(f'enum:{r[0]} refl={r[1]} vec=({float(r[2][0]):.4f},{float(r[2][1]):.4f}) S=({float(Sv[0]):.4f},{float(Sv[1]):.4f}) T=({float(Tc[0]):.4f},{float(Tc[1]):.4f})' if r[2] else f'enum:{r}')
        print(' '.join(res), flush=True)
print('cpu', round(time.process_time() - t0, 1))
