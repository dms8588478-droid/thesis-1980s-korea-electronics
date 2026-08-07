# 내일 바로 시작하는 고려대 사학과 석사논문 킥오프 가이드

작성일: 2026-08-07

대상: 코딩 경험이 많지 않은 역사학 대학원생

기준 문서: [D03 주제선정 메모](../deliverables/D03_topic_selection_memo.md), [D04 연구 툴체인 검토](../deliverables/D04_quarto_mcp_toolchain_review.md)

> **목표:** 오늘 밤 설치를 끝내고, 내일 지도에서는 주제 결정을 10~15분 안에 기록한 뒤 곧바로 Quarto 논문·사료대장·인용 검증 작업을 시작한다.

---

## 0. 내일 2시간 뒤 남아야 할 결과

- [ ] 지도교수의 결정이 기록된 1쪽 메모
- [ ] Quarto Book 미리보기 화면
- [ ] 확정 또는 잠정 제목·연구질문·작업가설이 들어간 서론 파일
- [ ] 실제 자료 5건이 등록된 사료대장
- [ ] 원문·쪽수까지 확인한 주장 카드 3건
- [ ] Zotero에서 내보낸 `sources/bibliography.bib`와 실제 인용 1건
- [ ] 변경사항 Git 커밋 1건

**설치 자체는 논문 성과가 아니다.** 내일은 위 7개가 만들어져야 끝난다.

---

# PART A. 오늘 밤 사전 설치

## 1. 설치 순서

Windows는 **PowerShell**, Mac은 **터미널**을 사용한다. 설치가 끝날 때마다 창을 닫고 새로 연 뒤 확인 명령을 실행한다.

### 1-1. Git

- 설치: <https://git-scm.com/downloads/>
- Windows 설치 옵션은 기본값을 유지한다.

확인:

```bash
git --version
```

### 1-2. VS Code

- 설치: <https://code.visualstudio.com/download>
- 확장 메뉴에서 다음 3개만 설치한다.
  - **Quarto**
  - **Python** (Microsoft)
  - **R**

처음부터 확장을 많이 설치하지 않는다.

### 1-3. Python

- 설치: <https://www.python.org/downloads/>
- Windows에서는 설치 화면의 **Add Python to PATH**를 반드시 선택한다.
- 호환성을 우선해 이 연구에서는 **Python 3.13 계열**을 권장한다.

확인:

```powershell
py --version
```

Mac:

```bash
python3 --version
```

연구용 최소 패키지 설치:

```powershell
py -m pip install --upgrade pip
py -m pip install jupyter pandas matplotlib pyyaml requests
```

Mac에서는 `py` 대신 `python3`를 사용한다.

### 1-4. R

- 설치: <https://cran.r-project.org/>
- Windows는 **Download R for Windows → base**, Mac은 **Download R for macOS**를 선택한다.

R 프로그램을 한 번 실행해 아래를 입력한다.

```r
R.version.string
install.packages(c("knitr", "rmarkdown", "tidyverse"))
```

패키지 저장소 선택 창이 나오면 가까운 한국 또는 기본 cloud 저장소를 고른다.

### 1-5. Quarto

- 설치: <https://quarto.org/docs/get-started/>
- Windows는 `.msi`, Mac은 `.pkg` 설치 파일을 사용한다.

확인:

```bash
quarto --version
quarto check
```

PDF 출력은 논문 구조가 잡힌 뒤 설치한다. 내일은 HTML 미리보기부터 성공시키며, 처음부터 LaTeX 문제로 시간을 쓰지 않는다.

### 1-6. Node.js — Codex 설치에 필요

- 설치: <https://nodejs.org/en/download>
- **LTS** 버전을 선택한다.

확인:

```bash
node --version
npm --version
```

### 1-7. OpenAI Codex CLI

Windows·Mac 공통:

```bash
npm install --global @openai/codex
codex --version
```

프로젝트 폴더에서 처음 `codex`를 실행하면 **Sign in with ChatGPT**를 선택해 로그인한다. 공식 안내: <https://developers.openai.com/codex/cli/>

Mac/Linux에서는 공식 단독 설치 방식도 사용할 수 있다.

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

### 1-8. Zotero — 각주 재작업 방지

- Zotero: <https://www.zotero.org/download/>
- Better BibTeX: <https://retorque.re/zotero-better-bibtex/installation/>

내일은 Zotero 컬렉션을 하나 만들고 `sources/bibliography.bib`로 **Better BibTeX 자동 내보내기**를 연결한다. 서지의 단일 원장은 Zotero이며, BibTeX 파일을 손으로 이중 관리하지 않는다.

---

## 2. 저장소 내려받기

Windows PowerShell:

```powershell
cd $HOME\Documents
git clone https://github.com/waterfirst/thesis-1980s-korea-electronics.git
cd thesis-1980s-korea-electronics
code .
```

Mac:

```bash
cd ~/Documents
git clone https://github.com/waterfirst/thesis-1980s-korea-electronics.git
cd thesis-1980s-korea-electronics
code .
```

이미 내려받았다면 다시 clone하지 않는다.

```bash
cd thesis-1980s-korea-electronics
git pull --ff-only
```

> 공개 저장소에는 저작권이 있는 PDF·스캔·개인정보를 올리지 않는다. 원문은 저장소 밖의 비공개 폴더에 두고, 저장소에는 서지·소재·쪽수·검증 상태만 기록한다.

---

## 3. 오늘 밤 설치 완료 판정

아래 결과를 한 화면에서 확인한다.

Windows:

```powershell
git --version
code --version
py --version
R --version
quarto --version
node --version
npm --version
codex --version
```

Mac에서는 `py` 대신 `python3`를 사용한다. `code` 또는 `R`만 인식되지 않아도 앱 자체가 실행되면 내일 진행할 수 있지만, **Python·Quarto·Codex·Git** 오류는 오늘 해결한다.

---

# PART B. 내일 디스커션 10~15분

## 4. 교수와 결정할 것만 묻기

긴 설명 대신 [D03](../deliverables/D03_topic_selection_memo.md)을 열고 아래 네 가지에 답을 받는다.

### 결정 1 — 제목의 강도

- **권고:** 연구계획 단계에서는 중립형 제목 사용
- 중립형: 「1980년대 후반 초고집적반도체 공동개발사업과 정부–기업 관계의 재편 — 4M DRAM 개발사업(1986~1989)을 중심으로」
- 분석형: 「‘자율과 경쟁’과 공동개발의 병존 — 1986~1989년 4M DRAM 공동개발사업을 통해 본 정부–기업 관계의 재편」

### 결정 2 — 핵심 기여의 우선순위

하나를 1순위로 고른다.

1. 공업발전법의 ‘자율과 경쟁’과 선택적 기술지원이 병존한 **제도사**
2. 정부·ETRI·연구조합·기업이 규칙을 협상한 **관계사** — 현재 권고
3. 당대 기록과 후대 기관사·사사의 공로 서술을 비교하는 **기억·서사 연구**

나머지는 보조축으로 둔다. 세 축을 같은 비중으로 쓰지 않는다.

### 결정 3 — 작업가설의 지위

‘조정된 경쟁’은 결론이 아니라 **반증 가능한 작업가설**로 둘 것인지 확인한다. 반대 사료가 나오면 수정한다는 원칙을 함께 기록한다.

### 결정 4 — 자료가 부족할 때의 축소안

반도체연구조합·기업 내부문서를 확보하지 못할 경우:

> 공업발전법의 정책언어와 1986년 「초고집적반도체기술 공동개발안」의 집행 논리를 비교하는 정책사 연구로 축소한다.

이 대체안을 미리 승인받으면 자료 부족 때문에 주제를 다시 처음부터 정하는 일을 막을 수 있다.

---

## 5. 1분 결정 기록

면담 중 아래 블록만 복사해 `consulting/session_log/2026-08-08_kickoff.md`에 채운다.

```markdown
# 2026-08-08 지도 기록

- 잠정 제목:
- 핵심 기여 1순위: 제도사 / 관계사 / 기억·서사
- 주질문:
- 작업가설 유지·수정:
- 필수 확보 사료:
- 주제 유지 판정일:
- 자료 부족 시 축소안:
- 지도교수의 핵심 지적:
- 다음 면담 전 산출물:
```

결정되지 않은 항목은 추측해 채우지 말고 `미정`으로 쓴다.

---

# PART C. 디스커션 직후 2시간 실행

## 6. 0~10분 — Git 상태 확인과 Codex 첫 실행

```bash
git pull --ff-only
git status
codex
```

Codex의 첫 프롬프트:

```text
이 저장소에서 deliverables/D03_topic_selection_memo.md,
deliverables/D04_quarto_mcp_toolchain_review.md,
consulting/session_log/2026-08-08_kickoff.md만 먼저 읽어라.

목표는 고려대 사학과 석사논문용 Quarto Book 작업환경을 만드는 것이다.
지금은 파일을 수정하지 말고 다음만 보고하라.
1. 오늘 지도에서 확정된 결정과 미정 항목
2. 기존 파일을 보존하면서 필요한 최소 변경
3. 2시간 완료 기준
4. 사료·쪽수 없이 사실로 쓰일 위험이 있는 문장

해석이 둘 이상이면 조용히 고르지 말고 나열하라.
```

보고를 읽고 잘못된 전제가 없을 때만 다음 단계로 간다.

## 7. 10~35분 — Quarto Book 최소 구조 만들기

Codex에 다음 작업을 요청한다.

```text
방금 합의한 계획대로 Quarto Book 최소 구조를 만들어라.
기존 docs/, deliverables/, sources/, research/ 파일은 삭제·이동·개명하지 마라.

최소 요구사항:
- _quarto.yml
- index.qmd
- chapters/01_introduction.qmd
- chapters/02_historiography.qmd
- chapters/03_policy_context.qmd
- chapters/04_joint_development.qmd
- chapters/05_actor_relations.qmd
- chapters/06_memory_narratives.qmd
- chapters/07_conclusion.qmd
- sources/bibliography.bib 연결
- HTML 출력 우선

각 장에는 제목과 '확인할 질문'만 넣고 사실 서술이나 인용을 만들어내지 마라.
완료 후 quarto render를 실행하고 변경 파일과 검증 결과를 보고하라.
```

검증:

```bash
quarto render
quarto preview
```

브라우저에 목차와 7개 장이 보이면 성공이다.

## 8. 35~55분 — 제목·질문·가설만 이식

`consulting/session_log/2026-08-08_kickoff.md`에 기록한 결정만 `index.qmd`와 `chapters/01_introduction.qmd`에 반영한다.

Codex 프롬프트:

```text
지도 기록에서 확정된 제목·주질문·작업가설만 index.qmd와
chapters/01_introduction.qmd에 반영하라.
미정 항목은 [미정]으로 표시하라.
작업가설을 확정된 결론처럼 고쳐 쓰지 마라.
새로운 역사적 사실·인용·참고문헌을 추가하지 마라.
```

## 9. 55~80분 — 사료대장 5건 등록

[D03의 핵심 사료군](../deliverables/D03_topic_selection_memo.md#6-핵심-사료군과-사료비판)에서 실제 접근 가능한 자료만 골라 `sources/primary_sources.md`에 기록한다.

각 항목의 필수 필드:

```text
자료 ID / 정식 제목 / 생산기관 / 생산일 / 원본·사본 여부
소장기관·URL·청구기호 / 열람일 / 쪽수 범위 / 확보 상태
이 자료로 검증할 질문 / 예상 편향 / 공개 저장소 수록 여부
```

첫 5건 권고:

1. 「초고집적반도체기술 공동개발안」(1986.8.22)
2. 공업발전법 제정 법률·제정 이유
3. 1986~1989년 ETRI 당대 연보 또는 사업보고서
4. 반도체연구조합 결성·사업 관련 당대 기사
5. 삼성·금성·현대 중 확보 가능한 기업 사사 또는 연차보고서

**후대 ETRI사와 기업 사사는 당대 기록과 같은 층위로 취급하지 않는다.**

## 10. 80~100분 — Zotero 인용 1건 성공

1. Zotero에 `4M DRAM thesis` 컬렉션을 만든다.
2. 실제로 열어 확인한 선행연구 1편을 저장한다.
3. 저자·제목·발행연도·학술지·권호·쪽수를 원문과 대조한다.
4. Better BibTeX로 `sources/bibliography.bib`에 자동 내보낸다.
5. `chapters/02_historiography.qmd`에 인용키를 1개 넣는다.

```markdown
주대영의 연구는 공동연구의 추진 단계와 경쟁적 공동연구 방식을 검토했다 [@실제인용키].
```

인용키는 예시를 복사하지 말고 실제 BibTeX에 생성된 값을 사용한다. 이후 다시 `quarto render`해 참고문헌이 표시되는지 확인한다.

## 11. 100~115분 — 주장 카드 3건 작성

`research/` 아래에 당일 주장 카드를 만들고, **주장과 근거를 분리**한다.

```markdown
## C001
- 잠정 주장:
- 상태: 후보 / 원문확인 / 교차검증 / 반박됨
- 근거 자료 ID:
- 정확한 쪽수:
- 원문 발췌:
- 연구자의 해석:
- 반대 또는 대안 설명:
- 추가 확인 자료:
```

완료 조건:

- 카드 3건 중 최소 1건은 `원문확인`
- `원문확인` 카드는 정확한 쪽수 필수
- AI가 제안했지만 원문을 못 본 주장은 모두 `후보`
- 동일 기관의 후대 기념서사만으로는 `교차검증` 처리 금지

## 12. 115~120분 — 렌더·검토·커밋

```bash
quarto render
git diff --check
git status
git diff
```

Codex에서 `/review`를 실행해 **인용 없는 단정, 존재하지 않는 파일, 잘못된 링크, 미정 사항의 임의 확정**을 점검한다.

문제가 없으면:

```bash
git add _quarto.yml index.qmd chapters sources research consulting
git commit -m "논문 킥오프: 주제 결정과 Quarto 연구환경 구성"
git push
```

---

# PART D. Codex를 역사논문 조수로 쓰는 규칙

## 13. 반드시 지킬 6개 규칙

1. **Codex는 사료를 발명하지 않는다.** 확인하지 못하면 `미확인`으로 쓴다.
2. **인용문에는 원문과 쪽수가 있어야 한다.** URL만 있으면 인용 확정이 아니다.
3. **사실·사료 발췌·연구자 해석을 분리한다.** AI 요약을 원문처럼 쓰지 않는다.
4. **사사는 자기서술이다.** 정부문서·당대 언론·타 기관 기록과 교차한다.
5. **한 번에 한 작업만 시킨다.** 탐색, 추출, 검증, 글쓰기를 한 프롬프트에 섞지 않는다.
6. **수정 전 계획, 수정 후 검증.** 바뀐 모든 줄은 현재 요청까지 추적 가능해야 한다.

## 14. 토큰을 아끼는 작업 단위

- 새 작업마다 저장소 전체가 아니라 **관련 파일 2~4개만 지정**한다.
- PDF 전체를 반복 첨부하지 않고, 쪽수 있는 사료카드와 주장 카드를 넘긴다.
- 긴 대화를 이어가기보다 `session_log`에 결정을 남기고 새 세션을 연다.
- “논문을 써줘” 대신 “C001~C003의 검증된 근거만으로 600자 문단 초안을 작성하라”고 요청한다.
- 초고 생성 전에는 반드시 `후보`와 `원문확인` 상태를 분리한다.

---

## 15. 막혔을 때 중단 기준

- 설치 오류에 10분 이상 걸리면 오류 화면과 명령을 기록하고 다음 단계로 넘어간다.
- 교수 결정이 없으면 Codex가 대신 결정하게 하지 않는다.
- 사료 원문을 못 찾으면 범위를 넓히지 말고 D03의 1주일 타당성 시험을 실행한다.
- 1주일 뒤 확정 조건 6개 중 4개를 충족하지 못하면 승인받은 축소안으로 전환한다.

---

## 공식 설치 문서

- [Python 다운로드](https://www.python.org/downloads/)
- [R/CRAN](https://cran.r-project.org/)
- [Quarto 시작하기](https://quarto.org/docs/get-started/)
- [Quarto + VS Code 튜토리얼](https://quarto.org/docs/get-started/hello/vscode.html)
- [Node.js LTS](https://nodejs.org/en/download)
- [Git 다운로드](https://git-scm.com/downloads/)
- [VS Code 다운로드](https://code.visualstudio.com/download)
- [OpenAI Codex CLI](https://developers.openai.com/codex/cli/)
