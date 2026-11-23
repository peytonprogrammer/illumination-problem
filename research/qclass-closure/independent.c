/* Independent fixed-polyomino count. Assign individual frontier squares, and
   prune impossible completed or partial vertex stars. No tile placement. */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <stdint.h>
enum { W=96, ROOT=40*W+40 };
static uint8_t grid[W*W], star[W*W], phase_vertex[W*W], queued[W*W];
static int agenda[256], points[40], count, top, rlo, vlo, bad, phase;
static long long bins[37],nodes;
typedef struct{int bad,r,v;} Bound;
static Bound table[2][256];
static const int shift[4]={0,1,W,W+1}, step[4]={W,-W,1,-1};

static void update(int z,int occupied){
    for(int i=0;i<4;i++){
        int p=z+shift[i],old=star[p],next=old^(1<<(i+4*!occupied));
        Bound *row=table[phase_vertex[p]];
        bad+=row[next].bad-row[old].bad;
        rlo+=row[next].r-row[old].r;
        vlo+=row[next].v-row[old].v;
        star[p]=next;
    }
}

static void finish(void){
    int vertices=0, shared=0, marks=0;
    for(int j=0;j<count;j++){
        int z=points[j];
        shared+=(grid[z+1]==1)+(grid[z+W]==1);
        for(int i=0;i<4;i++){
            int mask=star[z+shift[i]]&15;
            if((mask&-mask)==(1<<i)){vertices++;marks+=mask==15;}
        }
    }
    // All actual rooms are face-connected by construction. Euler counts holes.
    if(marks>=2 && vertices-3*count+shared==1)bins[count]++;
}

static void visit(void){
    nodes++;
    if(rlo>8||vlo>12||bad||count>36)return;
    if(!top){finish();return;}
    int z=agenda[--top],base=top;
    if(z!=ROOT){
        grid[z]=2;update(z,0);visit();update(z,0);grid[z]=0;
    }
    grid[z]=1;update(z,1);points[count++]=z;
    for(int i=0;i<4;i++){
        int t=z+step[i];
        if(!grid[t]&&!queued[t]){
            agenda[top++]=t;queued[t]=1;
        }
    }
    visit();
    while(top>base)queued[agenda[--top]]=0;
    --count;update(z,1);grid[z]=0;
    agenda[top++]=z;
}

int main(int argc,char**argv){
    assert(argc==2);phase=atoi(argv[1]);
    for(int q=0;q<2;q++)for(int id=0;id<256;id++){
        int valid=0,must_r=1,must_v=1;
        for(int m=0;m<16;m++){
            int d=__builtin_popcount((unsigned)m);
            if(m==6||m==9||(q&&d!=0&&d!=1&&d!=3))continue;
            if((m&(id&15))!=(id&15)||(m&(id>>4)))continue;
            valid=1;must_r&=d==3;must_v&=d==1;
        }
        table[q][id]=(Bound){!valid,valid&&must_r,valid&&must_v};
    }
    for(int z=0;z<W*W;z++)phase_vertex[z]=((z%W)%2+2*((z/W)%2)==phase);
    // Root is the leftmost cell of the bottom row. Permanently set the adjacent
    // forbidden row and forbidden bottom prefix absent, including their stars.
    for(int x=1;x<W-1;x++){
        int z=39*W+x;grid[z]=2;update(z,0);
        if(x<40){z+=W;grid[z]=2;update(z,0);}
    }
    agenda[top++]=ROOT;queued[ROOT]=1;visit();
    for(int n=1;n<=36;n++)printf("%d %lld\n",n,bins[n]);
    fprintf(stderr,"phase %d: %lld binary decisions and leaves\n",phase,nodes);
}
