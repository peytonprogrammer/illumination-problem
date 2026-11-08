// Enumerate strictly simple parity rooms in the canonical 45-degree tiling.
// A = 2Z^2, C = odd-odd, B = mixed. Diagonal edges only join A and C.
// Every B or C boundary vertex must be a corner (nonzero turn); at B the turn is +-90.
// Output: rooms whose interior lattice points are all A, with >= 2 interior A points.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int DX[8]={1,1,0,-1,-1,-1,0,1},DY[8]={0,1,1,1,0,-1,-1,-1};
#define M 80
#define OFF 40
static unsigned char used[M][M];
static int PX[200],PY[200],PD[200],n,WMAX,sx,sy;
static long found=0,closed=0;
static int cls(int x,int y){int a=x&1,b=y&1;return a&&b?2:(a||b?1:0);} // 0=A 1=B 2=C
static int turnOK(int c,int t){ if(t==4||t==-4)return 0; if(c==1)return t==2||t==-2; if(c==2)return t!=0; return 1;}
static int norm(int t){t%=8;if(t>4)t-=8;if(t<-4)t+=8;return t;}
static int below(int x,int y){return y<sy||(y==sy&&x<sx);}
static void check(int walls){
  // interior lattice points: all A, count >= 2
  int minx=1<<30,maxx=-(1<<30),miny=1<<30,maxy=-(1<<30);
  for(int i=0;i<n;i++){if(PX[i]<minx)minx=PX[i];if(PX[i]>maxx)maxx=PX[i];if(PY[i]<miny)miny=PY[i];if(PY[i]>maxy)maxy=PY[i];}
  int nA=0;
  for(int y=miny+1;y<maxy;y++)for(int x=minx+1;x<maxx;x++){
    if(used[x+OFF][y+OFF])continue;
    int in=0;
    for(int i=0;i<n;i++){int ax=PX[i],ay=PY[i],bx=PX[(i+1)%n],by=PY[(i+1)%n];
      if((ay>y)!=(by>y)){ // x-intersection > x ?  ax+(y-ay)*(bx-ax)/(by-ay) > x
        long num=(long)(y-ay)*(bx-ax),den=by-ay; long lhs=(long)(x-ax)*den;
        if(den>0? num>lhs : num<lhs) in^=1; }}
    if(in){ if(cls(x,y))return; nA++; }
  }
  if(nA<2)return;
  found++;
  printf("%d %d",walls,nA);
  for(int i=0;i<n;i++){int t=norm(PD[(i)%n]-PD[(i-1+n)%n]);if(t)printf(" %d,%d",PX[i],PY[i]);}
  printf("\n");
}
// state: vertices PX[0..n-1], PD[i] = direction of edge from vertex i to i+1
static void dfs(int walls,int turnsum){
  int x=PX[n-1],y=PY[n-1];
  for(int d=0;d<8;d++){
    if((d&1)&&cls(x,y)==1)continue;
    int t=norm(d-PD[n-2]);
    if(!turnOK(cls(x,y),t))continue;
    int w=walls+(t!=0); if(w>WMAX)continue;
    int nx=x+DX[d],ny=y+DY[d];
    if(nx==sx&&ny==sy){
      int t0=norm(PD[0]-d);
      if(!turnOK(cls(sx,sy),t0))continue;
      int ww=w+(t0!=0); if(ww>WMAX)continue;
      if(turnsum+t+t0!=8)continue;
      PD[n-1]=d;closed++;check(ww);continue;
    }
    if(below(nx,ny)||used[nx+OFF][ny+OFF])continue;
    // remaining edges <= 2*(WMAX-w)+1 ; need Chebyshev distance back
    int dist=abs(nx-sx)>abs(ny-sy)?abs(nx-sx):abs(ny-sy);
    if(dist>2*(WMAX-w)+1)continue;
    PD[n-1]=d;PX[n]=nx;PY[n]=ny;used[nx+OFF][ny+OFF]=1;n++;
    dfs(w,turnsum+t);
    n--;used[nx+OFF][ny+OFF]=0;
  }
}
int main(int argc,char**argv){
  WMAX=atoi(argv[1]);
  int starts[4][2]={{0,0},{1,0},{0,1},{1,1}};
  for(int k=0;k<4;k++){
    sx=starts[k][0];sy=starts[k][1];memset(used,0,sizeof used);
    for(int d0=0;d0<8;d0++){
      if((d0&1)&&cls(sx,sy)==1)continue;
      int nx=sx+DX[d0],ny=sy+DY[d0];
      if(below(nx,ny))continue;
      n=2;PX[0]=sx;PY[0]=sy;PX[1]=nx;PY[1]=ny;PD[0]=d0;used[sx+OFF][sy+OFF]=used[nx+OFF][ny+OFF]=1;
      dfs(0,0);
    }
  }
  fprintf(stderr,"WMAX %d closed %ld found %ld\n",WMAX,closed,found);
}
