from pathlib import Path
import sys
base=Path(__file__).resolve().parent
source=next(base.parents[1].glob('illumination-generalization*/fable/directions*/d13-cylinder-cover/cover.c')).read_text()
def add(needle,change):
    global source
    assert source.count(needle)==1
    source=source.replace(needle,change)
add('int ref; int n, cap; QP *a;', 'int ref; int n, cap; QP *a; int epoch; unsigned long long mask[(9*MAXCELL+63)/64];')
add('int main(int argc', (base/'reverse.inc').read_text()+'\nint main(int argc')
add('        /* ---- pole test ---- */','        init_buckets();\n'+(base/'order.inc').read_text()+'\n        /* ---- pole test ---- */')
add('                nl = nnl;', '                nl = nnl;\n                if(nl)prune_reverse();')
Path(sys.argv[1]).write_text(source)
