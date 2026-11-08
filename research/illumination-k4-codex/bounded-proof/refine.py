from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,wait,FIRST_COMPLETED
from collections import defaultdict,deque
import json,sys,time
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from encode import fan_table
from verify import verify
from pysat.formula import CNF
from pysat.solvers import Solver


def unit_trace(clauses):
 occ=defaultdict(list);rem=[];sat=[False]*len(clauses);queue=deque();values={};trace=[]
 for ci,c in enumerate(clauses):
  rem.append(len(c))
  if not c:return values,trace,ci
  for lit in c:occ[lit].append(ci)
  if len(c)==1:queue.append((c[0],ci))
 while queue:
  lit,reason=queue.popleft();v=abs(lit)
  if v in values:
   if values[v]!=(lit>0):return values,trace,reason
   continue
  values[v]=lit>0;trace.append([lit,reason])
  for ci in occ[lit]:sat[ci]=True
  for ci in occ[-lit]:
   if sat[ci]:continue
   rem[ci]-=1
   if rem[ci]==0:return values,trace,ci
   if rem[ci]==1:
    unset=[l for l in clauses[ci] if abs(l) not in values]
    assert len(unset)==1
    queue.append((unset[0],ci))
 return values,trace,None


def work(path,first=False):
 folder=Path(path)
 if (folder/'verification.json').exists():return dict(kind='closed',path=path,receipt=json.loads((folder/'verification.json').read_text()))
 cnf=CNF(from_file=str(folder/'formula.cnf'))
 if not first:
  start=time.monotonic()
  with Solver(name='cadical300',bootstrap_with=cnf.clauses,with_proof=True) as s:
   s.conf_budget(10000);got=s.solve_limited();proof=s.get_proof() if got is False else []
  if got is False:
   (folder/'proof.drat').write_text('\n'.join(proof)+'\n');r=json.loads((folder/'result.json').read_text());r['status']='UNSAT';r['refined_seconds']=round(time.monotonic()-start,3);(folder/'result.json').write_text(json.dumps(r,indent=2)+'\n')
   return dict(kind='closed',path=path,receipt=verify(folder))
  if got is True:return dict(kind='SAT',path=path)
 known,trace,conflict=unit_trace(cnf.clauses)
 (folder/'unit-trace.json').write_text(json.dumps(dict(trace=trace,conflict_clause=conflict))+'\n')
 if conflict is not None:
  (folder/'proof.drat').write_text('');r=json.loads((folder/'result.json').read_text());r['status']='UNSAT';(folder/'result.json').write_text(json.dumps(r,indent=2)+'\n');return dict(kind='closed',path=path,receipt=verify(folder))
 tiles={tuple(sorted(map(tuple,t))):v for t,v in json.loads((folder/'tile-variables.json').read_text())}
 cells=defaultdict(list)
 for t,v in tiles.items():
  
  for a in t:cells[a].append((t,v))
 choices=[];fulls={tuple(2*c for c in p) for p in json.loads((folder/'result.json').read_text())['full']}
 for center,rows in cells.items():
  rows=sorted(rows);ring=[v for t,v in rows]
  if all(v in known for v in ring):continue
  relative=tuple(tuple((p[0]-center[0],p[1]-center[1]) for p in t) for t,v in rows)
  kind='A' if center[0]%2==center[1]%2==0 else 'B' if center[0]%2 and center[1]%2 else 'C'
  masks=[r[0] for r in fan_table(relative) if kind!='A' or r[2]==(center in fulls)]
  compatible=[m for m in masks if all(v not in known or bool(m>>i&1)==known[v] for i,v in enumerate(ring))]
  assert compatible
  active=any(known.get(v)==True for v in ring)
  choices.append((0 if active else 1,len(compatible),-sum(v in known for v in ring),center,ring,masks,compatible))
 assert choices,'no unresolved fan without a contradiction'
 _,_,_,center,ring,masks,compatible=min(choices)
 children=[];meta=json.loads((folder/'result.json').read_text())
 for mask in compatible:
  child=folder/'children'/f'mask{mask}';child.mkdir(parents=True,exist_ok=True)
  units=[[v if mask>>i&1 else -v] for i,v in enumerate(ring)]
  f=CNF(from_clauses=cnf.clauses+units);f.to_file(str(child/'formula.cnf'))
  (child/'tile-variables.json').write_bytes((folder/'tile-variables.json').read_bytes());(child/'connectivity-cuts.json').write_text('[]\n')
  r=dict(meta,tag=meta['tag']+f'/mask{mask}',status='UNKNOWN');(child/'result.json').write_text(json.dumps(r,indent=2)+'\n');children.append(str(child))
 (folder/'refinement.tmp').write_text(json.dumps(dict(center=center,ring_variables=ring,legal_masks=masks,compatible_masks=compatible,children=children),indent=2)+'\n')
 (folder/'refinement.tmp').replace(folder/'refinement.json')
 return dict(kind='split',path=path,children=children)


def main():
 d=json.loads((HERE/'split-summary.json').read_text());roots=[]
 for r in d['cases']:
  if r['status']!='VERIFIED':
   parent,mask=r['tag'].split('/');roots.append(str(HERE/'cases'/parent/'split'/mask))
 stats=dict(roots=len(roots),closed=0,split=0,SAT=0,errors=[]);pending={}
 with ProcessPoolExecutor(max_workers=6) as pool:
  def gather(path,first):
   p=Path(path)
   if (p/'verification.json').exists():
    try:
     if json.loads((p/'verification.json').read_text()).get('status')=='VERIFIED':return
    except json.JSONDecodeError:(p/'verification.json').unlink()
   if (p/'refinement.json').exists():
    try:meta=json.loads((p/'refinement.json').read_text())
    except json.JSONDecodeError:(p/'refinement.json').unlink();meta=None
    if meta is not None:
     base=CNF(from_file=str(p/'formula.cnf'))
     for child,mask in zip(meta['children'],meta['compatible_masks']):
      c=Path(child)
      if not (c/'verification.json').exists():
       units=[[v if mask>>i&1 else -v] for i,v in enumerate(meta['ring_variables'])]
       CNF(from_clauses=base.clauses+units).to_file(str(c/'formula.cnf'))
       if not (c/'result.json').exists() or not (c/'result.json').read_text().strip():
        r=json.loads((p/'result.json').read_text());r['tag']+=f'/mask{mask}';r['status']='UNKNOWN';(c/'result.json').write_text(json.dumps(r)+'\n')
      gather(child,False)
     return
   pending[pool.submit(work,path,first)]=path
  for path in roots:gather(path,True)
  while pending:
   done,_=wait(pending,timeout=30,return_when=FIRST_COMPLETED)
   for f in done:
    path=pending.pop(f)
    try:r=f.result()
    except Exception as e:stats['errors'].append(dict(path=path,error=repr(e)));print('ERROR',path,repr(e),flush=True);continue
    stats[r['kind']]+=1
    if r['kind']=='split':
     for child in r['children']:pending[pool.submit(work,child)]=child
    if r['kind']=='SAT':print('SAT',path,flush=True)
   stats['pending']=len(pending);(HERE/'refine-summary.json').write_text(json.dumps(stats,indent=2)+'\n')
   if done:print('REFINE',json.dumps(stats),flush=True)
 print('REFINE FINISHED',json.dumps(stats),flush=True)

if __name__=='__main__':main()
