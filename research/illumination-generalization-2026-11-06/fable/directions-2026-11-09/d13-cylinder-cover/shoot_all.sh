#!/bin/sh
# usage: sh shoot_all.sh PAIRS OUT R   -- 4 parallel shoot.py workers
set -e
P=$1; OUT=$2; R=$3
TMP=${TMPDIR:-/tmp}/d13shoot.$$
mkdir -p "$TMP"
for i in 0 1 2 3; do
  awk -v i=$i 'NR % 4 == i' "$P" > "$TMP/part$i"
  python3 shoot.py "$R" < "$TMP/part$i" > "$TMP/out$i" &
done
wait
cat "$TMP"/out0 "$TMP"/out1 "$TMP"/out2 "$TMP"/out3 > "$OUT"
rm -r "$TMP"
