# -*- coding: utf-8 -*-
"""part1~5를 합치고 각주 본문을 붙인 뒤 작성 원칙을 점검한다."""
import os, io, json, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, '..', '..', 'drafts', '')
FN = json.load(io.open(os.path.join(HERE, 'fn_v2.json'), encoding='utf-8'))

parts = []
for i in range(1, 6):
    parts.append(io.open(R + 'thesis_v2_part%d.md' % i, encoding='utf-8').read().strip())
body = '\n\n'.join(parts)

# 각주 정의를 끝에 붙인다 (본문 등장 순서)
order = []
for m in re.finditer(r'\[\^([^\]]+)\]', body):
    if m.group(1) not in order:
        order.append(m.group(1))
defs = '\n\n'.join('[^%s]: %s' % (k, FN[k]) for k in order)
full = body + '\n\n' + defs + '\n'
io.open(R + 'thesis_v2.md', 'w', encoding='utf-8').write(full)

# ── 점검 ────────────────────────────────────────────────
rep = []
# 본문만 뽑는다: 각주 정의·참고문헌·표(| 로 시작)·출전 줄을 뺀다
lines = body.split('\n')
btxt = []
inbib = False
for ln in lines:
    if ln.startswith('# 참고문헌'):
        inbib = True
    if inbib or ln.startswith('|') or ln.startswith('출전:') or ln.startswith('〈'):
        continue
    btxt.append(ln)
btxt = '\n'.join(btxt)
# 각주 참조 마커는 지운다
btxt_nofn = re.sub(r'\[\^[^\]]+\]', '', btxt)

rep.append('본문 글자수(공백 제외): %d' % len(re.sub(r'\s', '', btxt_nofn)))
rep.append('굵은 글씨: %d' % len(re.findall(r'\*\*', btxt)))
rep.append('본문 줄표(—): %d' % btxt_nofn.count('—'))
hanja = re.findall(r'[\u4e00-\u9fff]', btxt_nofn)
rep.append('본문 한자: %d (%s)' % (len(hanja), ''.join(sorted(set(hanja)))[:60]))
rep.append('본문 물결표 서지: %d' % len(re.findall(r'\d쪽', btxt_nofn)))

# 각주 짝
used = set(re.findall(r'\[\^([^\]]+)\]', body))
rep.append('각주 참조 %d종 / 정의 %d종 / 미정의 %s' % (len(used), len(order), sorted(used - set(FN))))

# 제목 점검
titles = re.findall(r'^#{1,2} (.+)$', body, re.M)
bad = [x for x in titles if (',' in x or '그리고' in x)]
rep.append('제목 쉼표·그리고: %s' % (bad or '없음'))
for x in titles:
    if x.startswith('제') and ('장' in x[:4] or '절' in x[:4]):
        rep.append('  %2d자  %s' % (len(x.split(' ', 1)[-1]), x))

# 분량 비율
def seg(a, b=None):
    i = body.index(a)
    j = body.index(b) if b else len(body)
    s = body[i:j]
    s = re.sub(r'\[\^[^\]]+\]', '', s)
    return len(re.sub(r'\s', '', s))

rep.append('머리말 %d자 / 장별 %d자 / 맺음말 %d자' % (
    seg('# 머리말', '# 제1장'), seg('# 제1장', '# 맺음말'), seg('# 맺음말', '# 참고문헌')))
rep.append('머리말/장별 = %.1f%%' % (100.0 * seg('# 머리말', '# 제1장') / seg('# 제1장', '# 맺음말')))

io.open(os.path.join(HERE, 'assemble_out.txt'), 'w', encoding='utf-8').write('\n'.join(rep))
