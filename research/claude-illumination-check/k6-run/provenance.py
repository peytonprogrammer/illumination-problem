# For each case: formula.cnf = regenerated frozen-encoder base clauses, followed only by clauses
# that clauses() derives from audited guards (k5 library + every k6 guard file).
import sys,json,os
sys.argv,tags=['run.py'],sys.argv[1:]
import run
from pysat.formula import CNF
L=run.library()
cs={c['tag']:c for c in json.load(open(run.H+'/cases.json'))}
for tag in tags:
    c=cs[tag]
    case={'full':c['full'],'allowed':[(a+dx,b+dy) for a,b in c['full'] for dx in range(-14,15) for dy in range(-14,15) if abs(dx)+abs(dy)<=14]}
    cnf,pool,x,ts=run.enc.geometry(case,wmax=21,kmax=6); base=cnf.clauses
    f=CNF(from_file=f'cases/{tag}/formula.cnf').clauses
    prefix=f[:len(base)]==base
    s,t=[(2*a,2*b) for a,b in c['pair']]
    ok=set()
    for rec in L: ok|=run.clauses(rec,s,t,x)
    ok={frozenset(k) for k in ok}
    added=f[len(base):]; bad=[i for i,cl in enumerate(added) if frozenset(cl) not in ok]
    print(json.dumps({'tag':tag,'base':len(base),'prefix_match':prefix,'added':len(added),'unexplained':len(bad),'first':bad[:3]}),flush=True)
