# D04 — 사료조사 MCP·Quarto 논문작성 툴체인 검토

> 검토일: 2026-08-07  
> 대상: 「1986~1989년 4M DRAM 공동개발사업을 통해 본 정부–기업 관계의 재편」 석사논문  
> 원칙: AI는 검색·정리·검증 보조 도구이며, 논지와 사료 해석은 연구자가 결정한다.

## 1. 현재 저장소 진단

현재 저장소에는 연구질문, 사료 대장, 정독 노트, 연표와 BibTeX 파일이 있으나 아직 다음 요소가 없다.

- Quarto 프로젝트 설정(`_quarto.yml`)과 장별 `.qmd` 원고
- 사료마다 소장처·청구기호·판본·쪽수·권리·OCR 상태를 관리하는 정규화된 대장
- 본문의 주장과 근거 사료를 연결하는 claim ledger
- Zotero에서 `sources/bibliography.bib`를 자동 갱신하는 흐름
- 인용키·링크·Quarto 렌더를 검사하는 자동 QA

## 2. 핵심 결정

### 2.1 석사논문은 Quarto Manuscript보다 Quarto Book이 적합

Quarto Manuscript는 학술지 논문과 계산 노트북 공개에 맞춰져 있다. 80~120쪽의 다장(多章) 석사논문은 장·부록·목차·HTML 전체검색을 기본 지원하는 **Quarto Book**으로 구성하는 편이 낫다.

- 공식 Book 문서: <https://quarto.org/docs/books/>
- 장·부록 구조: <https://quarto.org/docs/books/book-structure>
- 참고할 실제 사례: <https://github.com/james-d-h/quarto-phd-thesis>
- 여러 논문 템플릿 목록: <https://github.com/Jupyter4Science/awesome-quarto-thesis>
- 단순한 extension 구조 참고: <https://github.com/quarto-monash/thesis>

위 템플릿은 **구조만 참고**하고 그대로 복제하지 않는다. 고려대학교 대학원 학위논문 작성지침의 표지, 판형, 여백, 글꼴, 각주 형식을 먼저 확보한 뒤 전용 PDF/Word 형식을 맞춘다.

### 2.2 서지는 Zotero 8 + Better BibTeX를 단일 원장으로 사용

수동으로 `.bib`를 편집하면 저자명·발행연도·인용키가 쉽게 어긋난다. Zotero 컬렉션을 원장으로 두고 Better BibTeX 자동 내보내기로 `sources/bibliography.bib`를 갱신한다.

- Better BibTeX: <https://github.com/retorquere/zotero-better-bibtex>
- 안정적 citation key와 자동 내보내기: <https://retorque.re/zotero-better-bibtex/>
- Quarto의 Zotero·Crossref 인용 입력: <https://quarto.org/docs/visual-editor/technical.html>
- Quarto citation/CSL 문법: <https://quarto.org/docs/authoring/footnotes-and-citations>
- CSL 스타일 저장소: <https://github.com/citation-style-language/styles>

역사학 논문은 일반적으로 각주형 스타일을 사용하므로 `Chicago full note with bibliography`를 출발점으로 삼되, 최종 형식은 사학과 지침과 기존 통과 논문을 대조해 수정한다.

## 3. MCP 채택안

### A. 웹 사료 탐색: Microsoft Playwright MCP — 채택

- 저장소: <https://github.com/microsoft/playwright-mcp>
- 역할: 국가기록원·대통령기록관·KCI 등에서 검색어 반복, 상세화면 열기, 메타데이터와 영구 URL 확인
- 제한: 로그인·캡차·유료벽을 우회하지 않는다. DBpia·KISS·RISS 원문 다운로드는 연구자의 합법적 기관 인증과 이용약관 범위에서 수동 처리한다.

Playwright MCP가 수집해야 하는 것은 원문을 무단 복제한 파일이 아니라 `제목, 생산기관, 생산일, 기록물철/건, 청구기호, URL, 열람일`이다.

### B. 국내 공식 검색 API용 소형 MCP — 직접 구축 권장

범용 academic MCP보다 논문 주제에 직접 맞는 API wrapper가 유용하다.

- 국가기록원 검색 Open API: <https://www.archives.go.kr/next/newsearch/openAPI03.do>
- KCI Open API: <https://www.kci.go.kr/kciportal/po/openapi/openApiConnSamp.kci>

최소 도구는 다음 네 개면 충분하다.

1. `search_archives(query, year_from, year_to, agency)`
2. `get_archive_record(record_id)`
3. `search_kci(query, year_from, year_to)`
4. `save_source_packet(metadata, accessed_at, research_note)`

검색 결과는 곧바로 논문 근거가 아니라 **후보 사료 패킷**이다. 연구자가 원문을 열어 쪽수와 문맥을 확인해야 `verified` 상태가 된다.

### C. Zotero MCP — 제한적 채택

1순위는 기능이 적고 안정적인 read-only 방식이다.

- Pyzotero MCP: <https://github.com/urschrei/pyzotero>
- 대안(기능이 많아 권한 검토 필요): <https://github.com/54yyyu/zotero-mcp>

활용 범위는 컬렉션 검색, 서지 메타데이터, PDF outline, 지정 쪽수 읽기까지로 제한한다. 초기에는 item 생성·수정·삭제 권한을 AI에 주지 않는다.

### D. PDF 구조화: Docling MCP — 조건부 채택

- 저장소: <https://github.com/docling-project/docling>
- 강점: PDF의 읽기 순서·표·제목 구조를 보존해 Markdown/JSON으로 내보내며 로컬 실행과 MCP를 지원한다.
- 적용: 텍스트 PDF, OCR이 끝난 백서·보고서의 구조화
- 주의: 한국어 스캔본 OCR 정확도는 별도 검증 없이 신뢰하지 않는다.

### E. OCR: OCRmyPDF + PaddleOCR 비교시험 — 조건부 채택

- 검색 가능한 PDF 생성: <https://github.com/ocrmypdf/OCRmyPDF>
- 한국어 인식 모델과 공식 MCP를 제공하는 PaddleOCR: <https://github.com/PaddlePaddle/PaddleOCR>

바로 전량 변환하지 않고 대표 사료 20쪽으로 benchmark한다.

1. 깨끗한 1980년대 인쇄물
2. 세로쓰기·다단 편집
3. 표와 도표가 많은 백서
4. 복사 품질이 낮은 사사

고유명사·연도·수치·표 제목의 오류율을 사람이 대조해 더 나은 파이프라인을 고른다. OCR 텍스트는 검색 보조물이며 인용은 반드시 원본 이미지/PDF 쪽수에서 재확인한다.

### F. GitHub MCP — 유지

- 공식 서버: <https://github.com/github/github-mcp-server>
- 역할: 이슈, 연구 할 일, 장별 변경, 검토 요청 관리
- 금지: 저작권 PDF, 사사 스캔, 기관 인증 쿠키·토큰을 GitHub에 커밋하지 않는다.

## 4. MCP가 아닌 보조 도구

### Tropy — 현장 촬영 사료 관리에 가장 유용

- 공식 사이트: <https://tropy.org/>
- 소스: <https://github.com/tropy/tropy>

도서관·기록관에서 촬영한 사료 사진을 `archive / collection / box / folder / identifier / page` 메타데이터와 함께 관리한다. 역사학 연구에는 일반 RAG보다 먼저 도입할 가치가 있다.

### OpenRefine — 사료 대장 정규화

- 저장소: <https://github.com/OpenRefine/OpenRefine>

상공부·상공자원부, 금성사·LG전자처럼 시기별로 달라지는 기관명과 인명·날짜·문서유형 표기를 정리한다. 원본 값은 보존하고 정규화 값은 별도 열로 둔다.

### DataLad — 대용량 원문이 늘어난 뒤 검토

- 저장소: <https://github.com/datalad/datalad>

Git과 git-annex로 대용량·비공개 파일의 버전과 출처를 관리할 수 있다. 다만 현재 단계에는 복잡도가 높다. 원문이 수천 파일로 늘어나기 전까지는 암호화된 로컬 폴더 + 백업 + SHA-256 manifest로 충분하다.

### eScriptorium — 필기 사료가 생길 때만

- 공식 사이트: <https://escriptorium.eu/>

역사 문헌의 레이아웃 분석·HTR·수동 교정에 강하지만, 현재 핵심 사료가 1980년대 인쇄 문서라면 우선순위가 낮다.

## 5. 권장 저장소 구조

```text
.
├── _quarto.yml
├── index.qmd
├── chapters/
│   ├── 01_introduction.qmd
│   ├── 02_policy_transition.qmd
│   ├── 03_joint_development.qmd
│   ├── 04_negotiation_and_coordination.qmd
│   └── 05_conclusion.qmd
├── research/
│   ├── source_registry.csv
│   ├── claim_ledger.csv
│   ├── timeline.csv
│   └── notes/
├── sources/
│   ├── bibliography.bib
│   └── chicago-fullnote-bibliography.csl
├── scripts/
│   ├── validate_sources.py
│   └── validate_citations.py
└── private_sources/        # Git 제외: PDF·스캔·OCR 원문
```

`source_registry.csv` 필수 열:

```text
source_id,source_type,title,creator,date,institution,collection,
call_number,page_range,url,accessed_at,rights,local_sha256,
ocr_engine,ocr_status,verification_status,notes
```

`claim_ledger.csv` 필수 열:

```text
claim_id,chapter,claim_text,source_id,page,verbatim_quote,
context_checked,cross_checked,status,researcher_note
```

## 6. Quarto 최소 설계

```yaml
project:
  type: book

book:
  title: "‘자율과 경쟁’과 공동개발의 병존"
  chapters:
    - index.qmd
    - chapters/01_introduction.qmd
    - chapters/02_policy_transition.qmd
    - chapters/03_joint_development.qmd
    - chapters/04_negotiation_and_coordination.qmd
    - chapters/05_conclusion.qmd

bibliography: sources/bibliography.bib
csl: sources/chicago-fullnote-bibliography.csl

format:
  html:
    toc: true
  pdf:
    pdf-engine: xelatex
  docx: default
```

PDF 형식은 고려대 지침 확보 후 조정한다. 지도교수 검토를 위해 DOCX 출력도 유지한다. GitHub Pages 배포는 공개 가능한 연구계획·목차·방법론만 대상으로 하며, 미공개 원고와 사료는 비공개로 유지한다.

- Quarto GitHub Pages 공식 절차: <https://quarto.org/docs/publishing/github-pages.html>

## 7. 도입 순서

### 이번 주에 적용

1. Quarto Book 기본 구조
2. Zotero 8 + Better BibTeX 자동 export
3. `source_registry.csv`와 `claim_ledger.csv`
4. Playwright MCP + 국가기록원/KCI Open API 시험
5. 대표 사료 20쪽 OCR benchmark
6. `quarto render`, 인용키 존재 여부, 링크 오류를 검사하는 CI

### 지금은 보류

- arXiv MCP: 한국 현대 경제·산업사 핵심 문헌의 범위가 좁다.
- 범용 vector RAG: 페이지·판본·원문 문맥 보존 설계가 먼저다.
- DataLad: 파일 수가 적은 초기에는 운영 복잡도가 더 크다.
- 화려한 외부 Quarto 테마: 고려대 형식 검증 전에는 조판을 확정하지 않는다.

## 8. 최종 권장 조합

```text
국가기록원·KCI API + Playwright MCP
                ↓
source_registry + Tropy
                ↓
OCRmyPDF/PaddleOCR → Docling 구조화
                ↓
Zotero 8 + Better BibTeX + read-only Zotero MCP
                ↓
claim ledger(쪽수·원문·교차검증)
                ↓
Quarto Book(HTML + PDF + DOCX)
                ↓
GitHub MCP + CI(렌더·인용·링크 검증)
```

이 구조의 핵심은 RAG의 답을 믿는 것이 아니라, **모든 문장이 다시 원문 사료의 정확한 위치로 돌아갈 수 있게 만드는 것**이다.
