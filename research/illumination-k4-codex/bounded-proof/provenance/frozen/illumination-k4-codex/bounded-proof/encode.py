"""Independent CNF model of simple canonical rooms; static certified guards only.
No peer executable imports. Support list is the earlier Codex geometric reduction.
"""
from pathlib import Path
from itertools import combinations,product
from collections import defaultdict,Counter
from fractions import Fraction as F
import json,sys,time,hashlib
from functools import lru_cache
HERE=Path(__file__).resolve().parent;BASE=HERE.parent.parent;sys.path.insert(0,str(BASE))
from illumination_geometry import patch,label,owners_of,local_sectors,check
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc,EncType as CardType
from pysat.pb import PBEnc,EncType as PBType
from pysat.solvers import Solver


def add_card(cnf,pool,lits,bound):
 if len(lits)>bound:cnf.extend(CardEnc.atmost(lits=lits,bound=bound,vpool=pool,encoding=CardType.seqcounter).clauses)


@lru_cache(maxsize=None)
def fan_table(relative):
 rows=[]
 for mask in range(1<<len(relative)):
  chosen=[t for i,t in enumerate(relative) if mask>>i&1];own=owners_of(chosen);opened={edge for edge,ids in own.items() if len(ids)==2}
  sectors,full=local_sectors(chosen,(0,0),opened)
  if chosen and not full and len(sectors)!=1:continue
  smooth=bool(chosen) and not full and sectors==[4]
  corner=bool(chosen) and not full and not smooth
  rows.append((mask,bool(chosen),full,smooth,corner,sectors[0] if corner else 0))
 return rows


def geometry(case,wmax=21,kmax=4):
 F0={tuple(p) for p in case['full']};R0=F0|{(a+dx,b+dy) for a,b in F0 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))}
 radius=max(0,(wmax-4*len(F0)+2*kmax)//2-len(R0-F0));allowed=set(R0)
 for step in range(radius):allowed|={(a+dx,b+dy) for a,b in allowed for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))}
 assert allowed<={tuple(p) for p in case['allowed']}
 ts=sorted({t for a,b in allowed for t in patch(2*a-1,2*a+1,2*b-1,2*b+1)})
 pool=IDPool();x={t:pool.id(('t',t)) for t in ts};cnf=CNF();inc=defaultdict(list)
 for t in ts:
  for p in t:inc[p].append(t)
 fulls={tuple(2*c for c in p) for p in case['full']};a_used={};walls=[]
 for tri,v in x.items():
  if any(a in tri for a in fulls):cnf.append([v]);exceptions=[];angle_lits=[];angle_weights=[]
 for p,r in sorted(inc.items()):
  kind=label(p);w=pool.id(('corner',p));walls.append(w)
  if kind=='A':
   a_used[p]=pool.id(('A-used',p));cnf.append([-a_used[p]]+[x[tri] for tri in r])
   for tri in r:cnf.append([-x[tri],a_used[p]])
  e=pool.id(('exception',p)) if kind!='A' else None
  if e:exceptions.append(e)
  bits=[pool.id(('angle',p,i)) for i in range(3)]
  # Propagation-strengthening consequences of the exact local truth table.
  for bit in bits:cnf.append([-bit,w])
  cnf.append([-w]+bits);cnf.append([-w]+[x[tri] for tri in r])
  if e:
   cnf.append([-e,-w]);cnf.append([-e]+[x[tri] for tri in r])
   for tri in r:cnf.append([-x[tri],e,w])
  if kind=='C':cnf.extend([[-bits[0]],[-bits[1],w],[-w,bits[1]]])
  for bit,weight in zip(bits,(1,2,4)):angle_lits.append(-bit);angle_weights.append(weight)
  relative=tuple(tuple((q[0]-p[0],q[1]-p[1]) for q in tri) for tri in r)
  rows=[row for row in fan_table(relative) if kind!='A' or row[2]==(p in fulls)]
  selectors=[];rowvalues=[]
  for mask,occupied,full,smooth,corner,angle in rows:
   sel=pool.id(('fan',p,mask));selectors.append(sel)
   vals=[(x[tri],bool(mask>>i&1)) for i,tri in enumerate(r)]+[(w,corner)]
   if e:vals.append((e,occupied and (full or smooth)))
   if kind=='A':vals.append((a_used[p],occupied))
   vals.extend((bit,bool(angle>>i&1)) for i,bit in enumerate(bits))
   for var,val in vals:cnf.append([-sel,var if val else -var])
   rowvalues.append(dict(vals))
  cnf.append(selectors)
  # Support clauses provide propagation from each channel literal to legal rows.
  channels=[x[tri] for tri in r]+[w]+([e] if e else [])+([a_used[p]] if kind=='A' else [])+bits
  for var in channels:
   cnf.append([-var]+[sel for sel,vals in zip(selectors,rowvalues) if vals[var]])
   cnf.append([var]+[sel for sel,vals in zip(selectors,rowvalues) if not vals[var]])
 # Exactly all full A stars above; all BC exceptions remain at-most, covering C1 too.
 add_card(cnf,pool,list(x.values()),4*(wmax-2+2*kmax)//3)
 add_card(cnf,pool,walls,wmax);add_card(cnf,pool,exceptions,kmax)
 # Connected-cell degree inequality: P+missing <= floor((W-4I+2k)/2).
 # Thus occupied A cells outside full cells plus their four-neighbors <= cap-b.
 Fcells={tuple(p) for p in case['full']};R=Fcells|{(a+dx,b+dy) for a,b in Fcells for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))}
 cap=(wmax-4*len(Fcells)+2*kmax)//2;outside=[v for p,v in a_used.items() if (p[0]//2,p[1]//2) not in R]
 budget=cap-len(R-Fcells)
 if budget<0:cnf.append([])
 else:add_card(cnf,pool,outside,budget)
 # Necessary connectivity of occupied A cells; finite reachability from a full cell.
 # A connected room has at most I+cap occupied A cells, so depth I+cap-1 suffices.
 root=min(fulls);depth=len(fulls)+cap-1
 previous={p:pool.id(('reach',0,p)) for p in a_used}
 for p,r in previous.items():cnf.append([r if p==root else -r])
 for step in range(1,depth+1):
  current={p:pool.id(('reach',step,p)) for p in a_used}
  for p,r in current.items():
   cnf.append([-r,a_used[p]])
   pred=[previous[p]]+[previous[q] for q in ((p[0]+2,p[1]),(p[0]-2,p[1]),(p[0],p[1]+2),(p[0],p[1]-2)) if q in previous]
   cnf.append([-r]+pred)
  previous=current
 for p,v in a_used.items():cnf.append([-v,previous[p]])
 # Exact triangle connectivity from all eight triangles of a forced full A star.
 adjacency={tri:set() for tri in ts}
 for ids in owners_of(ts).values():
  if len(ids)==2:
   ta,tb=[ts[j] for j in ids];adjacency[ta].add(tb);adjacency[tb].add(ta)
 depth=4*(wmax-2+2*kmax)//3-8;origin=min(fulls)
 previous={tri:pool.id(('tri-reach',0,tri)) for tri in ts}
 for tri,r in previous.items():cnf.append([r if origin in tri else -r])
 for step in range(1,depth+1):
  current={tri:pool.id(('tri-reach',step,tri)) for tri in ts}
  for tri,r in current.items():
   cnf.append([-r,x[tri]])
   cnf.append([-r,previous[tri]]+[previous[u] for u in sorted(adjacency[tri])])
  previous=current
 for tri,v in x.items():cnf.append([-v,previous[tri]])
 # Gauss-Bonnet for a disk: sum_corner(4-angle_units)=8.
 # Negative corner-angle bits are complemented into positive PB terms.
 rhs=8+sum(angle_weights)
 pb=PBEnc.equals(lits=walls+angle_lits,weights=[4]*len(walls)+angle_weights,bound=rhs,vpool=pool,encoding=PBType.adder)
 cnf.extend(pb.clauses)
 return cnf,pool,x,ts


def map_guard(raw,g,source):
 return frozenset(tuple(sorted((g[0]*p[0]+g[1]*p[1]+source[0],g[2]*p[0]+g[3]*p[1]+source[1]) for p in t)) for t in raw)


def guards(case,pair,x,cnf):
 s,t=[tuple(2*c for c in p) for p in pair];v=(t[0]-s[0],t[1]-s[1]);q=tuple(sorted(map(abs,v),reverse=True))
 matrices=[(a,0,0,b) for a,b in product((1,-1),repeat=2)]+[(0,a,b,0) for a,b in product((1,-1),repeat=2)]
 g=next(g for g in matrices if (g[0]*q[0]+g[1]*q[1],g[2]*q[0]+g[3]*q[1])==v)
 inp=HERE.parent/'persisted-replay/inputs';entries=[]
 p=inp/f'certs-paths-{q[0]}_{q[1]}.json'
 if p.exists():entries.extend(json.loads(p.read_text()))
 p=inp/f'claude-k4-w21-learned-L{q[0]},{q[1]}.jsonl'
 if p.exists():entries.extend(json.loads(l) for l in p.read_text().splitlines() if l.strip())
 count=0;seen=set()
 for r in entries:
  U=map_guard(r['U'],g,s)
  if not U<=x.keys():continue
  Z=map_guard(r['Z'],g,s)
  clause=tuple(sorted([-x[u] for u in U]+[x[z] for z in Z if z in x]))
  if clause not in seen:cnf.append(clause);seen.add(clause);count+=1
 return count


def components(selected):
 own=owners_of(selected);adj={t:set() for t in selected}
 for ids in own.values():
  if len(ids)==2:
   a,b=[selected[i] for i in ids];adj[a].add(b);adj[b].add(a)
 out=[];left=set(selected)
 while left:
  seed=next(iter(left));todo=[seed];part={seed};left.remove(seed)
  for t in todo:
   for u in adj[t]&left:left.remove(u);part.add(u);todo.append(u)
  out.append(part)
 return out


def solve_case(case,index,pair,seconds=120,solver_name="glucose4"):
 tag=f'{case["tag"]}-pair{index}';folder=HERE/'cases'/tag;folder.mkdir(parents=True,exist_ok=True);start=time.monotonic()
 cnf,pool,x,ts=geometry(case);ng=guards(case,pair,x,cnf);conncuts=0;cut_records=[]
 print(json.dumps(dict(tag=tag,phase='encoded',variables=cnf.nv,clauses=len(cnf.clauses),guards=ng,seconds=round(time.monotonic()-start,2))),flush=True)
 s=tuple(2*c for c in pair[0]);t=tuple(2*c for c in pair[1]);root=next(tri for tri in ts if s in tri)
 # Marks are two selected full stars from the fixed full-cell support.
 assert s in {tuple(2*c for c in p) for p in case['full']} and t in {tuple(2*c for c in p) for p in case['full']}
 own_all=owners_of(ts);adj=defaultdict(set)
 for ids in own_all.values():
  if len(ids)==2:
   a,b=[ts[i] for i in ids];adj[a].add(b);adj[b].add(a)
 with Solver(name=solver_name,bootstrap_with=cnf.clauses,with_proof=True) as solver:
  # A timeout yields UNKNOWN; it cannot be an exclusion.
  import threading
  timer=threading.Timer(seconds,solver.interrupt) if solver_name=="glucose4" else None
  if timer:timer.start()
  else:solver.conf_budget(1000000)
  try:
   while True:
    sat=solver.solve_limited(expect_interrupt=True)
    if sat is None:status='UNKNOWN';break
    if not sat:status='UNSAT';break
    model=set(solver.get_model());selected=[tri for tri in ts if x[tri] in model];parts=components(selected)
    if len(parts)==1:
     room=dict(triangles=selected,marked=[s,t],require_simple=True);receipt=check(room,strict=False)
     (folder/'residual-room.json').write_text(json.dumps(room)+'\n');status='RESIDUAL';break
    for part in parts:
     if root in part:continue
     boundary=set().union(*(adj[tri] for tri in part))-part
     # Every connected completion containing root and this fixed seed crosses boundary.
     seed=min(part);clause=[-x[seed]]+[x[tri] for tri in sorted(boundary)]
     solver.add_clause(clause);cnf.append(clause);conncuts+=1;cut_records.append(dict(seed=seed,component=sorted(part),boundary=sorted(boundary),clause=clause))
   proof=solver.get_proof() if status=='UNSAT' else []
   stat=solver.accum_stats()
  finally:
   if timer:timer.cancel()
 cnf.to_file(str(folder/'formula.cnf'))
 (folder/'connectivity-cuts.json').write_text(json.dumps(cut_records)+'\n')
 (folder/'tile-variables.json').write_text(json.dumps([[t,v] for t,v in x.items()])+'\n')
 if status=='UNSAT':(folder/'proof.drat').write_text('\n'.join(proof)+'\n')
 result=dict(tag=tag,status=status,solver=solver_name,variables=cnf.nv,clauses=len(cnf.clauses),tiles=len(ts),guards=ng,connectivity_cuts=conncuts,seconds=round(time.monotonic()-start,3),solver_stats=stat,
             full=case['full'],marks=pair,scope='At most four exceptions, at most 21 walls; fixed full-A support; necessary geometric relaxation plus static validated paths.')
 (folder/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
 return result

if __name__=='__main__':
 cases=json.loads((HERE.parent/'branch-support.json').read_text())['cases']
 tag=sys.argv[1] if len(sys.argv)>1 else 'I2_1_1'
 for c in cases:
  if c['tag']==tag:
   for i,pair in enumerate(c['mark_pairs']):solve_case(c,i,pair)
