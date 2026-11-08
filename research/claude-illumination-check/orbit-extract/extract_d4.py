import sys,random,glob,json,math
from collections import Counter
exec(open('extract_bfs.py').read().split('fs=sorted')[0])
G=[lambda x,y:(x,y),lambda x,y:(-y,x),lambda x,y:(-x,-y),lambda x,y:(y,-x),lambda x,y:(x,-y),lambda x,y:(-x,y),lambda x,y:(y,x),lambda x,y:(-y,-x)]
fs=sorted(glob.glob('../../illumination-k4-codex/k5-proof-continuation/cases/*/generations/*/vertices.json'))
random.seed(3); fs=random.sample(fs,100); C=Counter(); F=Counter()
for f in fs:
    j=json.load(open(f))
    for g in G:
        V=[g(*p) for p in j['vertices']]; S,T=[g(*p) for p in j['marked']]
        x=extract(V,S,T)
        if not isinstance(x,tuple): C[str(x)]+=1; continue
        B,fr=x; F[str(fr)]+=1; dev=(B[0][0],B[1][0]); d=ap(tuple(zip(*fr)),dev)
        C['formula '+('lit' if run(V,S,T,B=5000,dirs=[d])[0] else 'FAIL')]+=1
        alt=ap(fr,dev)
        if alt!=d: C['ctl-frame '+('lit' if run(V,S,T,B=5000,dirs=[alt])[0] else 'fail')]+=1
print(dict(C)); print('frames',dict(F))
