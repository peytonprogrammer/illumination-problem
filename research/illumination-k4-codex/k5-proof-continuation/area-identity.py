"""Redundant exact area/angle ledger for simple canonical rooms.
3N + E_A = 4(W-2) + 4k + 4J,
where J counts full interior non-A vertices and k counts full or smooth
non-A vertices. Each canonical triangle contributes angle units 1 at A,
1 at B,2 at C. Non-A total is 3N; remove 8 per full and4 per smooth
vertex. Adding A corner angles gives the polygon's 4(W-2) angle sum.
"""
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as F
import importlib.util,json
ROOT=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('pilot',ROOT.parent/'k5-proof-pilot/pass.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
sp=importlib.util.spec_from_file_location('a',ROOT.parent/'persisted-replay/audit.py');a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)

def add_area(cnf,pool,x):
 points=sorted({v for t in x for v in t});walls=[pool.id(('corner',v)) for v in points]
 exceptions=[];full=[];angle=[];weights=[]
 for v in points:
  if p.model.label(v)=='A':
   for i,w in enumerate((1,2,4)):angle.append(pool.id(('angle',v,i)));weights.append(w)
  else:
   exceptions.append(pool.id(('exception',v)));j=pool.id(('area-full-nonA',v));full.append(j)
   incident=a.incident(tuple(map(F,v)))
   if not incident<=x.keys():cnf.append([-j]);continue
   for tri in incident:cnf.append([-j,x[tri]])
   cnf.append([j]+[-x[tri] for tri in sorted(incident)])
 complemented=walls+exceptions+full
 rhs=4*len(complemented)-8
 pb=p.model.PBEnc.equals(lits=list(x.values())+angle+[-v for v in complemented],weights=[3]*len(x)+weights+[4]*len(complemented),bound=rhs,vpool=pool,encoding=p.model.PBType.adder)
 cnf.extend(pb.clauses)
 return dict(full_variables=len(full),area_clauses=len(pb.clauses),variables=cnf.nv)

def census(room):
 receipt=p.model.check(room,strict=False);ts=a.triangles(room['triangles']);points={v for t in ts for v in t};ea=0;j=0
 for v in points:
  complete=a.incident(tuple(map(F,v)))<=ts
  if complete and p.model.label(v)!='A':j+=1
  if p.model.label(v)=='A':
   fan=receipt['sectors'].get(str(v),[])
   ea+=sum(n for n in fan if n!=4)
 N=len(ts);W=receipt['walls'];k=len(receipt['transparent_vertices'])
 assert 3*N+ea==4*(W-2)+4*k+4*j,(N,ea,W,k,j)
 return dict(N=N,W=W,k=k,J=j,E_A=ea)

def main():
 from pysat.solvers import Solver
 fixtures=sorted((ROOT/'cases').glob('*/generations/*/residual-room.json'))[::29][:250];rows=[]
 for f in fixtures:
  raw=json.loads(f.read_text());rows.append(census(raw['room']))
 # Known22room is a negative control for a 21-wall exclusion.
 cases=json.loads((p.ROOT/'inputs/branch-support.json').read_text())['cases'];case=dict(next(c for c in cases if c['tag']=='I2_1_1'));allowed=set(map(tuple,case['allowed']));allowed|={(x+dx,y+dy) for x,y in list(allowed) for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))};case['allowed']=sorted(allowed)
 cnf,pool,x,ts=p.model.geometry(case,wmax=22,kmax=5);info=add_area(cnf,pool,x);room=json.loads((p.ROOT/'inputs/cand-2_2-1.json').read_text());chosen=a.triangles(room['triangles']);assert chosen<=x.keys()
 with Solver(name='glucose4',bootstrap_with=cnf.clauses) as solver:assert solver.solve(assumptions=[v if t in chosen else -v for t,v in x.items()])
 out=dict(status='PASS',fixed_room_ledgers=len(rows),known22_allowed=True,encoding=info,rows=rows,scope='Exact angle counting and redundant CNF identity; no optical searches.')
 (ROOT/'area-identity-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'}))
if __name__=='__main__':main()
