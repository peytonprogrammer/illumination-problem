"""Symbolic local incidence audit. No cap assignments or completed rooms enumerated."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
RAYS=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
CENTERS={'L':(-2,0),'B':(0,-2),'D':(2,-2),'R':(4,0),'E':(4,2),'Tc':(2,4),'N':(0,2)}
def tri(t):return tuple(sorted(t))
def at(a,sectors):return {tri((a,(a[0]+RAYS[i%8][0],a[1]+RAYS[i%8][1]),(a[0]+RAYS[(i+1)%8][0],a[1]+RAYS[(i+1)%8][1]))) for i in sectors}
def fan(k,sectors):return at(CENTERS[k],sectors)
H=set().union(*(at(a,range(8)) for a in [(0,0),(2,0),(2,2)]))
def kind(p):return 'A' if p[0]%2==p[1]%2==0 else 'B' if p[0]%2==p[1]%2==1 else 'C'
def angleunits(tiles,p):return sum((1 if kind(p) in ['A','B'] else 2) for t in tiles if p in t)
def vertices(tiles):return set().union(*(set(t) for t in tiles))
# Seven cyclic windows from m3 or m4, containing forced inward sector0.
# This is a local fan identity, not room/cap-assignment enumeration.
windows={frozenset((a+j)%8 for j in range(m)) for m in [3,4] for a in range(8) if 0 in {(a+j)%8 for j in range(m)}}
Lforms={'lower3':[6,7,0],'upper3':[7,0,1],'outer3':[0,1,2], 'lower4':[5,6,7,0],'rectangle':[6,7,0,1],'fullnorth':[7,0,1,2],'outer4':[0,1,2,3]}
assert windows=={frozenset(v) for v in Lforms.values()}
# Ordinary sectors allowed at each remaining cap slot. Coefficients are
# computed separately per sector; no product of cap choices is formed.
CAP={'B+':('B',1),'B-':('B',2),'E-':('E',4),'T-':('Tc',5),'T+':('Tc',6),
     'Nb-':('N',5),'Nb+':('N',6),'Nr-':('N',7),'Nr+':('N',0),'D+':('D',1),'D-':('D',2),'R+':('R',3),'R-':('R',4)}
def coeff(k,p):
 cell,sector=CAP[k];return angleunits(fan(cell,[sector]),p)
def formula(base,variables,p):return {'fixed_45deg_units':angleunits(base,p),'coefficients':{v:coeff(v,p) for v in variables if coeff(v,p)}}
checks={}
# Exact B-angle formula for lower3+BC; N=Nb- is the unresolved branch.
base=H|fan('L',Lforms['lower3'])|fan('B',[1,2])
variables=['E-','T-','D+','D-','R+','R-','Nb-','Nb+','Nr-','Nr+']
for point,expected in [((-1,1),(3,{'Nb-':1})),((1,3),(2,{'T-':1,'Nr+':1})),((3,-1),(2,{'D+':1,'R-':1}))]:
 row=formula(base,variables,point);assert row=={'fixed_45deg_units':expected[0],'coefficients':expected[1]},(point,row)
 checks['lower_BC_'+str(point)]=row
# lower3+BO already consumes b1 at(-1,-1), ordinaryN6 gives no other B.
base=H|fan('L',Lforms['lower3'])|fan('B',[0,1])
assert angleunits(base,(-1,-1))==4
assert all(coeff(k,(-1,-1))==0 for k in ['E-','T-','D+','D-','R+','R-','Nb+'])
checks['lower_BO_fixed_smooth_B']={'point':[-1,-1],'units':4}
# Upper+EC and rectangle+EC: b=(1-nb)+nr+X, with extra1 for rectangle.
for name in ['upper3','rectangle']:
 base=H|fan('L',Lforms[name])|fan('E',[3,4])
 variables=['B+','T-','D+','D-','R+','R-','Nb-','Nb+','Nr-','Nr+']
 expected=[((-1,1),4,{'Nb-':1}),((1,3),2,{'T-':1,'Nr+':1}),((3,-1),2,{'D+':1,'R-':1})]
 for point,c,terms in expected:
  row=formula(base,variables,point)
  assert row=={'fixed_45deg_units':c,'coefficients':terms},(name,point,row)
  checks[name+'_'+str(point)]=row
 # After forcedB+, lower B angle differs by45deg between the two L forms.
 assert angleunits(base|fan('B',[1]),(-1,-1))==(4 if name=='rectangle' else 3)
 checks[name+'_lower_B']={'point':[-1,-1],'units_after_Bplus':angleunits(base|fan('B',[1]),(-1,-1))}
# Lower4 must consume one outsideC; Bcenter repairs its lower B but N5
# would create a second smooth B at(-1,1).
base=H|fan('L',Lforms['lower4'])
assert angleunits(base,(-2,-1))==4
assert angleunits(base,(-1,-1))==4
assert coeff('B-',(-1,-1))==1 and coeff('B+',(-1,-1))==0
assert angleunits(base|fan('B',[1,2]),(-1,1))==3
assert coeff('Nb-',(-1,1))==1
checks['lower4_repairs']={'outside_C':[-2,-1],'lower_B':[-1,-1],'only_B2_repairs_lower_B':True,'N5_would_add_second_smooth_B':True}
# All outside-C largerL forms: same forced north repair, one consumes
# another lower smoothB iff L7 and Bcenter both present.
for name in ['outer3','fullnorth','outer4']:
 base=H|fan('L',Lforms[name])
 assert angleunits(base,(-2,1))==4
 assert angleunits(base,(-1,1))==4
 assert coeff('Nb-',(-1,1))==1
 assert all(coeff(k,(-1,1))==0 for k in CAP if k!='Nb-')
 assert angleunits(base|fan('B',[1,2]),(-1,-1))==(4 if name=='fullnorth' else 3)
 checks[name+'_outside_repairs']={'outside_C':[-2,1],'smooth_B_needs_N5':[-1,1],'Bcenter_extra_lower_B':name=='fullnorth'}
# Unit N45 also repairs the north B; its other sector is allowed at that B.
assert angleunits(fan('N',[4,5]),(-1,1))==2
# Remote neighboring A needed to heal outerC is not in K or the full core.
assert (-2,2) not in set(CENTERS.values())|{(0,0),(2,0),(2,2)}
assert (-2,-2) not in set(CENTERS.values())|{(0,0),(2,0),(2,2)}
# Per-vertex repair identities for outsideC-table D/R restrictions.
base=H|fan('D',[0,1]);assert angleunits(base,(3,-1))==4
assert coeff('R-',(3,-1))==1
base=H|fan('R',[4,5]);assert angleunits(base,(3,-1))==4
assert coeff('D+',(3,-1))==1
base=H|fan('D',[1,2]);assert angleunits(base,(3,-1))==3
base=H|fan('R',[3,4]);assert angleunits(base,(3,-1))==3
checks['DR_outside_table_repairs']={'D01_needs_R4':True,'R45_needs_D1':True,'D12_forbids_R4_with_b_consumed':True,'R34_forbids_D1_with_b_consumed':True}
# Symbolic h,c,n identity, not an assignment census.
# J=2+h+c, Q=5+n, sN=7-n, k=J+sN=6 => n=3+h+c.
for h,c in [(0,0),(0,1),(1,0),(1,1)]:
 J=2+h+c;n=3+h+c;Q=5+n;sN=7-n
 assert J+sN==6 and Q+sN-8==4 and 32-2*(J+sN)==20
# Expose every vertex's affine coefficient row in the named inward shapes,
# so omitted smooth-angle terms can be checked without cap enumeration.
all_tables={}
for name,Lsectors,partner in [('lower_BC',Lforms['lower3'],('B',[1,2])),('lower_BO',Lforms['lower3'],('B',[0,1])),('upper_EC',Lforms['upper3'],('E',[3,4])),('rectangle_EC',Lforms['rectangle'],('E',[3,4]))]:
 base=H|fan('L',Lsectors)|fan(*partner)
 variables=[v for v,(k,s) in CAP.items() if k not in ['L',partner[0]]]
 universe=vertices(base)|set().union(*(vertices(fan(*CAP[v][:1],[CAP[v][1]])) for v in variables))
 all_tables[name]=[{'point':p,'kind':kind(p),**formula(base,variables,p)} for p in sorted(universe) if kind(p)!='A']
# Exhaustive symbolic B checks after forced ordinary references. This is
# five named local base identities, never a product of cap assignments.
capvars=['D-','D+','R-','R+','Nb-','Nb+','Nr-','Nr+']
captiles=set().union(*(fan(CAP[v][0],[CAP[v][1]]) for v in capvars))
base_specs=[('lower_BC',H|fan('L',Lforms['lower3'])|fan('B',[1,2])|fan('E',[4])|fan('Tc',[5]),{(-1,1),(1,3),(3,-1)}),
 ('lower_BO',H|fan('L',Lforms['lower3'])|fan('B',[0,1])|fan('E',[4])|fan('Tc',[5]),{(-1,-1),(-1,1),(1,3),(3,-1)}),
 ('lower4_BC',H|fan('L',Lforms['lower4'])|fan('B',[1,2])|fan('E',[4])|fan('Tc',[5]),{(-1,1),(1,3),(3,-1)}),
 ('upper_EC',H|fan('L',Lforms['upper3'])|fan('E',[3,4])|fan('B',[1])|fan('Tc',[5]),{(-1,1),(1,3),(3,-1)}),
 ('rectangle_EC',H|fan('L',Lforms['rectangle'])|fan('E',[3,4])|fan('B',[1])|fan('Tc',[5]),{(-1,-1),(-1,1),(1,3),(3,-1)})]
for label,base,tracked in base_specs:
 for point in vertices(base|captiles):
  if kind(point)!='B':continue
  fixed=angleunits(base,point);increase=sum(coeff(v,point) for v in capvars)
  if point not in tracked:
   assert fixed>=5 or fixed+increase<4,(label,point,fixed,increase)
 checks[label+'_no_omitted_smooth_B']={'tracked_points':sorted(tracked),'all_other_B_fixed_above180_or_max_below180':True}

inputs=[ROOT/'surplus-four-local/e2-e1-b1/critical-L.txt',ROOT/'surplus-four-local/e2-e1-b1/argument.txt',Path(__file__)]
out={'status':'SYMBOLIC_PER_VERTEX_CHECKS_PASS','checks':checks,'all_named_inward_vertex_coefficients':all_tables,
 'seven_L_windows':Lforms,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
 'limits':'Local incidence/coefficient checks only; no completed-room construction, cap-assignment enumeration, geometry validity census, optical guard replay, ray/direction/word search, archive, solver or worker. Hand review supplies exclusivity and budget deductions.'}
(HERE/'check.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: seven local fan windows, named B/C repair equations and symbolic cap budget; full affine vertex tables recorded without cap-assignment enumeration.')
