"""Conservative reciprocal raster at the end of a tile calculation."""
import sys,subprocess
from pathlib import Path
out=Path(sys.argv[1])
s=(out/'tile.c').read_text()
p=s.index('int main(int argc')
s=s[:p]+'''#define SIDE 16
#define BINS (SIDE*SIDE)
#define WORDS (BINS/64)
static int raster(const Poly *p,int cell,int ids[BINS]){
 ll xmin=SIDE,xmax=0,ymin=SIDE,ymax=0;
 for(int j=0;j<p->n;j++){
  Pt v=p->v[j];ll x=SIDE*(v.x-v.d*CX[cell])/v.d,y=SIDE*(v.y-v.d*CY[cell])/v.d;
  if(x>=SIDE)x=SIDE-1;if(y>=SIDE)y=SIDE-1;
  if(x<xmin)xmin=x;if(x>xmax)xmax=x;if(y<ymin)ymin=y;if(y>ymax)ymax=y;
 }
 int n=0;for(int x=xmin;x<=xmax;x++)for(int y=ymin;y<=ymax;y++)ids[n++]=SIDE*x+y;
 return n;
}
'''+s[p:]
p=s.index('                // Group product');b=s.index('            if (big) status',p)
s=s[:p]+'''                static unsigned long long rel[2][BINS][WORDS];
                memset(rel,0,sizeof rel);
                for(int t=0;t<nl;t++){
                  Live *src=live+t;int si[BINS],ni=raster(&src->P,src->cell,si);
                  unsigned long long mask[WORDS]={0};
                  for(int h=0;h<src->Q->n;h++){
                     QP *q=src->Q->a+h;int ti[BINS],nt=raster(&q->P,q->cell,ti);
                     for(int u=0;u<nt;u++){int k=ti[u];mask[k/64]|=1ULL<<(k%64);}
                  }
                  int e=(src->cell!=ca);
                  for(int u=0;u<ni;u++)for(int w=0;w<WORDS;w++)rel[e][si[u]][w]|=mask[w];
                }
                for(int i=0;i<BINS;i++)for(int j=0;j<BINS;j++)
                   if((rel[0][i][j/64]>>(j%64)&1)&&(rel[ca!=cb][j][i/64]>>(i%64)&1))
                     printf("PIX %d %d %d %d\\n",ca,cb,i,j);
            }
'''+s[b:]
(out/'grid.c').write_text(s)
subprocess.run(['cc','-O3',out/'grid.c','-o',out/'grid'],check=True)
