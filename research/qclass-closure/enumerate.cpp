// Connected, anchored polyominoes with one prescribed opaque parity class.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdio>
#include <cstdlib>
#include <vector>
using namespace std;
constexpr int stride=100, grid_size=10000, origin=4040;
constexpr int corners[]={0,1,stride,stride+1}, neighbors[]={-1,1,-stride,stride};
int state[grid_size], inside[grid_size], filled[42], n, reflex, convex, invalid, maxr, minarea, px, py;
int scores[16][16][3]; // inevitable reflex, inevitable convex, impossible
long long nodes, leaves;
FILE *output;

void assign_cell(int cell,int value,int sign){
    state[cell]=sign>0?value:0;
    for(int k=0;k<4;k++){
        int v=cell+corners[k], bit=1<<k;
        // low four bits are present, high four bits are absent.
        int old=inside[v], now=old^(value==1?bit:bit<<4);
        int *a=scores[old&15][old>>4],*b=scores[now&15][now>>4];
        reflex+=b[0]-a[0];convex+=b[1]-a[1];invalid+=b[2]-a[2];inside[v]=now;
    }
}
bool forbidden(int cell){return cell/stride<origin/stride || (cell/stride==origin/stride && cell<origin);}

void emit(){
    if(n<minarea)return;
    int r=0,v=0,counts[4]={};
    for(int i=0;i<n;i++)for(int k=0;k<4;k++){
        int z=filled[i]+corners[k],mask=inside[z]&15;
        if((mask&-mask)!=(1<<k))continue;
        if(mask==6||mask==9)return;
        int cnt=__builtin_popcount((unsigned)mask);
        r+=cnt==3;v+=cnt==1;
        if(cnt==4)counts[((z%stride)&1)+2*((z/stride)&1)]++;
    }
    if(v-r!=4||r>maxr||counts[0]+counts[1]+counts[2]+counts[3]<2)return;
    // Keep the least oriented tuple of sorted cell coordinates.
    int coords[40], trans[40];
    for(int op=0;op<8;op++){
        int mx=100,my=100;
        for(int i=0;i<n;i++){
            int x=filled[i]%stride-40,y=filled[i]/stride-40;
            if(op&1)swap(x,y);
            if(op&2)x=-x;
            if(op&4)y=-y;
            mx=min(mx,x);my=min(my,y);trans[i]=x*100+y;
        }
        for(int i=0;i<n;i++)trans[i]-=100*mx+my;
        sort(trans,trans+n);
        if(!op)copy(trans,trans+n,coords);
        else if(lexicographical_compare(trans,trans+n,coords,coords+n))return;
    }
    fprintf(output,"%d %d",n,2*r+4);
    for(int i=0;i<n;i++)fprintf(output," %d %d",coords[i]/100,coords[i]%100);
    fputc('\n',output);leaves++;
}

void walk(int cellindex,int side){
    nodes++;
    if(invalid||reflex>maxr||convex>maxr+4||n>4*maxr+4)return;
    int z=origin; // initial call forces origin present
    if(cellindex>=0){
        while(cellindex<n){
            z=filled[cellindex]+neighbors[side];
            if(++side==4){cellindex++;side=0;}
            if(!state[z]&&!forbidden(z))break;
        }
        if(state[z]||forbidden(z)){emit();return;}
        assign_cell(z,2,1);walk(cellindex,side);assign_cell(z,2,-1);
    }else{cellindex=0;side=0;}
    // Lower left cell of the disjoint 2x2 block around a prescribed parity vertex.
    int base=z-(((z%stride)^px)&1)-stride*(((z/stride)^py)&1);
    for(int mask:{1,2,4,8,7,11,13,14}){
        int bit=(z-base)%stride+2*((z-base)/stride);
        if(!(mask&(1<<bit)))continue;
        bool ok=true;
        for(int k=0;k<4;k++){
            int c=base+corners[k],v=(mask&(1<<k))?1:2;
            if((state[c]&&state[c]!=v)||(v==1&&forbidden(c)))ok=false;
        }
        if(!ok)continue;
        int changed=0, saved=n;
        for(int k=0;k<4;k++){
            int c=base+corners[k]; if(state[c])continue;
            int val=(mask&(1<<k))?1:2;
            assign_cell(c,val,1);changed|=1<<k;if(val==1)filled[n++]=c;
        }
        walk(cellindex,side);
        n=saved;
        for(int k=0;k<4;k++)if(changed&(1<<k)){int c=base+corners[k];assign_cell(c,state[c],-1);}
    }
}

int main(int argc,char**argv){
    if(argc!=5)return 1;
    maxr=atoi(argv[1]);minarea=atoi(argv[2]);int parity=atoi(argv[3]);px=parity%2;py=parity/2;
    assert(maxr>=0&&maxr<=8&&parity>=0&&parity<4);
    output=fopen(argv[4],"w");assert(output);
    for(int i=0;i<16;i++)for(int j=0;j<16;j++){
        bool can=false,allr=true,allv=true;
        for(int m=0;m<16;m++)if(m!=6&&m!=9&&(m&i)==i&&!(m&j)){
            can=true;int d=__builtin_popcount((unsigned)m);allr&=d==3;allv&=d==1;}
        scores[i][j][0]=can&&allr;scores[i][j][1]=can&&allv;scores[i][j][2]=!can;
    }
    walk(-1,0);fclose(output);
    fprintf(stderr,"r=%d phase=%d nodes=%lld records=%lld\n",maxr,parity,nodes,leaves);
}
