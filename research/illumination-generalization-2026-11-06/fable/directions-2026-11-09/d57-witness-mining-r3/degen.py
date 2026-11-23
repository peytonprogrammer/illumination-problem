"""Witness complexity near degenerations.

For a pair and one gap (or offset) eps -> 0 with all else fixed, find the
shortest exactly verified itinerary (float mining, then the exact point
certifier and the independent replay) and the witness radius: the largest
rho = 2^-k such that one mined itinerary is certified on the box
gap*(1 +- rho), offset +- rho*gap around the point. Prints JSON lines.
Usage: degen.py study_name"""
import sys, json, time, math
from fractions import Fraction as Fr
import wm, replay

SC = 1 << 24

STUDIES = {
    # name: (nx, ny, mask, S, T, base values, varied variable, lemma-U data)
    'door122_tab': (3, 3, 122, (1, 3), (3, 1),
                    dict(gx0=1, gx1=1, gx2=1, gy0=1, gy1=1, gy2=1, as1=.5, as2=.5, at1=.5, at2=.5), 'gx1'),
    'door122_bar': (3, 3, 122, (1, 3), (3, 1),
                    dict(gx0=1, gx1=1, gx2=1, gy0=1, gy1=1, gy2=1, as1=.5, as2=.5, at1=.5, at2=.5), 'gy1+gy2'),
    'chain4991_col0': (4, 4, 4991, (1, 7), (7, 1),
                       dict(gx0=1, gx1=1, gx2=1, gx3=1, gy0=1, gy1=1, gy2=1, gy3=1, as1=.5, as2=.5, at1=.5, at2=.5), 'gx0'),
    'coll125_gx1': (3, 3, 125, (1, 2), (5, 2), dict(gx0=1, gx1=1, gx2=1, gy0=1, gy1=1, gy2=1, as1=.5, at1=.5), 'gx1'),
    'coll125_gy1': (3, 3, 125, (1, 2), (5, 2), dict(gx0=1, gx1=1, gx2=1, gy0=1, gy1=1, gy2=1, as1=.5, at1=.5), 'gy1'),
    'coll125_gx0big': (3, 3, 125, (1, 2), (5, 2), dict(gx0=1, gx1=1, gx2=1, gy0=1, gy1=1, gy2=1, as1=.5, at1=.5), 'gx1+gx2+gy0+gy1+gy2'),
}


def setv(base, var, eps):
    v = dict(base)
    for nm in var.split('+'):
        v[nm] = base[nm] * eps
        for o in ('as1', 'as2', 'at1', 'at2'):     # offsets scale with their gap
            pass
    return v


def to_int(par, v):
    """Offsets in `v` are fractions of their gap; convert to scaled ints."""
    out = [0] * len(par.names)
    for k, nm in enumerate(par.names):
        if nm[0] == 'g': out[k] = int(round(v[nm] * SC))
    for k, nm in enumerate(par.names):
        if nm[0] == 'a': out[k] = int(round(v[nm] * out[par.gapvar(nm)]))
    return out


def radius(par, conds, vint):
    for k in range(1, 26):
        box = []
        for j, nm in enumerate(par.names):
            x = vint[j]
            if nm == 'gx0': box.append((x, x)); continue
            r = (x if nm[0] == 'g' else vint[par.gapvar(nm)]) >> k
            box.append((x - r, x + r))
        if wm.certify(conds, box): return k
    return None


def run(name, eps_list, nang=6000, maxref=40):
    nx, ny, mask, S, T, base, var = STUDIES[name]
    ot = wm.OT.from_mask(nx, ny, mask)
    par = wm.Param(ot, S, T)
    for e in eps_list:
        t0 = time.process_time()
        vint = to_int(par, setv(base, var, e))
        vals = {k: x / SC for k, x in enumerate(vint)}
        pb = [(x, x) for x in vint]
        exact = {k: Fr(x, SC) for k, x in enumerate(vint)}
        ev = lambda f: sum(c * exact[k] for k, c in f)
        xs = [ev(f) for f in par.xf]; ys = [ev(f) for f in par.yf]
        Sx = (ev(par.Sf[0]), ev(par.Sf[1])); Tx = (ev(par.Tf[0]), ev(par.Tf[1]))
        found = []
        for it, sx, sy in wm.mine(par, vals, nang, maxref):
            conds, B = wm.conditions(par, it, sx, sy)
            if not wm.certify(conds, pb): continue
            ok, _ = replay.lit_by(ot.cells, xs, ys, Sx, Tx, (ev(B['Tstar'][0]), ev(B['Tstar'][1])))
            found.append((len(it), it, ok, conds))
            if len(found) >= 6: break
        o = dict(study=name, var=var, eps=e, n_valid=len(found))
        if found:
            o['min_ref'] = found[0][0]; o['replay_ok'] = all(f[2] for f in found)
            o['shortest'] = list(found[0][1])
            o['radius_log2'] = max((radius(par, f[3], vint) or 99) * -1 for f in found) * -1
        o['cpu'] = round(time.process_time() - t0, 2)
        print(json.dumps(o), flush=True)


if __name__ == '__main__':
    name = sys.argv[1]
    eps = [Fr(1, 2 ** k) for k in range(0, 9)]
    run(name, [float(e) for e in eps])
