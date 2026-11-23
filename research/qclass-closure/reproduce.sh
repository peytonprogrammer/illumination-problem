#!/usr/bin/env bash
# Run in a fresh directory. Pass its path as the sole argument.
set -euo pipefail
src=$(cd "$(dirname "$0")" && pwd)
project="$src/../illumination-generalization-2026-11-06/fable/directions-2026-11-09"
mkdir "${1:?supply a new output directory}"
cd "$1"
export LC_ALL=C
c++ -std=c++17 -O3 "$src/enumerate.cpp" -o enum
cc -O3 "$src/independent.c" -o independent
c++ -std=c++17 -O3 "$src/compare_fixed.cpp" -o compare
patch -o all_pairs.c "$project/d9-census-w22/shoot.c" < "$src/all-pairs.patch"
patch -o brute.c "$project/d67-review-d64/polyo.c" < "$src/brute-check.patch"
cc -O3 all_pairs.c "$project/d9-census-w22/verify_plane.c" -o shoot
cc -O3 brute.c -o brute
for phase in 0 1 2 3; do
    ./enum 8 1 "$phase" "rooms-$phase" 2>"phase-$phase.log"
    ./independent "$phase" >"ind-$phase.tsv" 2>"ind-$phase.log"
done
sort -u rooms-{0,1,2,3} >rooms
./compare <rooms >compare.log
./brute 15 > brute15.log
./shoot 12 36 rooms first survivors
awk '!seen[$1]++ {printf "%d %d",$2,$3; for(i=13;i<=NF;i++)printf " %d",$i; print ""}' survivors >retry
./shoot 60 36 retry second survivors60
test ! -s survivors60
grep -qx '# verify_fail 0' first
grep -qx '# verify_fail 0' second
gzip -nc first >witnesses.txt.gz
gzip -nc second >witnesses-retry.txt.gz
python3 "$src/audit.py" . >audit.log
python3 "$src/covers_input.py" >covers
./shoot 45 40 covers covers-certs covers-survivors
test ! -s covers-survivors
grep -qx '# verify_fail 0' covers-certs
gzip -nc covers-certs >witnesses-covers.txt.gz
./shoot 60 36 "$src/r22-control.room" control.log control-survivor
test "$(wc -l <control-survivor)" -eq 1
cat audit.log compare.log
