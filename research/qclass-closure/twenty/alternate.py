"""For failed four-branch boxes, prove one transverse displacement must be positive on a chosen axis."""
from collections import defaultdict
from pathlib import Path
from math import lcm
import subprocess,sys
def boxes_for(shear_dir):
    rows=defaultdict(dict)
    for path in sorted(shear_dir.glob('*/ends-*')):
        orient=int(path.parent.name);r=int(path.name.split('-')[1])
        marks=list(map(str.split,path.read_text().splitlines()))
        statuses=[int(l.split()[5]) for l in (path.parent/f'cert-{r}').read_text().splitlines() if l.startswith('END ')]
        assert len(statuses)%len(marks)==0
        n=len(statuses)//len(marks)
        assert n in (2,4)
        for j,m in enumerate(marks):
            vals=list(map(int,m));i,x,y,a,b,k,X,Y,A,B=vals
            if orient:x,y,a,b,X,Y,A,B=y,x,b,a,Y,X,B,A
            key=(i,k,x-a+2*(y-b),X-A+2*(Y-B),r)
            rows[key][orient]=(vals,all(statuses[j*n:(j+1)*n]))
    return rows
def run(root,hard):
    import shutil
    rows=boxes_for(hard/'shears')
    for key,v in rows.items():
        if v[0][1] and v[1][1]:continue
        r=key[-1];name='_'.join(map(str,key))
        dest=hard/'alternate'/name;dest.mkdir(parents=True,exist_ok=True)
        for axis in sorted((0,1),key=lambda a:not v[a][1]):
            m,_=v[axis];src=hard/'shears'/str(axis)
            raw=list(map(int,(src/'room').read_text().split()[2:]));C=set(zip(raw[::2],raw[1::2]))
            # A=0 puts both marks on their designated horizontal grid lines.
            # At least one of those lines must be a physical wall of its tile.
            if not any((a,b+(1 if y==b+1 else -1)) not in C for c,x,y,a,b in (m[:5],m[5:])):continue
            widths=[]
            for x,y in C:
                if (x-1,y) in C:continue
                z=x+1
                while (z,y) in C:z+=1
                widths.append(2*(z-x))
            proof=dest/str(axis);proof.mkdir(exist_ok=True)
            shutil.copy(src/'room',proof/'room')
            (proof/f'ends-{r}').write_text(' '.join(map(str,m))+'\n')
            with (proof/f'ends-{r}').open() as inp,(proof/f'cert-{r}').open('w') as out:
                subprocess.run([root/'axis',src/'labels',str(r),str(lcm(*widths)),'40','50000'],stdin=inp,stdout=out,check=True)
            flags=[l.split()[5] for l in (proof/f'cert-{r}').read_text().splitlines() if l.startswith('END ')]
            if flags and all(f=='1' for f in flags):
                (dest/'axis').write_text(str(axis)+'\n');break
        else:print('open',hard.name,key,flush=True)
if __name__=='__main__':
    root=Path(sys.argv[1])
    for name in sys.argv[2:]:run(root,root/'hard'/name)
