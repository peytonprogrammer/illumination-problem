#!/usr/bin/env bash
# D177: extend d107's shear-box residual check (cert2 B = 18, cap 20,000 + compare.py)
# to the named rooms d107 left undone, fewest saved boxes first, 4-49 skipped.
# Hard budget: 10 CPU-minutes total. Each cert2 run is wrapped in timeout and ulimit -t.
# Writes only under this directory. Set KEEP=1 to keep work/.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd); cd "$here"
Q=../../../../qclass-closure/twenty
(cd "$Q" && shasum -a 256 -c data/SHA256SUMS)
rm -rf work && mkdir -p work/twenty
tar xzf "$Q/data/twenty-wall.tar.gz" -C work/twenty
H=work/twenty/hard
cpu() { awk '/^user|^sys/{s+=$2} END{printf "%.1f", s}' "$1"; }
/usr/bin/time -p c++ -std=c++17 -O2 -o work/cert2 cert2.cpp 2> work/t-build
BUDGET=600; used=$(cpu work/t-build)
# Order: saved box count ascending, then name. 4-49 is skipped (d107: > 295 CPU-s).
rooms=$(for r in 1-244 2-300 4-244 5-252 6-213 6-219 7-234 7-241 8-220 8-239 8-240 9-240; do
    echo "$(wc -l < $H/$r/boxes) $r"; done | sort -k1,1n -k2,2 | awk '{print $2}')
: > compare.log; : > cert2.log; : > cpu.log
for r in $rooms; do
    left=$(awk -v b=$BUDGET -v u=$used 'BEGIN{printf "%d", b - u - 15}')
    if [ "$left" -lt 30 ]; then echo "$r NOT-RUN budget" >> cpu.log; continue; fi
    cap=$left; [ "$cap" -gt 200 ] && cap=200
    st=0
    (ulimit -t $cap; /usr/bin/time -p timeout $((cap + 10)) ./work/cert2 "$H/$r/room" 0 18 20000 > work/res-$r.txt) 2> work/t-$r || st=$?
    c=$(cpu work/t-$r); used=$(awk -v u=$used -v c=$c 'BEGIN{print u + c}')
    { echo "# $r cert2 exit $st cpu $c cap $cap"; grep -E '^(PAIR|DONE)' work/res-$r.txt || true; } >> cert2.log
    if [ "$st" = 0 ] && grep -q '^DONE' work/res-$r.txt; then
        /usr/bin/time -p python3 -B compare.py "$H/$r/room" work/res-$r.txt "$H/$r/boxes" $r >> compare.log 2> work/tc-$r
        cc=$(cpu work/tc-$r); used=$(awk -v u=$used -v c=$cc 'BEGIN{print u + c}')
        echo "$r DONE cert2 $c compare $cc total $used" >> cpu.log
    else
        echo "$r TIMEOUT/ERROR exit $st cert2 $c total $used" >> cpu.log
    fi
done
echo "4-49 NOT-RUN skipped by brief" >> cpu.log
# Timed-out rooms: compare only the tile pairs cert2 finished (PROD lines precede their PAIR line).
# compare.py crashes at its "unused" line when some box is never reached (d107 bug, after the
# uncovered count is printed), hence "|| true". nearest.py names each product's nearest corner pair.
: > partial.log; : > nearest.log
for r in $rooms; do
    grep -q "^$r TIMEOUT" cpu.log || continue
    n=$(grep -n "^PAIR " work/res-$r.txt | tail -1 | cut -d: -f1); head -n "$n" work/res-$r.txt > work/part-$r.txt
    python3 -B compare.py "$H/$r/room" work/part-$r.txt "$H/$r/boxes" $r-partial >> partial.log 2>/dev/null || true
    grep -E '^PAIR' work/part-$r.txt | awk '$5 > 0 {print $2, $3}' | while read a b; do
        grep -E "^(PROD|PAIR) $a $b " work/part-$r.txt > work/pp.txt
        python3 -B compare.py "$H/$r/room" work/pp.txt "$H/$r/boxes" "$r pair $a $b" 2>/dev/null | head -1 >> partial.log || true
        python3 -B nearest.py "$H/$r/room" work/part-$r.txt $a $b 3000 >> nearest.log
    done
done
grep RESULT compare.log || true
cat cpu.log
[ "${KEEP:-0}" = 1 ] || rm -rf work
