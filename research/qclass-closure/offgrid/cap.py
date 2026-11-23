"""Sufficient physical-wall certificate, in unit-grid doubled position types."""
import functools
@functools.lru_cache(None)
def frames(cells):
    out=[]
    for swap in (False,True):
        for sign in (1,-1):
            C={(y if swap else x, (x if swap else y)*sign-(sign<0)) for x,y in cells}
            lo=min(x for x,y in C);hi=max(x for x,y in C)+1
            bot=min(y for x,y in C);top=max(y for x,y in C)+1
            chambers=[]
            for l in range(lo,hi):
                for r in range(l+1,hi+1):
                    for roof in range(bot+1,top+1):
                        if any((i,roof) in C for i in range(l,r)):continue
                        for door in range(roof-1,bot-1,-1):
                            if (l-1,door) in C or (r,door) in C or any((i,door) not in C for i in range(l,r)):break
                            if all((i,door-1) in C for i in range(l,r)):
                                chambers.append((l,r,door,roof))
            out.append((swap,sign,C,chambers))
    return out
def cap(cells,S,T):
    for swap,sign,C,chambers in frames(frozenset(cells)):
        def coord(P):
            x,y=P
            return (y,x*sign) if swap else (x,y*sign)
        for viewer,mark in ((S,T),(T,S)):
            x,y=coord(viewer);u,v=coord(mark)
            for l,r,d,e in chambers:
                if not (2*l<u<2*r and 2*d<v<2*e and y<2*d):continue
                # D<ell, including an open source interval with sup D=ell.
                if y<=2*(2*d-e):continue
                if all((i,j) in C for i in range(min(l,x//2),max(r,(x+1)//2))
                                  for j in range(y//2,d)):
                    return True
    return False
