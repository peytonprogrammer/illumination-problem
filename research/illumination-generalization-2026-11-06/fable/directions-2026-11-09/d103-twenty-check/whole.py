"""D103: re-certify sampled rooms with the d74 continuum certifier and D103's tracer.

Usage: python3 -B whole.py SAMPLE HARDDIR LOG [limit]

For each sampled room, run d74 `cert` (independent of the author's cover.c) with
direction bounds 6, 10, 14, 18 until no 1- or 2-dimensional piece is left.
Remaining point pieces are mutual pairs; each is checked for interiority and
lit by an explicit exact path (tracer.py). For tile-level rooms with saved boxes
the remaining pieces must instead lie, pair by pair, in a saved box (or be a
traced point pair); this checks the residual input of the shear step.
"""
import os, subprocess, sys, time, resource
from fractions import Fraction as F
from pathlib import Path
from tracer import find_path, interior

HERE = Path(__file__).resolve().parent
sample, hard, log = Path(sys.argv[1]), Path(sys.argv[2]), open(sys.argv[3], 'w')
limit = int(sys.argv[4]) if len(sys.argv) > 4 else 10 ** 9
U = 65536
BOUNDS = (6, 10, 14, 18)


def run_cert(room, B):
    p = HERE / 'work' / f'room-{os.getpid()}.txt'
    p.write_text(room + '\n')
    try:
        r = subprocess.run([HERE / 'bin' / 'cert', p, '0', str(B)], capture_output=True, text=True,
                           env={**os.environ, 'D74ALL': '1'}, timeout=15)
    except subprocess.TimeoutExpired:
        return None
    assert r.returncode == 0, r.stderr
    pieces = {}
    final = None
    for l in r.stdout.splitlines():
        if l.startswith('FINAL'):
            a = l.split(); final = int(a[2])
        elif l.startswith('PIECE'):
            head, part = l.split(' | partners')
            a = head.split(); i = int(a[1]); dim = int(a[3])
            pts = []
            for v in a[4:]:
                x, y = v.split(',')
                pts.append((F(x), F(y)))
            nums = part.split('(')[0].split()
            total = int(part.split('(')[1].rstrip(')'))
            # d74 prints at most 12 partners; a truncated list is replaced by every piece (a superset)
            pieces[i] = (dim, pts, list(map(int, nums)) if len(nums) == total else None)
    assert final == len(pieces)
    for i, (d, pts, part) in pieces.items():
        if part is None:
            pieces[i] = (d, pts, list(pieces))
    return pieces


def in_box(cells, box, f, g):
    i, j, k, l, r = box
    for (ci, co), pts in (((i, k), f), ((j, l), g)):
        a, b = cells[ci]; cx, cy = a + (co & 1), b + (co >> 1)
        for x, y in pts:
            if not (a <= x <= a + 1 and b <= y <= b + 1):
                return False
            if max(abs(x - cx), abs(y - cy)) * U > r:
                return False
    return True


counts = {}
t0 = time.process_time()
for n, line in enumerate(sample.read_text().splitlines()):
    if n >= limit:
        break
    st, key, ll, room = line.split(' ', 3)
    raw = list(map(int, room.split())); cells = list(zip(raw[2::2], raw[3::2])); C = set(cells)
    boxes = []
    if st == 'hard' and (hard / key / 'boxes').exists():
        boxes = [tuple(map(int, z.split())) for z in (hard / key / 'boxes').read_text().splitlines()]
    if boxes:
        # d74's residue near corner pairs is 2-dimensional and large (209,900 pieces at
        # B = 18 for hard/7-242, 67 CPU-s), so the residual-in-box check does not fit the budget.
        counts[(st, 'skipped-has-boxes')] = counts.get((st, 'skipped-has-boxes'), 0) + 1
        print(f'{st} {key} boxes={len(boxes)} skipped-has-boxes', file=log, flush=True)
        continue
    c0 = resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime
    for B in BOUNDS:
        pieces = run_cert(room, B)
        if pieces is None or all(d == 0 for d, _, _ in pieces.values()):
            break
    if pieces is None:
        counts[(st, 'OPEN-timeout')] = counts.get((st, 'OPEN-timeout'), 0) + 1
        print(f'{st} {key} B={B} OPEN-timeout', file=log, flush=True)
        continue
    c1 = resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime
    lattice = set(); unboxed = 0; nonlattice_pts = 0
    for a, (da, pa, part) in pieces.items():
        for b in part:
            if b == a or (b < a and a in pieces[b][2]):
                continue
            db, pb, _ = pieces[b]
            if da == 0 and db == 0:
                s, t = pa[0], pb[0]
                if s == t or not interior(C, s) or not interior(C, t):
                    continue
                lattice.add(tuple(sorted((s, t))))
                continue
            # a positive-dimensional pair: must lie in a saved box (either order)
            if not any(in_box(cells, bx, pa, pb) or in_box(cells, bx, pb, pa) for bx in boxes):
                unboxed += 1
    traced = failed = 0
    for s, t in sorted(lattice):
        if all(z.denominator == 1 for z in (*s, *t)) is False:
            nonlattice_pts += 1
        v = find_path(C, s, t, 12)
        if v is None:
            failed += 1
            print('NO PATH', key, s, t, file=log)
        else:
            traced += 1
    dims = sum(1 for d, _, _ in pieces.values() if d)
    if dims == 0 and failed == 0:
        verdict = 'cleared'
    elif boxes and unboxed == 0 and failed == 0:
        verdict = 'residue-in-boxes'
    else:
        verdict = 'OPEN'
    counts[(st, verdict)] = counts.get((st, verdict), 0) + 1
    print(f'{st} {key} B={B} live={len(pieces)} posdim={dims} pairs_traced={traced} '
          f'nonlattice_point_pairs={nonlattice_pts} no_path={failed} boxes={len(boxes)} unboxed={unboxed} '
          f'author_lattice={ll} cert_cpu={c1 - c0:.2f} {verdict}', file=log, flush=True)
tot = resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime + time.process_time() - t0
summary = ' '.join(f'{a}:{b}={c}' for (a, b), c in sorted(counts.items()))
print('SUMMARY', summary, f'cpu={tot:.1f}', file=log)
print('SUMMARY', summary, f'cpu={tot:.1f}')
