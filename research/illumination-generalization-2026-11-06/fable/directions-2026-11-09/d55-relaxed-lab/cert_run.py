"""Certificates for every dark pair of the full run, independent re-check, and the lit-pair control.

usage: python3 -B cert_run.py dark OUT.tsv IN1.rooms.tsv.gz [IN2 ...]
       python3 -B cert_run.py lit OUT.tsv NSAMPLE POLYFILE AMIN AMAX SEED

dark: one output row per dark pair: room, pair, classes, W conventions, certificate class
  (full / partial / none), per lift pair and target the certificate kinds, factor degrees
  (blocks of N), relative base if used, d10-Cut-only flags, canonical (R3-adapted) agreement,
  and the independent verdict of d6 marked_orbit (DP pillowcase orbit; scaled by 2 for a
  different-class pair).
lit: random relaxed rooms (smax 3) and random pairs that orbitr calls LIT; reports how many get a
  full certificate (soundness requires 0) and how many pass only through the unadapted d10 Cut.
"""
import gzip
import resource
import random
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lab                                     # noqa: E402
import certs                                   # noqa: E402

KIND = {1: 'b', 2: 'c', 3: 'd'}


def summarize(c):
    """Compact description of the certificate data of one pair."""
    parts = []
    for d in c['lifts']:
        if d['over_b']:
            parts.append('B:' + '/'.join(KIND[x] + '=' + '+'.join(sorted(d['perx'][x])) + str(d['degs'][x])
                                         for x in sorted(d['perx'])))
        elif d['rel']:
            parts.append('%s(deg P->B %d)' % (d['rel'][0], d['rel'][1]))
        else:
            parts.append('NONE[' + '/'.join(KIND[x] + '=' + ('+'.join(sorted(d['perx'][x])) or '-')
                                            for x in sorted(d['perx'])) + ']')
    return ' | '.join(parts)


def kinds_used(c):
    k = set()
    for d in c['lifts']:
        if d['over_b']:
            for x in d['perx']:
                k |= d['perx'][x]
        elif d['rel']:
            k.add(d['rel'][0])
    return '+'.join(sorted(k))


def needs(c):
    """Kinds that some target of some lift pair can't do without (over B)."""
    out = set()
    for d in c['lifts']:
        if d['over_b']:
            for x, s in d['perx'].items():
                if len(s) == 1:
                    out |= s
        elif d['rel']:
            out.add(d['rel'][0])
    return '+'.join(sorted(out)) or '-'


def canon_agree(c):
    ok = True
    for d in c['lifts']:
        for x, (cp, cr) in d['canon'].items():
            if cp != ('Par' in d['perx'][x]) or cr != ('Rig' in d['perx'][x]):
                ok = False
    return ok


def dark_mode(out, inputs):
    rows = []
    t0 = time.process_time()
    for fn in inputs:
        with gzip.open(fn, 'rt') as f:
            next(f)
            for line in f:
                fs = line.rstrip('\n').split('\t')
                status = fs[9]                     # FULL = orbitr DARK, CAP = orbitr undecided
                kind, area, npin, nsl, w = fs[0], int(fs[1]), int(fs[2]), int(fs[3]), fs[4]
                rs, ds = fs[10].split(' D=')
                cells, slits = lab.parse_room(rs)
                for pr in ds.split(';'):
                    a, b = pr.split(':')
                    S = tuple(map(int, a.split(',')))
                    T = tuple(map(int, b.split(',')))
                    c = certs.certify_pair(cells, slits, S, T)
                    hd, hs, hc = certs.hurwitz_dark(cells, slits, S, T)
                    same = (S[0] - T[0]) % 2 == 0 and (S[1] - T[1]) % 2 == 0
                    cutonly = any(d['cutd10'][x] and 'Cut' not in d['perx'][x] for d in c['lifts'] for x in d['perx'])
                    rows.append('\t'.join(map(str, [
                        status, kind, area, npin, nsl, w, 'same' if same else 'diff', '%d,%d' % S, '%d,%d' % T,
                        c['cls'], kinds_used(c), needs(c), canon_agree(c), cutonly,
                        'DARK' if hd else 'LIT', hs, hc, c['nblocksystems'], summarize(c), rs])))
                    print(rows[-1][:200], flush=True)
    with open(out, 'w') as f:
        f.write('\t'.join(['orbitr_status', 'kind', 'area', 'pinches', 'slits', 'W_walk,W_slit1,W_seg', 'classes', 'S', 'T',
                           'cert_class', 'kinds_used', 'kinds_needed', 'canonical_R3_agrees',
                           'd10_cut_without_cut+', 'recheck_marked_orbit', 'recheck_states',
                           'recheck_complete', 'block_systems', 'certificates_per_lift_pair', 'room']) + '\n')
        for r in rows:
            f.write(r + '\n')
    print('dark pairs', len(rows), 'cpu', round(time.process_time() - t0, 1))


def lit_mode(out, nsample, polyfile, amin, amax, seed):
    rng = random.Random(seed)
    polys = []
    with open(polyfile) as f:
        for line in f:
            v = list(map(int, line.split()))
            if amin <= v[0] <= amax and (v[1] > 0 or rng.random() < 0.3):   # oversample pinched
                polys.append(tuple((v[3 + 2 * i], v[4 + 2 * i]) for i in range(v[0])))
    proc = subprocess.Popen([str(HERE / 'orbitr'), '1000000'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            text=True, bufsize=1)
    n = full = cutonly = partial = 0
    kinds = {}
    rows = []
    t0 = time.process_time()
    while n < nsample:
        cells = set(rng.choice(polys))
        tab0 = lab.sector_table(cells, set())
        cfgs = list(lab.slit_configs(cells, tab0, 3, 99, 2))
        nonempty = [c for c in cfgs if c]
        cfg = rng.choice(nonempty) if nonempty and rng.random() < 0.75 else rng.choice(cfgs)   # bias to slits
        slits = {e for (_, _, es) in cfg for e in es}
        tab = lab.sector_table(cells, slits)
        src = lab.interior_points(cells, slits, tab)
        if len(src) < 2:
            continue
        if rng.random() < 0.5:                 # half the sample: same-class pairs only
            same = [(p, q) for i, p in enumerate(src) for q in src[i + 1:]
                    if (p[0] - q[0]) % 2 == 0 and (p[1] - q[1]) % 2 == 0]
            if not same:
                continue
            S, T = rng.choice(same)
        else:
            S, T = rng.sample(src, 2)
        proc.stdin.write(lab.problem_line(cells, slits, [S, T], tab) + '\n')
        proc.stdin.flush()
        st, nst, pairs = lab.parse_result(proc.stdout.readline())
        if pairs:
            continue                      # dark or undecided: not a lit control
        c = certs.certify_pair(cells, slits, S, T, want_canonical=False)
        n += 1
        if c['cls'] == 'full':
            full += 1
        if c['cls'] == 'partial':
            partial += 1
        co = any(d['cutd10'][x] and 'Cut' not in d['perx'][x] for d in c['lifts'] for x in d['perx'])
        # would the unadapted d10 Cut complete a certificate for some lift pair?
        cut_completes = any(all(d['perx'][x] or d['cutd10'][x] for x in d['perx']) and not d['over_b']
                            for d in c['lifts'])
        cutonly += cut_completes
        rows.append('\t'.join(map(str, [lab.room_str(cells, slits), '%d,%d' % S, '%d,%d' % T, len(cfg),
                                        c['cls'], co, cut_completes, summarize(c)])))
    proc.stdin.close()
    proc.wait()
    with open(out, 'w') as f:
        f.write('room\tS\tT\tslits\tcert_class\td10_cut_only_somewhere\td10_cut_would_complete\tcertificates\n')
        for r in rows:
            f.write(r + '\n')
    print('lit sample', n, 'full certificates (must be 0):', full, 'partial:', partial,
          'lift pairs completed only by unadapted d10 Cut:', cutonly, 'cpu', round(time.process_time() - t0, 1))


if __name__ == '__main__':
    resource.setrlimit(resource.RLIMIT_CPU, (300, 300))
    if sys.argv[1] == 'dark':
        dark_mode(sys.argv[2], sys.argv[3:])
    else:
        lit_mode(sys.argv[2], int(sys.argv[3]), sys.argv[4], int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
