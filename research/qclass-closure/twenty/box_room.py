"""Generate two-axis certificates for every bounded product in one room."""
from collections import defaultdict
from math import lcm
from pathlib import Path
import subprocess,sys
def generate(bins,path,room,boxes):
    flat=list(map(int,room.split()))
    cells=list(zip(flat[2::2],flat[3::2]))
    path.mkdir(exist_ok=True)
    for swap in (0,1):
        def pos(c):return c[::-1] if swap else c
        C=set(map(pos,cells))
        widths=[]
        for x,y in C:
            if (x-1,y) not in C:
                z=x+1
                while (z,y) in C:z+=1
                widths.append(2*(z-x))
        period=lcm(*widths)
        assert period<100000
        d=path/str(swap);d.mkdir(exist_ok=True)
        (d/'room').write_text(' '.join(map(str,[*flat[:2],*(z for c in cells for z in pos(c))]))+'\n')
        with (d/'room').open() as f,(d/'labels').open('w') as g:subprocess.run([bins/'labels'],stdin=f,stdout=g,check=True)
        groups=defaultdict(list)
        for i,j,ci,cj,r in sorted(set(map(tuple,boxes))):
            marks=[]
            for idx,k in ((i,ci),(j,cj)):
                a,b=cells[idx]
                marks.extend([idx,*pos((a+(k&1),b+(k>>1))),*pos((a,b))])
            groups[r].append(' '.join(map(str,marks)))
        for r,rows in groups.items():
            (d/f'ends-{r}').write_text('\n'.join(rows)+'\n')
            with (d/f'ends-{r}').open() as f,(d/f'cert-{r}').open('w') as g:subprocess.run([bins/'shear',d/'labels',str(r),str(period),'35','50000'],stdin=f,stdout=g,check=True)
if __name__=='__main__':
    root=Path(sys.argv[1]);room=(root/'early.room').read_text()
    boxes=[list(map(int,l.split()[2:])) for l in (root/'early.out').open() if l.startswith('BOX ')]
    generate(root,root/'early-check',room,boxes)
