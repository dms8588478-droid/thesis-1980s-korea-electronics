# -*- coding: utf-8 -*-
"""빌드한 HWP를 열어 각주 수와 표와 고친 자리를 확인한다."""
import hwptxt, re, sys, io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = r'C:/Users/user/OneDrive/바탕 화면/1980년대 전자공업/261000 최낙은 발표문 _new.hwp'
t = hwptxt.extract(P)
d = json.load(io.open(os.path.join(HERE, 'fn_v2.json'), encoding='utf-8'))
miss = [k for k, v in d.items() if v[:26].replace('`', '') not in t]
print('글자수', len(re.sub(r'\s', '', t)))
print('백틱', t.count('`'), '/ 굵은 글씨', t.count('**'))
print('표', len(set(re.findall(r'표 [1-9]〉', t))), '종')
print('각주 %d개 중 본문에 없는 것: %s' % (len(d), miss or '없음'))
for k in ['기만적 이중장부', '뒷받침한 세력', '인문논총』 78-3', '위의 협약서 제9조',
          '조합이 발족하던 1986년 4월', '삼성반도체통신과 현대전자산업 셋을']:
    print(('OK  ' if k in t else 'MISS ') + k)
TITLE = io.open(os.path.join(HERE, 'title.txt'), encoding='utf-8').read().strip()
head = t.strip()[:200]
print(('OK  ' if head.startswith(TITLE[:20]) else 'MISS ') + '첫 줄이 제목이다: ' + head[:40].replace(chr(10), ' '))
