import subprocess,sys,tempfile
from pathlib import Path
base=Path(__file__).resolve().parent
with tempfile.NamedTemporaryFile() as f:
    subprocess.run([sys.executable,str(base/'build_cover.py'),f.name],check=True);s=Path(f.name).read_text()
a=s.index('                for (int t = 0; t < nl; t++) {',s.index('            int big = 0;'))
s=s[:a]+s[a:].replace('                    qrelease(L->Q);','''                    if(nnl>MAXLIVE*2){break;}''',1)
a=s.index('                Live *tmp = live;')
b=s.index('                if (changed)',a)
s=s[:a]+'''                if(nnl>MAXLIVE*2){
                    for(int j=0;j<nnl;j++)qrelease(nlive[j].Q);
                    continue;
                }
                int oldn=nl;
                Live *tmp=live;live=nlive;nlive=tmp;
                int tc=capl;capl=capnl;capnl=tc;
                nl=nnl;
                if(nl)prune_reverse();
                if(nl>MAXLIVE || (oldn>300 && nl>3*oldn)){
                    for(int j=0;j<nl;j++)qrelease(live[j].Q);
                    tmp=live;live=nlive;nlive=tmp;
                    tc=capl;capl=capnl;capnl=tc;nl=oldn;
                    continue;
                }
                for(int j=0;j<oldn;j++)qrelease(nlive[j].Q);
'''+s[b:]
Path(sys.argv[1]).write_text(s)
