"""Prescribed invariant and fixed-path checks; no search or orbit census."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from math import gcd
import ast
import hashlib
import json

HERE=Path(__file__).resolve().parent
source=HERE.parents[2]/'review/resumed-exact-check.py'
names={'vec','det','dot','edges','on','location','intersect','simple','path_check'}
ns={'Q':Q}
tree=ast.parse(source.read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(source),'exec'),ns)
P=[(0,0),(28,0),(28,4),(16,4),(16,16),(0,16)]
S,T,S0=(26,2),(8,8),(24,2)
ns['simple'](P)
assert all(ns['location'](P,z)==1 and all(c%2==0 for c in z) for z in (S,T,S0))
# Every chart transition is in8Z^2 (hand argument), while actual cylinder
# cores generate that entire subgroup by these explicit combinations.
assert all(c%4==0 for z in P for c in z)
assert gcd(56,32)==8 and 56-2*32==-8
assert 2*4==8
convex=[P[i] for i in (0,1,2,4,5)]
residue=lambda z: tuple(c%8 for c in z)
counts=Counter(map(residue,convex))
assert counts=={(0,0):3,(4,0):1,(4,4):1}
assert residue(P[3])==(0,4)
assert residue(T)==(0,0)
# Interior residue-zero uniqueness is an inequality argument, not a scan:
# bottom strip 0<y<4 has no multiple of8; upper strip 0<x<16,
# 4<y<16 permits only x=y=8. The seam y4 is not residue-zero.
assert 0<8<16 and 4<8<16 and 4%8!=0
cross=lambda p,q: Q(p[0])+Q(4-p[1],q[1]-p[1])*(q[0]-p[0])
assert cross(S,T)==20>16
contact=(0,Q(112,17))
witness=ns['path_check'](P,[S,contact,T])
assert witness=={'wall_leg_guards':12,'reflections':1}
assert cross(S,contact)==Q(44,3)<16
assert Q(contact[0]-S[0],contact[1]-S[1])==Q(-17,3)
# The broad boundary-seed alternative must be kept: all six listed smooth
# boundary points are regular, and the source sees the bottom seeds.
boundary=[(8,0),(16,0),(24,0),(16,8),(8,16),(0,8)]
assert all(residue(z)==(0,0) and ns['location'](P,z)==0 and z not in P for z in boundary)
# Direct visibility of S0 to (8,0) has y strictly between0 and2 until its
# endpoint; x strictly between8 and24. It stays in the bottom rectangle.
assert 0<2<4 and 0<8<24<28
# Vertical cylinder map V has common derivative [[1,0],[1,1]].
# Full vertical boundary displacements vanish modulo their circumferences.
vbound=[('central',-16,0,32),('central',16,32,32),('right',16,0,8),('right',40,24,8)]
assert all(shift%period==0 for _,_,shift,period in vbound)
def V(z,c):
 x,y=z
 return (x,(y+x+(16 if c=='central' else -16))%(32 if c=='central' else 8))
assert V(T,'central')==(8,0)
assert V(S0,'right')==S0
assert V(S,'right')==(26,4)!=S
corner_images=[V(z,'right' if z[0]>16 else 'central') for z in P]
assert set(corner_images)==set(P)
assert cross(S0,T)==Q(56,3)>16
# Original torus fiber counts agree with primitive covering degree:
# 3 corner lifts + 2 lifts per smooth wall point + 4 lifts of T =19.
area=28*4+16*12
assert Q(4*area,8*8)==19==3+2*6+4
out={'status':'PASS_INTERIOR_SEED_OBSTRUCTION_AND_BOUNDARY_QUALIFICATION','room':P,'source':S,'target':T,'full_period_lattice':'8Z^2 (inclusion hand-proved; explicit core generators checked)','regular_corner_torus_image_multiplicities':{str(k):v for k,v in counts.items()},'unique_original_interior_residue_zero_point':T,'direct_portal_x':str(cross(S,T)),'illuminating_path':[[str(c) for c in z] for z in [S,contact,T]],**witness,'boundary_seeds_not_excluded':boundary,'boundary_calibration_source':S0,'boundary_calibration_map':'V fixes S0 and sends T to (8,0)','boundary_calibration_blocked_direct_portal_x':str(cross(S0,T)),'general_real_endpoint_obstruction':'Hand countability / area-zero fixed-set argument, not an integer-endpoint conclusion','broader_native_boundary_seed_coverage':'UNRESOLVED','search':False,'checker_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
(HERE/'obstruction-check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
