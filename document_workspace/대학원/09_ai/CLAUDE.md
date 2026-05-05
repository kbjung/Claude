# 09_ai 폴더 작업 규칙

> **이 문서는 `09_ai/` 폴더에서 작업할 때 적용되는 전용 규칙입니다.**
> 공통 규칙(파일명·KST·HTML CSS 체크리스트·세션 요약)은 상위 `대학원/CLAUDE.md`를 참조한다.

---

## 1. 폴더 구조

```
09_ai/
├── 01_news/     ← AI·BIO AI 핵심뉴스 html 파일 (매주 월요일 자동 저장)
├── 02_paper/    ← AI 관련 논문·중요 paper 정리 문서
└── _sessions/   ← 세션 간 대화 요약 저장 (BIO AI 뉴스 관련 탐색·분석 대화)
```

---

## 2. 뉴스 파일명 규칙

`[YYYY-MM-DD] AI 핵심뉴스.html` / `[YYYY-MM-DD] BIO AI 핵심뉴스.html`

- 예시: `[2026-04-12] AI 핵심뉴스.html`
- 예시: `[2026-04-12] BIO AI 핵심뉴스.html`
- 날짜는 반드시 `TZ='Asia/Seoul' date +%Y-%m-%d` 명령으로 실제 KST 날짜 확인 후 사용 (공통 규칙 준수)

---

## 3. 자동 스케줄 작업

| 작업명 | 주기 | 산출물 |
|--------|------|-------|
| `weekly-ai_news` | 매주 월요일 오전 | `[YYYY-MM-DD] AI 핵심뉴스.html` |
| `weekly-bio_ai_news` | 매주 월요일 오전 | `[YYYY-MM-DD] BIO AI 핵심뉴스.html` |

저장 경로: `09_ai/01_news/`

---

## 4. 뉴스 콘텐츠 기준

- **AI 뉴스**: 빅테크·AI 모델·정책·연구 동향 등 4~6개 카테고리
- **BIO AI 뉴스**: 빅파마 AI 파트너십·M&A, AI 신약개발 플랫폼, 펩타이드·단백질 AI 연구, 국내 동향 등 4~6개 카테고리
- 각 뉴스에 **날짜·출처·핵심 내용** 포함
- **논문이 포함될 경우 저자 소속·공동 연구기관 명시** (memory 파일의 `feedback_ai_news_format` 피드백 준수)
- 기존 HTML 파일의 디자인 스타일(카드형·색상·폰트 등) 그대로 유지
- HTML 작성 시 상위 CLAUDE.md의 **CSS 체크리스트** 반드시 준수 (특히 `.tag` nowrap, 분류 칼럼 width:1%)

---

## 5. 세션 요약 저장

BIO AI 뉴스 관련 탐색·분석 대화는 `09_ai/_sessions/`에 저장한다.
파일명: `대화요약_[주제]_YYYYMMDD_HHMM.md` (공통 규칙 준수)

---

## 6. 변경 이력

| 날짜 | 변경 내용 |
|------|----------|
| 2026.04.12 | 09_ai_news 폴더 파일명 규칙 추가 (`[YYYY-MM-DD] AI 핵심뉴스.html` 형식) |
| 2026.04.21 | 09_ai_news → 09_ai 폴더 재구조화 (01_news, 02_paper, _sessions 서브폴더 생성) |
| 2026.04.21 | 스케줄 작업(weekly-ai_news, weekly-bio_ai_news) 저장 경로 09_ai/01_news 로 수정 |
| 2026.05.05 | 09_ai 전용 CLAUDE.md 신규 생성 (3-Tier 구조 분리, 펩타이드 프로젝트 CLAUDE.md에서 09_ai 규칙 추출) |
