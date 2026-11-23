#!/bin/sh
# usage: run_filter.sh ROOM_INDEX B [DEADSAMPLE_FILE]   (run from this directory)
# Runs dpcover on one room of runs/rooms12.txt and pipes its live cells into orbitfilter.py.
n=$1; B=$2; dead=$3
mkdir -p runs/b$B
sed -n ${n}p runs/rooms12.txt | DP_LIVE=1 ./dpcover $B 1 100000000 2>&1 >/dev/null \
  | python3 orbitfilter.py runs/rooms12.txt $n $dead > runs/b$B/room${n}_candidates.txt
