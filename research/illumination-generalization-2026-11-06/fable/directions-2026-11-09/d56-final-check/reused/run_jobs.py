"""d46 resumable job runner for cert_check campaigns.

  python3 run_jobs.py init CAMPAIGN_DIR NJ SPLIT WMIN WMAX AMIN AMAX CAP5R FSTAR SCOPE3 CHECK [--env K=V]
  python3 run_jobs.py run  CAMPAIGN_DIR --procs P --hours H [--only 0,1,2]

A job is done when CAMPAIGN_DIR/job_NNNN.out exists.  It is written as job_NNNN.tmp and
renamed only after cert_check exits 0 with a SUMMARY line, so a finished job is never rerun and
a killed job restarts from scratch.  At the wall-clock limit, or on SIGINT/SIGTERM, running jobs
are killed and their .tmp files removed.  A job exiting 10 found a positive with r <= 8: the
runner kills every other job, keeps the output as job_NNNN.POSITIVE, writes ALERT, and stops.
Any other failure is logged to failures.log and the job stays pending.
"""
import hashlib, json, os, signal, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
BIN = Path(os.environ.get('CERT_CHECK_BIN', HERE / 'cert_check'))   # override only for runner tests


def bin_hash():
    return hashlib.sha256(BIN.read_bytes()).hexdigest()[:16]


def log(cdir, msg):
    line = time.strftime('%Y-%m-%d %H:%M:%S ') + msg
    print(line, flush=True)
    with open(cdir / 'runner.log', 'a') as f:
        f.write(line + '\n')


def init(argv):
    cdir = Path(argv[0]); nj, split = int(argv[1]), int(argv[2]); args = [int(x) for x in argv[3:11]]
    env = dict(e.split('=', 1) for e in argv[12:]) if len(argv) > 11 and argv[11] == '--env' else {}
    cdir.mkdir(parents=True, exist_ok=True)
    cfg = cdir / 'config.json'
    # the job split depends on the binary's DFS order, so a campaign is tied to one binary
    new = {'nj': nj, 'split': split, 'args': args, 'env': env, 'binary_sha256_16': bin_hash()}
    if cfg.exists() and json.loads(cfg.read_text()) != new:
        sys.exit('config.json exists with different settings; refusing to change a started campaign')
    cfg.write_text(json.dumps(new, indent=1) + '\n')
    print('initialised', cdir, new)


def run(argv):
    cdir = Path(argv[0])
    procs = int(argv[argv.index('--procs') + 1]); hours = float(argv[argv.index('--hours') + 1])
    only = None
    if '--only' in argv:
        only = {int(x) for x in argv[argv.index('--only') + 1].split(',')}
    cfg = json.loads((cdir / 'config.json').read_text())
    if cfg['binary_sha256_16'] != bin_hash():
        sys.exit('cert_check differs from the binary this campaign started with; start a new campaign')
    if (cdir / 'ALERT').exists():
        sys.exit('ALERT present: a positive was found; investigate before resuming')
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
    nj = cfg['nj']
    pending = [j for j in range(nj) if not (cdir / ('job_%04d.out' % j)).exists() and (only is None or j in only)]
    log(cdir, 'start: %d of %d jobs pending, procs %d, limit %.2f h' % (len(pending), nj, procs, hours))
    deadline = time.time() + hours * 3600
    running = {}
    stop = {'flag': None}

    def handler(sig, frm):
        stop['flag'] = 'signal %d' % sig
    signal.signal(signal.SIGINT, handler); signal.signal(signal.SIGTERM, handler)
    env = dict(os.environ, **cfg['env'])
    done = 0
    try:
        while (pending or running) and not stop['flag']:
            if time.time() > deadline:
                stop['flag'] = 'wall-clock limit'; break
            while pending and len(running) < procs:
                j = pending.pop(0)
                cmd = [str(BIN)] + [str(a) for a in cfg['args']] + [str(nj), str(j), str(cfg['split'])]
                out = open(cdir / ('job_%04d.tmp' % j), 'w'); err = open(cdir / ('job_%04d.err' % j), 'w')
                running[j] = (subprocess.Popen(cmd, stdout=out, stderr=err, env=env), out, err, time.time())
            time.sleep(0.5)
            for j in list(running):
                p, out, err, t0 = running[j]
                rc = p.poll()
                if rc is None:
                    continue
                out.close(); err.close(); del running[j]
                tmp = cdir / ('job_%04d.tmp' % j)
                text = tmp.read_text()
                if rc == 10:
                    tmp.rename(cdir / ('job_%04d.POSITIVE' % j))
                    (cdir / 'ALERT').write_text('job %d found a positive with r <= 8; see job_%04d.POSITIVE\n' % (j, j))
                    log(cdir, 'ALERT: job %d found a positive with r <= 8' % j)
                    stop['flag'] = 'positive'
                    break
                if rc == 0 and 'SUMMARY' in text:
                    tmp.rename(cdir / ('job_%04d.out' % j)); done += 1
                    log(cdir, 'job %d done in %.0f s wall (%d left)' % (j, time.time() - t0, len(pending) + len(running)))
                else:
                    tmp.unlink()
                    with open(cdir / 'failures.log', 'a') as f:
                        f.write('job %d exit %s; stderr in job_%04d.err\n' % (j, rc, j))
                    log(cdir, 'job %d FAILED exit %s' % (j, rc))
    finally:
        for j, (p, out, err, t0) in running.items():
            p.terminate()
        for j, (p, out, err, t0) in running.items():
            try:
                p.wait(10)
            except subprocess.TimeoutExpired:
                p.kill(); p.wait()
            out.close(); err.close()
            t = cdir / ('job_%04d.tmp' % j)
            if t.exists():
                t.unlink()
        lock.unlink(missing_ok=True)
        left = sum(1 for j in range(nj) if not (cdir / ('job_%04d.out' % j)).exists())
        log(cdir, 'stop (%s): %d jobs finished this run, %d of %d jobs not done'
            % (stop['flag'] or 'all jobs finished', done, left, nj))


if __name__ == '__main__':
    {'init': init, 'run': run}[sys.argv[1]](sys.argv[2:])
