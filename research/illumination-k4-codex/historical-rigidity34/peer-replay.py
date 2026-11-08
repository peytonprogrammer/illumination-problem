"""Reconstruct every supplied peer event using our own event geometry."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys,json
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B.parent/'rigidity-review'))
from event_geometry import EventModel,canon,rank,dot
if __name__=='__main__':
 model=EventModel(json.loads((B/'room.json').read_text()));given=json.loads((B/'inputs/events-room-tokarsky34-R18.json').read_text())['rows'];peer=json.loads((B/'inputs/funcs-room-tokarsky34-R18.json').read_text());rows=[tuple(map(F,r)) for r in peer['funcs']];assert len(rows)==len(given)==179
 # The peer traverses the same boundary in the opposite direction. Its
 # positive edge-length coordinates are therefore reversed. Off closure,
 # corner formulas may additionally differ by a closure row; compare on V.
 def ownchart(row):return tuple(list(map(F,row[:2]))+list(reversed(list(map(F,row[2:2+model.W]))))+list(map(F,row[2+model.W:])))
 peerclosure=[ownchart(c) for c in peer['clos']]
 assert rank([*model.closure,*peerclosure])==2
 uniform=ownchart(peer['syms'][2]);assert uniform==model.theta
 rows=[ownchart(r) for r in rows]
 assert rank([*model.syms,*[ownchart(s) for s in peer['syms']]])==4
 directions=sorted({tuple(e['dir']) for e in given});found={};other=Counter()
 for q in directions:
  for side in (-1,1):
   e=model.event(q,side)
   if e['status']=='EVENT':found[(canon(model.project(e['row'])),tuple(e['direction']),tuple(e['corner']),tuple(e['unfolded_target_minus_s']))]=e
   else:other[e['status']]+=1
 for row,meta in zip(rows,given):
  e=found[(canon(model.project(row)),tuple(meta['dir']),tuple(meta['corner']),tuple(meta['unfolded_target_minus_s']))]
  assert list(e['direction'])==meta['dir'] and list(e['corner'])==meta['corner'] and e['unfolded_target_minus_s']==meta['unfolded_target_minus_s']
 coefficients=json.loads((B/'inputs/posspan-room-tokarsky34-R18.json').read_text())['coefficients'];coeff={int(i):F(v) for i,v in coefficients.items()}
 assert set(coeff)==set(range(len(rows))) and all(v>0 for v in coeff.values())
 total=[sum(coeff[i]*row[j] for i,row in enumerate(rows)) for j in range(model.dim)];assert rank([*model.closure,total])==2
 r=rank([*model.closure,*rows])-2;assert r==34 and all(dot(g,s)==0 for g in rows for s in model.syms)
 out=dict(status='PASS',supplied_events=len(rows),matched_events=len(rows),supplied_directions=len(directions),sides_replayed=2*len(directions),other_limits=dict(other),rank_on_closure=r,kernel_dimension=model.dim-2-r,axis_affine_symmetry_dimension=rank(model.syms),strict_positive_coefficients=len(coeff),dependency_verified_exactly=True,parameter_chart='Peer positive edge lengths reversed; gradients compared modulo the two closure equations',scope='Fixed179-event peer certificate replay with independent geometry; not a new direction scan.')
 (B/'peer-replay.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
