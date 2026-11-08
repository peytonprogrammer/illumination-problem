"""Two fixed hand transport compositions, not a ray/word/direction search."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
# Affine height states a+b*d on the prescribed vertical portal.
def move(state,steps):return state[0],state[1]+steps
def normal(state):return move(state,2)
def four(state):return -state[0],2-state[1]
def Nfour(state):return 4-state[0],-2-state[1]
def at(state,d):return state[0]+state[1]*d
def target_root(state):return F(2-state[0],state[1])
# A: S v(1,d), R far x4 then back to x3 at5d, N entry x1 at7d.
R_A=(0,5);N_A=move(R_A,2);N_A_out=normal(N_A)
A=move(N_A_out,1);assert N_A==(0,7) and N_A_out==(0,9) and A==(0,10)
a=target_root(A);assert a==F(1,5)
gateA=(F(1,7),F(1,5));assert a==gateA[1]
assert at(R_A,a)==1
# B: R far then roof gives return x3 at2-5d, heading(-1,-d).
R_B=(2,-5);L_entry=move(R_B,-4);assert L_entry==(2,-9)
L_out=four(L_entry);assert L_out==(-2,11)
E_entry=move(L_out,4);E_out=normal(E_entry)
N_entry=move(E_out,2);N_out=Nfour(N_entry)
B=move(N_out,-1)
assert E_entry==(-2,15) and E_out==(-2,17) and N_entry==(-2,19)
assert N_out==(6,-21) and B==(6,-22)
b=target_root(B);assert b==F(2,11)
gateB=(F(1,5),F(4,19));assert b<gateB[0]
# All combined bounds follow from affine finite-contact inequalities.
# B N7 ceiling-first x=20-4/d; 0<x<1 iff1/5<d<4/19.
# L ceiling-first four's first floor x=8-2/d lies(-2,-1)
# iff1/5<d<2/9, containing the chosen combined interval.
assert gateB[1]<F(2,9)<F(1,4)
# N7 final output lies inside base and below actual T throughout gateB.
assert 1<=at(N_out,gateB[1])<at(N_out,gateB[0])<2
assert at(E_entry,gateB[0])==1 and at(E_out,gateB[1])<2
assert at(L_entry,gateB[1])>0 and at(L_out,gateB[1])<1
sources=[HERE/'joined-top-absent.txt',HERE/'R23-N7-algebra.json']
old=json.loads(sources[1].read_text());assert old['corner_local_degrees']=={'H':180,'R23':90,'E4':45}
out={'status':'TWO_EARLY_R23_HAND_ROUTES_RETIRED','A':{'prefix':'S->R23 far->N7 normal3->xT2','endpoint_height':'10d','target_root':str(a),'strict_gate':list(map(str,gateA)),'decisive_event':'R23 return portal (3,1), genuine315 corner'},'B':{'prefix':'S->R23 far+top->L0 four->E4 normal3->N7 ceiling-first four->xT2','endpoint_height':'6-22d','target_root':str(b),'strict_gate':list(map(str,gateB)),'decisive_event':'formal target root below1/5; prescribed first R top contact absent there'},'source_sha256':{str(p.relative_to(HERE.parent.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'limits':'Two analytically prescribed maps only. Gate arithmetic and inherited local corner-angle receipt, not optical replay/full U-Z. No room, cap-assignment product, direction sample, reflection-word enumeration, archive, worker or extended loop. No family darkness/illumination closure.'}
(HERE/'R23-early-square-algebra.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS hand identities: Rfar/N3 root1/5 is genuine315 portal corner; Rfar/top-L4-E3-N4 root2/11 below strict1/5 gate. No new closure.')
