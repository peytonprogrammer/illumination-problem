"""Bounded single-room illumination worker. A cutoff always stays undecided."""
from pathlib import Path
from collections import deque
from math import gcd
from fractions import Fraction as F
import json
import sys
import time

ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'inputs'))
from exact import run as trace
import origami_frame as o
import origami_dark as decider
from geometry import replay


def solve(data,budget,settings):
    started=time.monotonic(); deadline=started+budget
    V=list(map(tuple,data['vertices']));S,T=map(tuple,data['marks'])
    delta=(T[0]-S[0],T[1]-S[1]);g=gcd(*map(abs,delta));direct=(delta[0]//g,delta[1]//g)
    r=settings['short_direction_radius']
    candidates=sorted({(p,q) for p in range(-r,r+1) for q in range(-r,r+1) if gcd(p,q)==1},key=lambda p:(p[0]*p[0]+p[1]*p[1],p))
    candidates=[direct]+[p for p in candidates if p!=direct]
    tested=0
    def result(status,**extra):
        return {'status':status,'seconds':time.monotonic()-started,'short_directions_tested':tested,**extra}
    def lit(method,direction,path,**extra):
        reflections=replay(V,S,T,path)
        return result('LIT',method=method,direction=direction,reflections=reflections,
                      path=[[str(x),str(y)] for x,y in path],**extra)
    for direction in candidates:
        if time.monotonic()>=deadline:return result('UNDECIDED',reason='optical_time_limit')
        tested+=1
        d,P=trace(V,S,T,B=settings['short_reflection_cap'],dirs=[direction])
        if d is not None:return lit('short_direction',d,P,orbit_states=0)
    if time.monotonic()>=deadline:return result('UNDECIDED',reason='optical_time_limit')
    R,U,labels,s0,frame=o.build(V,S,T)
    start=o.canon(R,U,labels,s0);seen={start};queue=deque([(start,((1,0),(0,1)))])
    def mul(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
    while queue:
        if time.monotonic()>=deadline:return result('UNDECIDED',reason='orbit_time_limit',orbit_states=len(seen))
        (R,U,labels),M=queue.popleft();s=R[0]
        while s!=0:
            if labels[s]=='block':break
            if labels[s]=='T':
                developed=(M[0][0],M[1][0])
                direction=(frame[0][0]*developed[0]+frame[1][0]*developed[1],
                           frame[0][1]*developed[0]+frame[1][1]*developed[1])
                d,P=trace(V,S,T,B=20000,dirs=[direction])
                if d is None:return result('UNDECIDED',reason='orbit_witness_replay_limit_or_mismatch',orbit_states=len(seen),direction=direction)
                return lit('finite_orbit_witness',d,P,orbit_states=len(seen))
            s=R[s]
        Ri,Ui=o.inv(R),o.inv(U)
        for a,b,N in ((R,tuple(o.comp(U,Ri)),((1,-1),(0,1))),
                      (tuple(o.comp(R,Ui)),U,((1,0),(-1,1)))):
            nxt=o.canon(a,b,labels,0)
            if nxt not in seen:
                seen.add(nxt)
                if len(seen)>settings['orbit_state_cap']:
                    return result('UNDECIDED',reason='orbit_state_cap',orbit_states=len(seen))
                queue.append((nxt,mul(M,N)))
    # Never call a bounded short-ray failure dark. This branch requires full
    # labeled-orbit exhaustion and a second, separately traversed exact check.
    if time.monotonic()>=deadline:return result('UNDECIDED',reason='confirmation_time_limit',orbit_states=len(seen))
    verdict,count=decider.decide(V,S,T,limit=settings['orbit_state_cap'])
    return result('CANDIDATE_DARK' if verdict=='DARK' else 'UNDECIDED',
                  reason='two_completed_orbit_traversals' if verdict=='DARK' else 'orbit_confirmation_disagreement_or_cap',
                  orbit_states=len(seen),confirmation=verdict,confirmation_states=count)

if __name__=='__main__':
    data=json.loads(Path(sys.argv[1]).read_text());settings=json.loads((ROOT/'case.json').read_text())['budgets']
    out=solve(data,float(sys.argv[3]),settings)
    Path(sys.argv[2]).write_text(json.dumps(out,indent=2)+'\n')
