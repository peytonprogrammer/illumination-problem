#!/usr/bin/env bash
# D177 follow-up phase 2: room 2-300, the other 13 saved tile pairs (unfinished ones first), re-run with no piece cap
# (cap 10^9, so no direction can be skipped), then compare.py. Budget 600 CPU-s total.
# Census parameters for reference (qclass-closure/twenty/tiles.py): tile 18 1 6000, COVER_ALLDIRS=1.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd); cd "$here"
Q=../../../../qclass-closure/twenty
(cd "$Q" && shasum -a 256 -c data/SHA256SUMS)
mkdir -p work/twenty; tar xzf "$Q/data/twenty-wall.tar.gz" -C work/twenty hard/2-300
H=work/twenty/hard/2-300
cpu() { awk '/^user|^sys/{s+=$2} END{printf "%.1f", s}' "$1"; }
/usr/bin/time -p c++ -std=c++17 -O2 -o work/cert2pair cert2pair.cpp 2> work/t-b
used=$(cpu work/t-b); BUDGET=${BUDGET:-460}
: > followup2-cert2.log; : > followup2-compare.log; : > followup2-cpu.log
run() {  # tag cap a b maxcpu
    local tag=$1 cap=$2 a=$3 b=$4 lim=$5 st=0
    (ulimit -t $lim; /usr/bin/time -p timeout $((lim + 10)) ./work/cert2pair $H/room 0 18 $cap $a $b > work/f-$tag.txt) 2> work/t-$tag || st=$?
    local c; c=$(cpu work/t-$tag); used=$(awk -v u=$used -v c=$c 'BEGIN{print u + c}')
    { echo "# $tag pair $a $b cap $cap exit $st cpu $c"; grep -E '^(PAIR|DONE)' work/f-$tag.txt || true; } >> followup2-cert2.log
    if grep -q '^DONE' work/f-$tag.txt; then
        /usr/bin/time -p python3 -B compare.py $H/room work/f-$tag.txt $H/boxes "2-300 $tag" 2> work/tc-$tag | head -3 >> followup2-compare.log || true
        python3 -B nearest.py $H/room work/f-$tag.txt $a $b >> followup2-compare.log
        local cc; cc=$(cpu work/tc-$tag); used=$(awk -v u=$used -v c=$cc 'BEGIN{print u + c}')
        echo "$tag DONE cert2 $c compare $cc total $used" >> followup2-cpu.log
    else echo "$tag TIMEOUT/ERROR exit $st cert2 $c total $used" >> followup2-cpu.log; fi
}
for p in "8 28" "15 20" "15 27" "19 20" "19 27" "20 28" "27 28" "0 7" "0 8" "0 20" "0 27" "7 19" "7 28"; do
    set -- $p
    left=$(awk -v b=$BUDGET -v u=$used 'BEGIN{printf "%d", b - u - 10}')
    [ "$left" -gt 70 ] && left=70
    [ "$left" -lt 20 ] && { echo "nocap-$1-$2 NOT-RUN budget" >> followup2-cpu.log; continue; }
    run nocap-$1-$2 1000000000 $1 $2 $left
done
cat followup2-cpu.log
[ "${KEEP:-0}" = 1 ] || rm -rf work
