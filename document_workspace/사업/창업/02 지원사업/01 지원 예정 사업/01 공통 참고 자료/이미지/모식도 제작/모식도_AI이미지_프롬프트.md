# 기술 모식도 A안 — AI 이미지 생성 프롬프트

> **총 2개 프롬프트**: 행1-좌(한계) 1장 + 행1-우(필요성) 1장
> **텍스트는 AI가 아닌 PPT에서 직접 입력** (한국어 깨짐 방지)

---

## 사용 방법

### 나노바나나2
1. 나노바나나2 열기
2. 아래 프롬프트를 **그대로** 복사 → 붙여넣기
3. 생성된 이미지 다운로드
4. PPT에서 행1-좌/우 배경으로 삽입 → 위에 텍스트 오버레이

### ChatGPT (GPT-4o)
1. ChatGPT 열기
2. **"아래 설명대로 이미지를 만들어줘"** 라고 먼저 입력
3. 바로 이어서 아래 프롬프트 붙여넣기
4. 생성된 이미지 다운로드

### 공통 팁
- 비율: **가로로 긴 직사각형 (16:9 또는 3:1)** 권장
- 결과가 마음에 안 들면: "좀 더 심플하게" / "플랫 디자인으로" / "배경을 흰색으로" 등 추가 요청
- 3개 아이콘 간격이 너무 좁으면: "3개 아이콘을 더 넓은 간격으로 배치해줘" 요청

---

## 프롬프트 1: 행1-좌 — 기존 치료제의 한계 (한 장)

```
Create a wide horizontal infographic panel (3:1 ratio) with a light pink/red-tinted background (#fce4ec), showing THREE side-by-side medical limitation icons in a clean row, evenly spaced:

[LEFT ICON] An oral pill/capsule with red warning arrows radiating outward toward a faded human body silhouette, representing systemic side effects from oral medication. A small red caution/warning symbol nearby.

[CENTER ICON] A topical dropper applying liquid onto a simplified scalp cross-section, but the liquid pools on the skin surface and does NOT penetrate down to the hair follicle. A red "X" mark showing the drug is blocked at the surface.

[RIGHT ICON] A spray bottle misting solution onto a scalp surface, where the solution forms a thin polymer film/layer sitting only on the top of the skin. An arrow pointing downward is blocked, showing no deep penetration into the hair follicle.

Style: Clean flat design, minimal medical infographic style, soft pastel pink/red tones, professional and suitable for a scientific presentation. NO text, NO labels, NO words anywhere in the image. Only icons and visual elements. White or very light pink background.
```

---

## 프롬프트 2: 행1-우 — 보유 기술 도입의 필요성 (한 장)

```
Create a wide horizontal infographic panel (3:1 ratio) with a light blue-tinted background (#e3f2fd), showing THREE side-by-side medical solution icons in a clean row, evenly spaced:

[LEFT ICON] A hair follicle cross-section showing small blue nanoparticles/peptides successfully penetrating through all skin layers (epidermis → dermis) and reaching deep into the hair follicle bulb (dermal papilla). Blue arrows pointing downward along the penetration path. A green checkmark at the bottom.

[CENTER ICON] A human body silhouette with a protective shield/barrier around it. A small blue droplet is applied only to the scalp area (localized treatment). The rest of the body is clean and unaffected — no drug spreading. A green checkmark near the body. Concept: minimal systemic exposure.

[RIGHT ICON] A peptide molecule chain (shown as a string of small colored beads/circles) that simultaneously carries a drug molecule attached to it AND emits a gentle green/blue healing glow or anti-inflammatory aura around itself. Visual concept: the carrier itself is also a medicine (dual-function). Two small arrows: one pointing to the drug cargo, one pointing to the healing glow.

Style: Clean flat design, minimal medical infographic style, soft pastel blue/green tones, professional and suitable for a scientific presentation. NO text, NO labels, NO words anywhere in the image. Only icons and visual elements. White or very light blue background.
```

---

## PPT 편집 가이드

### AI 이미지 삽입 후 텍스트 오버레이

행1-좌 이미지 위에 PPT 텍스트 박스로 아래 내용을 배치:

| 위치 | 라벨 (볼드) | 키워드 |
|------|-----------|--------|
| 좌측 아이콘 아래 | 경구 Finasteride | 전신 부작용 (성기능 저하 등) |
| 중앙 아이콘 아래 | Minoxidil 외용제 | DHT 미억제, 중단 시 효과 소실 |
| 우측 아이콘 아래 | 핀쥬베 (국소 Fin) | 표면 체류만, 자체 전달·치료능 없음 |

행1-우 이미지 위에 PPT 텍스트 박스로 아래 내용을 배치:

| 위치 | 라벨 (볼드) | 키워드 |
|------|-----------|--------|
| 좌측 아이콘 아래 | 모낭 심부 직접 전달 | 표피→진피→모유두까지 |
| 중앙 아이콘 아래 | 전신 부작용 구조적 최소화 | 경구 대비 1/40 투여량 |
| 우측 아이콘 아래 | 운반체 자체 항염 치료능 | Carrier-free, Fin과 시너지 |

### PPT 도형으로 직접 만드는 파트

| 파트 | 만드는 방법 |
|------|-----------|
| 타이틀 바 | 사각형 도형 (진한 남색 #16213e) + 흰색 볼드 텍스트 |
| 행1 섹션 라벨 | 좌: "❌ 기존 치료제의 한계 (Limitations)" / 우: "✅ 보유 기술 도입의 필요성 (Necessity)" |
| 중간 연결 바 | 사각형 도형 (진한 남색) + "▼ 한계 극복 및 필요성 충족을 위한 솔루션 ▼" |
| 하단 3단계 번호 | 원형 도형 안에 ①②③ + 단계 제목 + 설명 텍스트 + 화살표(➤) |
| 하단 파이프라인 바 | 사각형 3칸: 🧬 탈모 치료제 | 🧫 피부암 치료제 | 🧴 비의약 두피케어 |

### 실제 실험 이미지 삽입 (기존 데이터)

| 위치 | 삽입할 이미지 | 출처 |
|------|------------|------|
| 행3-① 경피 전달 | 피부투과 형광 이미지 (표피→진피 투과 확인) | 논문/이노베어 |
| 행3-② 이중기능 | 모유두 세포 내부 전달 확인 이미지 | 논문/이노베어 |
| 행3-③ 치료 효능 | 모발 성장 효능 비교 그래프 (빨간/초록) | 논문/이노베어 |
