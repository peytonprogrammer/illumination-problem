#!/bin/zsh
# Run one k=4 placement per line of queue-k4.txt, 5 at a time; each log ends with "exit N".
cd ${0:a:h}
cat queue-k4.txt | xargs -P 5 -I{} zsh -c '/opt/homebrew/bin/pypy3.11 -B claude_k_enum_fast.py 4 23 38 3 L{} {} > log-k4-L{}.txt 2>&1; echo exit $? >> log-k4-L{}.txt'
