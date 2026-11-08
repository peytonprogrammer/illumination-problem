"""Finite sufficient darkness certificate retaining reflected square identities.

A primitive positive lattice segment crosses a palindromic H/V word: the
crossings at times t and 1-t have the same edge type in opposite order. We
compute all endpoint pairs of all palindromic words, a safe overapproximation
of primitive directions. Continuing with potentially different words at each
regular vertex only enlarges visibility. No source-to-target path in that
finite graph therefore proves darkness in every direction. A graph path is
only a possibility, never a proof of illumination.
"""
from collections import deque
from illumination_cover import build,inverse,visibility

def relation(H,V):
    """Least fixed point R = identity ∪ H ∪ V ∪ H R H ∪ V R V."""
    n=len(H);Hi,Vi=inverse(H),inverse(V);rows=[0]*n;queue=deque()
    def add(a,b):
        mask=1<<b
        if not rows[a]&mask:rows[a]|=mask;queue.append((a,b))
    for i in range(n):add(i,i);add(i,H[i]);add(i,V[i])
    count=0
    while queue:
        a,b=queue.popleft();count+=1
        add(Hi[a],H[b]);add(Vi[a],V[b])
    return tuple(rows),count

def certify(data,include_relation=False):
    import time
    started=time.monotonic();c=build(data);H,V,colors=c['H'],c['V'],c['colors'];R,count=relation(H,V);n=len(H);ordinary={i for i,v in enumerate(colors) if v!=3};sources={i for i,v in enumerate(colors) if v==1};targets={i for i,v in enumerate(colors) if v==2}
    # W's endpoint is the NE corner of its final square. V then H chooses
    # a SW corner at that same vertex. At a regular vertex this is the unique
    # next NE departure sector, so graph walks include every actual ray.
    shift=tuple(H[V[i]] for i in range(n));graph={}
    for i in ordinary:
        graph[i]={shift[j] for j in range(n) if R[i]>>j&1 and shift[j] in ordinary}
    seen=set(sources);queue=deque(sources)
    while queue:
        i=queue.popleft()
        for j in graph[i]:
            if j not in seen:seen.add(j);queue.append(j)
    # Axis directions are exact separate maps; source lifts cover all physical
    # axis orientations. The positive word relation need not model these.
    axis_h=visibility(c,H);axis_v=visibility(c,V);dark=not(seen&targets) and axis_h is None and axis_v is None
    result=dict(status='DARK' if dark else 'INCONCLUSIVE',all_directions_covered=dark,method='palindromic crossing-word endpoint relation on actual unfolded sheets',cover_squares=n,palindrome_pairs=count,nonabsorbing_sectors=len(ordinary),source_sectors=len(sources),target_sectors=len(targets),reachable_regular_sectors=len(seen),potential_target_sectors=len(seen&targets),axis_h_possible=axis_h is not None,axis_v_possible=axis_v is not None,seconds=time.monotonic()-started)
    if include_relation:result['certificate']=dict(H=list(H),V=list(V),colors=list(colors),palindrome_rows=[str(r) for r in R],reachable=sorted(seen))
    return result

if __name__=='__main__':
    import argparse,json
    from pathlib import Path
    ap=argparse.ArgumentParser();ap.add_argument('room');ap.add_argument('--out');args=ap.parse_args();result=certify(json.loads(Path(args.room).read_text()),True);result['room']=args.room
    if args.out:Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='certificate'}))
