"""Find a finite four-sheet mechanism obstruction via a rational failure rectangle."""
from pathlib import Path
from fractions import Fraction as F
from math import gcd
import json,time
B=Path(__file__).parent;E=json.loads((B/'rational-rectangle-effort.json').read_text())
def guard():
    if time.time()>=E['deadline']:raise TimeoutError('original840s effort deadline')
def works(A,C,q):
    Q=4*q
    for u in (0,2):
      for sign in (1,-1):
       for M in range(q):
        x=((q-A)*2+A*sign+4*A*(u+4*M))%(4*Q)
        y=((q-C)*2+C*sign+4*C*(u+4*M))%(4*Q)
        c=1 if Q<x<2*Q else 3 if 2*Q<x<3*Q else None
        if c is None:continue
        lo,hi={(0,1):(1,2),(0,3):(2,3),(2,1):(0,1),(2,3):(3,4)}[u,c]
        if lo*Q<y<hi*Q:return (u,sign,M,c)
    return None

def main():
    edges={};tested=0
    for q in range(3,E['phase_denominator_cap']+1):
      for A in range(1,q-1):
       for C in range(A+1,q):
        guard()
        if gcd(gcd(A,C),q)!=1:continue
        tested+=1
        if works(A,C,q) is None:
            a,b=F(A,C-A),F(q-C,C-A)
            edges[a,b]=(A,C,q)
      neighbors={}
      for a,b in edges:neighbors.setdefault(a,set()).add(b)
      aa=sorted(neighbors)
      for i,a in enumerate(aa):
       for A in aa[i+1:]:
        bs=sorted(neighbors[a]&neighbors[A])
        if len(bs)>=2:
            b,Bb=bs[:2];hm=(a+A)/2;hp=(b+Bb)/2
            rows=[{'a':str(x),'b':str(y),'phase':[edges[x,y][0],edges[x,y][1],edges[x,y][2]]} for x,y in [(a,b),(A,b),(a,Bb),(A,Bb)]]
            out={'status':'FOUR_CAP_PORTAL_MECHANISM_REFUTED','s':'1/2','t':'1/4','a':str(a),'b':str(b),'hm':str(hm),'hp':str(hp),
                 'effective_A':str(A),'effective_B':str(Bb),'four_complete_failure_rows':rows,'rational_phase_pairs_tested':tested,
                 'phase_denominator_prefix':q,'effort':E,'scope':'No vertical-only chart on ANY of four endpoint-cap sheets. NOT a dark room.'}
            (B/'rational-rectangle.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out));return
    out={'status':'NO_RECTANGLE_IN_BOUNDED_PHASE_CONTROLS','phase_pairs_tested':tested,'failure_edges':len(edges),'failure_rows':[{'a':str(a),'b':str(b),'phase':list(v)} for (a,b),v in sorted(edges.items())],'effort':E,
         'scope':'No universal cap-cover or darkness conclusion.'}
    (B/'rational-rectangle.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
