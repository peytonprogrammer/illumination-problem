// Filter bases: for each pair of non-corner A marks, search for a lit billiard path a -> b.
// Float tracer with early exit; prints pairs with no lit path for primitive directions up to R.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
typedef long double LD;
static int R=10,BOUNCE=400;
static int n,VX[64],VY[64];
static int gcd(int a,int b){a=abs(a);b=abs(b);while(b){int t=a%b;a=b;b=t;}return a;}
static int onseg(int px,int py,int i){int ax=VX[i],ay=VY[i],bx=VX[(i+1)%n],by=VY[(i+1)%n];
  if((long)(bx-ax)*(py-ay)-(long)(by-ay)*(px-ax))return 0;
  return (px-ax)*(px-bx)<=0&&(py-ay)*(py-by)<=0;}
static int inside(LD x,LD y){int c=0;for(int i=0;i<n;i++){LD ax=VX[i],ay=VY[i],bx=VX[(i+1)%n],by=VY[(i+1)%n];
  if((ay>y)!=(by>y)){LD xi=ax+(y-ay)*(bx-ax)/(by-ay);if(x<xi)c^=1;}}return c;}
// trace from (ax,ay) direction (p,q); return 1 if hits target (bx,by)
static int lit(int ax,int ay,int p,int q,int bx,int by){
  LD x=ax,y=ay,dx=p,dy=q; LD L=sqrtl(dx*dx+dy*dy);
  // must start into the room
  if(!inside(x+dx*1e-6L,y+dy*1e-6L))return 0;
  int last=-1;
  for(int k=0;k<BOUNCE;k++){
    LD best=1e30L;int bi=-1;
    for(int i=0;i<n;i++){ if(i==last)continue;
      LD ex=VX[(i+1)%n]-VX[i],ey=VY[(i+1)%n]-VY[i];
      LD den=dx*ey-dy*ex; if(fabsl(den)<1e-15L)continue;
      LD t=((VX[i]-x)*ey-(VY[i]-y)*ex)/den, s=((VX[i]-x)*dy-(VY[i]-y)*dx)/den;
      if(t>1e-12L&&s>-1e-12L&&s<1+1e-12L&&t<best){best=t;bi=i;}}
    if(bi<0)return 0;
    // target on the open segment (or at the hit point)?
    LD tx=bx-x,ty=by-y; LD cr=tx*dy-ty*dx, dot=tx*dx+ty*dy;
    if(fabsl(cr)<1e-9L*L&&dot>1e-12L&&dot<=best*(dx*dx+dy*dy)+1e-9L)return 1;
    LD hx=x+best*dx,hy=y+best*dy;
    // corner hit -> blocked
    for(int i=0;i<n;i++)if(fabsl(hx-VX[i])<1e-9L&&fabsl(hy-VY[i])<1e-9L)return 0;
    LD ex=VX[(bi+1)%n]-VX[bi],ey=VY[(bi+1)%n]-VY[bi],ee=ex*ex+ey*ey,dd=(dx*ex+dy*ey)/ee;
    dx=2*dd*ex-dx;dy=2*dd*ey-dy;x=hx;y=hy;last=bi;
  }
  return 0;
}
int main(int argc,char**argv){
  if(argc>1)R=atoi(argv[1]);
  char line[4096];long bases=0,darkb=0;
  while(fgets(line,sizeof line,stdin)){
    char*tok=strtok(line," \n");int W=atoi(tok);strtok(NULL," \n");char*kk=strtok(NULL," \n");
    n=0;while((tok=strtok(NULL," \n"))){sscanf(tok,"%d,%d",&VX[n],&VY[n]);n++;}
    bases++;
    int minx=1e9,maxx=-1e9,miny=1e9,maxy=-1e9;
    for(int i=0;i<n;i++){if(VX[i]<minx)minx=VX[i];if(VX[i]>maxx)maxx=VX[i];if(VY[i]<miny)miny=VY[i];if(VY[i]>maxy)maxy=VY[i];}
    int MX[64],MY[64],nm=0;
    for(int x=minx;x<=maxx;x++)for(int y=miny;y<=maxy;y++){ if((x&1)||(y&1))continue;
      int corner=0,bd=0;for(int i=0;i<n;i++){if(VX[i]==x&&VY[i]==y)corner=1;if(onseg(x,y,i))bd=1;}
      if(corner)continue; if(bd||inside(x+1e-7L,y+2e-7L)){MX[nm]=x;MY[nm]=y;nm++;}}
    int any=0;
    for(int i=0;i<nm;i++)for(int j=i+1;j<nm;j++){
      int L=0;
      for(int p=-R;p<=R&&!L;p++)for(int q=-R;q<=R&&!L;q++){ if(gcd(p,q)!=1)continue;
        if(lit(MX[i],MY[i],p,q,MX[j],MY[j])){L=1;if(getenv("LITOUT")){printf("LIT %d,%d %d,%d %d,%d |",MX[i],MY[i],MX[j],MY[j],p,q);for(int v=0;v<n;v++)printf(" %d,%d",VX[v],VY[v]);printf("\n");}}}
      if(getenv("DBG")&&L)fprintf(stderr,"lit %d,%d-%d,%d\n",MX[i],MY[i],MX[j],MY[j]);
      if(!L){any=1;printf("%d %s a=%d,%d b=%d,%d |",W,kk,MX[i],MY[i],MX[j],MY[j]);
        for(int v=0;v<n;v++)printf(" %d,%d",VX[v],VY[v]);printf("\n");}
    }
    darkb+=any;
  }
  fprintf(stderr,"bases %ld with-dark-pair %ld\n",bases,darkb);
}
