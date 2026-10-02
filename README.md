# 1980년대 전자공업 — 석사학위논문 저장소

고려대학교 한국사학과 석사학위논문(1986년 초고집적반도체기술 공동개발사업)의 작업 저장소다. 규칙은 `CLAUDE.md`에 있다.

## 어디부터 읽는가

| 차례 | 문서 | 구실 |
|---|---|---|
| 1 | `CLAUDE.md` | 작업 규칙 |
| 2 | `docs/05_handoff.md` | 인계 문서. 새 대화는 여기서 시작한다 |
| 3 | `drafts/thesis_v2_part1~5.md` | **지금의 원고.** 각주 본문은 `tools/build_v2/fn_v2.json`, 빌드는 `tools/build_v2/README.md` |
| 4 | ~~`drafts/thesis_plan.qmd`~~ | **2026-10-02에 지웠다**(커밋 기록 `git show 8fde44a:drafts/thesis_plan.qmd`). 유보·조사 계획은 사료 카드와 인계 문서 §7에 둔다 |
| 5 | `docs/07_writing_rules.md`, `docs/11_style_model.md`, `docs/13_thesis_frame_model.md` | 작성 원칙과 형식 준거 |
| 6 | `research/00_index.md` | 사료 카드 색인. 자료를 조사하기 전에 반드시 연다 |
| 7 | `docs/12_reading_ledger.md`, `docs/09_materials_ledger.md`, `docs/10_copy_request_list.md`, `docs/04_information_disclosure_requests.md` | 판독 대장, 폴더 자료 대장, 사본·청구 목록, 정보공개청구 문안 |
| 8 | `research/00_verification_ledger.md` | 검증되지 않은 에이전트 산출물의 판정 |

## 폴더

- `drafts/` — 원고. `thesis_v2.md`·`thesis_v2_presentation.md`는 빌드 산출물이므로 손으로 고치지 않는다. `thesis_draft.qmd`는 2026-09-29에 멈춘 종전 원고다. 구상 원고 `thesis_conception.qmd`, 논문계획 `thesis_plan.qmd`, 구상 렌더본 `thesis_proposal_draft.pdf`와 `pdf_preview*/`는 2026-10-02에 지웠다(커밋 기록에 있다)
- `research/` — 사료 카드(`source_card_*.md`)와 조사 기록
- `docs/` — 인계·원칙·대장
- `tools/build_v2/` — 원고를 한글 문서로 만드는 빌드
- `archive/` — 지금은 쓰지 않는 문서를 원문 그대로 모아 둔 곳. 2026년 8월 초의 기획 문서는 `archive/2026-08_초기기획.md`에 있다

원문 PDF와 스캔본은 저작권 때문에 저장소에 올리지 않고 작업 폴더에만 둔다(`.gitignore`).
