import json
for l in open('results.jsonl'):
    r=json.loads(l); V=[tuple(v) for v in r['V']]; n=len(V)
    if sum(V[i][0]*V[(i+1)%n][1]-V[(i+1)%n][0]*V[i][1] for i in range(n))<0: V=V[::-1]
    for h in r['hits']:
        c=tuple(h['verified'][0]); idx=[i for i,v in enumerate(V) if v==c]
        for i in idx:
            a,b=V[i-1],V[(i+1)%n]; turn=(c[0]-a[0])*(b[1]-c[1])-(c[1]-a[1])*(b[0]-c[0])
            if turn>0: print(r['W'],r['S'],r['T'],'corner',c,'occurrences',len(idx),'prev',a,'next',b,'w',h['w'],'T-dir',h['verified'][1]); print(V)
