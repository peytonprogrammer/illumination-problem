import sys, time
sys.path.insert(0,'.')
from origami_dark import build, canon, inv, comp
V=[(0,0),(1,1),(2,1),(2,0),(3,1),(4,1),(4,0),(5,1),(5,2),(6,2),(5,3),(4,3),(4,4),(3,3),(3,2),(1,2),(1,3),(0,4),(0,3),(-1,3),(-1,2),(-2,2),(-1,1),(0,1)]
S,T=(0,2),(4,2)
r,u,lab,s0=build(V,S,T)
from collections import Counter
print('squares',len(r),Counter(lab))
def orbit(lab,limit):
    st=canon(r,u,lab,s0); seen={st}; todo=[st]
    while todo:
        R,U,L=todo.pop()
        Ri,Ui=inv(R),inv(U)
        for a,b in ((R,tuple(comp(U,Ri))),(tuple(comp(R,Ui)),U)):
            n=canon(a,b,L,0)
            if n not in seen:
                seen.add(n); todo.append(n)
                if len(seen)>limit: return '>%d'%limit
    return len(seen)
mode=sys.argv[1]; limit=int(sys.argv[2])
if mode=='nolab': L=['.']*len(r)
elif mode=='noS': L=[x if x!='S' else '.' for x in lab]
elif mode=='block': L=[x if x=='block' else '.' for x in lab]
else: L=lab
t=time.time(); print(mode, orbit(L,limit), round(time.time()-t,1),'s')
