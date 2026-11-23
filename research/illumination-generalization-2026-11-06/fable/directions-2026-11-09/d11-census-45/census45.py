"""Census driver: star-growth enumeration piped into the exact shooter.

usage:
  python3 -B census45.py run MODE NMAX WMAX WORKERS [CHUNKS]
      MODE = star (A/B pairs, every class analysed) or cstar (C pairs only).
      For every pair vector of `enum45 dlist|cdlist NMAX`, runs CHUNKS chunks
      (default 16) of `enum45 MODE ... | shoot45 40 0 - ...`, WORKERS at a time.
      Each chunk writes census/MODE-NMAX/<vector>-<job>.{counts,out,sv,prob};
      a chunk whose .counts and .out both end in "# DONE" is skipped on rerun
      (checkpointing).  Room lines never touch the disk.
"""
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent


def done(p):
    return p.exists() and p.read_text().rstrip().endswith('# DONE')


def chunk(mode, nmax, wmax, a, b, jobs, job, split, d):
    stem = d / ('%d_%d-%02d' % (a, b, job))
    counts, out, sv, prob = (stem.with_suffix(s) for s in ('.counts', '.out', '.sv', '.prob'))
    if done(counts) and done(out):
        return stem.name, 0.0, 'skip'
    t0 = time.time()
    env = dict(__import__('os').environ, CLASSES='C' if mode == 'cstar' else 'ABC')
    e = subprocess.Popen([str(HERE / 'enum45'), mode, str(nmax), str(wmax), str(a), str(b), str(jobs), str(job), str(split),
                          '/dev/stdout', str(counts)], stdout=subprocess.PIPE)
    s = subprocess.run([str(HERE / 'shoot45'), '40', '0', '-', str(out), str(sv), str(prob)], stdin=e.stdout, env=env)
    e.stdout.close()
    rc = e.wait()
    if rc or s.returncode:
        raise RuntimeError('chunk %s failed: enum %d shoot %d' % (stem.name, rc, s.returncode))
    return stem.name, time.time() - t0, 'ok'


def run(mode, nmax, wmax, workers, chunks):
    d = HERE / 'census' / ('%s-%d' % (mode, nmax))
    d.mkdir(parents=True, exist_ok=True)
    lst = subprocess.run([str(HERE / 'enum45'), 'dlist' if mode == 'star' else 'cdlist', str(nmax)],
                         capture_output=True, text=True, check=True).stdout.split('\n')
    vecs = [tuple(map(int, l.split())) for l in lst if l.strip()]
    (d / 'vectors.txt').write_text(''.join('%d %d %d\n' % v for v in vecs))
    base = 8 if mode == 'star' else 4
    tasks = []
    for a, b, need in vecs:
        # vectors whose minimum room size is close to NMAX are small: one chunk
        jobs = chunks if nmax - need >= 6 else 1
        split = base + 6 if jobs > 1 else 0
        for job in range(jobs):
            tasks.append((mode, nmax, wmax, a, b, jobs, job, split, d))
    t0 = time.time()
    with ThreadPoolExecutor(workers) as ex:
        for name, dt, st in ex.map(lambda t: chunk(*t), tasks):
            print('%-12s %-4s %7.1f s  (elapsed %.0f s)' % (name, st, dt, time.time() - t0), flush=True)
    print('# DONE %s NMAX %d WMAX %d chunks %d in %.0f s' % (mode, nmax, wmax, len(tasks), time.time() - t0))


if __name__ == '__main__':
    if sys.argv[1] == 'run':
        run(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]) if len(sys.argv) > 6 else 16)
