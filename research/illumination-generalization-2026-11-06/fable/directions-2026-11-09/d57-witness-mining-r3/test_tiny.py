"""Tiny driver test: type 122 resonance room of r3.md (x 0,3,9,12; y 0,2,5,6;
S=(1,4), T=(4,1)). Mines itineraries in floats, then checks each exactly with
the interval certifier on the degenerate box and with the independent replay.
They must agree."""
import time
import wm, replay
ot = wm.OT.from_mask(3, 3, 122)
par = wm.Param(ot, (1, 3), (3, 1))
val = dict(gx0=3, gx1=6, gx2=3, gy0=2, gy1=3, gy2=1, as1=1, as2=2, at1=1, at2=1)
vals = {par.ix[n]: v for n, v in val.items()}
xs, ys, S, T = wm.realize(par, vals)
t0 = time.process_time()
c = wm.mine(par, vals, nang=4000, maxref=10)
print('mined', len(c), 'cpu %.2f' % (time.process_time() - t0))
box = wm.point_box([vals[k] for k in range(len(par.names))])
ev = lambda f: sum(cf * vals[v] for v, cf in f)
agree = dis = nvalid = 0
for it, sx, sy in c:
    conds, B = wm.conditions(par, it, sx, sy)
    ok = wm.certify(conds, box)
    rp, n = replay.lit_by(ot.cells, xs, ys, S, T, (ev(B['Tstar'][0]), ev(B['Tstar'][1])))
    agree += ok == rp; dis += ok != rp; nvalid += ok
    if ok != rp: print('MISMATCH', it, ok, rp)
print('valid', nvalid, 'agree', agree, 'disagree', dis, 'shortest', c[0][0] if c else None)
