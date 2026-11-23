/* enum_rooms.c -- exhaustive enumeration of strictly simple polyomino rooms.
 *
 * Redelmeier enumeration of fixed polyominoes with at most NMAX cells.  For
 * every polyomino:
 *   - per lattice point, a 4-bit mask of the surrounding cells;
 *   - reject pinch points (exactly two diagonal cells);
 *   - reject holes: with no pinch point the closed union is a surface with
 *     boundary, and it is a disc iff V - E + F == 1;
 *   - W = number of corners (lattice points with 1 or 3 cells); keep W <= WMAX;
 *   - keep one representative per free polyomino: the fixed polyomino whose
 *     normalised key is minimal over the 8 lattice symmetries.
 * Counts per (area, W) are written for all kept rooms.  Rooms with at least
 * two interior lattice points of one parity class ("eligible") are written,
 * normalised (min x = min y = 0), one per line: "area W x0 y0 x1 y1 ...".
 *
 * Parallel split: nodes of size SPLIT are dealt round-robin to NJ jobs; nodes
 * of size < SPLIT are processed by job 0 only.
 *
 * usage: enum_rooms NMAX WMAX NJ J outfile countsfile   (outfile "-" = stdout)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 24
#define SPLIT 11

static int NMAX, WMAX, NJ, J;
static int GW;                        /* grid width for cells */
static unsigned char *seen, *occ;     /* cell grid */
static unsigned char *pm;             /* lattice point masks */
static int PW;                        /* lattice grid width */
static int px[MAXN + 1], py[MAXN + 1];
static long long cnt_split = 0;
static long long rooms[MAXN + 1][4 * MAXN + 8];
static long long elig[MAXN + 1][4 * MAXN + 8];
static long long fixed_nodes = 0;
static long long fixed_by_size[MAXN + 1];
static int shoot_mode, min_area;
void start_shoot(void);
void shoot_room(int area,int walls,int width,int height,const uint32_t *rows,int marks);
void finish_shoot(FILE *out);
static long long expected_pairs[MAXN+1][64];

static inline int cid(int x, int y) { return (y + 1) * GW + (x + NMAX + 1); }
static inline int pid(int x, int y) { return (y + 1) * PW + (x + NMAX + 1); }

typedef struct { int w, h; uint32_t row[MAXN + 1]; } Key;

static void make_key(int k, int t, Key *K) {
    int ax[MAXN + 1], ay[MAXN + 1];
    int mnx = 1 << 20, mny = 1 << 20, mxx = -(1 << 20), mxy = -(1 << 20);
    for (int i = 0; i < k; i++) {
        int x = px[i], y = py[i], a, b;
        switch (t) {
        case 0: a = x;  b = y;  break;
        case 1: a = -x; b = y;  break;
        case 2: a = x;  b = -y; break;
        case 3: a = -x; b = -y; break;
        case 4: a = y;  b = x;  break;
        case 5: a = -y; b = x;  break;
        case 6: a = y;  b = -x; break;
        default: a = -y; b = -x; break;
        }
        ax[i] = a; ay[i] = b;
        if (a < mnx) mnx = a; if (a > mxx) mxx = a;
        if (b < mny) mny = b; if (b > mxy) mxy = b;
    }
    K->w = mxx - mnx + 1; K->h = mxy - mny + 1;
    memset(K->row, 0, sizeof(uint32_t) * (K->h));
    for (int i = 0; i < k; i++) K->row[ay[i] - mny] |= (uint32_t)1 << (ax[i] - mnx);
}

static int key_cmp(const Key *A, const Key *B) {
    if (A->w != B->w) return A->w < B->w ? -1 : 1;
    if (A->h != B->h) return A->h < B->h ? -1 : 1;
    for (int r = 0; r < A->h; r++)
        if (A->row[r] != B->row[r]) return A->row[r] < B->row[r] ? -1 : 1;
    return 0;
}

/* Maintain the same vertex masks and Euler test as d9 incrementally.
 * A cell toggles corner parity at its four vertices. */
static uint64_t rowbits[MAXN+1];
static int corner[16],pinch[16];
static void process(int k,int W,int holes_test,int pinches,int marks,int xmin,int xmax,int ymax) {
    if(k<min_area || W>WMAX || pinches || holes_test!=1) return;
    Key K0,K;
    K0.w=xmax-xmin+1; K0.h=ymax+1;
    if(K0.w>K0.h) return;
    int shift=xmin+MAXN;
    for(int r=0;r<K0.h;r++) K0.row[r]=rowbits[r]>>shift;
    if(K0.row[0]>K0.row[ymax]) return;
    for(int t=1;t<(K0.w==K0.h?8:4);t++) {
        if(t==2) {
            for(int r=0;r<K0.h;r++) K.row[r]=K0.row[ymax-r];
        } else {
            for(int r=0;r<K0.h;r++) {
                int from=t==3?ymax-r:r;
                if(t<4) K.row[r]=__builtin_bitreverse32(K0.row[from])>>(32-K0.w);
            }
            if(t>=4) make_key(k,t,&K);
        }
        K.w=K0.w; K.h=K0.h;
        if(key_cmp(&K,&K0)<0) return;
    }
    rooms[k][W]++;
    if(marks<2) return;
    int classes[4]={0};
    for(int y=1;y<K0.h;y++) {
        uint32_t common=K0.row[y-1]&K0.row[y];
        uint32_t points=common&(common<<1);
        classes[2*(y&1)]+=__builtin_popcount(points&0x55555555u);
        classes[2*(y&1)+1]+=__builtin_popcount(points&0xaaaaaaaau);
    }
    int cross=marks*(marks-1)/2;
    for(int c=0;c<4;c++) cross-=classes[c]*(classes[c]-1)/2;
    if(!cross) return;
    elig[k][W]++;
    expected_pairs[k][W]+=cross;
    if(shoot_mode) shoot_room(k,W,K0.w,K0.h,K0.row,marks);
}
static int allowed(int x, int y) {
    if (y < 0 || y >= NMAX) return 0;
    if (y == 0 && x < 0) return 0;
    if (x <= -NMAX || x >= NMAX) return 0;
    return 1;
}

static void rec(int n, const int *untried, int nu,int W,int chi,int pinches,int marks,int xmin,int xmax,int ymax) {
    int buf[4 * MAXN + 8];
    int U[4 * MAXN + 8];
    memcpy(U, untried, sizeof(int) * nu);
    while (nu > 0) {
        int c = U[--nu];
        int x = c % GW - NMAX - 1, y = c / GW - 1;
        int s = n + 1;
        if (s == SPLIT) {
            long long me = cnt_split++;
            if (me % NJ != J) continue;
        }
        px[n] = x; py[n] = y; occ[c] = 1;
        const int loc=pid(x,y), offsets[4]={0,1,PW,PW+1};
        int newW=W,newPinch=pinches,newMarks=marks,newChi=chi-3;
        for(int i=0;i<4;i++) {
            int old=pm[loc+offsets[i]], next=old | (8>>i);
            newW+=corner[next]-corner[old];
            newPinch+=pinch[next]-pinch[old];
            newMarks+=(next==15);
            newChi+=!old;
            pm[loc+offsets[i]]=next;
        }
        newChi+=occ[c+1]+occ[c-1]+occ[c+GW]+occ[c-GW];
        rowbits[y]|=1ULL<<(x+MAXN);
        int mn=x<xmin?x:xmin,mx=x>xmax?x:xmax,my=y>ymax?y:ymax;
        if(s>=SPLIT || J==0) {
            fixed_nodes++; fixed_by_size[s]++;
            process(s,newW,newChi,newPinch,newMarks,mn,mx,my);
        }
        /* Preserve d9's complete Redelmeier node counts for validation. */
        if (s < NMAX) {
            int m = nu, added = 0;
            memcpy(buf, U, sizeof(int) * nu);
            int nb[4][2] = {{x + 1, y}, {x - 1, y}, {x, y + 1}, {x, y - 1}};
            int addl[4];
            for (int d = 0; d < 4; d++) {
                int a = nb[d][0], b = nb[d][1];
                if (!allowed(a, b)) continue;
                int q = cid(a, b);
                if (seen[q]) continue;
                seen[q] = 1; buf[m++] = q; addl[added++] = q;
            }
            rec(s,buf,m,newW,newChi,newPinch,newMarks,mn,mx,my);
            for (int d = 0; d < added; d++) seen[addl[d]] = 0;
        }
        rowbits[y]^=1ULL<<(x+MAXN);
        for(int i=0;i<4;i++) pm[loc+offsets[i]]^=8>>i;
        occ[c] = 0;
    }
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: enum_rooms NMAX WMAX NJ J outfile countsfile\n"); return 1; }
    NMAX = atoi(argv[1]); WMAX = atoi(argv[2]); NJ = atoi(argv[3]); J = atoi(argv[4]);
    if (NMAX > MAXN || NMAX < SPLIT) { fprintf(stderr, "NMAX out of range\n"); return 1; }
    min_area=atoi(argv[5]);
    shoot_mode=(argc==8 && strcmp(argv[7],"shoot")==0);
    if(NMAX>20 || WMAX!=20 || NJ<=0 || J<0 || J>=NJ || min_area<1) return 2;
    if(shoot_mode) start_shoot();
    GW = 2 * NMAX + 4; PW = 2 * NMAX + 6;
    seen = calloc((size_t)GW * (NMAX + 4), 1);
    occ = calloc((size_t)GW * (NMAX + 4), 1);
    pm = calloc((size_t)PW * (NMAX + 6), 1);
    int start = cid(0, 0);
    seen[start] = 1;
    int U[1] = {start};
    for(int m=0;m<16;m++) {corner[m]=__builtin_popcount(m)%2;pinch[m]=(m==6||m==9);}
    rec(0,U,1,0,0,0,0,0,0,0);
    FILE *cf = fopen(argv[6], "w");
    fprintf(cf, "# fixed_nodes_processed %lld\n", fixed_nodes);
    for (int k = 1; k <= NMAX; k++) fprintf(cf, "# fixed area %d %lld\n", k, fixed_by_size[k]);
    for (int k = 1; k <= NMAX; k++)
        for (int w = 4; w <= WMAX; w += 2)
            if (rooms[k][w])
                fprintf(cf, "# count area %d W %d rooms %lld eligible %lld\n", k, w, rooms[k][w], elig[k][w]);
    for(int a=min_area;a<=NMAX;a++) for(int w=4;w<=WMAX;w+=2) if(expected_pairs[a][w]) fprintf(cf,"EXPECT %d %d %lld\n",a,w,expected_pairs[a][w]);
    if(shoot_mode) finish_shoot(cf);
    fprintf(cf, "# DONE\n");
    if(ferror(cf) || fclose(cf)) return 5;
    return 0;
}
