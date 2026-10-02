import os, io, json, re, glob
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, '..', '..', 'drafts', '')
fn = json.load(io.open(os.path.join(HERE, 'fn_v2.json'), encoding='utf-8'))
used = []
for p in sorted(glob.glob(R + 'thesis_v2_part*.md')):
    t = io.open(p, encoding='utf-8').read()
    used += re.findall(r'\[\^([^\]]+)\]', t)
miss = [u for u in dict.fromkeys(used) if u not in fn]
extra = [k for k in fn if k not in used]
io.open(os.path.join(HERE, 'chk.txt'),'w',encoding='utf-8').write('USED %d UNIQ %d\nMISSING: %s\nUNUSED: %s' % (len(used), len(set(used)), ', '.join(miss), ', '.join(extra)))
