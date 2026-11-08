#!/bin/zsh
# Run one k=4 placement per line of queue-k4-w21.txt, 8 at a time; each log ends with "exit N".
cd ${0:a:h}
cat queue-k4-w21.txt | xargs -P 8 -I{} zsh -c '/opt/homebrew/bin/pypy3.11 -B claude_k_enum_fast.py 4 21 38 3 L{} {} > log-k4w21-L{}.txt 2>&1; echo exit $? >> log-k4w21-L{}.txt'
