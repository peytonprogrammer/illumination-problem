# Keep lit verdicts whose pair could be interiorized by a 2-copy fold:
# each mark is interior in P, or lies on a wall with two convex endpoints (a possible seam); not both on walls.
import sys
def ccw(V):
    n=len(V);return V if sum(V[i][0]*V[(i+1)%n][1]-V[(i+1)%n][0]*V[i][1] for i in range(n))>0 else V[::-1]
def convex(V,i):
    n=len(V);a,b,c=V[i-1],V[i],V[(i+1)%n];return (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])>0
def status(V,p):
    n=len(V)
    for i in range(n):
        a,b=V[i],V[(i+1)%n]
        if (b[0]-a[0])*(p[1]-a[1])==(b[1]-a[1])*(p[0]-a[0]) and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1]):
            return 'seam' if convex(V,i) and convex(V,(i+1)%n) else 'dead'
    return 'int'
keep=0;tot=0
for line in sys.stdin:
    h,v=line.split('|');_,a,b,d=h.split();tot+=1
    V=ccw([tuple(map(int,s.split(','))) for s in v.split()])
    sa,sb=status(V,tuple(map(int,a.split(',')))),status(V,tuple(map(int,b.split(','))))
    if 'dead' in (sa,sb):continue  # two marks on one seam wall are possible
    keep+=1;sys.stdout.write(line)
print('lit verdicts',tot,'fold-relevant',keep,file=sys.stderr)
