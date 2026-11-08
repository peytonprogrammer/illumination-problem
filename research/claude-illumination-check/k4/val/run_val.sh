#!/bin/zsh
# Old (stubbed OR-Tools, unused) vs fast enumerator on small instances; compare room sets.
cd ${0:a:h}
for a in "2 20 21 2" "3 18 20 2" "4 18 20 2"; do
  set -- ${=a}
  PYTHONPATH=../stub:../../tokarsky-n /opt/homebrew/bin/pypy3.11 -B claude_k_enumerate.py ${=a} > old-$1-$2.log 2>&1
  /opt/homebrew/bin/pypy3.11 -B claude_k_enum_fast.py ${=a} new > new-$1-$2.log 2>&1
  python3 -c "
import json
rd=lambda f:{json.dumps(json.loads(l)['triangles']) for l in open(f)}
o=rd('claude-k$1-w$2-rooms.jsonl'); n=rd('claude-k$1-w$2-rooms-new.jsonl')
print('k=$1 w=$2 old',len(o),'new',len(n),'EQUAL' if o==n else 'DIFFER')"
done
echo exit
