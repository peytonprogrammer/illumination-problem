"""Build the existing whole-room checkers and a tile checker with exact residual bounds."""
from pathlib import Path
import sys,subprocess
base=Path(__file__).resolve().parent
out=Path(sys.argv[1])
geom=base.parent/'offgrid'
stock=next(base.parents[1].glob('illumination-generalization*/fable/directions*/d13-cylinder-cover/cover.c'))
s=stock.read_text()
needle='        /* ---- pole test ---- */'
assert s.count(needle)==1
(out/'order.c').write_text(s.replace(needle,(geom/'order.inc').read_text()+needle))
for name in ('cover','skip','pairskip'):
    subprocess.run([sys.executable,geom/f'build_{name}.py',out/f'{name}.c'],check=True)
s=(out/'pairskip.c').read_text()
a='            if (big) status = "BIG";'
assert s.count(a)==1
s=s.replace(a,'''            if(nle || nlf){
                // Group product regions by a chosen vertex of each owning tile.
                // Store a safe L-infinity radius in units of 1/65536.
                int radius[4][4];memset(radius,-1,sizeof radius);
                for(int t=0;t<nl;t++){
                    Live *src=live+t;
                    for(int h=0;h<src->Q->n;h++){
                        QP *q=src->Q->a+h;
                        const Poly *polys[2]={&src->P,&q->P};
                        int cells[2]={src->cell,q->cell},corner[2],rad=0;
                        for(int e=0;e<2;e++){
                            int best=65537;
                            for(int k=0;k<4;k++){
                                int x=CX[cells[e]]+(k&1),y=CY[cells[e]]+(k>>1),hi=0;
                                for(int z=0;z<polys[e]->n;z++){
                                    Pt v=polys[e]->v[z];
                                    ll a=llabs(v.x-v.d*x),b=llabs(v.y-v.d*y);
                                    int d=(int)((65536*(a>b?a:b)+v.d-1)/v.d);
                                    if(d>hi)hi=d;
                                }
                                if(hi<best){corner[e]=k;best=hi;}
                            }
                            if(best>rad)rad=best;
                        }
                        if(cells[0]!=ca){int k=corner[0];corner[0]=corner[1];corner[1]=k;}
                        int *r=&radius[corner[0]][corner[1]];if(rad>*r)*r=rad;
                    }
                }
                for(int x=0;x<4;x++)for(int y=0;y<4;y++)if(radius[x][y]>=0)
                    printf("BOX %lld %d %d %d %d %d\\n",rid,ca,cb,x,y,radius[x][y]);
            }
'''+a)
(out/'tile.c').write_text(s)
for name in ('order','cover','skip','tile'):
    subprocess.run(['cc','-O3',out/f'{name}.c','-o',out/name],check=True)
