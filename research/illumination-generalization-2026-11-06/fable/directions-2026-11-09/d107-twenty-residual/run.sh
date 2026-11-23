#!/usr/bin/env bash
# D107: residual boxes and bin-pair certificates at 20 walls (review queue Q50).
# Writes only under this directory. About 4 CPU-minutes. Set KEEP=1 to keep work/.
# Room 4-49 is left out: cert2 needed more than 295 CPU-s on it (see README).
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd); cd "$here"
Q=../../../../qclass-closure/twenty
(cd "$Q" && shasum -a 256 -c data/SHA256SUMS)
rm -rf work && mkdir -p work/twenty work/near
tar xzf "$Q/data/twenty-wall.tar.gz" -C work/twenty
H=work/twenty/hard
c++ -std=c++17 -O2 -o work/cert2 cert2.cpp
g++ -O2 -std=c++17 -o work/labchk labchk.cpp
g++ -O2 -std=c++17 -o work/leafchk ../d103-twenty-check/leafchk.cpp
# 1. Own residual (d100 cert2, B = 18) for 11 shear-box rooms, then compare with the saved boxes.
: > compare.log
for r in 0-10 0-32 1-170 1-47 2-269 9-41 8-243 7-244 7-242 6-12 7-15; do
    (ulimit -t 120; ./work/cert2 "$H/$r/room" 0 18 20000 > work/res-$r.txt)
    python3 -B compare.py "$H/$r/room" work/res-$r.txt "$H/$r/boxes" $r >> compare.log
done
grep RESULT compare.log
# 2. Bin-pair rooms: replay every receipt, check labels, near-corner trees, and 7-230's bin coverage.
for r in 7-230 2-266 5-0; do
    python3 -B pixchk.py "$H/$r" work/q-$r.txt work/near/n-$r
    ./work/labchk < work/q-$r.txt
done > pixchk.log
python3 -B ../d103-twenty-check/shear_check.py work/near work/near-leaves.txt
./work/leafchk < work/near-leaves.txt | tail -1 >> pixchk.log
(ulimit -t 60; ./work/cert2 "$H/7-230/room" 0 18 20000 > work/res-7-230.txt)
python3 -B bincov.py "$H/7-230/room" work/res-7-230.txt "$H/7-230/pixel/grid" 7-230 >> pixchk.log
cat pixchk.log
# 3. Negative controls (each must fail).
{
    echo "# 1. residual control: 0-32 boxes shrunk to r = 3856"
    awk '{$5=3856; print}' "$H/0-32/boxes" > work/boxes-0-32-shrunk
    python3 -B compare.py "$H/0-32/room" work/res-0-32.txt work/boxes-0-32-shrunk 0-32-shrunk-control || true
    echo "# 2. label control, 7-230 receipts with j -> j+1 in every L and K leaf"
    python3 -B pixchk.py "$H/7-230" work/qm-7-230.txt work/near/m-7-230 --mutate > /dev/null
    ./work/labchk < work/qm-7-230.txt | tail -1
    echo "# 3. label control, 5-0 near-corner trees with j -> j+1 (D103 --mutate)"
    python3 -B ../d103-twenty-check/shear_check.py work/near work/near-mut.txt --mutate 2> /dev/null
    ./work/leafchk < work/near-mut.txt | tail -1
} > control.log
[ "${KEEP:-0}" = 1 ] || rm -rf work
