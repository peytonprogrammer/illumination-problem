import pickle, math
L, role, XY = pickle.load(open('/tmp/n6leaves.pkl','rb'))
res = []
for used in L:
    cnt = {}
    for t in used:
        for i in range(3):
            e = tuple(sorted((t[i], t[(i+1)%3]))); cnt[e] = cnt.get(e,0)+1
    bd = [e for e,c in cnt.items() if c==1]
    adj = {}
    for a,b in bd: adj.setdefault(a,[]).append(b); adj.setdefault(b,[]).append(a)
    simple = all(len(v)==2 for v in adj.values())
    # one cycle?
    start = bd[0][0]; prev=None; cur=start; cyc=[]
    while True:
        cyc.append(cur); nx=[q for q in adj[cur] if q!=prev]
        if not nx: break
        prev,cur=cur,nx[0]
        if cur==start: break
    one = simple and len(cyc)==len(adj)
    corners=[]; smoothA=[]
    n=len(cyc)
    for i,p in enumerate(cyc):
        a,b=XY[cyc[i-1]],XY[cyc[(i+1)%n]]; q=XY[p]
        cr=(q[0]-a[0])*(b[1]-q[1])-(q[1]-a[1])*(b[0]-q[0])
        if abs(cr)>1e-9: corners.append(p)
        elif role[p]=='A': smoothA.append(p)
    res.append((len(corners), one, len(used), smoothA))
from collections import Counter
print('simple single-cycle:', sum(r[1] for r in res), 'of', len(res))
print('walls of simple ones:', sorted(Counter(r[0] for r in res if r[1]).items()))
print('simple with >=1 smooth boundary A (second mark):', sorted(Counter(r[0] for r in res if r[1] and r[3]).items()))
