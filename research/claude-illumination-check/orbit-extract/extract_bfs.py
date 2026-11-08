"""BFS orbit extraction with my own derivation of the coordinate change, replayed by my tracer.
New surface after T=(R,U R^-1): new up = old (-1,1), new right = old (1,0)  -> B *= [[1,-1],[0,1]].
After L=(R U^-1,U): new right = old (1,-1), new up = old (0,1)          -> B *= [[1,0],[-1,1]].
Developed direction = B e1; physical = frame^T (frame is orthogonal). Controls: frame un-transposed, B row."""
import sys,glob,json,random,importlib.util,math
from collections import deque,Counter
sys.path.insert(0,'../folded'); from exact import run
K='../../illumination-k4-codex/k5-proof-pilot/'
spec=importlib.util.spec_from_file_location('of',K+'inputs/origami_frame.py'); o=importlib.util.module_from_spec(spec); spec.loader.exec_module(o)
def mul(A,B): return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def extract(V,S,T,limit=300000):
    r,u,lab,s0,frame=o.build(list(V),S,T); st=o.canon(r,u,lab,s0); seen={st}; Q=deque([(st,((1,0),(0,1)))])
    while Q:
        (R,U,lab),B=Q.popleft(); s=R[0]
        while s!=0:
            if lab[s]=='block': break
            if lab[s]=='T': return B,frame
            s=R[s]
        Ri,Ui=o.inv(R),o.inv(U)
        for a,b,M in ((R,tuple(o.comp(U,Ri)),((1,-1),(0,1))),(tuple(o.comp(R,Ui)),U,((1,0),(-1,1)))):
            n=o.canon(a,b,lab,0)
            if n not in seen: seen.add(n); Q.append((n,mul(B,M)))
        if len(seen)>limit: return None
    return 'DARK'
def ap(M,v): return (M[0][0]*v[0]+M[0][1]*v[1],M[1][0]*v[0]+M[1][1]*v[1])
fs=sorted(glob.glob('../../illumination-k4-codex/k5-proof-continuation/cases/*/generations/*/vertices.json'))
random.seed(int(sys.argv[1])); fs=random.sample(fs,int(sys.argv[2]))+sorted(glob.glob(K+'cases/*/vertices.json'))
C=Counter(); mx=0
for f in fs:
    j=json.load(open(f)); V=[tuple(p) for p in j['vertices']]; S,T=map(tuple,j['marked'])
    x=extract(V,S,T)
    if not isinstance(x,tuple): C[str(x)]+=1; continue
    B,fr=x; dev=(B[0][0],B[1][0]); d=ap(tuple(zip(*fr)),dev); mx=max(mx,abs(d[0]),abs(d[1]))
    C['formula '+('lit' if run(V,S,T,B=5000,dirs=[d])[0] else 'FAIL')]+=1
    for name,alt in (('ctl-frame',ap(fr,dev)),('ctl-row',ap(tuple(zip(*fr)),(B[0][0],B[0][1])))):
        if alt!=d and math.gcd(*alt)==1: C[name+' '+('lit' if run(V,S,T,B=5000,dirs=[alt])[0] else 'fail')]+=1
print(len(fs),'rooms; max |dir| =',mx,dict(C))
