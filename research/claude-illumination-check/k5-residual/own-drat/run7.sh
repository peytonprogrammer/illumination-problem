#!/bin/zsh
for d in certified/I2_1_1-pair0 cases/I2_2_0-pair0 cases/I2_2_1-pair0 cases/I2_3_0-pair0 cases/I2_2_2-pair0 cases/I2_3_1-pair0 cases/I2_3_2-pair0; do
  t=${d:t}
  ( h1=$(shasum -a 256 ../../../illumination-k4-codex/k5-proof-continuation/$d/formula.cnf | cut -c1-64); h2=$(shasum -a 256 ../../../illumination-k4-codex/k5-proof-continuation/$d/proof.drat | cut -c1-64)
    s=$(date +%s); ./drat-trim ../../../illumination-k4-codex/k5-proof-continuation/$d/formula.cnf ../../../illumination-k4-codex/k5-proof-continuation/$d/proof.drat -t 20000 > $t.log 2>&1; e=$?
    echo "$t exit=$e $(grep -a -o 's [A-Z-]*VERIFIED\|s NOT VERIFIED' $t.log | head -1) secs=$(($(date +%s)-s)) cnf=$h1 drat=$h2" >> results.txt ) &
done
wait; echo ALLDONE >> results.txt
