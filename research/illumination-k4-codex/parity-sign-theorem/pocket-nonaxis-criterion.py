"""Fixed exact linear-algebra controls, not geometric or optical discovery."""
from fractions import Fraction as F
from pathlib import Path
import json

BASE = Path(__file__).resolve().parent

def mat(rows):
    return [[F(x) for x in row] for row in rows]

def transpose(a):
    return list(map(list, zip(*a)))

def mul(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]

def sub(a, b):
    return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]

def rref(a):
    a = [r[:] for r in a]
    pivots = []
    for j in range(len(a[0])):
        i = next((i for i in range(len(pivots),len(a)) if a[i][j]), None)
        if i is None:
            continue
        k = len(pivots)
        a[k], a[i] = a[i], a[k]
        d = a[k][j]
        a[k] = [v/d for v in a[k]]
        for i in range(len(a)):
            if i != k:
                d = a[i][j]
                a[i] = [x-d*y for x,y in zip(a[i],a[k])]
        pivots.append(j)
    return a, pivots

def rank(a):
    return len(rref(a)[1])

def kernel(a):
    b, pivots = rref(a)
    vectors = []
    for j in range(len(a[0])):
        if j in pivots:
            continue
        v = [F(0)] * len(a[0])
        v[j] = F(1)
        for i,k in enumerate(pivots):
            v[k] = -b[i][j]
        vectors.append(v)
    return transpose(vectors)

def zero(a):
    return all(x == 0 for row in a for x in row)

def serial(a):
    return [[str(x) for x in row] for row in a]

# Ordered homology basis a1,a2,b1,b2; all cores point in +x.
L = mat([[2,3,0,0],[0,0,1,1]])
N = mat([[0,0,3,0],[0,0,0,2],[0,0,0,0],[0,0,0,0]])
AminusI = mat([[0,6],[0,0]])
C = mat([[1,0],[0,1],[0,0],[0,0]])
K = kernel(L)
NK = mul(N,K)
assert zero(mul(N,N))
assert mul(L,N) == mul(AminusI,L)
assert rank(N) == rank(C) == 2
assert rank(NK) == rank(C)-rank(mul(L,C)) == 1
assert zero(mul(L,NK))
assert zero(mul(N,C))
Q = mat([[0,0,0,0],[2,0,0,0]])
Qequal = mat([[2,3,0,0],[4,6,0,0]])
x = mat([[0],[0],[1],[-1]])
assert zero(mul(L,x))
assert mul(N,x) == mat([[3],[-2],[0],[0]])
assert mul(Q,mul(N,x)) == mat([[0],[6]])
assert zero(mul(Qequal,NK))

# Same homology operator with two refined, homologous pieces of the first core.
T = mat([[1,1,0],[0,0,1],[0,0,0],[0,0,0]])
M = mat([[1,0,0],[0,2,0],[0,0,2]])
J = mat([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]])
assert mul(mul(mul(T,M),transpose(T)),J) == N
assert rank(mul(mul(T,M),transpose(T))) == rank(T)

# One maximal cylinder split at marked levels: both cores represent a.
Tsingle = mat([[1,1],[0,0]])
Msingle = mat([[1,0],[0,1]])
Js = mat([[0,1],[-1,0]])
Ns = mul(mul(mul(Tsingle,Msingle),transpose(Tsingle)),Js)
Ls = mat([[1,0],[0,1]])
assert rank(Ns) == 1
assert rank(Tsingle)-rank(mul(Ls,Tsingle)) == 0
# Relative arc from y=0 to y=1/2 under shear2 has displacement1.
arc_increment = F(2)*F(1,2)
assert arc_increment == 1 and arc_increment % 2 != 0
assert F(2)*F(1,2)/F(1) == 1  # Each refined strip twist is1.

# Distinct one-core-span directions fix a nontrivial zero-holonomy block.
Lblock=mat([[1,0,0,0],[0,1,0,0]])
Kblock=kernel(Lblock)
Hmap=mat([[1,2,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
Vmap=mat([[1,0,0,0],[-3,1,0,0],[0,0,1,0],[0,0,0,1]])
assert mul(Hmap,Kblock)==mul(Vmap,Kblock)==Kblock
assert mul(mul(Hmap,Vmap),Kblock)==Kblock

# Same-sign coefficients are essential to rank(im N)=dim C.
Tmixed = mat([[1,1],[0,0]])
Mmixed = mat([[1,0],[0,-1]])
assert zero(mul(mul(Tmixed,Mmixed),transpose(Tmixed))) and rank(Tmixed)==1

# Previously proved period data: z=C-A-2B is a detected absolute kernel class.
periodA=mat([[-2],[0]]);periodB=mat([[0],[-2]]);periodC=mat([[-2],[-4]])
assert zero(sub(sub(periodC,periodA),mul(mat([[2,0],[0,2]]),periodB)))

out = {
    'status':'PRESCRIBED_NONAXIS_LINEAR_ALGEBRA_PASS',
    'core_kernel_identity':'N(ker hol in absolute H)=span(cores) intersect ker hol',
    'criterion':'Q N nonzero on absolute ker hol iff normalized core defects differ',
    'controls':{
        'two_independent_cores':{'hol':serial(L),'N':serial(N),'kernel_basis':serial(K),'increment_image':serial(NK),'detected_increment':['0','6']},
        'equal_normalized_flux_is_blind':True,
        'dependent_refined_core_rank':True,
        'one_maximal_cylinder_has_zero_core_hol_kernel':True,
        'marked_arc_requires_refinement':{'unrefined_twist':2,'actual_increment':1,'refined_twists':[1,1]},
        'mixed_sign_rank_countercontrol':True,
        'different_one_core_span_twists_fix_zero_holonomy_block':True,
        'inherited_detected_kernel_cycle':{'class':'C-A-2B','base_holonomy':[0,0],'slide_defect':[0,2]},
    },
    'scope':'Fixed exact rational matrices and one prescribed marked torus arc. No new mirror rooms, rays, directions, event words, cylinders, or surface orbits were generated. Abstract detected cycles are not actual endpoint events.',
    'independent_review':'TOOLS_DISABLED_OPUS_ACCEPTED_EXIT0_WITH_PAIRING_REFINEMENT_AND_CUSP_CORRECTIONS; no independent code execution claimed',
    'goal_complete':False,
    'discovery_runs':0,
}
(BASE/'pocket-nonaxis-criterion.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'controls':list(out['controls']),'goal_complete':False,'discovery_runs':0},indent=2))
