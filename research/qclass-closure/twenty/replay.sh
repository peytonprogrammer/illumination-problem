#!/usr/bin/env bash
set -euo pipefail
base=$(cd "$(dirname "$0")" && pwd)
mkdir "${1:?provide a new output directory}"
work=$(cd "$1" && pwd)
export COVER_ALLDIRS=1 LC_ALL=C PYTHONDONTWRITEBYTECODE=1
src=$(echo "$base"/../../illumination-generalization*/fable/directions*/d13-cylinder-cover/cover.c)
python3 - "$base/../enumerate.cpp" "$work/enum.cpp" <<'PY'
from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
a='||counts[0]+counts[1]+counts[2]+counts[3]<2'
assert s.count(a)==1
Path(sys.argv[2]).write_text(s.replace(a,''))
PY
c++ -std=c++17 -O3 "$work/enum.cpp" -o "$work/enum"
python3 "$base/independent.py" "$work/ind.c"
cc -O3 "$work/ind.c" -o "$work/ind"
for k in 0 1 2 3; do
    "$work/enum" 8 1 "$k" "$work/phase$k" 2>"$work/phase$k.log"
    "$work/ind" "$k" >"$work/ind-$k.tsv" 2>"$work/ind-$k.log"
done
sort -u "$work"/phase[0-3] | awk '$2==20' > "$work/rooms"
c++ -O3 -std=c++17 "$base/../compare_fixed.cpp" -o "$work/compare"
(cd "$work" && ./compare <rooms >compared)
awk -v d="$work" '{print > (d "/i" ((NR-1)%10))}' "$work/rooms"
cc -O3 "$src" -o "$work/stock"
python3 "$base/build.py" "$work"
python3 "$base/shear_build.py" "$work"
for k in {0..9}; do "$work/stock" 5 0 4000 <"$work/i$k" >"$work/a$k" & done
wait
python3 "$base/passes.py" "$work"
python3 "$base/tiles.py" "$work"
python3 "$base/gridbuild.py" "$work"
python3 "$base/raybuild.py" "$work"
python3 "$base/receipts.py" "$work"
python3 "$base/check_missing.py" "$work"
python3 "$base/audit.py" "$work"
