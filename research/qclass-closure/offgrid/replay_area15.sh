#!/usr/bin/env bash
# Recompute all continuum stages starting from the independently checked census.
set -eu -o pipefail
base=$(cd "$(dirname "$0")" && pwd)
src=$(echo "$base"/../../illumination-generalization*/fable/directions*/d13-cylinder-cover/cover.c)
mkdir "${1:?supply a fresh directory}"
cd "$1"
export COVER_ALLDIRS=1
gzip -dc "$base/results/og15rooms.gz" > rooms
cc -O3 "$src" -o stock
for type in cover skip pairskip; do
    python3 "$base/build_$type.py" "$type.c"
    cc -O3 "$type.c" -o "$type"
done
unresolved() {
    awk -F' *[|] *' '{split($1,a," "); if(a[5]!="DONE" || a[13]!=0)print a[3],a[4],$2}' "$1"
}
./stock 6 0 8000 < rooms > first
unresolved first > second-in
./cover 12 0 35000 < second-in > second
unresolved second > third-in
./skip 18 0 7000 < third-in > third
unresolved third > final-in
./pairskip 18 1 6000 < final-in > final
awk '/^ROOM/{if($5!="DONE" || $13!=0)exit 1; n++}END{print n,"tile pairs checked"}' final
wc -l rooms second-in third-in final-in
