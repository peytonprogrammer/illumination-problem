#!/bin/sh
# usage: partA-run.sh NMAX NJ OUTDIR JSTART JEND [CYLB [GRIDMAX]]
# Runs jobs JSTART..JEND (of NJ) in parallel; each job is
#   partA-enum NMAX 22 NJ J - countsfile all | partA-cert 40 CYLB GRIDMAX - out sv rf
# A job is complete when its .out and .counts files end with "# DONE".
set -e
N=$1; NJ=$2; O=$3; JS=$4; JE=$5; CB=${6:-15:25}; GM=${7:-12}
cd "$(dirname "$0")"
mkdir -p "$O"
for J in $(seq "$JS" "$JE"); do
  ( ./partA-enum "$N" 22 "$NJ" "$J" - "$O/job-$J.counts" all \
      | ./partA-cert 40 "$CB" "$GM" - "$O/job-$J.out" "$O/job-$J.sv" "$O/job-$J.rf" ) 2> "$O/job-$J.err" &
done
wait
echo "jobs $JS-$JE finished $(date)" >> "$O/FINISHED"
