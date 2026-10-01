# -*- coding: utf-8 -*-
"""발표문 판을 만든다: 제목을 붙이고 국문초록·표 목차·참고문헌을 뺀다."""
import os, io, re

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, '..', '..', 'drafts', '')
t = io.open(R + 'thesis_v2.md', encoding='utf-8').read()

m = re.search(r'^\[\^', t, re.M)
body, defs = t[:m.start()], t[m.start():]


def cut(head, txt):
    i = txt.index(head)
    j = txt.index('\n# ', i + 1)
    return txt[:i] + txt[j + 1:]


body = cut('# 국문초록', body)
body = cut('# 표 목차', body)
body = body[:body.index('# 참고문헌')]

# 목차에서 표 목차와 참고문헌 줄을 뺀다
body = body.replace('표 목차\n\n', '')
body = body.replace('맺음말\n\n참고문헌\n', '맺음말\n')
body = re.sub(r'^(?:---\n\n)+', '', body)

TITLE = io.open(os.path.join(HERE, 'title.txt'), encoding='utf-8').read().strip()
# 2026-10-01: title.txt가 다른 스크립트에 덮어써져 9월 30일부터 발표문 첫머리에 분석 결과가 들어갔다.
assert chr(10) not in TITLE and len(TITLE) < 120 and '중심으로' in TITLE, '제목 파일이 제목이 아니다: ' + TITLE[:40]
body = '# ' + TITLE + '\n\n최낙은(고려대학교 대학원 한국사학과)\n\n' + body

used = set(re.findall(r'\[\^([^\]]+)\]', body))
keep = ['[^%s]: %s' % b for b in re.findall(r'^\[\^([^\]]+)\]: (.*)$', defs, re.M) if b[0] in used]
io.open(R + 'thesis_v2_presentation.md', 'w', encoding='utf-8').write(
    body.rstrip() + '\n\n' + '\n\n'.join(keep) + '\n')

bodytxt = re.sub(r'\[\^[^\]]+\]', '', body)
print('본문 %d자 / 각주 %d개' % (len(re.sub(r'\s', '', bodytxt)), len(keep)))
print('%s' % ('참고문헌' in body.split('# 머리말')[0] and '목차에 참고문헌 남음' or '목차 정리됨'))
