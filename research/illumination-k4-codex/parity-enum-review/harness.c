#define main peer_main
#include "inputs/enum2.c"
#undef main
#include <assert.h>
static int clean(void){
 if(req||conflict)return 0;
 for(int x=0;x<M;x++)for(int y=0;y<M;y++)if(visited[x][y]||vin[x][y])return 0;
 for(int x=0;x<TM;x++)for(int y=0;y<TM;y++)if(tin[x][y]||tout[x][y])return 0;
 return 1;
}
static int direction(int x,int y){for(int d=0;d<8;d++)if(DX[d]==x&&DY[d]==y)return d;return -1;}
int main(int argc,char **argv){
 if(argc>1&&!strcmp(argv[1],"--local")){
  int sites[4][2]={{0,0},{1,0},{0,1},{1,1}};
  for(int j=0;j<4;j++)for(int din=0;din<8;din++)for(int dout=0;dout<8;dout++){
   int x=sites[j][0],y=sites[j][1],c=cls(x,y),t=norm(dout-din);
   if(c==1&&((din|dout)&1))continue;
   if(!turnOK(c,t))continue;
   visited[x+OFF][y+OFF]=1;wedge(x,y,din,dout,1);
   printf("{\"site\":[%d,%d],\"din\":%d,\"dout\":%d,\"req\":%d,\"conflict\":%d,\"tiles\":[",x,y,din,dout,req,conflict);
   int step=c==1?2:1;
   for(int k=0;k<8;k+=step){int T[3][2];tile_of(x,y,k,step,T);int a=T[0][0]+T[1][0]+T[2][0]+TOFF,b=T[0][1]+T[1][1]+T[2][1]+TOFF;printf("%s[%d,%d,%d,%d,%d,%d,%d]",k?",":"",T[0][0],T[0][1],T[1][0],T[1][1],T[2][0],T[2][1],tin[a][b]>0);}
   printf("]}\n");wedge(x,y,din,dout,-1);visited[x+OFF][y+OFF]=0;assert(clean());
  }
  return 0;
 }
 int expected_found;assert(scanf("%d %d %d",&WMAX,&n,&expected_found)==3);assert(n>2&&n<300);
 for(int i=0;i<n;i++)assert(scanf("%d %d",&PX[i],&PY[i])==2);
 sx=PX[0];sy=PY[0];int L=n;
 for(int i=0;i<L;i++){PD[i]=direction(PX[(i+1)%L]-PX[i],PY[(i+1)%L]-PY[i]);assert(PD[i]>=0);}
 visited[sx+OFF][sy+OFF]=1;visit(PX[1],PY[1],1);int walls=0,turns=0,maxreq=0;
 for(int i=1;i<L;i++){
  int t=norm(PD[i]-PD[i-1]);assert(turnOK(cls(PX[i],PY[i]),t));walls+=t!=0;turns+=t;
  wedge(PX[i],PY[i],PD[i-1],PD[i],1);assert(!conflict);
  if(i<L-1){
   int x=PX[i+1],y=PY[i+1];assert(!below(x,y)&&!visited[x+OFF][y+OFF]);visit(x,y,1);
   int dist=abs(x-sx)>abs(y-sy)?abs(x-sx):abs(y-sy);
   assert(walls+req<=WMAX);assert(dist<=2*(WMAX-walls)+1);if(req>maxreq)maxreq=req;
  }
 }
 int t0=norm(PD[0]-PD[L-1]);assert(turnOK(cls(sx,sy),t0));assert(turns+t0==8);walls+=t0!=0;assert(walls<=WMAX);
 wedge(sx,sy,PD[L-1],PD[0],1);assert(!conflict&&req==0);check(walls);assert(found==expected_found);wedge(sx,sy,PD[L-1],PD[0],-1);
 for(int i=L-1;i>=1;i--){if(i<L-1)visit(PX[i+1],PY[i+1],-1);wedge(PX[i],PY[i],PD[i-1],PD[i],-1);}
 visit(PX[1],PY[1],-1);visited[sx+OFF][sy+OFF]=0;assert(clean());
 fprintf(stderr,"FIXED PASS walls=%d atomic_vertices=%d maxreq=%d\n",walls,L,maxreq);return 0;
}
