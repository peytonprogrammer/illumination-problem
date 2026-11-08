import sys; from exact import run
bad=0;n=0
for line in open(sys.argv[1]):
    h,v=line.split('|');_,a,b,d=h.split()
    V=[tuple(map(int,s.split(','))) for s in v.split()]
    a,b,d=[tuple(map(int,x.split(','))) for x in (a,b,d)]
    from fractions import Fraction
    import exact
    res=exact.run1(V,a,b,d)
    n+=1
    if not res: bad+=1; print('UNCONFIRMED',line.strip())
print('checked',n,'unconfirmed',bad)
