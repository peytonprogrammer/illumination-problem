#!/usr/bin/env bash
# d100: independent residual recomputation for the two 18-wall rooms, plus large-K samples.
# Writes only under this directory. Set KEEP=1 to keep work/ (about 25 MB).
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
two18="$here/../../../../qclass-closure/two18"
mkdir -p "$here/work"
cd "$here"
c++ -std=c++17 -O2 -fsanitize=undefined -fno-sanitize-recover=all -o work/cert2 cert2.cpp
cmp rooms.txt "$two18/rooms"
# 1. d100's own residual (d74 core + d100 two-sided tile-pair driver), B = 18.
for r in 0 1; do
    ./work/cert2 rooms.txt $r 18 20000 > work/res_r$r.txt
    grep -v '^PROD' work/res_r$r.txt > cert2_r$r.log
done
# 2. The census residual to compare against (author's census code, as in d90's run.sh).
(cd work && python3 -B "$two18/localize.py" "$here/work" && cc -O2 localize.c -o localize \
    && COVER_ALLDIRS=1 ./localize 18 1 6000 < rooms > regions.txt)
python3 -B compare.py work/res_r0.txt work/res_r1.txt work/regions.txt 300 | tee compare.log
# 3. Large-K pairs from inside the d100 residual, traced along the certificate path.
python3 -B sample_k.py work/res_r0.txt work/res_r1.txt work/regions.txt 100 | tee sample_k.log
[ "${KEEP:-0}" = 1 ] || rm -rf work
