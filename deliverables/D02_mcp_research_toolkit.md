# D02 — 논문 연구용 MCP 툴킷 세팅

> 컨설팅 산출물 #2. AI 환각(Hallucination) 방지 + 방대한 사료 정밀 분석을 위한 MCP 서버 4종.
> ⚠️ 원문 추천 중 **일부는 현재(2026) 상태로 정정**했다. 아래 표의 "정정" 열을 확인할 것.

## 0. 한눈에 (정정 반영)

| # | 용도 | 채택 서버 | 실행 | 원문 대비 정정 |
|---|---|---|---|---|
| 1 | 논리 설계·가설/목차 | **sequential-thinking** (MCP 공식 레퍼런스) | `npx` | 원문 커뮤니티 레포도 가능하나 공식 레퍼런스 권장 |
| 2 | 사사·백서 RAG 검색 | **로컬 RAG(벡터DB) — 구체 레포 선정 필요** | uv/docker | `document-management-mcp`는 특정 패키지가 아닌 **검색 키워드**. 아래 §2 주의 |
| 3 | 선행연구 교차검증 | **blazickjp/arxiv-mcp-server** | `uvx` | 실재·유지보수 확인됨 |
| 4 | 원고·사료 버전관리 | **github/github-mcp-server (공식)** | 원격 or docker | 원문 `@modelcontextprotocol/server-github`는 **deprecated → 이 레포로 이전** |

## 1. Sequential Thinking — 논리 설계
가설 설정·목차 구조·인과관계 추론을 Problem→Research→Analysis→Synthesis 단계로 강제(수정·분기 지원).
- Claude Code 등록:
  ```bash
  claude mcp add sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking
  ```
- 활용 프롬프트 예: "1980년대 상공부 전자공업 육성정책이 삼성전자 반도체 투자에 미친 인과관계를 단계적으로 분해하고, 반례를 분기해 검토하라."

## 2. 사사·백서 RAG — 방대한 텍스트 정밀검색 *(주의: 구체 레포 선정 필요)*
`document-management-mcp` / `rag-postgres-mcp`는 **단일 공식 패키지가 아니라 검색어**다. 아무거나 붙이지 말고 아래 기준으로 1개를 골라 검증 후 채택한다.
- **선정 기준**: (a) 로컬 파일 인덱싱 + 시맨틱 청크 검색, (b) 메타데이터(연도·쪽수) 보존, (c) 활발한 유지보수, (d) 로컬 실행(사료 외부 유출 방지).
- **현실적 대안 2가지**:
  1. 전용 RAG MCP 레포를 골라 `uv`/docker로 실행 (후보 비교 후 `sources/`에 근거 기록).
  2. **당장은** arxiv 서버의 로컬 저장 + Claude Code 기본 파일도구로 대체하고, 사료 텍스트를 `연도/장` 단위로 잘게 쪼개(chunk) 폴더 관리 → 토큰 초과 회피.
- ⚠️ 사사·백서 스캔 원문은 저작권 자료이므로 **이 저장소에 커밋 금지**(`.gitignore`). RAG 인덱스도 로컬에만 둔다.

## 3. arXiv / 학술 교차검증
사사의 기업 측 일방 기록을 학술 논문으로 교차검증. 인용 그래프 추적으로 '선행연구 검토' 가속.
- 등록:
  ```bash
  claude mcp add arxiv -- uvx arxiv-mcp-server
  ```
- 참고: arXiv는 이공계 위주라 **1980년대 한국 경제·경영사**는 커버가 얕다. 실제 교차검증은
  RISS·DBpia·KISS·구글 스콜라를 병행해야 한다(arXiv는 반도체 기술사·거시배경 보조용).

## 4. GitHub MCP — 원고·사료 버전관리 *(정정됨)*
원문의 `@modelcontextprotocol/server-github`는 **deprecated**. 공식은 `github/github-mcp-server`.
- **간편(권장): 원격 호스팅 서버** — 로컬 설치 없이 OAuth로 연결.
  ```bash
  claude mcp add --transport http github https://api.githubcopilot.com/mcp/
  ```
- **로컬 실행: Docker 이미지**
  ```bash
  claude mcp add github -- docker run -i --rm \
    -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server
  ```
- 활용: 장(Chapter)별 커밋, 연구노트 관리, 이 private 레포(`waterfirst/thesis-1980s-korea-electronics`) 이슈로 할 일 추적.

## 5. 환경 메모
- 이 컨설팅 서버 환경: `uv/uvx`, `npx`, `docker`, `claude` CLI 모두 사용 가능, 현재 MCP 등록 0개.
- 등록 방식은 **Claude Code = `claude mcp add`**. 원문의 `claude_desktop_config.json`은 **Claude Desktop 전용**이고 경로 예시가 Windows(`C:/`)라 이 환경엔 그대로 안 맞음.
- Claude Desktop(개인 PC)에서 쓸 경우 config 예시(Linux/Mac 경로):
  ```json
  {
    "mcpServers": {
      "sequential-thinking": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"] },
      "arxiv": { "command": "uvx", "args": ["arxiv-mcp-server"] }
    }
  }
  ```

## 6. 다음 액션
- [ ] §1, §3 먼저 등록해 논리설계·학술검색부터 가동(리스크 낮음).
- [ ] §2 RAG 후보 레포 2~3개 비교·검증 후 1개 채택, 근거를 `sources/`에 기록.
- [ ] §4는 GitHub PAT 준비 후 원격/도커 중 택1.
