"""Fixed-room check of the cylinder-adjacency form (findings Section 7.6). In the base frame (strip direction
w = e1, v = e2), the seed in direction w' = (m, 1) is predicted to end at labels u r^m u r^m (s) and
u r^(m+1) u r^(m-1) (s). Ground truth: transform the origami so that (m, 1) maps to e1, then read r^2 and
r u r u^-1 at the base square. No discovery scan: fixed rooms, |m| <= 12. Run: python3 -B cylinder.py"""
import sys,json
sys.argv=['x']
import types  # the room encoder imports pysat at load time; this check never calls a solver
class _Stub(types.ModuleType):
    __path__=[]
    def __getattr__(self,k): return object
for n in ('pysat','pysat.formula','pysat.solvers','pysat.card','pysat.pb'): sys.modules[n]=_Stub(n)
__file__='<SOURCE_WORKSPACE>/.context/claude-illumination-check/seed-unbounded/seedcheck.py'
exec(open(__file__).read().split("if __name__")[0])
src=open(E+'origami_frame.py').read()
src=src.replace("lab[s]='block' if v in corners else ('T' if v==T else ('S' if v==S else '.'))",
                "lab[s]='block' if v in corners else (v if cls(v)==0 else 'bc')")
g2={}; exec(src,g2); build2=g2['build']
def pw(P,k,x):
    Pi=o.inv(P)
    for _ in range(abs(k)): x=P[x] if k>0 else Pi[x]
    return x
def check(V,S,ms):
    r,u,lab,s0,_=build2(list(V),S,S); r,u,lab=o.canon(r,u,lab,s0); r,u=list(r),list(u); bad=0
    for m in ms:
        R,U=r,u
        for _ in range(abs(m-1)): U=o.comp(U,R) if m-1>0 else o.comp(U,o.inv(R))   # N1^(-(m-1)): first column stays e1
        R=o.comp(R,U)                                                                # N2^(-1): M e1 = (m, 1)
        Ui=o.inv(U); truth={lab[R[R[0]]],lab[R[U[R[Ui[0]]]]]}
        pred={lab[u[pw(r,m,u[pw(r,m,0)])]],lab[u[pw(r,m+1,u[pw(r,m-1,0)])]]}
        bad+=truth!=pred
    return bad
rooms=[json.loads(l) for l in open('study.jsonl')][11:12]+[json.loads(l) for l in open('res_rooms.jsonl')][:4]
ms=[m for m in range(-12,13)]
for r in rooms:
    V=[tuple(v) for v in r['V']]
    print(len(V),r['S'],r['T'],'m in [-12,12]: mismatches',check(V,tuple(r['S']),ms))
