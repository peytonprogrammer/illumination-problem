"""d46: sum a campaign's job outputs.  usage: aggregate.py CAMPAIGN_DIR [--cells]
Prints per-W shape/pattern counts, per-(W, area) rooms, survivors, pairs, positives, and the
SUMMARY totals with CPU seconds.  Also lists POSITIVE lines, if any.
"""
import json, re, sys
from collections import defaultdict
from pathlib import Path

def load(cdir):
    cdir = Path(cdir)
    cfg = json.loads((cdir / 'config.json').read_text())
    cells = defaultdict(lambda: [0] * 6); shapes = defaultdict(lambda: [0] * 4)
    tot = defaultdict(float); jobs = []; pos = []
    for f in sorted(cdir.glob('job_*.out')) + sorted(cdir.glob('job_*.POSITIVE')):
        for ln in f.read_text().splitlines():
            if ln.startswith('CELL'):
                v = ln.split(); W, a = int(v[2]), int(v[4])
                for k, idx in enumerate((6, 8, 10, 12, 14, 16)):
                    cells[(W, a)][k] += int(v[idx])
            elif ln.startswith('SHAPES'):
                v = ln.split(); W = int(v[2])
                for k, idx in enumerate((4, 6, 8, 10)):
                    shapes[W][k] += int(v[idx])
            elif ln.startswith('SUMMARY'):
                d = dict(zip(ln.split()[1::2], ln.split()[2::2]))
                for k in ('shapes', 'rooms_generated', 'rooms_passing_fstar', 'rooms_checked', 'pairs_checked', 'positives', 'cpu_s'):
                    tot[k] += float(d[k])
                jobs.append(float(d['cpu_s']))
            elif ln.startswith('POSITIVE') or ln.startswith('ABORT'):
                pos.append('%s: %s' % (f.name, ln))
    return cfg, cells, shapes, tot, jobs, pos

if __name__ == '__main__':
    cfg, cells, shapes, tot, jobs, pos = load(sys.argv[1])
    print('campaign', sys.argv[1], 'config', cfg)
    print('jobs done %d of %d' % (len(jobs), cfg['nj']))
    for W in sorted(shapes):
        s = shapes[W]
        print('W %d canonical shapes %d parity patterns %d in scope (>= 3 classes) %d passing F* at some area %d' % (W, *s))
    if '--cells' in sys.argv:
        print('| W | area | rooms generated | fixed rooms | rooms passing F* | rooms checked | pairs | positives |')
        print('| --- | --- | --- | --- | --- | --- | --- | --- |')
        for (W, a), v in sorted(cells.items()):
            print('| %d | %d | %s |' % (W, a, ' | '.join('{:,}'.format(x) for x in v)))
    print('TOTAL ' + ' '.join('%s %d' % (k, v) for k, v in tot.items() if k != 'cpu_s') +
          ' cpu_s %.1f (max job %.1f)' % (tot['cpu_s'], max(jobs) if jobs else 0))
    for p in pos:
        print(p)
