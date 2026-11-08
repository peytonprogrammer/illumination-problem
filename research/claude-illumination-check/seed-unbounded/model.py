"""Random-model prediction of the full-orbit seed fraction for each study room (no search; counts only)."""
import sys,json
ARGS=sys.argv[1:]; sys.argv=['x']
__file__='<SOURCE_WORKSPACE>/.context/claude-illumination-check/seed-unbounded/seedcheck.py'
exec(open(__file__).read().split("if __name__")[0])
def angle8(V,p):
    """Interior angle at lattice point p in units of 45 degrees, by counting room triangles at p."""
    r,u,lab,s0,fr=None,None,None,None,None
rows=[json.loads(l) for l in open('study.jsonl')]
for i,rw in enumerate(rows):
    V=[tuple(v) for v in rw['V']]; R,U,lab,s0,fr=o.build(V,tuple(rw['S']),tuple(rw['T']))
    N=len(R); A=sum(1 for x in lab if x in '.ST'); nT=lab.count('T')
    # cone mass among B/C: squares whose lower-left is a B/C corner lift with cone angle >2pi.
    # A lift's cone multiplicity k = length of the cycle of the corner permutation c = r u r^-1 u^-1 through its square.
    Ri,Ui=o.inv(R),o.inv(U); comm=[R[U[Ri[Ui[x]]]] for x in range(N)]
    seen=set(); cone=bc=0
    for x in range(N):
        if x in seen: continue
        cyc=[x]; y=comm[x]
        while y!=x: cyc.append(y); y=comm[y]
        seen.update(cyc)
        if lab[x]=='block':
            # B/C vs A corner: A corners also 'block'; skip cycles that contain no B/C class; approximate by excluding cycles whose square sits at an even-even developed point is unavailable here
            bc+=len(cyc); cone+=len(cyc) if len(cyc)>1 else 0
    pc=cone/bc; pred=pc*(1-(1-nT/A)**2)
    print(json.dumps(dict(i=i,W=rw['W'],T=rw['T'],N=N,Asq=A,Tsq=nT,cone_frac=round(pc,3),pred=round(pred,3))))
