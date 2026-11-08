"""Finite k<=5, W<=21 proof pass. Frozen path implications only; no ray discovery."""
from pathlib import Path
from itertools import product
from collections import Counter, defaultdict
import importlib.util,sys,json,time,hashlib,threading,subprocess,shutil
ROOT=Path(__file__).resolve().parent;OWNER=ROOT.parent;LEGACY=OWNER/'bounded-proof'
sys.path.insert(0,str(OWNER.parent))
spec=importlib.util.spec_from_file_location('encoder',ROOT/'inputs/encode.py')
model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
from pysat.solvers import Solver

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def matrices():return [(a,0,0,b) for a,b in product((1,-1),repeat=2)]+[(0,a,b,0) for a,b in product((1,-1),repeat=2)]
def frozen_guards(pair,x,cnf):
 s,t=[tuple(2*c for c in p) for p in pair];v=(t[0]-s[0],t[1]-s[1]);q=tuple(sorted(map(abs,v),reverse=True))
 g=next(g for g in matrices() if (g[0]*q[0]+g[1]*q[1],g[2]*q[0]+g[3]*q[1])==v)
 inp=ROOT/'inputs/guards';entries=[]
 for name in (f'certs-paths-{q[0]}_{q[1]}.json',f'claude-k4-w21-learned-L{q[0]},{q[1]}.jsonl'):
  p=inp/name
  if p.exists():entries.extend(json.loads(p.read_text()) if p.suffix=='.json' else [json.loads(l) for l in p.read_text().splitlines() if l.strip()])
 clauses=set()
 def add(r,g,origin):
  U=model.map_guard(r['U'],g,origin);Z=model.map_guard(r['Z'],g,origin)
  if U<=x.keys():clauses.add(tuple(sorted([-x[u] for u in U]+[x[z] for z in Z if z in x])))
 for r in entries:add(r,g,s)
 old=len(clauses)
 if q==(2,2):
  r=json.loads((ROOT/'cases/I2_1_1-pair0/guard.json').read_text())
  for origin,end in ((s,t),(t,s)):
   delta=(end[0]-origin[0],end[1]-origin[1])
   for g in matrices():
    if (2*g[0]+2*g[1],2*g[2]+2*g[3])==delta:add(r,g,origin)
 for clause in sorted(clauses):cnf.append(list(clause))
 return dict(old=old,new=len(clauses)-old,total=len(clauses))

def boundary(selected):
 adjacency=defaultdict(list)
 for e,ids in model.owners_of(selected).items():
  if len(ids)==1:
   a,b=e;adjacency[a].append(b);adjacency[b].append(a)
 assert all(len(v)==2 for v in adjacency.values())
 start=min(adjacency);cycle=[start];prev=None;current=start
 while True:
  nxt=next(v for v in sorted(adjacency[current]) if v!=prev)
  if nxt==start:break
  cycle.append(nxt);prev,current=current,nxt
  assert len(cycle)<=len(adjacency)
 assert len(cycle)==len(adjacency)
 vertices=[]
 for i,p in enumerate(cycle):
  a=cycle[i-1];b=cycle[(i+1)%len(cycle)]
  if (p[0]-a[0])*(b[1]-p[1])!=(p[1]-a[1])*(b[0]-p[0]):vertices.append(p)
 return vertices

def run(case,index,pair,seconds=45):
 tag=f'{case["tag"]}-pair{index}';folder=ROOT/'cases'/tag;folder.mkdir(parents=True,exist_ok=True)
 # Preserve the already independently verified pilot; no repeated work.
 if tag=='I2_6_0-pair0':return json.loads((folder/'result.json').read_text())
 start=time.monotonic();cnf,pool,x,ts=model.geometry(case,wmax=21,kmax=5);ng=frozen_guards(pair,x,cnf)
 cnf.to_file(str(folder/'formula.cnf'))
 (folder/'tile-variables.json').write_text(json.dumps([[t,v] for t,v in x.items()])+'\n')
 print(json.dumps(dict(tag=tag,phase='encoded',variables=cnf.nv,clauses=len(cnf.clauses),guards=ng)),flush=True)
 proof=[];sat=None;receipt=None
 with Solver(name='glucose4',bootstrap_with=cnf.clauses,with_proof=True) as solver:
  timer=threading.Timer(seconds,solver.interrupt);timer.start()
  try:
   sat=solver.solve_limited(expect_interrupt=True)
   if sat is False:proof=solver.get_proof()
   if sat is True:
    assignment=set(solver.get_model());selected=[t for t,v in x.items() if v in assignment]
    room=dict(triangles=selected,marked=[[2*a,2*b] for a,b in pair],require_simple=True)
    receipt=model.check(room,strict=False)
    assert receipt['walls']<=21 and len(receipt['transparent_vertices'])<=5
    vertices=boundary(selected);assert len(vertices)==receipt['walls']
    (folder/'residual-room.json').write_text(json.dumps(dict(room=room,geometry_receipt=receipt))+'\n')
    (folder/'vertices.json').write_text(json.dumps(dict(vertices=vertices,marked=room['marked'],scope='Fixed geometric SAT residual; no darkness assertion'),indent=2)+'\n')
   stats=solver.accum_stats()
  finally:timer.cancel()
 status='UNKNOWN' if sat is None else 'RESIDUAL' if sat else 'UNSAT_UNVERIFIED'
 if sat is False:
  with (folder/'proof.drat').open('w') as stream:
   for line in proof:stream.write(line+'\n')
  with (folder/'proof-check.log').open('w') as log:
   try:checked=subprocess.run([str(LEGACY/'drat-trim'),str(folder/'formula.cnf'),str(folder/'proof.drat')],stdout=log,stderr=subprocess.STDOUT,timeout=120)
   except subprocess.TimeoutExpired:checked=None
  if checked and checked.returncode==0 and 's VERIFIED' in (folder/'proof-check.log').read_text():status='VERIFIED_UNSAT'
 result=dict(tag=tag,status=status,W_cap=21,exception_cap=5,N_cap=38,partial_or_missing_cap=(31-4*len(case['full']))//2,full=case['full'],marks=pair,variables=cnf.nv,clauses=len(cnf.clauses),tiles=len(ts),guards=ng,seconds=round(time.monotonic()-start,3),solver_stats=stats,geometry_receipt=receipt,cnf_sha256=digest(folder/'formula.cnf'),encoder_sha256=digest(ROOT/'inputs/encode.py'),scope='Fixed full-star support and marked pair; necessary disk geometry and fixed universally validated illumination guards, k<=5,W<=21.')
 if sat is False:result['proof_sha256']=digest(folder/'proof.drat')
 (folder/'result.json').write_text(json.dumps(result,indent=2)+'\n');(folder/'run.log').write_text(json.dumps(result)+'\n')
 print(json.dumps(result),flush=True)
 return result

def main():
 cases=json.loads((ROOT/'inputs/branch-support.json').read_text())['cases']
 inp=ROOT/'inputs/guards';inp.mkdir(exist_ok=True)
 for c in cases:
  for pair in c['mark_pairs']:
   a,b=pair;q=sorted((abs(2*(b[0]-a[0])),abs(2*(b[1]-a[1]))),reverse=True)
   for name in (f'certs-paths-{q[0]}_{q[1]}.json',f'claude-k4-w21-learned-L{q[0]},{q[1]}.jsonl'):
    source=OWNER/'persisted-replay/inputs'/name
    if source.exists() and not (inp/name).exists():shutil.copy2(source,inp/name)
 inputs={str(p.relative_to(ROOT)):digest(p) for p in sorted(inp.iterdir()) if p.is_file()}
 # Positive control includes the newly added guard in all compatible orientations.
 controlcase=dict(next(c for c in cases if c['tag']=='I2_1_1'));allowed=set(map(tuple,controlcase['allowed']))
 allowed|={(x+dx,y+dy) for x,y in list(allowed) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))};controlcase['allowed']=sorted(allowed)
 cnf,pool,x,ts=model.geometry(controlcase,wmax=22,kmax=5);ng=frozen_guards(controlcase['mark_pairs'][0],x,cnf)
 chosen={tuple(sorted(map(tuple,t))) for t in json.loads((ROOT/'inputs/cand-2_2-1.json').read_text())['triangles']}
 assert chosen<=x.keys()
 with Solver(name='glucose4',bootstrap_with=cnf.clauses) as solver:assert solver.solve(assumptions=[v if t in chosen else -v for t,v in x.items()])
 print('known22 positive control PASS including new guards',flush=True)
 results=[]
 for c in cases:
  for i,pair in enumerate(c['mark_pairs']):
   results.append(run(c,i,pair))
   summary=dict(caps=dict(W=21,k=5,N=38),positive_control=True,input_hashes=inputs,counts=dict(Counter(r['status'] for r in results)),completed=len(results),expected=31,results=results)
   (ROOT/'pass-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print('COMPLETE',summary['counts'],flush=True)
if __name__=='__main__':main()
