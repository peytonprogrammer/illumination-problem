"""Independently check the peer's four missing in-K single-leaf orientations."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,json,runpy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
# Reuse our own geometry helpers and prior verified implication, not peer code.
a=runpy.run_path(str(HERE/'check.py'))
H,caps,fan,polygon,g=a['H'],a['caps'],a['fan'],a['polygon'],a['geom']
from guard_checker import path_requirements
from boundary_replay import replay
tri=a['tri'];decode=lambda raw:[tuple(F(*v) for v in p) for p in raw]
zero=json.loads((ROOT/'zero-surplus-L/cover-check.json').read_text())['paths']
short=json.loads((ROOT/'first-surplus-review/square-exchange-check.json').read_text())['paths']
five=json.loads((ROOT/'second-surplus-review/five-path-check.json').read_text())['five_path']
paths={'one':decode(zero['one']['path']),'one_sigma':decode(zero['one_sigma']['path']),'sigma_four':decode(zero['four_sigma']['path']),'B_two':decode(short['B_four']['path']),'five':decode(five),'sigma13':decode(zero['thirteen_sigma']['path'])}
B=fan((0,-2),0,2);D=fan((2,-2),3,1)
allcaps=set(caps.values());fixed0=H|B|D
remaining={n:t for n,t in caps.items() if n not in ['B-','B+','D-','D+']}
base=fixed0|{caps[n] for n in ['L+','E-','T-']}
cases={
 'missing_E':('one_sigma',fixed0,(fixed0|set(remaining.values()))-{caps['E-']}),
 'missing_L':('sigma_four',fixed0|{caps['E-']},(fixed0|set(remaining.values()))-{caps['E+'],caps['L+']}),
 'missing_T':('B_two',fixed0,(fixed0|set(remaining.values()))-{caps['T-']}),
 'Nbplus_absent':('five',base,(base|{caps[n] for n in ['R-','R+','Nb-','Nr-','Nr+']})),
 'Nbplus_present':('sigma13',base|{caps['Nb+']},base|{caps[n] for n in ['Nb+','R-','R+']}),
}
sigma=lambda p:(2-p[1],2-p[0])
transform=lambda ts:{tri(sigma(p) for p in t) for t in ts}
receipts={}
for name,(which,fixed,possible) in cases.items():
 P=paths[which];u,z=path_requirements(P)
 assert u<=fixed and not z&possible,(name,u-fixed,z&possible)
 Ps=[sigma(p) for p in P][::-1];us,zs=path_requirements(Ps)
 assert us==transform(u) and zs==transform(z)
 receipts[name]={'path':which,'reflections':len(P)-2,'symbolic':'PASS','sigma':'PASS'}
# Opposite root orientation: D quarter2/3, B single0, hence B+ absent.
other=H|fan((2,-2),2,2)|fan((0,-2),0,1)
u,z=path_requirements(paths['one'])
assert u<=other and not z&(other|set(remaining.values()))
control=base|{caps[n] for n in ['Nb-','R+']}
data=g.check({'triangles':sorted(control),'marked':[(0,0),(2,2)],'require_simple':True},strict=False)
assert data['walls']==20 and len(data['transparent_vertices'])==6 and set(data['interior_A'])=={(0,0),(2,0),(2,2)}
V=polygon(control);replay(V,(0,0),(2,2),paths['five']);replay(V,(2,2),(0,0),paths['five'][::-1])
# Direct local fan bookkeeping independent of the peer's ledger code.
os=g.owners_of(list(control));opens={e for e,ls in os.items() if len(ls)==2}
Q=J=sN=missing=0
for p in {p for t in control for p in t}:
 angles,full=g.check_fan_angles(list(control),p,os,opens)
 if g.label(p)=='A':
  if not full:Q+=3 if angles==[4] else sum(angles)
 else:
  J+=full;sN+=not full and angles==[4]
  if g.label(p)=='C' and not full and angles==[4] and {t for t in control if p in t}=={t for t in H if p in t}:missing+=1
assert (Q,J,sN,Q+sN-8,sN-missing)==(8,2,4,4,2)
# Count distinct H-side C incidences for these two stated positive cells.
hbound={e for e,ls in g.owners_of(list(H)).items() if len(ls)==1}
charges=[]
for c,ts in [((0,-2),B),((2,-2),D)]:
 touched={next(p for p in t if g.label(p)=='C') for t in ts if tuple(sorted(p for p in t if p!=c)) in hbound}
 charges.append({'A':c,'q':len(ts),'d':len(touched),'e':len(ts)-len(touched)})
assert [(x['q'],x['d'],x['e']) for x in charges]==[(2,1,1),(1,0,1)]
out={'status':'ACCEPT_PEER_SUPPLEMENT','scope':'Four hand-classified root/leaf orientations, six named symbolic implications including sigma, one prescribed actual geometry; no discovery.','implications':receipts,'opposite_root_one_path':'PASS','control':{'W':20,'k':6,'Q':Q,'J':J,'sN':sN,'Delta':4,'b':2,'positive_cells':charges,'forward_reverse':'PASS'},'review_source_sha256':hashlib.sha256((ROOT/'fourth-surplus-review/two-unit-independent/review.txt').read_bytes()).hexdigest()}
(HERE/'two-unit-leaf-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: independent in-K leaf supplement, symbolic guards/sigma, W20/k6/Delta4/b2 control and physical replay')
