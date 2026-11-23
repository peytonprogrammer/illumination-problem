#!/bin/sh
# usage: sh enum/run_enum.sh NMAX OUTDIR
# Re-lists the class (iii) rooms with area <= NMAX, W <= 22 (normalized, as in
# Part A) with the copied Part A enumerator and classifier, in classify-only
# mode: no shooting, C3 lines written up to area NMAX, reduced rooms as RED.
# 4 parallel jobs.
set -e
N=$1; O=$2
D=$(dirname "$0")
mkdir -p "$O"
for J in 0 1 2 3; do
  ( "$D/partA-enum" "$N" 22 4 "$J" - "$O/job-$J.counts" all \
      | PARTA_CLASSIFY_ONLY=1 PARTA_RFMAX="$N" "$D/partA-cert" 40 15:25 0 - "$O/job-$J.out" "$O/job-$J.sv" "$O/job-$J.rf" ) 2> "$O/job-$J.err" &
done
wait
