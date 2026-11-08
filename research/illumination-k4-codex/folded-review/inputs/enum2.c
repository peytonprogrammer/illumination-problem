// Parity-room enumerator with incremental pruning.
// Room: strictly simple polygon on tiling lines of the canonical 45-degree tiling, A = 2Z^2.
// Every B/C point of the closed room must be a boundary corner. Walls <= WMAX.
// Pruning: tiles in the wedge at each visited vertex are inside, the others outside;
// every B/C vertex of an inside tile must be visited later, and costs a wall.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const int DX[8]={1,1,0,-1,-1,-1,0,1},DY[8]={0,1,1,1,0,-1,-1,-1};
#define M 96
#define OFF 48
#define TM 300
#define TOFF 144
static unsigned char visited[M][M];
static int vin[M][M];            // number of inside tiles incident to vertex
static int tin[TM][TM],tout[TM][TM];
static int PX[300],PY[300],PD[300],n,WMAX,sx,sy,req=0,conflict=0;
static long found=0,closed=0,nodes=0;
static int cls(int x,int y){int a=x&1,b=y&1;return a&&b?2:(a||b?1:0);}
static int norm(int t){t%=8;if(t>4)t-=8;if(t<-4)t+=8;return t;}
static int turnOK(int c,int t){ if(t==4||t==-4)return 0; if(c==1)return t==2||t==-2; if(c==2)return t!=0; return 1;}
static int below(int x,int y){return y<sy||(y==sy&&x<sx);}
// sector k at v: triangle v, v+D[k], v+D[k+step]
static void tile_of(int x,int y,int k,int step,int T[3][2]){T[0][0]=x;T[0][1]=y;T[1][0]=x+DX[k];T[1][1]=y+DY[k];int k2=(k+step)&7;T[2][0]=x+DX[k2];T[2][1]=y+DY[k2];}
static void mark_in(int T[3][2],int s){
  int kx=T[0][0]+T[1][0]+T[2][0]+TOFF,ky=T[0][1]+T[1][1]+T[2][1]+TOFF;
  int before=tin[kx][ky]; tin[kx][ky]+=s;
  if(s>0&&tout[kx][ky]>0)conflict+= 1; if(s<0&&tout[kx][ky]>0)conflict-=1;
  if((s>0&&before==0)||(s<0&&tin[kx][ky]==0)){
    for(int i=0;i<3;i++){int ux=T[i][0],uy=T[i][1];int b=vin[ux+OFF][uy+OFF];vin[ux+OFF][uy+OFF]+=s;
      if(cls(ux,uy)&&!visited[ux+OFF][uy+OFF]){ if(s>0&&b==0)req++; if(s<0&&vin[ux+OFF][uy+OFF]==0)req--; }}
  }
}
static void mark_out(int T[3][2],int s){
  int kx=T[0][0]+T[1][0]+T[2][0]+TOFF,ky=T[0][1]+T[1][1]+T[2][1]+TOFF;
  tout[kx][ky]+=s; if(tin[kx][ky]>0)conflict+=s;
}
static void wedge(int x,int y,int din,int dout,int s){
  int c=cls(x,y),step=c==1?2:1; int back=(din+4)&7;
  for(int k=(c==1?0:0);k<8;k+=step){
    // inside iff k in [dout, back) going counterclockwise
    int rel=(k-dout)&7,span=(back-dout)&7; if(span==0)span=8;
    int T[3][2];tile_of(x,y,k,step,T);
    if(rel<span)mark_in(T,s);else mark_out(T,s);
  }
}
static void visit(int x,int y,int s){
  if(s>0){visited[x+OFF][y+OFF]=1; if(cls(x,y)&&vin[x+OFF][y+OFF]>0)req--;}
  else{visited[x+OFF][y+OFF]=0; if(cls(x,y)&&vin[x+OFF][y+OFF]>0)req++;}
}
static void check(int walls){
  int minx=1<<30,maxx=-(1<<30),miny=1<<30,maxy=-(1<<30);
  for(int i=0;i<n;i++){if(PX[i]<minx)minx=PX[i];if(PX[i]>maxx)maxx=PX[i];if(PY[i]<miny)miny=PY[i];if(PY[i]>maxy)maxy=PY[i];}
  int nA=0;
  for(int y=miny+1;y<maxy;y++)for(int x=minx+1;x<maxx;x++){
    if(visited[x+OFF][y+OFF])continue;
    int in=0;
    for(int i=0;i<n;i++){int ax=PX[i],ay=PY[i],bx=PX[(i+1)%n],by=PY[(i+1)%n];
      if((ay>y)!=(by>y)){long num=(long)(y-ay)*(bx-ax),den=by-ay,lhs=(long)(x-ax)*den;if(den>0?num>lhs:num<lhs)in^=1;}}
    if(in){if(cls(x,y))return;nA++;}
  }
  if(nA<2)return;
  found++;printf("%d %d",walls,nA);
  for(int i=0;i<n;i++){int t=norm(PD[i]-PD[(i-1+n)%n]);if(t)printf(" %d,%d",PX[i],PY[i]);}
  printf("\n");fflush(stdout);
}
static void dfs(int walls,int turnsum){
  nodes++;
  int x=PX[n-1],y=PY[n-1],din=PD[n-2];
  for(int d=0;d<8;d++){
    if((d&1)&&cls(x,y)==1)continue;
    int t=norm(d-din); if(!turnOK(cls(x,y),t))continue;
    int w=walls+(t!=0); if(w>WMAX)continue;
    int nx=x+DX[d],ny=y+DY[d];
    if(!(nx==sx&&ny==sy)&&(below(nx,ny)||visited[nx+OFF][ny+OFF]))continue;
    wedge(x,y,din,d,1);
    if(!conflict){
      if(nx==sx&&ny==sy){
        int t0=norm(PD[0]-d);
        if(turnOK(cls(sx,sy),t0)&&turnsum+t+t0==8&&w+(t0!=0)<=WMAX){
          wedge(sx,sy,d,PD[0],1);
          if(!conflict&&req==0){PD[n-1]=d;closed++;check(w+(t0!=0));}
          wedge(sx,sy,d,PD[0],-1);
        }
      } else {
        visit(nx,ny,1);
        int dist=abs(nx-sx)>abs(ny-sy)?abs(nx-sx):abs(ny-sy);
        if(w+req<=WMAX && dist<=2*(WMAX-w)+1){PD[n-1]=d;PX[n]=nx;PY[n]=ny;n++;dfs(w,turnsum+t);n--;}
        visit(nx,ny,-1);
      }
    }
    wedge(x,y,din,d,-1);
  }
}
int main(int argc,char**argv){
  WMAX=atoi(argv[1]);
  int starts[4][2]={{0,0},{1,0},{0,1},{1,1}};
  int k0=argc>2?atoi(argv[2]):0,k1=argc>2?k0+1:4;
  for(int k=k0;k<k1;k++){
    sx=starts[k][0];sy=starts[k][1];
    int e0=argc>3?atoi(argv[3]):0,e1=argc>3?e0+1:8;
    for(int d0=e0;d0<e1;d0++){
      if((d0&1)&&cls(sx,sy)==1)continue;
      int nx=sx+DX[d0],ny=sy+DY[d0]; if(below(nx,ny))continue;
      n=2;PX[0]=sx;PY[0]=sy;PX[1]=nx;PY[1]=ny;PD[0]=d0;
      visited[sx+OFF][sy+OFF]=1; visit(nx,ny,1);
      dfs(0,0);
      visit(nx,ny,-1); visited[sx+OFF][sy+OFF]=0;
      if(req||conflict){fprintf(stderr,"state leak req=%d conflict=%d\n",req,conflict);return 1;}
    }
  }
  fprintf(stderr,"WMAX %d nodes %ld closed %ld found %ld\n",WMAX,nodes,closed,found);
}
