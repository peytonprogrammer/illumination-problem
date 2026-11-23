"""Compare shooting verdicts (check, mode X: all interior lattice pairs) with the exact SL(2,Z)-orbit
decider orbitc (copied from d9) on every pair of the given rooms.
usage: python3 -B val_orbit.py ROOMFILE... ; prints counts and every disagreement."""
import subprocess, sys, resource
from pathlib import Path
HERE = Path(__file__).resolve().parent
lim = lambda: resource.setrlimit(resource.RLIMIT_CPU, (300, 300))
rooms = [l.split() for f in sys.argv[1:] for l in open(f) if l.strip() and not l.startswith('#')]
probs, keys = [], []
for v in rooms:
    a = int(v[0]); cells = {(int(v[2 + 2 * i]), int(v[3 + 2 * i])) for i in range(a)}
    pts = sorted({(x + dx, y + dy) for (x, y) in cells for dx in (0, 1) for dy in (0, 1)})
    inner = [p for p in pts if all(((p[0] - u, p[1] - w) in cells) for u in (0, 1) for w in (0, 1))]
    if len(inner) < 2:
        continue
    probs.append(' '.join(v[:1] + v[2:]) + ' | %d ' % len(inner) + ' '.join('%d %d' % p for p in inner))
    keys.append((' '.join(v), inner))
out = subprocess.run([str(HERE.parent / 'orbitc'), '500000'], input='\n'.join(probs) + '\n', capture_output=True,
                     text=True, preexec_fn=lim).stdout.split('\n')
orb, k = {}, -1
for line in out:
    f = line.split()
    if not f:
        continue
    if f[0] == 'states':
        k += 1; complete = f[3] == '1'
        continue
    # LIT verdicts carry a found path; DARK needs a complete orbit (orbitc stops early once all pairs are lit)
    orb[(k, (int(f[0]), int(f[1])), (int(f[2]), int(f[3])))] = f[4] if (complete or f[4] == 'LIT') else 'INCOMPLETE'
agree = dis = lit = dark = 0
for k, (room, inner) in enumerate(keys):
    r = subprocess.run([str(HERE.parent / 'check'), 'stdin', 'X', '0'], input=room + '\n', capture_output=True,
                       text=True, preexec_fn=lim).stdout
    surv = set()
    for line in r.split('\n'):
        if line.startswith('SURVIVOR'):
            f = line.split(); surv.add(((int(f[5]), int(f[6])), (int(f[8]), int(f[9]))))
    for i in range(len(inner)):
        for j in range(i + 1, len(inner)):
            S, T = inner[i], inner[j]
            o = orb.get((k, S, T)) or orb.get((k, T, S))
            mine = 'DARK?' if (S, T) in surv else 'LIT'
            if o == 'LIT': lit += 1
            if o == 'DARK': dark += 1
            if (o == 'LIT') == (mine == 'LIT') and o in ('LIT', 'DARK'):
                agree += 1
            else:
                dis += 1; print('DISAGREE', room, S, T, 'orbitc', o, 'shoot', mine)
print('rooms', len(keys), 'pairs', agree + dis, 'agree', agree, 'disagree', dis, 'orbitc LIT', lit, 'DARK', dark)
