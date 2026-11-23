"""d56 resumable job runner (design copied from ../d46-cert-check/run_jobs.py), with CPU-time limits.

  python3 -B run_jobs.py init CAMPAIGN_DIR NJ_A NJ_E CERTRATE [--env K=V ...]
  python3 -B run_jobs.py run  CAMPAIGN_DIR --procs P --cpu-hours H [--only A0005,E0010]

Jobs are named A0000..A{NJ_A-1} (Set A) and E0000..E{NJ_E-1} (Set E), interleaved in the queue.
A job is done when CAMPAIGN_DIR/job_<name>.out exists.  It is written as .tmp and renamed only after
`check` exits 0 with a SUMMARY line, so a finished job is never rerun and a killed job restarts
from scratch.

CPU limit: H CPU-hours per `run` invocation, summed over all jobs (finished, failed, and killed),
measured with wait4() rusage for finished jobs and `ps -o cputime` for running ones.  When the sum
reaches H, running jobs are killed and the runner stops.  Each job also gets RLIMIT_CPU equal to
the budget left when it starts (a kernel-enforced backstop).  Wall-clock time is not used, so
machine sleep doesn't matter.  Every invocation adds its CPU to cpu_ledger.txt.

Exit 10 (certified pair) or 11 (tripwire) from any job: the runner kills every other job, keeps
the output as job_<name>.POSITIVE / .TRIPWIRE, writes ALERT, and stops.  Any other failure is
logged to failures.log and the job stays pending.
"""
import hashlib, json, os, signal, subprocess, sys, time, resource
from pathlib import Path

HERE = Path(__file__).resolve().parent
BIN = Path(os.environ.get('CHECK_BIN', HERE / 'check'))


def bin_hash():
    return hashlib.sha256(BIN.read_bytes()).hexdigest()[:16]


def log(cdir, msg):
    line = time.strftime('%Y-%m-%d %H:%M:%S ') + msg
    print(line, flush=True)
    with open(cdir / 'runner.log', 'a') as f:
        f.write(line + '\n')


def job_names(cfg):
    a = ['A%04d' % j for j in range(cfg['nj_a'])]
    e = ['E%04d' % j for j in range(cfg['nj_e'])]
    out = []
    for i in range(max(len(a), len(e))):          # interleave so a partial run touches both sets
        out += a[i:i + 1] + e[i:i + 1]
    return out


def init(argv):
    cdir = Path(argv[0]); nj_a, nj_e, rate = int(argv[1]), int(argv[2]), int(argv[3])
    env = dict(e.split('=', 1) for e in argv[5:]) if len(argv) > 4 and argv[4] == '--env' else {}
    cdir.mkdir(parents=True, exist_ok=True)
    cfg = cdir / 'config.json'
    # the job split depends on the binary's DFS order, so a campaign is tied to one binary
    new = {'nj_a': nj_a, 'nj_e': nj_e, 'certrate_per_million': rate, 'env': env, 'binary_sha256_16': bin_hash()}
    if cfg.exists() and json.loads(cfg.read_text()) != new:
        sys.exit('config.json exists with different settings; refusing to change a started campaign')
    cfg.write_text(json.dumps(new, indent=1) + '\n')
    print('initialised', cdir, new)


def ps_cpu(pid):
    """CPU seconds of a running process (macOS / Linux `ps -o cputime`), 0 if gone."""
    try:
        s = subprocess.run(['ps', '-o', 'cputime=', '-p', str(pid)], capture_output=True, text=True).stdout.strip()
    except OSError:
        return 0.0
    if not s:
        return 0.0
    d = 0
    if '-' in s:
        d, s = s.split('-'); d = int(d)
    parts = [float(x) for x in s.split(':')]
    while len(parts) < 3:
        parts.insert(0, 0.0)
    return d * 86400 + parts[0] * 3600 + parts[1] * 60 + parts[2]


def run(argv):
    cdir = Path(argv[0])
    procs = int(argv[argv.index('--procs') + 1]); hours = float(argv[argv.index('--cpu-hours') + 1])
    only = set(argv[argv.index('--only') + 1].split(',')) if '--only' in argv else None
    cfg = json.loads((cdir / 'config.json').read_text())
    if cfg['binary_sha256_16'] != bin_hash():
        sys.exit('check differs from the binary this campaign started with; start a new campaign')
    if (cdir / 'ALERT').exists():
        sys.exit('ALERT present: a positive or tripwire was found; investigate before resuming')
    lock = cdir / 'runner.pid'
    if lock.exists():
        try:
            os.kill(int(lock.read_text()), 0)
            sys.exit('another runner (pid %s) is active on this campaign' % lock.read_text())
        except (ProcessLookupError, ValueError):
            pass
    lock.write_text(str(os.getpid()))
    for t in cdir.glob('job_*.tmp'):
        t.unlink()                                   # leftovers of a killed run
    names = job_names(cfg)
    pending = [j for j in names if not (cdir / ('job_%s.out' % j)).exists() and (only is None or j in only)]
    budget = hours * 3600.0
    log(cdir, 'start: %d of %d jobs pending, procs %d, CPU limit %.3f h' % (len(pending), len(names), procs, hours))
    running = {}                                     # name -> (pid, out, err)
    keep = {}
    stop = {'flag': None}
    used = 0.0                                       # CPU of reaped jobs in this invocation

    def handler(sig, frm):
        stop['flag'] = 'signal %d' % sig
    signal.signal(signal.SIGINT, handler); signal.signal(signal.SIGTERM, handler)
    env = dict(os.environ, **cfg['env'])
    done = 0

    def launch(j):
        left = max(1, int(budget - used - sum(ps_cpu(p) for p, _, _ in running.values())))
        def lim():
            resource.setrlimit(resource.RLIMIT_CPU, (left, left + 5))
        s, num = j[0], int(j[1:])
        nj = cfg['nj_a'] if s == 'A' else cfg['nj_e']
        cmd = [str(BIN), s, str(nj), str(num), str(cfg['certrate_per_million'])]
        out = open(cdir / ('job_%s.tmp' % j), 'w'); err = open(cdir / ('job_%s.err' % j), 'w')
        p = subprocess.Popen(cmd, stdout=out, stderr=err, env=env, preexec_fn=lim)
        running[j] = (p.pid, out, err)
        keep[j] = p          # keep a reference: a collected Popen could be reaped by subprocess._cleanup

    def reap(j, status, ru):
        nonlocal used, done
        pid, out, err = running.pop(j)
        out.close(); err.close()
        cpu = ru.ru_utime + ru.ru_stime
        used += cpu
        rc = os.waitstatus_to_exitcode(status)
        tmp = cdir / ('job_%s.tmp' % j)
        text = tmp.read_text()
        if rc in (10, 11):
            kind = 'POSITIVE' if rc == 10 else 'TRIPWIRE'
            tmp.rename(cdir / ('job_%s.%s' % (j, kind)))
            (cdir / 'ALERT').write_text('job %s exited %d (%s); see job_%s.%s\n' % (j, rc, kind, j, kind))
            log(cdir, 'ALERT: job %s %s' % (j, kind))
            stop['flag'] = kind.lower()
        elif rc == 0 and 'SUMMARY' in text:
            tmp.rename(cdir / ('job_%s.out' % j)); done += 1
            log(cdir, 'job %s done, %.1f CPU s (%d pending, %d running, %.0f CPU s used)'
                % (j, cpu, len(pending), len(running), used))
        else:
            tmp.unlink()
            with open(cdir / 'failures.log', 'a') as f:
                f.write('job %s exit %s after %.1f CPU s; stderr in job_%s.err\n' % (j, rc, cpu, j))
            log(cdir, 'job %s FAILED exit %s' % (j, rc))

    try:
        while (pending or running) and not stop['flag']:
            while pending and len(running) < procs and not stop['flag']:
                launch(pending.pop(0))
            time.sleep(1.0)
            for j in list(running):
                pid = running[j][0]
                r = os.wait4(pid, os.WNOHANG)
                if r[0] == pid:
                    reap(j, r[1], r[2])
                    if stop['flag']:
                        break
            if not stop['flag'] and used + sum(ps_cpu(p) for p, _, _ in running.values()) >= budget:
                stop['flag'] = 'CPU limit'
    finally:
        for j, (pid, out, err) in list(running.items()):
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        for j, (pid, out, err) in list(running.items()):
            _, status, ru = os.wait4(pid, 0)
            used += ru.ru_utime + ru.ru_stime
            out.close(); err.close()
            t = cdir / ('job_%s.tmp' % j)
            if t.exists():
                t.unlink()
        lock.unlink(missing_ok=True)
        left = sum(1 for j in names if not (cdir / ('job_%s.out' % j)).exists())
        with open(cdir / 'cpu_ledger.txt', 'a') as f:
            f.write('%s run: %.1f CPU s, stop: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), used, stop['flag'] or 'all jobs finished'))
        log(cdir, 'stop (%s): %d jobs finished this run, %.1f CPU s used, %d of %d jobs not done'
            % (stop['flag'] or 'all jobs finished', done, used, left, len(names)))


if __name__ == '__main__':
    {'init': init, 'run': run}[sys.argv[1]](sys.argv[2:])
