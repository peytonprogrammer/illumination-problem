"""Overlap remaining fixed proof replays without duplicating the serial job.

Pause only our serial Python coordinator; its active verifier keeps running.
Resume the coordinator in finally, after companions have saved their receipts.
The unchanged replay.py does all verification and receipt/hash checks.
"""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import importlib.util
import json
import os
import shlex
import signal
import subprocess

HERE = Path(__file__).resolve().parent


def load():
    spec = importlib.util.spec_from_file_location('frozen_replay', HERE/'replay.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def job(row):
    m = load()
    frozen = m.manifest()
    assert row in frozen['proofs']
    # Narrow only the job list; retain all checker and certificate bindings.
    m.manifest = lambda: dict(frozen, proofs=[row])
    m.proofs()
    return row['tag']


def main():
    m = load()
    frozen = m.manifest()
    raw = subprocess.check_output(['ps','-axo','pid=,ppid=,args='],text=True)
    processes = []
    for line in raw.splitlines():
        pid, ppid, command = line.strip().split(None, 2)
        args = shlex.split(command)
        processes.append((int(pid),int(ppid),args))
    parents = [(pid,args) for pid,ppid,args in processes
               if len(args)>=2 and args[-1]=='drat'
               and args[-2].endswith('full-replay/replay.py')]
    assert len(parents)==1, parents
    parent, _ = parents[0]
    children = [args for pid,ppid,args in processes
                if ppid==parent and args[0]==frozen['drat_checker']]
    assert len(children)==1, children
    active = next(row for row in frozen['proofs'] if row['proof']==children[0][-1])
    os.kill(parent, signal.SIGSTOP)
    try:
        pending = [r for r in frozen['proofs'] if r['tag']!=active['tag']
                   and not (HERE/('drat-'+r['tag']+'.json')).exists()]
        pending.sort(key=lambda r:r['proof_bytes'],reverse=True)
        print(json.dumps(dict(serial_parent_paused=parent,active_serial=active['tag'],
                              companions=[r['tag'] for r in pending])),flush=True)
        # Three companions at most; the active serial verifier remains separate.
        with ProcessPoolExecutor(max_workers=min(3,len(pending))) as pool:
            for future in as_completed([pool.submit(job,row) for row in pending]):
                print('COMPANION VERIFIED '+future.result(),flush=True)
    finally:
        os.kill(parent, signal.SIGCONT)
        print('SERIAL COORDINATOR RESUMED',flush=True)


if __name__=='__main__':
    main()
