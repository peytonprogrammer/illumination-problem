"""d55 driver: enumerate relaxed orthogonal rooms and decide every interior pair exactly.

usage: python3 -B run.py POLYFILE AMIN AMAX SMAX LMAX PMAX JOBS JOB OUT [CAP]
  POLYFILE: output of enum_relaxed (canonical free polyominoes with simply connected interior and
  >= 2 interior points; "-" = generate in Python with lab.free_polyominoes).
  rooms: those polyominoes of area AMIN..AMAX (pinches allowed, at most PMAX), plus 0..SMAX straight slits of length 1..LMAX (disjoint closed
  segments, foot on the boundary, every other slit point interior to the slit-free room),
  up to the 8 lattice symmetries; at least 2 interior lattice points.
  Job split: polyomino index mod JOBS in JOB (an integer or a range lo-hi).
Writes OUT.rooms.tsv.gz (one row per room with a dark or undecided pair) and OUT.summary.json.
"""
import gzip
import json
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lab                                     # noqa: E402


def main():
    polyfile = sys.argv[1]
    amin, amax, smax, lmax, pmax, jobs = map(int, sys.argv[2:8])
    jlo, _, jhi = sys.argv[8].partition('-')          # JOB may be a range "lo-hi"
    myjobs = set(range(int(jlo), int(jhi or jlo) + 1))
    out = sys.argv[9]
    cap = int(sys.argv[10]) if len(sys.argv) > 10 else 1_000_000
    t0 = time.process_time()
    proc = subprocess.Popen([str(HERE / 'orbitr'), str(cap)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            text=True, bufsize=1)
    C = Counter()
    rows = []
    minw = {}
    batch = []

    def flush():
        if not batch:
            return
        proc.stdin.write(''.join(b[0] + '\n' for b in batch))
        proc.stdin.flush()
        for line, meta in batch:
            st, nst, pairs = lab.parse_result(proc.stdout.readline())
            cells, slits, src, kind, w, area, npin, nsl = meta
            npairs = len(src) * (len(src) - 1) // 2
            C['pairs'] += npairs
            C['pairs_' + kind] += npairs
            C['status_' + st] += 1
            C['states'] += nst
            if pairs:
                if st == 'FULL':
                    C['dark_pairs'] += len(pairs)
                    C['dark_pairs_' + kind] += len(pairs)
                    C['dark_rooms'] += 1
                    C['dark_rooms_' + kind] += 1
                    key = kind
                    if key not in minw or w[0] < minw[key][0]:
                        minw[key] = (w[0], w, lab.room_str(cells, slits))
                else:
                    C['undecided_pairs'] += len(pairs)
                    C['undecided_rooms'] += 1
                rows.append('%s\t%d\t%d\t%d\t%s\t%d\t%d\t%d\t%d\t%s\t%s' % (
                    kind, area, npin, nsl, ','.join(map(str, w)), len(src), npairs, nst, len(pairs), st,
                    lab.room_str(cells, slits) + ' D=' + ';'.join(
                        '%d,%d:%d,%d' % (src[a] + src[b]) for a, b in pairs)))
        batch.clear()

    idx = -1
    def source():
        if polyfile == '-':
            yield from lab.free_polyominoes(amax)
            return
        with open(polyfile) as f:
            for line in f:
                v = list(map(int, line.split()))
                yield v[0], tuple((v[3 + 2 * i], v[4 + 2 * i]) for i in range(v[0]))

    for area, poly in source():
        if area < amin or area > amax:
            continue
        idx += 1
        if idx % jobs not in myjobs:
            continue
        cells = set(poly)
        tab0 = lab.sector_table(cells, set())
        if not lab.is_valid(cells, set(), tab0):
            C['rejected_polys'] += 1
            continue
        if sum(1 for v in tab0.values() if v[0][0] == 'int') < 2:
            C['polys_lt2_interior'] += 1          # slits only remove interior points
            continue
        npin = lab.n_pinches(cells, set(), tab0)
        if npin > pmax:
            C['rejected_pinch_bound'] += 1
            continue
        C['polys'] += 1
        seen = set()
        for cfg in lab.slit_configs(cells, tab0, smax, lmax, 2):
            slits = {e for (_, _, es) in cfg for e in es}
            key = lab.canon(cells, slits)
            if key in seen:
                continue
            seen.add(key)
            tab = lab.sector_table(cells, slits)
            assert lab.is_valid(cells, slits, tab)
            src = lab.interior_points(cells, slits, tab)
            nsl = len(cfg)
            kind = ('slit' if nsl else '') + ('pinch' if npin else '') or 'strict'
            if kind == 'slitpinch':
                kind = 'both'
            C['rooms'] += 1
            C['rooms_' + kind] += 1
            if len(src) < 2:
                C['rooms_lt2_interior'] += 1
                continue
            w = lab.wall_counts(cells, slits, nsl, tab)
            C['decided_rooms'] += 1
            batch.append((lab.problem_line(cells, slits, src, tab), (cells, slits, src, kind, w, area, npin, nsl)))
            if len(batch) >= 500:
                flush()
    flush()
    proc.stdin.close()
    proc.wait()
    C['cpu_python_s'] = round(time.process_time() - t0, 2)
    import resource
    C['cpu_children_s'] = round(resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime
                                + resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime, 2)
    with gzip.open(out + '.rooms.tsv.gz', 'wt') as f:
        f.write('kind\tarea\tpinches\tslits\tW_walk,W_slit1,W_seg\tinterior\tpairs\tstates\tunreached\tstatus\troom\n')
        for r in rows:
            f.write(r + '\n')
    Path(out + '.summary.json').write_text(json.dumps(dict(args=sys.argv[1:], counts=dict(C), minw=minw),
                                                      indent=1) + '\n')
    print(json.dumps(dict(C)))


if __name__ == '__main__':
    main()
