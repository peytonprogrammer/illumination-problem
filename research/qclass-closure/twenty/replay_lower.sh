#!/usr/bin/env bash
set -euo pipefail
base=$(cd "$(dirname "$0")" && pwd)
mkdir "${1:?provide a new directory}"
work=$(cd "$1" && pwd)
export COVER_ALLDIRS=1 PYTHONDONTWRITEBYTECODE=1 LC_ALL=C
python3 - "$base/.." "$work" <<'PY'
from pathlib import Path
import sys
base,work=map(Path,sys.argv[1:])
s=(base/'enumerate.cpp').read_text()
key='||counts[0]+counts[1]+counts[2]+counts[3]<2'
assert s.count(key)==1
(work/'enum.cpp').write_text(s.replace(key,''))
s=(base/'independent.c').read_text().replace('marks>=2 && ','').replace('rlo>8||vlo>12||bad||count>36','rlo>6||vlo>10||bad||count>28')
(work/'ind.c').write_text(s)
PY
c++ -std=c++17 -O3 "$work/enum.cpp" -o "$work/enum"
cc -O3 "$work/ind.c" -o "$work/ind"
for k in 0 1 2 3; do
    "$work/enum" 6 1 "$k" "$work/phase$k" 2>"$work/phase$k.log"
    "$work/ind" "$k" >"$work/ind-$k.tsv" 2>"$work/ind-$k.log"
done
sort -u "$work"/phase[0-3] >"$work/rooms"
c++ -std=c++17 -O3 "$base/../compare_fixed.cpp" -o "$work/compare"
(cd "$work" && ./compare <rooms)
awk -v d="$work" '{print > (d "/i" ((NR-1)%2))}' "$work/rooms"
cc -O3 $(echo "$base"/../../illumination-generalization*/fable/directions*/d13-cylinder-cover/cover.c) -o "$work/stock"
python3 "$base/build.py" "$work"
python3 "$base/shear_build.py" "$work"
for k in 0 1; do "$work/stock" 5 0 4000 <"$work/i$k" >"$work/a$k" & done
wait
python3 "$base/passes.py" "$work"
python3 "$base/tiles.py" "$work"
python3 "$base/check_missing.py" "$work"
python3 "$base/audit.py" "$work" --lower
