from pathlib import Path
p=Path("verify_plane.c")
s=p.read_text().replace("int verify_plane(", "int reflections;\nint verify_plane(").replace("vp_n = ncell;", "reflections = 0;\n    vp_n = ncell;").replace("{ ex = -ex; ey = -ey; }","{ ex = -ex; ey = -ey; reflections++; }").replace("else ex = -ex;", "else { ex = -ex; reflections++; }").replace("else ey = -ey;", "else { ey = -ey; reflections++; }").replace("{ ci += ex; ey = -ey; }","{ ci += ex; ey = -ey; reflections++; }").replace("{ cj += ey; ex = -ex; }","{ cj += ey; ex = -ex; reflections++; }")
p.write_text(s)
p=Path('shoot.c')
s=p.read_text().replace('void start_shoot(void)', '''extern int reflections;
static FILE *pairs;
static long long hist[9][41];
static uint64_t ordinal;
struct example { int h, r, sx, sy, tx, ty, dx, dy, m, bounce, height; uint32_t rows[MAXC]; uint64_t room; };
static struct example top[20];

void start_shoot(void)''').replace('make_dirs(40);','''make_dirs(40);
    pairs = fopen(getenv("PAIR_FILE"), "wb");
    if (!pairs) abort();
    setvbuf(pairs,NULL,_IOFBF,1024*1024);''').replace('build_origami();','''build_origami();
    ordinal++;
    unsigned char header[3]={(walls-4)/2,height,np};
    unsigned char packedrows[2*MAXC];
    for(int y=0;y<height;y++){
        if(rows[y]>65535) abort();
        packedrows[2*y]=rows[y]; packedrows[2*y+1]=rows[y]>>8;
    }
    if(fwrite(header,1,3,pairs)!=3 || fwrite(packedrows,2,height,pairs)!=(size_t)height) abort();
    uint32_t record[MAXC][MAXC]={0};''').replace('pending &= ~(1ULL<<b);','''int p=DP_[d],q=DQ_[d],h=p>q?p:q,r=(walls-4)/2;
                hist[r][h]++;
                if(reflections>=4096 || m>=128 || d>=512) abort();
                record[a][b]=((uint32_t)reflections<<18)|(m<<11)|(sh<<9)|d;
                if(h>top[19].h){
                    int i=19;
                    while(i && h>top[i-1].h){top[i]=top[i-1]; i--;}
                    top[i]=(struct example){h,r,mx[a]-1,my[a]-1,mx[b]-1,my[b]-1,SX[sh]*p,SY[sh]*q,m,reflections,height,{0},ordinal};
                    memcpy(top[i].rows,rows,height*sizeof(*rows));
                }
                pending &= ~(1ULL<<b);''').replace('for(int i=0;i<n;i++) cellid', '''for(int a=0;a<np-1;a++)
        if(fwrite(record[a]+a+1,4,np-a-1,pairs)!=(size_t)(np-a-1)) abort();
    for(int i=0;i<n;i++) cellid''').replace('for(int a=1;a<=21;a++)', '''if(fclose(pairs)) abort();
    for(int r=0;r<=8;r++) for(int h=1;h<=40;h++) if(hist[r][h]) fprintf(out,"HIST %d %d %lld\\n",r,h,hist[r][h]);
    for(int i=0;i<20;i++){
        const struct example *e=top+i;
        fprintf(out,"TOP %d %d %llu %d %d %d %d %d %d %d %d",e->h,e->r,(unsigned long long)e->room,e->sx,e->sy,e->tx,e->ty,e->dx,e->dy,e->m,e->bounce);
        for(int y=0;y<e->height;y++) fprintf(out," %u",e->rows[y]);
        fputc('\\n',out);
    }
    for(int a=1;a<=21;a++)''')
p.write_text(s)
p=Path('batch.py')
s=p.read_text()
a=s.index("if stage=='a21':")
b=s.index("manifest=",a)
s=s[:a]+"""assert stage=='a21'
original=Path('../d205-census-a21')
assert sha('enum_rooms.c')==sha(original/'enum_rooms.c')
assert sha('orbitc')==json.loads((original/'validation/PASS.json').read_text())['orbit']
"""+s[b:]
s=s.replace('subprocess.Popen(args,stdout=sv,stderr=err)','subprocess.Popen(args,stdout=sv,stderr=err,env={**os.environ,"PAIR_FILE":str(base)+".bin"})')
s=s.replace("records=Path", """old=(original/'a21'/f'{i}.counts').read_text().splitlines()
        lines=Path(str(base)+'.counts').read_text().splitlines()
        assert [s for s in lines if not s.startswith(('TOP ','HIST '))]==old
        assert sum(int(s.split()[3]) for s in lines if s.startswith('HIST '))==data['same_pairs']+data['different_pairs']
        records=Path""")
p.write_text(s)
