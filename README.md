# 1980년대 한국 전자산업 — 석사논문 컨설팅 워크스페이스

고려대학교 사학과 석사학위논문 작성을 지원하기 위한 **FDE(Forward Deployed) 컨설팅** 작업 저장소.
연구 주제: **1980년대 한국 전자산업의 국산화·수출 확대와 반도체 산업의 기틀 형성**.

> 컨설턴트 역할: 연구자가 사료 확보 → 정독 → 목차 → 초고 → 각주·서지 정리에 이르는 전 과정을
> 막힘없이 진행하도록 자료 경로·연구 관리 체계·문헌 템플릿을 선제적으로 준비한다.
> 컨설턴트는 **자료·방법·틀**을 제공하고, 논지와 해석은 연구자 본인이 만든다.

## 저장소 구조

- `docs/` — 논문 기획 문서
  - `00_overview.md` — 주제·연구질문·범위·기여
  - `01_research_proposal.md` — 연구계획서 초안 템플릿
  - `02_outline.md` — 목차(장·절) 초안
- `deliverables/` — 컨설팅 산출물
  - `D01_source_acquisition_guide.md` — 사사(社史)·1차/대체 자료 확보 가이드
  - `D02_mcp_research_toolkit.md` — 환각 방지·사료 분석용 MCP 서버 4종 세팅(검증·정정본)
  - `D03_topic_selection_memo.md` — 4M DRAM 공동개발사업 중심 주제선정·타당성 시험
  - `D04_quarto_mcp_toolchain_review.md` — 사료조사 MCP·OCR·Zotero·Quarto Book 툴체인 검토
  - `D05_advisor_meeting_brief_2pages.qmd` — 지도교수 면담용 2쪽 주제·사료·목차·결정 문서
- `sources/` — 자료 관리 대장
  - `primary_sources.md` — 1차 사료(사사·백서·통계) 소재·청구기호 트래커
  - `secondary_sources.md` — 2차 문헌(단행본·논문)
  - `bibliography.bib` — BibTeX 서지 데이터베이스
- `research/`
  - `timeline_1980s_electronics.md` — 1980년대 전자산업 연표(사건·정책·기업)
  - `reading_note_template.md` — 문헌 정독 노트 템플릿
- `guide/` — **설치부터 실제 집필환경까지 연결하는 실습 가이드**
  - `README.md` — 가이드 선택·진행 순서·핵심 원칙
  - `tomorrow_thesis_kickoff_guide.md` — Python·R·Quarto·Codex 설치, 지도 토론, Quarto Book·사료대장·인용 검증 실행안
  - `2h_thesis_ai_guide.md` — 초기 Claude/MCP 실습안(참고용)
- `consulting/`
  - `methodology.md` — 컨설팅 방법론·역할분담·진행 단계
  - `session_log_template.md` — 세션 기록 템플릿
  - `session_log/` — 회차별 세션 기록 보관

## 사용 방법

1. `docs/00_overview.md`에서 주제·연구질문을 먼저 확정한다.
2. `deliverables/D01_source_acquisition_guide.md`를 따라 핵심 사료를 확보하고
   `sources/primary_sources.md` 대장에 소재·청구기호·확보상태를 기록한다.
3. 자료를 읽으며 `research/reading_note_template.md`를 복제해 정독 노트를 남긴다.
4. 노트가 쌓이면 `docs/02_outline.md`의 목차를 구체화하고 초고를 쓴다.

## 원칙

- 인용·서지는 처음부터 BibTeX(`sources/bibliography.bib`)로 관리해 각주 재작업을 없앤다.
- 1차 사료 우선, 회사 사사(社史)는 자기서술 편향을 감안해 정부 백서·타사 사사·통계로 **교차검증**한다.
- 저작권 있는 자료 원문(PDF 스캔 등)은 이 저장소에 커밋하지 않는다(`.gitignore` 참조).
