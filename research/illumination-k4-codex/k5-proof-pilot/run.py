"""Two fixed k5 proof pilots using frozen universal guards. No optical search."""
from pathlib import Path
import importlib.util,sys,json,time,hashlib,threading,subprocess
ROOT=Path(__file__).resolve().parent;OWNER=ROOT.parent;LEGACY=OWNER/'bounded-proof'
sys.path.insert(0,str(OWNER.parent))
spec=importlib.util.spec_from_file_location('audited_encoder',LEGACY/'encode.py')
model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
from pysat.solvers import Solver

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run(tag):
    case=next(c for c in json.loads((ROOT/'inputs/branch-support.json').read_text())['cases'] if c['tag']==tag)
    pair=case['mark_pairs'][0];folder=ROOT/'cases'/(tag+'-pair0');folder.mkdir(parents=True,exist_ok=True)
    started=time.monotonic();control=None
    if tag=='I2_1_1':
        # The known22wall dark room must remain allowed at W22,k5.
        controlcase=dict(case)
        allowed=set(map(tuple,case['allowed']))
        allowed|={(x+dx,y+dy) for x,y in list(allowed) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))}
        controlcase['allowed']=sorted(allowed)
        cnf,pool,variables,tiles=model.geometry(controlcase,wmax=22,kmax=5)
        ng=model.guards(controlcase,pair,variables,cnf)
        fixture=json.loads((ROOT/'inputs/cand-2_2-1.json').read_text())
        chosen={tuple(sorted(map(tuple,t))) for t in fixture['triangles']}
        assert chosen<=variables.keys()
        assumptions=[v if t in chosen else -v for t,v in variables.items()]
        with Solver(name='glucose4',bootstrap_with=cnf.clauses) as solver:assert solver.solve(assumptions=assumptions)
        control=dict(known_dark22_allowed_at_W22_k5=True,guards=ng)
        print(json.dumps(dict(tag=tag,phase='positive-control',status='PASS')),flush=True)
    cnf,pool,variables,tiles=model.geometry(case,wmax=21,kmax=5)
    ng=model.guards(case,pair,variables,cnf)
    cnf.to_file(str(folder/'formula.cnf'))
    (folder/'tile-variables.json').write_text(json.dumps([[t,v] for t,v in variables.items()])+'\n')
    print(json.dumps(dict(tag=tag,phase='encoded',variables=cnf.nv,clauses=len(cnf.clauses),tiles=len(tiles),guards=ng)),flush=True)
    proof=[];sat=None
    with Solver(name='glucose4',bootstrap_with=cnf.clauses,with_proof=True) as solver:
        timer=threading.Timer(45,solver.interrupt);timer.start()
        try:
            sat=solver.solve_limited(expect_interrupt=True)
            if sat is False:proof=solver.get_proof()
            if sat is True:
                assignment=set(solver.get_model());selected=[t for t,v in variables.items() if v in assignment]
                room=dict(triangles=selected,marked=[[2*x,2*y] for x,y in pair],require_simple=True)
                receipt=model.check(room,strict=False)
                (folder/'residual-room.json').write_text(json.dumps(dict(room=room,geometry_receipt=receipt))+'\n')
            stats=solver.accum_stats()
        finally:timer.cancel()
    status='UNKNOWN' if sat is None else 'RESIDUAL' if sat else 'UNSAT_UNVERIFIED'
    if sat is False:
        with (folder/'proof.drat').open('w') as stream:
            for line in proof:stream.write(line+'\n')
        print(json.dumps(dict(tag=tag,phase='proof-check',proof_lines=len(proof))),flush=True)
        with (folder/'proof-check.log').open('w') as log:
            try:
                checked=subprocess.run([str(LEGACY/'drat-trim'),str(folder/'formula.cnf'),str(folder/'proof.drat')],stdout=log,stderr=subprocess.STDOUT,timeout=120)
            except subprocess.TimeoutExpired:checked=None
        if checked and checked.returncode==0 and 's VERIFIED' in (folder/'proof-check.log').read_text():status='VERIFIED_UNSAT'
    source=LEGACY/'encode.py'
    assert digest(source)==digest(ROOT/'inputs/encode.py')
    result=dict(tag=tag+'-pair0',status=status,W_cap=21,exception_cap=5,N_cap=38,partial_or_missing_cap=11,
        variables=cnf.nv,clauses=len(cnf.clauses),tiles=len(tiles),guards=ng,positive_control=control,
        seconds=round(time.monotonic()-started,3),solver_stats=stats,
        cnf_sha256=digest(folder/'formula.cnf'),encoder_sha256=digest(source),
        scope='This one fixed full-star/marked-pair case only. Frozen universally validated guards; no new optical discovery.')
    if (folder/'proof.drat').exists():result['proof_sha256']=digest(folder/'proof.drat')
    (folder/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)

if __name__=='__main__':run(sys.argv[1])
