"""Replay frozen optical implications and DRAT certificates; no discovery/solve."""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import lru_cache
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
OWN = HERE.parents[1]
PEER = OWN.parent / 'claude-illumination-check/k6-run'


def digest(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def save(p, obj):
    tmp = Path(str(p) + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2)+'\n')
    os.replace(tmp, p)


def initialize():
    checker = OWN / 'persisted-replay/audit.py'
    frozen_checker = HERE / 'guard-checker.py'
    if not frozen_checker.exists():
        shutil.copyfile(checker, frozen_checker)
    assert digest(checker) == digest(frozen_checker)
    provenance = json.loads((HERE.parent / 'provenance/frozen-inputs.json').read_text())
    counts = json.loads((HERE.parent / 'provenance/summary.json').read_text())
    by_path = {r['path']: r for r in provenance['inputs']}
    guards = []
    for index, row in enumerate(counts['guard_files']):
        p = Path(row['path'])
        frozen = by_path[str(p)]
        assert digest(p) == frozen['sha256'] == row['sha256']
        guards.append(dict(index=index, path=str(p), sha256=frozen['sha256'],
                           records=row['records']))
    old = json.loads((OWN / 'k6-final-review/audit.json').read_text())
    proofs = []
    for row in old['receipt_hashes']:
        d = PEER / 'cases' / row['tag']
        cnf, proof = d/'formula.cnf', d/'proof.drat'
        assert digest(cnf) == row['cnf'] and digest(proof) == row['proof']
        proofs.append(dict(tag=row['tag'], cnf=str(cnf), proof=str(proof),
                           cnf_sha256=row['cnf'], proof_sha256=row['proof'],
                           proof_bytes=proof.stat().st_size))
    checker_bin = OWN / 'bounded-proof/drat-trim'
    manifest = dict(guards=guards, proofs=proofs, guard_checker=str(frozen_checker),
                    guard_checker_sha256=digest(frozen_checker),
                    drat_checker=str(checker_bin), drat_checker_sha256=digest(checker_bin),
                    runner_sha256=digest(__file__), records=sum(r['records'] for r in guards))
    assert len(guards) == 52 and manifest['records'] == 193480 and len(proofs) == 61
    p = HERE/'manifest.json'
    if p.exists():
        assert json.loads(p.read_text()) == manifest, 'reconcile changed replay inputs'
    else:
        save(p, manifest)
    print(json.dumps(dict(phase='frozen', files=len(guards), records=manifest['records'],
                          proofs=len(proofs))), flush=True)


def manifest():
    m = json.loads((HERE/'manifest.json').read_text())
    assert digest(__file__) == m['runner_sha256'], 'runner changed since checkpoints'
    assert digest(m['guard_checker']) == m['guard_checker_sha256']
    assert digest(m['drat_checker']) == m['drat_checker_sha256']
    return m


def load_checker(m):
    spec = importlib.util.spec_from_file_location('independent_saved_paths', m['guard_checker'])
    c = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c)
    # Same pure functions with bounded caches: two replay workers must not
    # retain every path/segment of this library simultaneously.
    for name, size in (('cell',4096),('incident',16000),('segment',8000),('bounce',12000)):
        setattr(c, name, lru_cache(maxsize=size)(getattr(c, name).__wrapped__))
    return c


def records(p):
    p = Path(p)
    if p.suffix == '.jsonl':
        with p.open() as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)
    else:
        value = json.loads(p.read_text())
        yield from value if isinstance(value, list) else [value]


def controls(m):
    c = load_checker(m)
    record = next(records(m['guards'][0]['path']))
    c.check_record(record, tuple(record['q']), 'room' in record)
    results = {}
    for name in ('wrong_target','missing_used','missing_absent','non_specular'):
        bad = json.loads(json.dumps(record))
        target = tuple(bad['q'])
        if name == 'wrong_target':
            target = (target[0]+2,target[1])
        elif name == 'missing_used':
            bad['U'] = []
        elif name == 'missing_absent':
            bad['Z'] = []
        else:
            bad['path'][1][0][0] += bad['path'][1][0][1]
        try:
            c.check_record(bad, target, False)
        except (AssertionError, ValueError, ZeroDivisionError):
            results[name] = 'REJECTED'
        else:
            raise AssertionError(('invalid guard control accepted', name))
    save(HERE/'controls.json', dict(status='PASS', valid_guard='ACCEPTED', mutations=results))


def guard_file(row):
    m = manifest()
    p = Path(row['path'])
    assert digest(p) == row['sha256']
    out = HERE / f"guard-{row['index']:02d}.json"
    binding = dict(input_sha256=row['sha256'], checker_sha256=m['guard_checker_sha256'],
                   runner_sha256=m['runner_sha256'], expected=row['records'])
    state = dict(status='RUNNING', path=str(p), binding=binding, checked=0,
                 vacuous=0, reflections=0, vertex_bounces=0, room_checks=0,
                 elapsed_seconds=0)
    if out.exists():
        state = json.loads(out.read_text())
        assert state['binding'] == binding
        if state['status'] == 'PASS':
            assert state['checked'] == row['records']
            return state
        assert state['status'] == 'RUNNING', 'previous failure requires inspection'
    begin = time.monotonic()
    prior_seconds = state['elapsed_seconds']
    c = load_checker(m)
    skip = state['checked']
    for index, rec in enumerate(records(p), 1):
        if index <= skip:
            continue
        try:
            result = c.check_record(rec, tuple(rec['q']), 'room' in rec)
        except Exception as error:
            state.update(status='FAIL', failed_record=index, error=repr(error))
            save(out, state)
            raise
        state['checked'] += 1
        state['vacuous'] += bool(result['vacuous'])
        state['reflections'] += result['reflections']
        state['vertex_bounces'] += result['vertex_bounces']
        state['room_checks'] += 'room' in rec
        if state['checked'] % 250 == 0:
            state['elapsed_seconds'] = prior_seconds + time.monotonic()-begin
            save(out, state)
    assert state['checked'] == row['records']
    assert digest(p) == row['sha256'], 'guard file changed during replay'
    state.update(status='PASS', elapsed_seconds=prior_seconds+time.monotonic()-begin)
    save(out, state)
    return state


def guards():
    m = manifest()
    controls(m)
    with ProcessPoolExecutor(max_workers=2) as pool:
        jobs = {pool.submit(guard_file, row):row for row in m['guards']}
        for future in as_completed(jobs):
            row = jobs[future]
            result = future.result()
            print(json.dumps(dict(phase='guard', file=row['index'], status=result['status'],
                                  checked=result['checked'], seconds=round(result['elapsed_seconds'],2))), flush=True)


def proofs():
    m = manifest()
    for row in sorted(m['proofs'], key=lambda r:r['proof_bytes']):
        out = HERE / ('drat-'+row['tag']+'.json')
        binding = dict(cnf=row['cnf_sha256'], proof=row['proof_sha256'],
                       checker=m['drat_checker_sha256'])
        assert digest(row['cnf']) == binding['cnf']
        assert digest(row['proof']) == binding['proof']
        if out.exists():
            result = json.loads(out.read_text())
            assert result['binding'] == binding and result['status'] == 'VERIFIED'
            continue
        log = HERE / ('drat-'+row['tag']+'.log')
        begin = time.monotonic()
        with log.open('w') as f:
            p = subprocess.run([m['drat_checker'], row['cnf'], row['proof']],
                               stdout=f, stderr=subprocess.STDOUT)
        verified = p.returncode == 0 and 's VERIFIED' in log.read_text()
        result = dict(tag=row['tag'], binding=binding,
                      status='VERIFIED' if verified else 'FAIL', returncode=p.returncode,
                      elapsed_seconds=round(time.monotonic()-begin,3), bytes=row['proof_bytes'])
        assert digest(row['cnf']) == binding['cnf']
        assert digest(row['proof']) == binding['proof']
        save(out, result)
        print(json.dumps(dict(phase='DRAT', **result)),flush=True)
        assert verified, row['tag']


def status():
    m = manifest()
    gs = [json.loads(p.read_text()) for p in HERE.glob('guard-*.json')]
    ps = [json.loads(p.read_text()) for p in HERE.glob('drat-*.json')]
    result = dict(guard_files_complete=sum(r['status']=='PASS' for r in gs),
                  guard_files_expected=len(m['guards']), guards_checked=sum(r['checked'] for r in gs),
                  guards_expected=m['records'], proofs_verified=sum(r['status']=='VERIFIED' for r in ps),
                  proofs_expected=len(m['proofs']), failures=[r for r in gs+ps if r['status']=='FAIL'])
    result['status'] = ('PASS' if result['guard_files_complete']==52 and
                        result['proofs_verified']==61 and not result['failures'] else
                        'FAIL' if result['failures'] else 'RUNNING')
    save(HERE/'summary.json', result)
    print(json.dumps(result,indent=2),flush=True)


if __name__ == '__main__':
    {'init':initialize, 'guards':guards, 'drat':proofs, 'status':status}[sys.argv[1]]()
