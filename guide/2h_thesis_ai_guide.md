# 2시간 완성 가이드 — AI로 석사논문 쓰기

> 순서대로 따라가세요. 명령어는 **한 줄씩 복사→붙여넣기→Enter**. Windows 기준이며 Mac은 〔Mac〕 표시.
> 막히면 그 STEP 끝의 "🩹 문제 해결"을 보세요.

---

## STEP 0 — 오늘 무엇을, 왜 (0:00–0:10)

오늘 만드는 것:
1. AI(Claude)가 내 **사료 폴더를 직접 읽고**, 특정 연도·키워드가 든 문단을 정확히 찾아주는 환경.
2. AI가 **단계적 추론**으로 논문 가설·목차를 설계하도록 강제하는 도구.
3. arXiv 등 **학술 검색**으로 사사의 주장을 교차검증하는 통로.

왜 이렇게 하나 — 그냥 챗봇에 "삼성전자 20년사 요약해줘" 하면 AI가 **없는 내용을 그럴듯하게 지어냅니다(환각)**. 이건 역사 논문에서 치명적입니다. 그래서 AI가 **실제 내 파일만** 근거로 쓰게 묶어두는 게 오늘의 핵심입니다.

용어 3개만:
- **Python / Node**: 도구들이 돌아가는 엔진(직접 코딩 안 함, 설치만).
- **uv / npx**: 도구를 자동으로 받아 실행해주는 심부름꾼.
- **MCP**: AI(Claude)에 기능(파일읽기·논리추론·논문검색)을 꽂는 **USB 포트**라고 생각하면 됩니다.

---

## STEP 1 — 엔진 설치: Python · uv · Node (0:10–0:30)

### 1-1. Python 설치
1. https://www.python.org/downloads/ 접속 → **Download Python** 클릭.
2. 설치 실행 → **⚠️ 맨 아래 `Add python.exe to PATH` 체크박스를 반드시 켠 뒤** "Install Now".
3. 확인: **시작 → "cmd" 검색 → 명령 프롬프트** 열고 입력:
   ```
   python --version
   ```
   `Python 3.12.x` 처럼 나오면 성공.

〔Mac〕 터미널에서 `python3 --version`. 없으면 https://www.python.org 에서 설치.

### 1-2. uv 설치 (도구 실행기)
명령 프롬프트(PowerShell)에 붙여넣기:
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
〔Mac〕
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
설치 후 **창을 닫았다 새로 열고** 확인:
```
uv --version
```

### 1-3. Node.js 설치 (일부 도구용)
1. https://nodejs.org 접속 → **LTS** 버전 다운로드·설치(전부 Next).
2. 새 명령 프롬프트에서 확인:
   ```
   node --version
   npx --version
   ```

🩹 **문제 해결**: `'python' 은(는) ... 인식되지 않습니다` → 1-1의 PATH 체크를 놓친 것. Python을 **제거 후 재설치**하며 체크박스를 켜세요. 명령어는 항상 **새 창**에서 테스트(설치 후 기존 창은 인식 못 함).

---

## STEP 2 — 논문 저장소 준비 (0:30–0:45)

이 저장소(`thesis-1980s-korea-electronics`)에는 이미 자료 가이드·사료 대장·목차 템플릿이 들어 있습니다.

### 2-1. Git 설치 & 내려받기
1. https://git-scm.com/download/win 에서 Git 설치(전부 기본값 Next).
2. 논문 폴더를 둘 곳으로 이동 후 클론. 예시(문서 폴더):
   ```
   cd %USERPROFILE%\Documents
   git clone https://github.com/waterfirst/thesis-1980s-korea-electronics.git
   cd thesis-1980s-korea-electronics
   ```
   〔Mac〕 `cd ~/Documents` 뒤 동일.

> 🔒 private 저장소라 로그인 창이 뜨면 GitHub 계정으로 인증하세요. (컨설턴트에게 collaborator 초대를 요청)

### 2-2. 폴더 이해 (1분)
- `deliverables/` 자료·도구 가이드(D01, D02)
- `sources/primary_sources.md` **1차 사료 확보 대장** ← 확보할 때마다 여기 갱신
- `docs/00_overview.md` 연구질문·논지 / `docs/02_outline.md` 목차
- `research/` 정독 노트 템플릿·연표
- **새로 만들 폴더**: `사료텍스트/` (아래 STEP 4에서 생성) — 스캔한 사료의 텍스트 보관.

---

## STEP 3 — AI(Claude) + MCP 도구 3종 연결 (0:45–1:15)

여기서 AI에 ①파일읽기 ②단계추론 ③학술검색 기능을 꽂습니다.
순서: **앱 설치(3-1) → 서버 직접 설치·검증(3-2) → 설정 등록(3-3) → 적용(3-4)**.

### 3-1. Claude Desktop 설치
1. https://claude.ai/download 에서 **Claude Desktop** 설치 후 로그인.
2. 앱 실행 → 좌상단 메뉴 **File → Settings → Developer → Edit Config** 클릭.
   - 이러면 `claude_desktop_config.json` 파일이 열립니다.
   - (수동 경로) Windows: `%APPDATA%\Claude\claude_desktop_config.json` / 〔Mac〕 `~/Library/Application Support/Claude/claude_desktop_config.json`

### 3-2. (직접 설치) 각 MCP 서버를 노트북에 미리 설치·검증 ⭐
> **왜 먼저 하나**: 설정 파일에 바로 붙이면, 앱에서 안 뜰 때 원인을 알 수 없습니다.
> 명령줄에서 하나씩 **직접 실행해 "돌아간다"를 눈으로 확인**하면, 문제를 여기서 다 잡고 갑니다.
> 덤으로 도구가 미리 내려받아져(캐시) 앱 첫 실행이 빨라집니다.

명령 프롬프트(또는 PowerShell)를 새로 열고 하나씩 실행하세요. 각 서버는 실행되면
`... running on stdio` 같은 메시지를 내고 **가만히 대기**합니다. → 그게 정상. **`Ctrl + C`로 빠져나온 뒤** 다음으로 갑니다.

**① Sequential Thinking (논리추론)**
```
npx -y @modelcontextprotocol/server-sequential-thinking
```
→ `Sequential Thinking MCP Server running on stdio` 뜨면 성공. `Ctrl + C`.

**② arXiv (학술검색)** — 첫 실행은 패키지 내려받느라 1~2분 걸립니다.
```
uvx arxiv-mcp-server
```
→ 오류 없이 대기하면 성공. `Ctrl + C`.
- (선택) 매번 받기 싫으면 고정 설치: `uv tool install arxiv-mcp-server` → 이후 `arxiv-mcp-server`로 바로 실행됨.

**③ Filesystem (내 사료 폴더 읽기)** — 뒤에 **읽게 할 폴더 경로**를 붙여 테스트:
```
npx -y @modelcontextprotocol/server-filesystem "%USERPROFILE%\Documents\thesis-1980s-korea-electronics"
```
→ `Secure MCP Filesystem Server running on stdio` + `Allowed directories: [...]` 뜨면 성공. `Ctrl + C`.
〔Mac〕 경로를 `~/Documents/thesis-1980s-korea-electronics` 로.

> ✅ 세 개 모두 `running on stdio`를 봤다면, 이제 앱에 붙일 준비 끝. 아래 3-3으로.

🩹 **Windows에서 자주 나는 문제 — 앱은 `npx`/`uvx`를 못 찾음**
명령줄에선 되는데 Claude Desktop에서만 도구가 안 뜨면, 앱(GUI)이 PATH를 못 읽는 경우입니다. 해결:
1. 설치 후 **노트북을 한 번 재부팅**하고 앱을 다시 실행(가장 흔한 해결).
2. 그래도 안 되면 설정 JSON에서 `"command"`를 **전체 경로**로 바꿉니다.
   - `npx` → `C:\\Program Files\\nodejs\\npx.cmd`
   - `uvx` → `%USERPROFILE%\.local\bin\uvx.exe`의 실제 경로(명령줄에서 `where uvx`로 확인 후 그 경로를 `\\`로).
3. 명령줄에서 `where npx`, `where uvx`가 아무것도 안 나오면 STEP 1 설치가 덜 된 것 → 재설치.

### 3-3. 도구 3종 등록 (설정 파일 붙여넣기)
열린 파일 내용을 **전부 지우고** 아래를 붙여넣습니다. **한 곳만 수정**: `사료텍스트` 폴더의 실제 경로.

```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    },
    "arxiv": {
      "command": "uvx",
      "args": ["arxiv-mcp-server"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "C:\\Users\\내이름\\Documents\\thesis-1980s-korea-electronics\\사료텍스트"]
    }
  }
}
```
- `C:\\Users\\내이름\\...` 부분을 **본인 사료텍스트 폴더 실제 경로**로 바꾸세요(역슬래시 `\\` 두 개 유지).
- 〔Mac〕 filesystem 경로는 `/Users/내이름/Documents/thesis-1980s-korea-electronics/사료텍스트`.

### 3-4. 적용
- 저장(Ctrl+S) → **Claude Desktop 완전 종료 후 재실행**.
- 채팅창 입력칸의 🔌(슬라이더/도구) 아이콘에 **sequential-thinking · arxiv · filesystem** 3개가 보이면 성공.

🩹 **문제 해결**: 도구가 안 보이면 (1) 설정 JSON의 쉼표·괄호 오타 확인(붙여넣은 그대로여야 함), (2) STEP 1의 `npx`, `uvx`가 새 창에서 동작하는지 확인, (3) 앱을 트레이에서까지 완전히 끄고 재실행. 처음 실행은 도구를 내려받느라 30초~2분 걸릴 수 있음.

---

## STEP 4 — 사료를 AI가 읽게 만들기 (1:10–1:30)

AI는 스캔 이미지 PDF를 직접 못 읽을 때가 많습니다. **텍스트로** 바꿔 폴더에 넣어줍니다.

### 4-1. 사료텍스트 폴더 만들기
논문 폴더 안에 `사료텍스트` 폴더를 만들고, 자료를 **자료별·장별로 잘게** 나눠 넣습니다. 예:
```
사료텍스트/
  삼성20년사_3장_반도체진입.txt
  전자공업백서_1983_수출통계.txt
  ETRI50년사_TDX개발.txt
```
> 잘게 나누는 이유: 파일이 너무 크면 AI가 한 번에 다 못 읽습니다(토큰 제한). **장/절 단위**가 딱 좋습니다.

### 4-2. PDF/한글 → 텍스트
- **글자 PDF**: PDF에서 텍스트 복사 → 메모장 붙여넣기 → `.txt` 저장.
- **스캔(이미지) PDF**: 글자 인식(OCR)이 필요. 네이버 클로바노트, 구글 문서(업로드 후 열기 시 OCR), 또는 어도비 스캔 등으로 텍스트화. *OCR 결과엔 오탈자가 있으니 인용 확정 전 원문 대조 필수.*
- 각 파일 맨 위 1줄에 **출처와 쪽수 범위**를 적어두세요. 예: `[삼성전자 30년사, pp.210-235]`.

### 4-3. AI에게 정밀검색 시키기 (실습)
Claude Desktop 채팅에 이렇게:
> "filesystem에서 `사료텍스트` 폴더의 파일들을 읽고, **1983년 반도체 관련 서술**이 담긴 문단을 찾아 **파일명과 원문 그대로** 인용해 줘. 요약하지 말고 원문을 보여줘. 없으면 없다고 해."

이때 AI가 **파일에 실제로 있는 문장**만 가져오는지 확인하세요. → STEP 6의 환각 방지와 직결.

---

## STEP 5 — AI로 가설·목차 설계 (1:30–1:50)

`sequential-thinking` 도구로 AI가 **한 번에 답하지 말고 단계적으로** 논리를 짜게 합니다.

### 5-1. 가설 다듬기
채팅에:
> "sequential-thinking을 사용해서, 다음 주제의 연구가설을 단계적으로 설계해 줘. 주제: **1980년대 상공부 전자공업 육성정책이 삼성전자 반도체 투자에 미친 인과관계**. Problem Definition → Research → Analysis → Synthesis 순서로 진행하고, 각 단계에서 **반례와 대안 가설도 분기**해서 검토해 줘."

AI가 단계별로 생각을 쪼개고 스스로 수정(Revision)하는 과정을 보며, **말이 되는 부분만** `docs/00_overview.md`에 옮겨 적으세요.

### 5-2. 목차로 확장
> "위 가설을 바탕으로 석사논문 5장 구성 목차를 제안하되, 각 절마다 **어떤 사료로 입증할지**(사사/백서/통계/논문)를 함께 적어 줘."

결과를 `docs/02_outline.md`의 기존 목차와 비교해 보완합니다.

### 5-3. 교차검증(선행연구)
> "arxiv에서 1980s Korea semiconductor industry, industrial policy 관련 논문을 검색하고, 핵심 주장과 인용된 문헌을 정리해 줘."
- 주의: arXiv는 이공계 위주라 경제·경영사는 **RISS·DBpia·구글 스콜라**를 반드시 병행하세요. AI 검색은 출발점일 뿐, 실제 논문은 본인이 원문 확인.

---

## STEP 6 — 논문 작성법: 인용·각주·서지·검증 (1:50–2:00)

여기가 논문의 품질과 **연구윤리**를 가르는 지점입니다.

### 6-1. 환각 방지 3원칙 (가장 중요)
1. **원문·쪽수로 확인 못 한 인용은 쓰지 않는다.** AI가 준 인용문은 반드시 `사료텍스트` 원본(궁극적으로 실제 책)에서 대조.
2. **AI에게 사실을 묻지 말고, 내 자료 안에서 찾게 한다.** "~에 대해 알려줘"(❌) → "이 파일에서 ~를 찾아 원문 인용"(✅).
3. **AI가 만든 참고문헌 목록을 믿지 않는다.** 존재하지 않는 논문을 지어내는 일이 흔함 → 모든 서지는 RISS 등에서 실재 확인.

### 6-2. 서지·각주 자동화
- 인용할 자료는 그때그때 `sources/bibliography.bib`에 BibTeX로 등록(이미 예시 있음).
- **Zotero**(무료) 설치 + 브라우저 커넥터를 쓰면 논문·책 정보를 원클릭 저장하고 각주를 자동 생성할 수 있어 강력 추천.
- 정독하며 `research/reading_note_template.md`를 복제해 **발췌+쪽수**를 남기면, 나중에 각주가 저절로 채워집니다.

### 6-3. 교차검증 습관
- 사사의 서술 1건 → 백서/통계/타사 사사/언론 중 **최소 1개**로 확인 후 본문에 반영.
- 상충하면 두 서술을 병기하고 각주로 차이를 설명(이게 곧 논문의 독창적 기여가 됩니다).

### 6-4. 버전 관리(파일 꼬임 방지)
- `논문_최종_진짜최종.docx` 지옥을 피하려면, 원고를 이 저장소에 두고 하루 끝에:
  ```
  git add docs research
  git commit -m "0000장 초고: xxx 보완"
  git push
  ```
  (커밋 = '저장 지점' 찍기. 언제든 과거 버전으로 되돌릴 수 있음.)

---

## 🏁 마무리 체크리스트
- [ ] `python`, `uv`, `node`, `git` 4개 명령이 새 창에서 동작
- [ ] 명령줄에서 3개 서버 각각 `running on stdio` 확인 (직접 설치 검증)
- [ ] Claude Desktop에 sequential-thinking · arxiv · filesystem 3개 연결됨
- [ ] `사료텍스트/`에 장별 텍스트 최소 1개 넣고 AI가 원문 인용에 성공
- [ ] `docs/00_overview.md`에 연구가설 1줄 확정
- [ ] `docs/02_outline.md` 목차 1차 보완
- [ ] 오늘 작업 `git commit` & `push`

## 다음 세션 예고
- 사료 확보(D01의 국중/RISS 경로) 실행 → `sources/primary_sources.md` 대장 채우기
- 장별 초고 쓰기 + 각주/서지 정리 실습
- (선택) GitHub MCP·Zotero 연동 심화
