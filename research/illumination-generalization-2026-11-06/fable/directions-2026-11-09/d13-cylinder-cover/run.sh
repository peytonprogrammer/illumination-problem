#!/bin/sh
# usage: sh run.sh ROOMS OUT B [FORCE] [MAXLIVE]
# Splits ROOMS round-robin into 4 parts, runs ./cover on each in parallel,
# and concatenates the ROOM lines into OUT.
set -e
ROOMS=$1; OUT=$2; B=$3; FORCE=${4:-0}; MAXLIVE=${5:-300000}
TMP=${TMPDIR:-/tmp}/d13run.$$
mkdir -p "$TMP"
for i in 0 1 2 3; do
  awk -v i=$i 'NR % 4 == i' "$ROOMS" > "$TMP/part$i"
  ./cover "$B" "$FORCE" "$MAXLIVE" < "$TMP/part$i" > "$TMP/out$i" &
done
wait
cat "$TMP"/out0 "$TMP"/out1 "$TMP"/out2 "$TMP"/out3 > "$OUT"
rm -r "$TMP"
