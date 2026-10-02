# -*- coding: utf-8 -*-
"""thesis_v2.md를 HWP COM이 실행할 연산 목록으로 바꾼다.
연산: H1/H2/H3(제목), S(글), F(각주), P(문단 끝), TB(표 시작 r c), TC(칸), TE(표 끝)"""
import os, io, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, '..', '..', 'drafts', '')
src = io.open(R + 'thesis_v2_presentation.md', encoding='utf-8').read()

# 각주 정의를 걷어 낸다
fns = {}
def grab(m):
    fns[m.group(1)] = m.group(2).strip()
    return ''
src = re.sub(r'^\[\^([^\]]+)\]: (.*)$', grab, src, flags=re.M)

ops = []
blocks = [b.strip() for b in src.split('\n\n')]
i = 0
while i < len(blocks):
    b = blocks[i]
    i += 1
    if not b or b == '---':
        continue
    # 표
    if b.startswith('|'):
        rows = [r for r in b.split('\n') if r.strip().startswith('|')]
        rows = [r for r in rows if not re.match(r'^\|[\s:\-|]+\|$', r.strip())]
        cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
        ncol = max(len(r) for r in cells)
        ops.append(('TB', '%d %d' % (len(cells), ncol)))
        for r in cells:
            r = r + [''] * (ncol - len(r))
            for c in r:
                ops.append(('TC', c))
        ops.append(('TE', ''))
        continue
    m = re.match(r'^(#{1,3}) (.+)$', b)
    if m:
        ops.append(('H%d' % len(m.group(1)), m.group(2).strip()))
        continue
    # 본문 문단: 각주 참조를 잘라 낸다
    text = b.replace('\n', ' ')
    pos = 0
    for mm in re.finditer(r'\[\^([^\]]+)\]', text):
        seg = text[pos:mm.start()]
        if seg:
            ops.append(('S', seg))
        ops.append(('F', fns.get(mm.group(1), '')))
        pos = mm.end()
    tail = text[pos:]
    if tail:
        ops.append(('S', tail))
    ops.append(('P', ''))

out = '\n'.join('%s\t%s' % (k, v.replace('\t', ' ').replace('`', '')) for k, v in ops)
io.open(os.path.join(HERE, 'ops.txt'), 'w', encoding='utf-8').write(out)
print('ops', len(ops), 'fns', len(fns))
