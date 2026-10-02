# 발표문 빌드 — 논문 초고 v2를 한글 문서로 만든다

**2026-10-01에 세션 임시 폴더에서 저장소로 옮겼다.** 그 전에는 빌드 스크립트와 각주 저장소(`fn_v2.json`)와 제목 파일이 임시 폴더에만 있었고, **제목 파일이 다른 분석 스크립트의 출력에 덮어써져 2026-09-30 19:49 커밋(`7ca3a95`)부터 10월 1일 10:32 빌드까지 발표문 첫머리에 제목 대신 학맥 논문 장절 제목 분석 결과 마흔두 줄이 들어가 있었다.** `mkpres.py`와 `verify_hwp.py`에 제목 점검을 넣었다.

| 파일 | 하는 일 |
|---|---|
| `fn_v2.json` | **각주 저장소.** 원고(`drafts/thesis_v2_part1~5.md`)에는 `[^키]`만 있고 각주 본문은 여기에 있다. 각주를 고치면 여기를 고친다 |
| `title.txt` | 발표문 제목 한 줄. **최종 제목은 지도교수 결정 사항** |
| `chk.py` | 원고의 각주 키와 `fn_v2.json`의 짝을 맞춘다 → `chk.txt` |
| `assemble.py` | part1~5를 합치고 각주 본문을 붙여 `drafts/thesis_v2.md`를 만들고 작성 원칙을 점검한다 → `assemble_out.txt` |
| `mkpres.py` | 발표문 판 `drafts/thesis_v2_presentation.md`를 만든다(제목을 붙이고 국문초록·표 목차·참고문헌을 뺀다) |
| `mkops.py` | 발표문을 한글 COM이 실행할 연산 목록 `ops.txt`로 바꾼다 |
| `build_hwp.ps1` | 한글 COM으로 `261000 최낙은 발표문 _new.hwp`를 만든다. **BOM이 있는 UTF-8이어야 한다**(Windows PowerShell 5.1) |
| `verify_hwp.py` | 만든 한글 문서에서 각주·표·백틱·굵은 글씨·첫 줄 제목을 확인한다. `hwptxt.py`가 한글 문서의 본문을 뽑는다(`olefile` 필요) |

## 차례

```bash
PY=/c/Users/user/AppData/Local/Python/pythoncore-3.14-64/python.exe
cd tools/build_v2
PYTHONIOENCODING=utf-8 $PY chk.py && cat chk.txt
PYTHONIOENCODING=utf-8 $PY assemble.py && cat assemble_out.txt
PYTHONIOENCODING=utf-8 $PY mkpres.py
PYTHONIOENCODING=utf-8 $PY mkops.py
```

그다음 PowerShell에서 `build_hwp.ps1`을 **배경으로** 돌린다(약 13분). 끝나면 `verify_hwp.py`로 확인하고, 문제가 없으면 `_new.hwp`를 `261000 최낙은 발표문.hwp`로 바꾼다.

> **창이 보이는 한글 프로세스는 죽이지 않는다.** 빌드가 대화상자에서 멈추면 PowerShell 작업만 멈추고 사용자에게 창을 닫아 달라고 한다. `MainWindowHandle`이 0인 잔여 프로세스만 정리한다.
