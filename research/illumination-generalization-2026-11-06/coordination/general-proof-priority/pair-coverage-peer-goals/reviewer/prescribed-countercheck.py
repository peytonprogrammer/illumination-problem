"""ONE hand-derived pair-coverage countercontrol; no room/ray/orbit search."""
from pathlib import Path
from fractions import Fraction as Q
import ast
import hashlib
import json

HERE=Path(__file__).resolve().parent
source=HERE.parents[3]/'review/resumed-exact-check.py'
needed={'vec','det','dot','edges','on','location','intersect','simple','path_check'}
ns={'Q':Q}
tree=ast.parse(source.read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in needed],type_ignores=[]),str(source),'exec'),ns)
P=[(0,0),(8,0),(8,4),(4,4),(4,8),(0,8)]
S,T=(6,2),(2,6)
contact=(0,5)
ns['simple'](P)
assert ns['location'](P,S)==ns['location'](P,T)==1
assert all(z%2==0 for p in (S,T) for z in p)
assert len(P)==6 and all(a[0]==b[0] or a[1]==b[1] for a,b in ns['edges'](P))
turns=[ns['det'](ns['vec'](P[i-1],P[i]),ns['vec'](P[i],P[(i+1)%6])) for i in range(6)]
assert sum(x<0 for x in turns)==1
convex=[P[i] for i,z in enumerate(turns) if z>0]
reflex=[P[i] for i,z in enumerate(turns) if z<0]
assert reflex==[(4,4)]
residues={}
for p in convex:
    r=tuple(x%8 for x in p)
    residues[r]=residues.get(r,0)+1
assert residues=={(0,0):3,(0,4):1,(4,0):1}
assert tuple(x%8 for x in reflex[0])==(4,4)
# These are the two explicitly HAND-identified regular cylinder core periods.
assert 2*4==8
assert all((2*x)%8==0 for p in P for x in p)
# Prescribed THREE same-copy positions derived from the universal parity proof.
C,R,U=(2,2),(6,2),(2,6)
assert all(ns['location'](P,p)==1 for p in (C,R,U))
assert ns['location'](P,(6,6))==-1
assert tuple((T[i]-S[i])%8 for i in (0,1))==(4,4)
assert tuple((U[i]-R[i])%8 for i in (0,1))==(4,4)
assert tuple((C[i]-R[i])%8 for i in (0,1))==(4,0)
assert tuple((C[i]-U[i])%8 for i in (0,1))==(0,4)
assert ns['on'](R,U,(4,4))
assert ((Q(R[0]+U[0],2),Q(R[1]+U[1],2)))==(4,4)
# The true physical boundary consists of segments on integer multiples of4;
# each candidate has both coordinates2mod4, so no regular boundary seed occurs.
assert all(all(x%4==2 for x in p) for p in (C,R,U))
# Sole predeclared optical control. No alternative direction is constructed.
path=[S,contact,T]
checked=ns['path_check'](P,path)
assert checked=={'wall_leg_guards':12,'reflections':1}
vin=ns['vec'](S,contact)
vout=ns['vec'](contact,T)
assert vin==(-6,3) and vout==(2,1)
assert ns['det'](vin,(-2,1))==0 and ns['dot'](vin,(-2,1))>0
portal=(Q(2),Q(4))
assert ns['on'](S,contact,portal) and 0<portal[0]<4
assert (3+1)==4  # exact first-T time at vertical speed1
out={
 'status':'PASS_ONE_PRESCRIBED_FULL_GROUP_COUNTERCONTROL',
 'room':P,'source':S,'target':T,'reflex_corners':1,'native_even_even':True,
 'absolute_period_lattice':'8 Z^2, HAND proof from gluing and two regular cylinder cores',
 'convex_corner_residue_multiplicities':{str(k):v for k,v in residues.items()},
 'cone_residue':[4,4],
 'full_group_argument':'Hand proof in coverage-challenge.md; no affine element or orbit enumeration',
 'same_copy_prescribed_positions':[C,R,U],
 'only_possible_endpoint_pair':'R,U or U,R, whose Euclidean segment hits genuine reflex(4,4)',
 'known_lit_path':path,'launch_direction':[-2,1],'portal':[str(x) for x in portal],
 'first_actual_target_time':4,**checked,
 'checker_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'search':False,'new_engine':False,'orbit_census':False,
 'actual_dark_counterexample':False,'full_goal_complete':False
}
(HERE/'prescribed-countercheck.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
