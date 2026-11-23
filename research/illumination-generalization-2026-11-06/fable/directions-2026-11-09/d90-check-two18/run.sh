#!/usr/bin/env bash
# D90 independent check of qclass-closure/two18. Writes only under this directory.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
two18="$here/../../../../qclass-closure/two18"
mkdir -p "$here/work"
cd "$here/work"
# Residual regions come from the census code (localize.py + build_pairskip.py); this
# is the accepted census input. Everything after this line is D90's own code.
python3 -B "$two18/localize.py" "$here/work"
cmp "$two18/rooms" rooms
cc -O2 localize.c -o localize
COVER_ALLDIRS=1 ./localize 18 1 6000 < rooms > regions.txt
cd "$here"
python3 -B check.py work/regions.txt 200 40
python3 -B mutate.py work/regions.txt | tail -1
