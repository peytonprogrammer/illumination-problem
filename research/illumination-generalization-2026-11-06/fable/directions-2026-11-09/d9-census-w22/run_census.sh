#!/bin/sh
# usage: run_census.sh NMAX NJ BOUND CERTMAX OUTDIR JSTART JEND
# Runs jobs JSTART..JEND (of NJ) in parallel; each job is
#   enum_rooms NMAX 22 NJ J - countsfile | shoot BOUND CERTMAX - outfile survivorfile
# A job is complete when its .out and .counts files end with "# DONE".
set -e
N=$1; NJ=$2; B=$3; CM=$4; O=$5; JS=$6; JE=$7
cd "$(dirname "$0")"
mkdir -p "$O"
for J in $(seq "$JS" "$JE"); do
  ( ./enum_rooms "$N" 22 "$NJ" "$J" - "$O/job-$J.counts" \
      | ./shoot "$B" "$CM" - "$O/job-$J.out" "$O/job-$J.sv" ) 2> "$O/job-$J.err" &
done
wait
echo "jobs $JS-$JE finished $(date)" >> "$O/FINISHED"
