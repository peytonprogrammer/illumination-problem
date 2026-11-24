/* D9 exact shooting, with all-parity D205 pair accounting. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int verify_plane(int ncell, const int *cx, const int *cy,
                 int sx0, int sy0, int dx, int dy, int m, int tx, int ty);

#define MAXC 40
#define G 48                       /* grid side for cells and points (coords 0..G-2) */
#define MAXP (G * G)

static int n, cx[MAXC], cy[MAXC];
static int cellid[G][G];           /* -1 if absent */
static int nsq;
static int H[4 * MAXC], V[4 * MAXC], LAB[4 * MAXC], BLK[4 * MAXC];
static const int SX[4] = {1, -1, 1, -1}, SY[4] = {1, 1, -1, -1};

static int has(int x, int y) { return x >= 0 && y >= 0 && x < G && y < G && cellid[x][y] >= 0; }
static int cnt_around(int x, int y) { return has(x - 1, y - 1) + has(x, y - 1) + has(x - 1, y) + has(x, y); }

/* primitive directions */
static int ndir, DP_[4000], DQ_[4000];
static unsigned char WORD[4000][128];
static int WLEN[4000];

static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

static void make_dirs(int bound) {
    ndir = 0;
    for (int s = 1; s <= bound; s++)
        for (int p = s; p >= 0; p--) {
            int q = s - p;
            if (gcd(p, q) != 1) continue;
            DP_[ndir] = p; DQ_[ndir] = q;
            int L = 0;
            if (p >= 1 && q >= 1) {
                int a = 1, b = 1;
                while (a < p || b < q) {
                    long uv = (a < p) ? (long)q * a : 1L << 60;
                    long uh = (b < q) ? (long)p * b : 1L << 60;
                    if (uv < uh) { WORD[ndir][L++] = 0; a++; }   /* vertical line: h */
                    else         { WORD[ndir][L++] = 1; b++; }   /* horizontal line: v */
                }
            }
            WLEN[ndir] = L;
            ndir++;
        }
}

static int sq(int c, int sh) { return 4 * c + sh; }

static void build_origami(void) {
    nsq = 4 * n;
    for (int c = 0; c < n; c++)
        for (int sh = 0; sh < 4; sh++) {
            int s = sq(c, sh), i = cx[c], j = cy[c], sx = SX[sh], sy = SY[sh];
            int fx = sh ^ 1, fy = sh ^ 2;   /* sheet with sx / sy flipped */
            H[s] = has(i + sx, j) ? sq(cellid[i + sx][j], sh) : sq(c, fx);
            V[s] = has(i, j + sy) ? sq(cellid[i][j + sy], sh) : sq(c, fy);
            int X = i + (sx < 0), Y = j + (sy < 0);
            LAB[s] = X * G + Y;
            int k = cnt_around(X, Y);
            BLK[s] = (k == 1 || k == 3);
        }
}

/* next start square after one lattice step from the bottom-left corner of s */
static int step(int s, int d) {
    int p = DP_[d], q = DQ_[d];
    if (q == 0) return H[s];
    if (p == 0) return V[s];
    int c = s;
    for (int t = 0; t < WLEN[d]; t++) c = WORD[d][t] ? V[c] : H[c];
    return H[V[c]];
}


static long long counted[22][24][4]; /* eligible rooms, same pairs, different pairs, survivors */
extern int reflections;
static FILE *pairs;
static long long hist[9][41];
static uint64_t ordinal;
struct example { int h, r, sx, sy, tx, ty, dx, dy, m, bounce, height; uint32_t rows[MAXC]; uint64_t room; };
static struct example top[20];

void start_shoot(void) {
    memset(cellid,-1,sizeof cellid);
    make_dirs(40);
    pairs = fopen(getenv("PAIR_FILE"), "wb");
    if (!pairs) abort();
    setvbuf(pairs,NULL,_IOFBF,1024*1024);
}
void shoot_room(int area,int walls,int width,int height,const uint32_t *rows,int marks) {
    int mx[MAXC],my[MAXC],np=0;
    static int indices[G*G];
    n=0;
    for(int y=0;y<height;y++) for(uint32_t cells=rows[y];cells;cells&=cells-1) {
        int x=__builtin_ctz(cells);
        cx[n]=x+1; cy[n]=y+1;
        cellid[x+1][y+1]=n++;
    }
    for(int y=1;y<height;y++) {
        uint32_t both=rows[y]&rows[y-1];
        for(uint32_t pts=both&(both<<1);pts;pts&=pts-1) {
            int x=__builtin_ctz(pts);
            mx[np]=x+1; my[np]=y+1;
            indices[mx[np]*G+my[np]]=np+1; np++;
        }
    }
    if(np!=marks || n!=area) abort();
    build_origami();
    ordinal++;
    unsigned char header[3]={(walls-4)/2,height,np};
    unsigned char packedrows[2*MAXC];
    for(int y=0;y<height;y++){
        if(rows[y]>65535) abort();
        packedrows[2*y]=rows[y]; packedrows[2*y+1]=rows[y]>>8;
    }
    if(fwrite(header,1,3,pairs)!=3 || fwrite(packedrows,2,height,pairs)!=(size_t)height) abort();
    uint32_t record[MAXC][MAXC]={0};
    long long *stats=counted[area][walls];
    stats[0]++;
    for(int a=0;a<np-1;a++) {
        uint64_t pending=((1ULL<<np)-1)^((1ULL<<(a+1))-1);
        for(int b=a+1;b<np;b++)
            stats[1+(((mx[a]^mx[b])|(my[a]^my[b]))&1)]++;
        for(int d=0;d<ndir && pending;d++) for(int sh=0;sh<4 && pending;sh++) {
            int src=sq(cellid[mx[a]-(SX[sh]<0)][my[a]-(SY[sh]<0)],sh);
            int s=src;
            for(int m=1;m<=nsq;m++) {
                s=step(s,d);
                if(BLK[s] || s==src) break;
                int b=indices[LAB[s]]-1;
                if(b<0 || !(pending&(1ULL<<b))) continue;
                if(!verify_plane(n,cx,cy,mx[a],my[a],SX[sh]*DP_[d],SY[sh]*DQ_[d],m,mx[b],my[b])) abort();
                int p=DP_[d],q=DQ_[d],h=p>q?p:q,r=(walls-4)/2;
                hist[r][h]++;
                if(reflections>=4096 || m>=128 || d>=512) abort();
                record[a][b]=((uint32_t)reflections<<18)|(m<<11)|(sh<<9)|d;
                if(h>top[19].h){
                    int i=19;
                    while(i && h>top[i-1].h){top[i]=top[i-1]; i--;}
                    top[i]=(struct example){h,r,mx[a]-1,my[a]-1,mx[b]-1,my[b]-1,SX[sh]*p,SY[sh]*q,m,reflections,height,{0},ordinal};
                    memcpy(top[i].rows,rows,height*sizeof(*rows));
                }
                pending &= ~(1ULL<<b);
                if(!pending) break;
            }
        }
        while(pending) {
            int b=__builtin_ctzll(pending);
            pending &= pending-1;
            stats[3]++;
            printf("%d",n);
            for(int i=0;i<n;i++) printf(" %d %d",cx[i]-1,cy[i]-1);
            printf(" | 2 %d %d %d %d\n",mx[a]-1,my[a]-1,mx[b]-1,my[b]-1);
            if(fflush(stdout)) abort();
        }
    }
    for(int a=0;a<np-1;a++)
        if(fwrite(record[a]+a+1,4,np-a-1,pairs)!=(size_t)(np-a-1)) abort();
    for(int i=0;i<n;i++) cellid[cx[i]][cy[i]]=-1;
    for(int i=0;i<np;i++) indices[mx[i]*G+my[i]]=0;
}
void finish_shoot(FILE *out) {
    if(fclose(pairs)) abort();
    for(int r=0;r<=8;r++) for(int h=1;h<=40;h++) if(hist[r][h]) fprintf(out,"HIST %d %d %lld\n",r,h,hist[r][h]);
    for(int i=0;i<20;i++){
        const struct example *e=top+i;
        fprintf(out,"TOP %d %d %llu %d %d %d %d %d %d %d %d",e->h,e->r,(unsigned long long)e->room,e->sx,e->sy,e->tx,e->ty,e->dx,e->dy,e->m,e->bounce);
        for(int y=0;y<e->height;y++) fprintf(out," %u",e->rows[y]);
        fputc('\n',out);
    }
    for(int a=1;a<=21;a++) for(int w=4;w<=20;w+=2) {
        const long long *s=counted[a][w];
        if(s[0]) fprintf(out,"SHOT %d %d %lld %lld %lld %lld\n",a,w,s[0],s[1],s[2],s[3]);
    }
}
