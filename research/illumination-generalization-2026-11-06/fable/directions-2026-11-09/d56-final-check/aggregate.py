"""Aggregate a d56 campaign: totals per set, survivors, positives, tripwires, CPU, extrapolation, and
count reconciliation against the d9 census.

usage: python3 -B aggregate.py CAMPAIGN_DIR > CAMPAIGN_DIR/aggregate.md

Reconciliation (run only when every job of a set is done):
  Set A: sum of enum_count = 169,672,127 (census_totals.md, W 20 area 20); and per d9 job
         J = j mod 26 the sum equals runs/a20/job-J.counts (same enumerator split, SPLIT = 11).
  Set E: per (W, area) rooms, reduced and c3 = partA-totals.json; per W the c3
         total equals the d50 table; per Part A job J = j mod 4 the c3 counts equal
         runs/partA/a16/job-J.out.
"""
import json, re, statistics, sys
from collections import defaultdict
from pathlib import Path

D9 = Path(__file__).resolve().parent.parent / 'd9-census-w22'
TABLE = {12: 22, 14: 287, 16: 3875, 18: 59893, 20: 881807}
FIELDS = ('enum_count rooms rooms_with_pairs reduced c3 pairs lit40 lit120 survivors verifyfail cert_tested '
          'certified tripwires cert_na g3_rooms g3_pairs g3_lit g6_pairs g6_lit cpu').split()


def main():
    cdir = Path(sys.argv[1])
    cfg = json.loads((cdir / 'config.json').read_text())
    nj = {'A': cfg['nj_a'], 'E': cfg['nj_e']}
    tot = {s: defaultdict(float) for s in 'AE'}
    cert = {s: defaultdict(int) for s in 'AE'}
    wa = {s: defaultdict(lambda: [0, 0, 0]) for s in 'AE'}
    wa4 = defaultdict(int)                       # (j mod 4, W, area) -> c3, Set E
    per_job = {s: {} for s in 'AE'}
    surv, alerts = [], []
    for f in sorted(cdir.glob('job_*.out')):
        s, j = f.stem[4], int(f.stem[5:])
        for line in f.read_text().splitlines():
            if line.startswith('SUMMARY'):
                v = line.split(); d = {v[i]: float(v[i + 1]) for i in range(1, len(v) - 1) if v[i] in FIELDS}
                for k, x in d.items():
                    tot[s][k] += x
                per_job[s][j] = d
            elif line.startswith('# rooms_WA'):
                for w, a, r, red, c3 in re.findall(r'W(\d+)_A(\d+):(\d+)/(\d+)/(\d+)', line):
                    o = wa[s][(int(w), int(a))]; o[0] += int(r); o[1] += int(red); o[2] += int(c3)
                    if s == 'E':
                        wa4[(j % 4, int(w), int(a))] += int(c3)
            elif line.startswith('# cert_instances'):
                v = line.split()
                for i in range(2, len(v) - 1, 2):
                    cert[s][v[i]] += int(v[i + 1])
            elif line.startswith('SURVIVOR'):
                surv.append(line)
    for f in list(cdir.glob('job_*.POSITIVE')) + list(cdir.glob('job_*.TRIPWIRE')):
        alerts.append(f.name)
    P = print
    P('# d56 campaign aggregate: %s\n' % cdir)
    P('ALERT file present: %s. Alert job files: %s\n' % ((cdir / 'ALERT').exists(), alerts or 'none'))
    P('| Set | jobs done | rooms | pairs | lit (bound 40) | lit (bound 120 only) | survivors | verify failures |'
      ' cert-tested pairs | certified | tripwires | cert n/a (sheared only) | CPU s |')
    P('| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |')
    for s in 'AE':
        t = tot[s]
        P('| %s | %d of %d | %d | %d | %d | %d | %d | %d | %d | %d | %d | %d | %.0f |' % (
            s, len(per_job[s]), nj[s], t['rooms'], t['pairs'], t['lit40'], t['lit120'], t['survivors'],
            t['verifyfail'], t['cert_tested'], t['certified'], t['tripwires'], t['cert_na'], t['cpu']))
    P('\nSet E extras: index-3 regression rooms %d, pairs %d, lit %d; index-6 pairs %d, lit %d.' % (
        tot['E']['g3_rooms'], tot['E']['g3_pairs'], tot['E']['g3_lit'], tot['E']['g6_pairs'], tot['E']['g6_lit']))
    for s in 'AE':
        P('Certificate instances, set %s: %s' % (s, dict(cert[s])))
    P('\n## Rates and extrapolation (CPU)\n')
    total_lo = total_mid = total_hi = 0.0
    for s in 'AE':
        jobs = per_job[s]
        if not jobs:
            continue
        t = tot[s]
        P('- Set %s: %.2f us per room, %.2f us per pair (CPU per room and per pair, everything included).'
          % (s, 1e6 * t['cpu'] / max(1, t['rooms']), 1e6 * t['cpu'] / max(1, t['pairs'])))
        rest = [d['cpu'] for j, d in jobs.items() if j != 0]
        fixed = jobs[0]['cpu'] if (s == 'E' and 0 in jobs) else 0.0
        nrest = nj[s] - (1 if s == 'E' else 0)
        if not rest:
            continue
        done_cpu = sum(d['cpu'] for d in jobs.values())
        mid = fixed + statistics.mean(rest) * nrest
        lo, hi = fixed + min(rest) * nrest, fixed + max(rest) * nrest
        if s == 'E' and 0 not in jobs:
            mid += statistics.mean(rest) * 2; hi += max(rest) * 3          # job 0 also takes all areas < 11
        total_lo += lo; total_mid += mid; total_hi += hi
        P('  Full set %s: %.2f CPU-h (range %.2f to %.2f: mean, min, max sampled job x %d jobs%s); %.0f CPU s done.'
          % (s, mid / 3600, lo / 3600, hi / 3600, nrest, ', plus job 0' if s == 'E' else '', done_cpu))
    P('- Both sets: %.2f CPU-h (range %.2f to %.2f).' % (total_mid / 3600, total_lo / 3600, total_hi / 3600))
    P('\n## Survivors (unresolved unless certified; send to the orbit decider)\n')
    P('\n'.join('    ' + x for x in surv) if surv else 'none')
    P('\n## Count reconciliation\n')
    if len(per_job['A']) == nj['A']:
        ref = 169672127
        P('- Set A rooms %d vs census %d: %s' % (tot['A']['enum_count'], ref, 'OK' if tot['A']['enum_count'] == ref else 'MISMATCH'))
        if nj['A'] % 26 == 0:
            bad = 0
            for J in range(26):
                txt = (D9 / ('runs/a20/job-%d.counts' % J)).read_text()
                r = int(re.search(r'count area 20 W 20 rooms (\d+)', txt).group(1))
                got = sum(d['enum_count'] for j, d in per_job['A'].items() if j % 26 == J)
                bad += got != r
            P('- Set A per d9 job (26 residues): %d mismatches' % bad)
    else:
        P('- Set A: %d of %d jobs done; total reconciliation runs when all are done.' % (len(per_job['A']), nj['A']))
    if len(per_job['E']) == nj['E']:
        rows = json.load(open(D9 / 'partA-totals.json'))['rows']
        bad = 0
        for k, (r, red, c3) in sorted(wa['E'].items()):
            pa = rows.get('%d,%d' % k, {})
            bad += (r, red, c3) != (pa.get('rooms'), pa.get('reduced'), pa.get('c3'))
        P('- Set E per (W, area): %d cells, %d mismatches against partA-totals.json (rooms, reduced, c3)' % (len(wa['E']), bad))
        for W, ref in TABLE.items():
            got = sum(v[2] for k, v in wa['E'].items() if k[0] == W)
            P('- Set E W = %d: c3 %d vs d50 table %d: %s' % (W, got, ref, 'OK' if got == ref else 'MISMATCH'))
        if nj['E'] % 4 == 0:
            bad = 0
            for J in range(4):
                for m in re.finditer(r'# T area (\d+) W (\d+) .*? c3 (\d+)', (D9 / ('runs/partA/a16/job-%d.out' % J)).read_text()):
                    a, W, c3 = int(m.group(1)), int(m.group(2)), int(m.group(3))
                    if 12 <= W <= 20 and a <= W - 4:
                        bad += wa4[(J, W, a)] != c3
            P('- Set E per Part A job (4 residues, every (W, area) cell): %d mismatches' % bad)
    else:
        P('- Set E: %d of %d jobs done; reconciliation runs when all are done. Pilot cells sampled: %d.'
          % (len(per_job['E']), nj['E'], len(wa['E'])))


if __name__ == '__main__':
    main()
