"""Incidences on named pillowcase covers. No billiard trajectories are enumerated."""
import sys
from pathlib import Path
from collections import Counter
b=next(Path(__file__).resolve().parents[2].glob('illumination-generalization*/fable/directions*'))
sys.path.insert(0,str(b/'d66-pair-level'))
from pair_level import room_tuple,named_rooms
sys.path.insert(0,str(b/'d69-bbbb'))
from decomp import handbuilt
import json
covers=sorted((r for r in json.loads((b/'d64-finite-case/data/covers.json').read_text())['rooms'] if r['normalized']),key=lambda r:(r['n'],r['cells']))
for name,C,S,T in [('cov4181',set(map(tuple,covers[4181]['cells'])),(2,3),(4,3)),('cov4269',set(map(tuple,covers[4269]['cells'])),(3,2),(3,4)),('R22',dict(named_rooms())['R22'],(0,0),(2,2)),('P6',dict(named_rooms())['P6'],(1,0),(3,-2)),('DB55',handbuilt()['DB55'],(1,1),(9,1))]:
    room,t=room_tuple(C,S);n=len(t[0])
    A=sum((list(x) for x in room.points_at((0,0))[1]),[])
    B=sum((list(x) for x in room.points_at((T[0]-S[0],T[1]-S[1]))[1]),[])
    seen=set();summary=[]
    for i in range(n):
      for j in range(n):
        if i==j or (i,j) in seen:continue
        O={(i,j)};q=[(i,j)]
        while q:
            a,b0=q.pop()
            for perm in t:
                z=perm[a],perm[b0]
                if z not in O:O.add(z);q.append(z)
        seen.update(O);d=len(O)//n
        split=[]
        for p in t:
            two=sum((a,p[a]) in O and p[a]!=a and p[p[a]]==a for a in range(n))//2
            three=sum((a,b0) in O and b0 in (p[a],p[p[a]]) and p[p[a]]!=a for a in range(n) for b0 in set((p[a],p[p[a]])) )//3
            split.append((two,three))
        assert sum(i+j for i,j in split)==2*d
        hit=sum((a,b0) in O for a in A for b0 in B)
        ram=0
        for perm in t:
            pending=set(O)
            while pending:
                z=next(iter(pending));ram-=1
                while z in pending:
                    pending.remove(z);ram+=1;z=perm[z[0]],perm[z[1]]
        genus=1-len(O)+ram//2
        summary.append((d,split,hit,genus))
        if hit and name=='R22':
            from rl_test import point_map
            print('R22 source-class collision points:',[v for cy,v in point_map(room,C,S).items() if tuple(cy) in O])
    print(name,'(valency, (regular,reflex) by branch value, marked sheet pairs, genus)',summary)
