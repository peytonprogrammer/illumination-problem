"""Claim-2 certificate strength on cross b=7: max over all generator maps F of
max(u,v)/gcd(u,v), u = F-period of s, v = F*-period, F* = iota F iota."""
import math, time, os
from surf import Room, full_group, compose
from run import cross, period
t0 = time.process_time()
out = []
log = lambda s: (print(s), out.append(s))
room = Room(cross(7))
gens, auts, idx = full_group(room, log)
I = room.viota
qc = room.qclass
for P in [(5, 1), (1, 1), (6, 1), (3, 1), (6, 0)]:
    s = room.vert((1, 1), P)
    best = (0, None)
    hist = {}
    for F in gens:
        Fs = compose(I, compose(F, I))
        u, v = period(F, s, qc), period(Fs, s, qc)
        r = max(u, v) // math.gcd(u, v)
        hist[r] = hist.get(r, 0) + 1
        if r > best[0]:
            best = (r, (u, v))
    log(f'  S={P}: max single-F ratio over {len(gens)} generator maps = {best[0]} at (u,v)={best[1]}; histogram {dict(sorted(hist.items()))}')
log(f'  cpu {time.process_time() - t0:.1f}s')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scan7.log'), 'w').write('\n'.join(out) + '\n')
