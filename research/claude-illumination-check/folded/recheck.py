import sys
from exact import run1, run
out=[]
for line in open('lit-rel.txt'):
    h,v=line.split('|');_,a,b,d=h.split()
    V=[tuple(map(int,s.split(','))) for s in v.split()]
    a,b,d=[tuple(map(int,x.split(','))) for x in (a,b,d)]
    if run1(V,a,b,d):continue
    d2,_=run(V,a,b,R=10)
    print('pair',a,b,'exact-R10',d2,'|',v.strip(),flush=True)
