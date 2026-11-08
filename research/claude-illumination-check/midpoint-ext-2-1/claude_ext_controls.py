"""Positive controls for the composed claim: types 4 and 11 are nonempty without cuts."""
import json
import sys
sys.argv = sys.argv[:1]
sys.modules['__main_guard__'] = None
src = open(__file__.replace('claude_ext_controls.py', 'claude_extension_check.py')).read()
exec(compile(src.split('out = dict(guard_failures=[])')[0].replace('Path(__file__)', 'Path(%r)' % __file__), 'check', 'exec'))
o = {}
for n in (4, 11):
    run(f'type{n}_no_cuts', o, patterns[n], [])
