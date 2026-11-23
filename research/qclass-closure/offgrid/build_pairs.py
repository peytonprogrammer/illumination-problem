from pathlib import Path
import subprocess,sys,tempfile
base=Path(__file__).resolve().parent
with tempfile.NamedTemporaryFile() as tmp:
    subprocess.run([sys.executable,str(base/'build_cover.py'),tmp.name],check=True)
    s=Path(tmp.name).read_text()
def edit(a,b):
    global s
    assert s.count(a)==1, a
    s=s.replace(a,b)
edit('        const char *status = "DONE";','''        for (int ca=0;ca<ncell;ca++) for(int cb=ca;cb<ncell;cb++) {
        const char *status = "DONE";''')
edit('if (nunshared > 0 && !FORCE)', 'if (0)')
edit('''            QSet *Q0 = qnew();
            for (int c = 0; c < ncell; c++) { Poly S = square(CX[c], CY[c]); qpush(Q0, c, &S); }
            nl = 0;
            for (int c = 0; c < ncell; c++) {''','''            nl = 0;
            for (int c = 0; c < ncell; c++) {
                if(c!=ca && c!=cb)continue;
                int targetcell=c==ca?cb:ca;
                QSet *Q0=qnew(); Poly target=square(CX[targetcell],CY[targetcell]);
                qpush(Q0,targetcell,&target);''')
edit('''            }
            qrelease(Q0);
            int big''','''                qrelease(Q0);
            }
            int big''')
edit('''        for (int c = 0; c < ncell; c++) cellid[CX[c]][CY[c]] = -1;''','''        printf("CELLPAIR %lld %d %d\\n",rid,ca,cb);
        }
        for (int c = 0; c < ncell; c++) cellid[CX[c]][CY[c]] = -1;''')
Path(sys.argv[1]).write_text(s)
