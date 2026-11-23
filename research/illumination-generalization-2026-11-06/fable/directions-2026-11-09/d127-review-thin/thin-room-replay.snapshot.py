"""Replay a prescribed certificate per pair. No trial directions or reflection words."""
from fractions import Fraction as F
from itertools import combinations
from math import gcd


def folded(z, lo, width):
    u = (z - lo) % (2 * width)
    return (lo + u, 1) if u <= width else (lo + 2 * width - u, -1)


def image(x, sign, lo):
    return lo + sign * (x - lo)


def four(q, S, T):
    c = 2*q - 1
    if (3*T + 2*S - 2*c) % (2*q) == 0:
        c = 2*q + 1
    s = F(c-S, 3)
    s += round(3*(T-4*q-s)/(4*q)) * F(4*q, 3)
    x4, e4 = folded(T-s, 4*q, 2*q)
    z3 = image(x4,e4,2*q)-s
    s += (-round((z3-2*q)/(2*q)) % 3) * 4*q
    x3,e3 = folded(image(x4,e4,2*q)-s, 2*q,3*q)
    x2,e2 = folded(S+3*s,0,2*q)
    l = 2*q-3
    diff = image(x3,e3,l)-image(x2,e2,l)-s
    assert diff.denominator == 1 and diff % 2 == 0
    mod = 2*q+3
    k = int(diff/2)*pow(6*q,-1,mod) % mod
    return (s+12*q*k) % (12*q*mod)


def two(U,V,left,right,lo,hi):
    g = gcd(left,right)
    center = F(U+V,2)
    cross = center+g*((lo-center)//g+1)
    assert lo < cross < hi
    k = int(cross-center)//g
    m = k*pow(left//g,-1,right//g) % (right//g)
    return cross-(U+2*left*m)


def replay(q):
    bands = [(0,2*q),(2*q-3,2*q+3),(2*q,3*q),(4*q,2*q)]
    rows = [(0,2*q),(2*q-3,2*q),(2*q,4*q),(4*q,5*q),(4*q,6*q)]
    pts = [(y,x) for y,(lo,hi) in enumerate(rows,1) for x in range(lo+1,hi)]
    counts = {}
    for (y,S),(v,T) in combinations(pts,2):
        if (v-y)%2 or (T-S)%2:
            continue
        counts[y,v] = counts.get((y,v),0)+1
        if y==v:
            continue
        sign = 1
        if (y,v)==(1,5):
            s = four(q,S,T)
            legs = [(0,1),(0,2),(1,1),(2,1),(3,1)]
        elif (y,v)==(3,5) and (S,T)==(3*q,5*q):
            s = F(3*q,2)
            legs = [(2,1),(3,2),(3,1)]
        else:
            i = y-1
            l,w = bands[i]
            r,h = bands[i+1]
            U,V = S,T
            if y==3 and (U+V)%(2*q)==0:
                if (S-l)%q:
                    U,sign = 2*l-S,-1
                else:
                    V = 2*r-T
            s = two(U,V,w,h,max(l,r),min(l+w,r+h))
            legs = [(i,1),(i+1,1)]
        x = S
        for j,(i,d) in enumerate(legs):
            lo,w = bands[i]
            x,sign = folded(image(x,sign,lo)+d*s,lo,w)
            if j+1<len(legs):
                lo2,w2 = bands[legs[j+1][0]]
                assert max(lo,lo2)<x<min(lo+w,lo2+w2), (q,y,v,S,T,s,j,x)
        assert x==T, (q,y,v,S,T,s,x)
    return sum(counts.values()), counts[1,5]


if __name__=='__main__':
    for q in (16,28,40,52,64):
        print(q,*replay(q))
