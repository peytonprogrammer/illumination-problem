"""Symbolic local-angle formulas for fourteen hand-listed e2 fans, no assignments."""
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'triangle-composition/inputs'))
import illumination_geometry as g
D=g.DIRS
tri=lambda t:tuple(sorted(map(tuple,t)))
def fan(c,st,m):return {tri((c,(c[0]+D[i%8][0],c[1]+D[i%8][1]),(c[0]+D[(i+1)%8][0],c[1]+D[(i+1)%8][1]))) for i in range(st,st+m)}
H=set().union(*(fan(c,0,8) for c in [(0,0),(2,0),(2,2)]))
caps={n:tri(t) for n,t in json.loads((ROOT/'triangle-composition/inputs/caps.json').read_text())['cap_options'].items()}
def angle(t,p):return len(g.wedge_slots(t,p)) if p in t else 0
out={}
for site,c,starts in [('L',(-2,0),{3:[6,7,0],4:[5,6,7,0]}),('B',(0,-2),{3:[7,0,1],4:[6,7,0,1]})]:
 for m,ss in starts.items():
  for st in ss:
   root=fan(c,st,m);fixed=H|root
   variables={n:t for n,t in caps.items() if not n.startswith(site)}
   force=['B+','E-','T-'] if site=='L' else ['L+','E-']
   fixed|={caps[n] for n in force}
   variables={n:t for n,t in variables.items() if n not in force and not any(n[0]==f[0] and n!='Nb+' and n!='Nr-' and n!='Nr+' and n!='Nb-' for f in force)}
   # The above filtering treats forced critical B/E/T/L slots only; N stays variable.
   points=set().union(*(set(t) for t in fixed|set(variables.values())))
   J=sum(sum(angle(t,p) for t in fixed)==8 for p in points if g.label(p)!='A')
   fC=[];B=[]
   for p in sorted(points):
    base=sum(angle(t,p) for t in fixed)
    terms={n:angle(t,p) for n,t in variables.items() if p in t}
    if g.label(p)=='C' and base==4 and {t for t in fixed if p in t}!={t for t in H if p in t}:
     fC.append(p)
    if g.label(p)=='B' and base<=4 and base+sum(terms.values())>=4 and (base or terms):
     B.append({'point':p,'fixed_angle_45':base,'variable_angles_45':terms,'smooth_when_sum':4-base})
   key=f'{site}_m{m}_start{st}'
   out[key]={'fixed_triangles':sorted(fixed),'variable_caps':variables,'J':J,'forced_caps':force,'outside_smooth_C':fC,'potential_smooth_B':B,'ordinary_count_required_at_k6_Delta4':J+3}
   print(key,'J',J,'n',J+3,'C',fC,'B',B)
(HERE/'single-e2-charge.json').write_text(json.dumps({'status':'SYMBOLIC_ANGLE_TABLE','scope':'14 hand-listed fans, local angle coefficient extraction only. No cap assignments, polygons, trajectories, archive or solver.','families':out},indent=2)+'\n')
