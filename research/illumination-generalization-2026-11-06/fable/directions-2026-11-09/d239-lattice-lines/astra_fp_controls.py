"""Three named controls; construct branch moves as products of edge involutions."""
from pathlib import Path
import json,csv
from itertools import combinations,product
D=Path(__file__).resolve().parent
def check(cells):
    n=len(cells)
    parity=list(product(range(2),repeat=2))
    edge=[[c[2+(0 if (c[0]&1)!=p else 2)] for c in cells] for p in range(2)]
    edge += [[c[2+(1 if (c[1]&1)!=p else 3)] for c in cells] for p in range(2)]
    edge=[[i if j<0 else j for i,j in enumerate(t)] for t in edge]
    gens={}
    for x,y in parity:
        a,b=edge[x],edge[2+y]
        if x!=y:a,b=b,a
        gens[x,y]=[b[a[i]] for i in range(n)]
    marks={}
    for i,(x,y,e,north,w,south) in enumerate(cells):
        if w>=0 and south>=0 and cells[w][5]>=0 and cells[w][5]==cells[south][4]:
            marks[x,y]=[i,w,south,cells[w][5]]
    def closure(pairs):
        cls=list(range(n))
        while True:
            changed=False
            for i,j in pairs:
                if cls[i]!=cls[j]:
                    old,new=cls[j],cls[i];cls=[new if v==old else v for v in cls];changed=True
            if not changed:return cls
            pairs=[(g[i],g[j]) for i,j in combinations(range(n),2) if cls[i]==cls[j] for g in gens.values()]
    size=min((s for i in range(1,n) if (s:=len(set(closure([(0,i)]))))>1),default=n)
    print('area',n,'minimum nontrivial block count or n',size,'marks',len(marks))
    for S,T in combinations(marks,2):
        a=tuple(v%2 for v in S)
        if a!=tuple(v%2 for v in T):continue
        cls=closure([(i,j) for p,g in gens.items() if p!=a for i,j in enumerate(g) if i<j and g[j]==i])
        img=lambda M:sorted({cls[i] for i in marks[M]})
        print(S,T,'canonical blocks',len(set(cls)),img(S),img(T),'FP',not(set(img(S))&set(img(T))))
with (D.parent/'d237-dark-examples-w22-26/astra/dark.tsv').open() as f:
    check(json.loads(next(csv.DictReader(f,delimiter='\t'))['complex']))
for line in (D/'folds-d237.tsv').read_text().splitlines()[:2]:
    s=line.split();nums=list(map(int,s[4:]));check([nums[i:i+6] for i in range(0,len(nums),6)])
