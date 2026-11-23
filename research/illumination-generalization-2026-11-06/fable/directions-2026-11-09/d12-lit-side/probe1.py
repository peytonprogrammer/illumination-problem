import sys, json
from collections import Counter, deque
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'd6-hurwitz-census'))
from hurwitz import *
LABELS=('a','b','c','d')
def full_orbit(t):
    """marked orbit with ALL a-points labelled (cycle ids of base g_a)."""
    n=len(t[0]); cid,plen=initial_pt(t[0]); pt=tuple(cid)
    roots=lambda p:[i for i in range(n) if p[i]==0]
    seen={canon_marked(t,pt,roots(pt))}; q=deque([(t,pt)]); out=[]
    while q:
        t_,pt_=q.popleft(); out.append((t_,pt_))
        for (i,s) in PURE_GENS:
            t2,_,pt2=pure_move(t_,LABELS,pt_,i,s)
            c=canon_marked(t2,pt2,roots(pt2))
            if c not in seen: seen.add(c); q.append((t2,pt2))
    return out,cid,plen
if __name__=='__main__':
    t=tuple(tuple(g) for g in json.loads(sys.argv[1])); x=int(sys.argv[2])
    out,cid,plen=full_orbit(t)
    print('a-points (id: len):',{c:plen[c] for c in set(cid)}, 'states',len(out))
    C=Counter()
    for t_,pt_ in out:
        for i,j in enumerate(t_[x]):
            if i<j and t_[x][j]==i:
                C[tuple(sorted((pt_[i],pt_[j])))]+=1
    print('pairs of a-points joined by a 2-cycle of g_x over the orbit:',dict(C))
