"""Six prescribed guard implications for the omitted e3+e1 row; no search."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
inputs={
 'caps':ROOT/'zero-surplus-L/guard-incidence-check.json',
 'zero':ROOT/'zero-surplus-L/cover-check.json',
 'square':ROOT/'first-surplus-review/square-exchange-check.json',
 'five':ROOT/'second-surplus-review/five-path-check.json',
 'guard':ROOT/'lower-bound-proof-audit/full-replay/guard-checker.py',
}
read=lambda n:json.loads(inputs[n].read_text())
tri=lambda t:tuple(sorted(map(tuple,t)))
dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
def fan(c,ss):
 return {tri((c,(c[0]+dirs[i%8][0],c[1]+dirs[i%8][1]),(c[0]+dirs[(i+1)%8][0],c[1]+dirs[(i+1)%8][1]))) for i in ss}
H=set().union(*(fan(c,range(8)) for c in [(0,0),(2,0),(2,2)]))
caps={n:tri(t) for n,t in read('caps')['cap_options'].items()}
C=lambda ns:{caps[n] for n in ns}
decode=lambda p:[tuple(F(*v) for v in q) for q in p]
z=read('zero')['paths'];sq=read('square')['paths']
paths={'one':decode(z['one']['path']),'one_sigma':decode(z['one_sigma']['path']),'sigma_four':decode(z['four_sigma']['path']),'B_two':decode(sq['B_four']['path']),'five':decode(read('five')['five_path']),'sigma13':decode(z['thirteen_sigma']['path'])}
B=fan((0,-2),[0,1]);D=fan((2,-2),[3,4,5]);Dall=fan((2,-2),range(8))
base=H|B|D
remaining=C([n for n in caps if n not in ['B-','B+','D-','D+']])
full=H|B|Dall|remaining
cases=[
 ('missing_E','one_sigma',base,full-C(['E-'])),
 ('missing_L','sigma_four',base|C(['E-']),full-C(['E+','L+'])),
 ('missing_T','B_two',base,full-C(['T-'])),
 ('Nbplus_absent','five',base|C(['L+','E-','T-']),H|B|Dall|C(['L+','E-','T-','R-','R+','Nb-','Nr-','Nr+'])),
 ('Nbplus_present','sigma13',base|C(['L+','E-','T-','Nb+']),H|B|Dall|C(['L+','E-','T-','Nb+','R-','R+'])),
 ('opposite_root_Bplus_absent','one',H|fan((2,-2),[2,3])|fan((0,-2),[6,7,0]),(H|Dall|fan((0,-2),range(8))|remaining)-C(['B+'])),
]
g=runpy.run_path(str(inputs['guard']))
sigma=lambda p:(2-p[1],2-p[0])
transform=lambda ts:{tri(sigma(p) for p in t) for t in ts}
out=[]
for name,which,fixed,possible in cases:
 P=paths[which];u,zz=g['path_requirements'](P)
 assert u<=fixed,(name,'required',u-fixed)
 assert not zz&possible,(name,'forbidden',zz&possible)
 assert P[0]==(0,0) and P[-1]==(2,2)
 us,zs=g['path_requirements']([sigma(p) for p in P[::-1]])
 assert us==transform(u) and zs==transform(zz)
 out.append({'name':name,'path':which,'reflections':len(P)-2,'status':'PASS','sigma':'PASS','required':sorted(u),'forbidden':sorted(zz),'fixed':sorted(fixed),'possible':sorted(possible)})
result={'status':'PASS','scope':'Six prescribed inherited path implications and sigma. Full D support in active B-root clauses. No new rooms, directions, words or archives. Hand completeness separate.','checks':out,'input_sha256':{n:hashlib.sha256(p.read_bytes()).hexdigest() for n,p in inputs.items()}}
(HERE/'local-partition-guards.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: six inherited implications with full neighboring-cell support, plus sigma')
