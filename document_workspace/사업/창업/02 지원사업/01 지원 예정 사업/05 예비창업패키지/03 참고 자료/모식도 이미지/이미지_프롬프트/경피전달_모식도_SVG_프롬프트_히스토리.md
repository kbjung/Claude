# 경피 전달 기술 모식도 — SVG 코드 생성 프롬프트 히스토리

> 용도: 예비창업패키지 사업계획서 "창업 아이템 개요(요약)" 파트 삽입용 모식도
> 출력 형식: SVG 코드 → PPT에서 개별 요소 편집 가능
> 참고 이미지: `03 참고자료/모식도 이미지/참고/` 내 전체 이미지
> 관련 문서: 동일 폴더의 `경피전달_모식도_프롬프트_히스토리.md` (DALL-E 이미지 생성용)

### SVG 방식의 장점
- PPT에서 개별 요소(피부층, 모낭, 나노입자, 화살표, 텍스트) 편집 가능
- 색상·크기·위치 자유롭게 수정
- 텍스트를 SVG 내에 직접 포함 가능 (한글 포함)
- 해상도 무관 (벡터)
- 사업계획서 다이어그램 스타일에 적합

### GPT 사용 워크플로우
1. 참고 이미지 4장 첨부 (`펩타이드와 물질01~03.png`, `나노복합체 형성 과정.png`)
2. A-1 프롬프트 입력 → SVG 코드 생성 → 브라우저에서 확인
3. 같은 대화에서 A-2 → A-3 순서로 생성 (스타일 일관성)
4. SVG 파일을 PPT에 삽입 후 그룹 해제하여 편집

### 피부 구조 및 침투 깊이 기준 (전 버전 공통)
```
[피부 표면] ─── 약물 도포 위치
│
├─ 각질층 (Stratum corneum) ─── 기존 약물: 여기서 막힘. 표면 확산·유실
│
├─ 표피층 (Epidermis) ─── 나노복합체: 여기까지 침투 (모낭 없는 부위)
│                         기존 약물: 거의 도달 못함
│
├─ 모낭 경로 (Follicular route) ─ 나노복합체: 모낭을 따라 모낭 심부까지 도달
│   ├─ 모낭 상부 (피지선 부위)
│   ├─ 모낭 벌지 (Bulge region)
│   └─ 모낭 심부 / 진피유두 (Dermal papilla) ─── 나노복합체 최종 도달 지점
│
├─ 진피층 (Dermis) ─── 나노복합체: 거의 도달 안함 (모낭 경로 외에는)
│                      기존 약물: 도달 안함
└─
```

### 나노복합체 구조 (참고 이미지 기반)
- **외곽 쉘**: 초록색 펩타이드 체인이 촘촘하게 감싸는 구형 외벽
- **중간층**: 남색(navy) 펩타이드 체인이 방사상으로 배열
- **코어**: 파란색(sky blue) 구형 약물 분자(Finasteride)가 중심에 캡슐화
- **자기조립**: 펩타이드 체인(초록+남색) + 파란 약물 → 별/성게 중간체 → 구형 나노복합체

---
---

## 2026-03-13 23:06 — v1.0 (SVG 코드 생성용 A안 3장 + B안 2장)

### A안 — SVG 코드 생성 프롬프트 (3장)

#### A-1. 기존 국소 투여의 한계 (문제점)

**GPT 입력 시**: 참고 이미지 4장 모두 첨부 + 아래 프롬프트.

```
I'm attaching reference images of a peptide nanocomplex. These show:
- Peptide chains (green + navy zigzag strands) self-assembling with blue drug molecules
- Final spherical nanocomplex: green outer shell, navy middle layer, blue drug core

For THIS image, the nanocomplex does NOT appear yet. But I need you to establish a consistent SVG visual style that will carry through a series of 3 SVG illustrations. I'll ask for the next two images in follow-up messages.

Please generate SVG code for the following scientific diagram:

SUBJECT: Cross-section of human scalp skin showing FAILED conventional drug delivery to a hair follicle.

SVG STRUCTURE & ELEMENTS:

1. SKIN LAYERS (horizontal bands, top to bottom):
   - Skin surface line at the top
   - Stratum corneum: thin band (~15px height), color #D4A574 (darker peach), with a clear defined border — this is the key barrier
   - Epidermis: medium band (~60px height), color #F5C5A3 (pink-peach)
   - Dermis: large band (~120px height), color #FDE8D0 (light cream)
   - Label each layer on the left side in Korean: 각질층, 표피층, 진피층

2. HAIR FOLLICLE (center of image):
   - A single follicle extending from the surface down through all layers
   - Thin, weak hair shaft (stroke-width: 1.5, color #8B7355) growing upward from the follicle
   - Follicle walls: slightly darker outlines following a tapered tube shape
   - Sebaceous gland: small oval blob (#E8C87A) attached to upper follicle
   - Dermal papilla: small rounded bump at the very base of the follicle (#D4A574)

3. DRUG MOLECULES — DELIVERY FAILURE:
   - 8-10 small blue circles (r=3, fill #4A90D9) scattered ON TOP of the stratum corneum surface
   - Most molecules positioned horizontally along the surface, spread out sideways
   - 2-3 molecules near the sebaceous gland area, being carried away by sebum flow
   - Small dashed arrows (gray) showing horizontal drift direction
   - CRITICAL: NO blue molecules below the stratum corneum. None in epidermis. None in dermis. None near follicle base.
   - A subtle red "X" or barrier indication at the stratum corneum to show blockage

4. VISUAL INDICATORS:
   - Small downward arrows near the drug molecules that are blocked (with a red X)
   - Curved arrow near sebaceous gland showing sebum flow carrying drugs away
   - Empty space around dermal papilla to emphasize "nothing reached here"

5. STYLING:
   - Clean, flat medical diagram style
   - Soft pastel colors
   - SVG viewBox: "0 0 400 500" (portrait, 4:5 ratio)
   - No gradients needed — flat fills with subtle borders
   - All text in Korean where labels are present
   - Include a subtle coral/warm tint (#FFF5F0) as background rectangle

OUTPUT: Complete, valid SVG code that I can save as .svg and open in a browser or import into PowerPoint.
```

**넣을 텍스트 (SVG 내 포함 또는 PPT에서 추가)**
- 각질층 / 표피층 / 진피층 ← 피부층 레이블 (SVG에 포함)
- Finasteride ← 파란 약물 분자 옆
- "각질층 투과 실패" ← 약물 차단 지점
- "피지 흐름에 의한 약물 유실" ← 피지선 쪽
- "모낭 심부 도달 실패" ← 모낭 하단 빈 공간

---

#### A-2. 펩타이드 나노운반체 경피전달 (솔루션)

**GPT 입력 시**: 같은 대화에서 이어서 아래 프롬프트만 입력.

```
Now create SVG image 2 of 3. Use the SAME visual style, skin layer structure, colors, and proportions as the previous SVG. The nanocomplex from the reference images now appears.

SUBJECT: Cross-section showing peptide nanocarrier delivering drugs through skin and via the hair follicle pathway.

SVG STRUCTURE & ELEMENTS:

1. SKIN LAYERS (same as image 1):
   - Same stratum corneum (#D4A574), epidermis (#F5C5A3), dermis (#FDE8D0)
   - Same proportions and layer labels in Korean

2. HAIR FOLLICLE (center):
   - Same follicle structure as image 1 but with a moderately healthy hair shaft (stroke-width: 2.5, slightly thicker than image 1)
   - Sebaceous gland, dermal papilla in same positions

3. NANOCOMPLEX PARTICLES:
   Design each nanocomplex as a small composite SVG group:
   - Outer circle: r=6, fill #4CAF50 (green, peptide shell)
   - Inner circle: r=3.5, fill #1A237E (navy, middle layer)
   - Core dot: r=1.5, fill #4A90D9 (blue, drug core)

   PLACEMENT — Two pathways:

   Pathway 1 — Transepidermal (non-follicular skin):
   - 3 nanocomplexes within the EPIDERMIS layer only (between stratum corneum and dermis boundary)
   - Position them at different depths within the epidermis
   - IMPORTANT: None in the dermis in non-follicular areas
   - Small downward arrows showing penetration direction

   Pathway 2 — Transfollicular (along hair follicle) — PRIMARY route:
   - 5 nanocomplexes along the follicle canal at different depths:
     * 1 near the follicle opening (surface)
     * 1 at sebaceous gland level
     * 1 at mid-follicle (bulge region)
     * 2 near the dermal papilla (deepest)
   - Downward arrows along the follicle showing flow direction
   - This route has MORE particles than Pathway 1

4. MAGNIFIED INSET (upper-right corner):
   - A circle (r=40) with thin border, showing enlarged nanocomplex:
     * Large green outer ring (peptide shell label)
     * Navy middle ring
     * Blue core with small dots (drug molecules)
   - Thin line connecting inset to one nanocomplex in main diagram
   - Label: "나노복합체 구조"

5. PATHWAY LABELS:
   - Dashed line + label "경피 침투 (표피 도달)" for Pathway 1
   - Dashed line + label "모낭 경로 (심부 도달)" for Pathway 2

6. STYLING:
   - Same viewBox "0 0 400 500"
   - Subtle blue tint background (#F0F5FF)
   - Same flat medical diagram style as image 1

OUTPUT: Complete, valid SVG code.
```

**넣을 텍스트 (SVG 내 포함)**
- 각질층 / 표피층 / 진피층
- "경피 침투 (표피 도달)" ← 모낭 외 경로
- "모낭 경로 (심부 도달)" ← 모낭 경로
- "펩타이드 나노운반체"
- (확대 인셋) "나노복합체 구조", "외벽: 펩타이드", "코어: 약물"

---

#### A-3. 치료 효과 극대화 및 안전성 증진 (기대효과)

**GPT 입력 시**: 같은 대화에서 이어서 아래 프롬프트만 입력.

```
Now create SVG image 3 of 3. Same visual style as images 1 and 2. This is the "success/result" image.

SUBJECT: Cross-section showing successful drug delivery results — healthy thick hair regrowth, nanocomplexes concentrated at follicle targets.

SVG STRUCTURE & ELEMENTS:

1. SKIN LAYERS (same style):
   - Same colors and proportions as previous images
   - Same Korean labels

2. HAIR FOLLICLES — HEALTHY STATE:
   - 2-3 follicles visible (wider view than previous images)
   - Thick, robust hair shafts (stroke-width: 4, color #3E2723, dark brown) — visibly much thicker than images 1 and 2
   - Well-developed dermal papilla at each follicle base
   - 4-5 total hair shafts growing upward, healthy-looking

3. NANOCOMPLEX DELIVERY RESULTS:
   - Same nanocomplex design as image 2 (green/navy/blue circles)
   - Nanocomplexes concentrated around dermal papilla of each follicle (2-3 per follicle base)
   - At dermal papilla: show blue dots (r=2) dispersing OUT from the nanocomplexes — representing drug release
   - A few nanocomplexes in the epidermis (non-follicular) — but NONE in dermis between follicles
   - The dermis between follicles is CLEAN (no particles) — visually showing "no systemic spread"

4. VISUAL INDICATORS:
   - Small "burst" or "release" lines around nanocomplexes at the dermal papilla
   - Subtle glow effect (light green circle, low opacity) around target areas
   - Empty/clean dermis between follicles to emphasize targeted delivery

5. LABELS:
   - "모낭 심부 약물 방출" near dermal papilla
   - "DHT 억제 + 항염증" near follicle base
   - "전신 노출 최소화" with arrow pointing to clean dermis area
   - "모발 성장 촉진" near the thick hair shafts

6. STYLING:
   - Same viewBox "0 0 400 500"
   - Subtle green tint background (#F0FFF5)
   - Same flat style

OUTPUT: Complete, valid SVG code.
```

**넣을 텍스트 (SVG 내 포함)**
- 각질층 / 표피층 / 진피층
- "모낭 심부 약물 방출"
- "DHT 억제 + 항염증 이중 작용"
- "전신 노출 최소화"
- "모발 성장 촉진"

---

### B안 — SVG 코드 생성 프롬프트 (2장)

#### B-1. 기존 국소 투여 (좌측 모낭)

**GPT 입력 시**: 참고 이미지 4장 모두 첨부 + 아래 프롬프트.

```
I'm attaching reference images of a peptide nanocomplex. These show:
- Peptide chains (green + navy zigzag strands) self-assembling with blue drug molecules
- Final spherical nanocomplex: green outer shell, navy middle layer, blue drug core

For THIS image, the nanocomplex does NOT appear. But establish a consistent SVG style for a 2-image series. I'll ask for the second image next.

Please generate SVG code:

SUBJECT: Cross-section of scalp skin — FAILED conventional drug delivery to hair follicle.

SVG STRUCTURE:

1. SKIN LAYERS (horizontal bands):
   - Stratum corneum: #D4A574, ~15px height, clear barrier line
   - Epidermis: #F5C5A3, ~50px height
   - Dermis: #FDE8D0, ~100px height
   - Korean labels on left: 각질층, 표피층, 진피층

2. HAIR FOLLICLE:
   - Single thin, miniaturized follicle (center)
   - Weak hair shaft: stroke-width 1.5, #8B7355
   - Sebaceous gland: oval #E8C87A
   - Dermal papilla: rounded bump at base

3. DRUG MOLECULES (FAILURE):
   - 8-10 blue circles (r=3, #4A90D9) scattered ON stratum corneum surface
   - Horizontal drift arrows (gray dashed)
   - 2-3 molecules flowing along sebum path
   - NO molecules in epidermis or below
   - Red X marks at stratum corneum showing blockage
   - Empty dermal papilla area

4. LABELS:
   - "기존 국소 투여" as title at top
   - "각질층에서 차단"
   - "표면 확산·유실"
   - "피지 흐름에 의한 손실"
   - "모낭 심부: 약물 미도달"

5. STYLING:
   - viewBox "0 0 300 450" (portrait 2:3)
   - Warm coral background tint (#FFF5F0)
   - Flat medical diagram style

OUTPUT: Complete, valid SVG code.
```

---

#### B-2. 펩타이드 나노운반체 전달 (우측 모낭)

**GPT 입력 시**: 같은 대화에서 이어서 입력.

```
Now create SVG image 2 of 2. SAME style, colors, proportions as image 1. Nanocomplexes from reference images now appear.

SUBJECT: Cross-section — SUCCESSFUL peptide nanocarrier drug delivery via follicular route.

SVG STRUCTURE:

1. SKIN LAYERS (same as image 1):
   - Same colors, proportions, Korean labels

2. HAIR FOLLICLE:
   - Same structure but with thick, healthy hair shaft (stroke-width: 3.5, #3E2723)
   - 2-3 hair shafts visible, healthy regrowth
   - Well-developed dermal papilla

3. NANOCOMPLEX PARTICLES:
   Each nanocomplex = SVG group:
   - Outer: r=6, #4CAF50 (green shell)
   - Middle: r=3.5, #1A237E (navy)
   - Core: r=1.5, #4A90D9 (blue drug)

   Route 1 — Transepidermal:
   - 2-3 in epidermis ONLY (not in dermis)

   Route 2 — Transfollicular (PRIMARY):
   - 5-6 along follicle canal at different depths
   - Deepest ones at dermal papilla
   - Blue dots dispersing from nanocomplexes at papilla (drug release)
   - Downward arrows along follicle path

4. MAGNIFIED INSET (upper-right):
   - Circle showing enlarged nanocomplex structure
   - Green ring / navy ring / blue core
   - Label "나노복합체 구조"
   - Connected to main diagram with thin line

5. LABELS:
   - "펩타이드 나노운반체 전달" as title at top
   - "경피 침투 → 표피 도달"
   - "모낭 경로 → 심부 도달"
   - "약물 방출"
   - "DHT 억제 + 항염증"

6. IMPORTANT: Dermis between follicles is CLEAN — no particles. Only follicular route reaches deep.

7. STYLING:
   - Same viewBox "0 0 300 450"
   - Cool mint background tint (#F0FFF5)
   - Same flat style as image 1

OUTPUT: Complete, valid SVG code.
```

---
---

### 공통 편집 가이드 (SVG)
1. SVG 코드를 `.svg` 파일로 저장 → 브라우저에서 미리보기 확인
2. PPT에 삽입: 삽입 > 그림 > SVG 파일 선택 → 마우스 우클릭 > "도형으로 변환" → 그룹 해제 → 개별 요소 편집 가능
3. 한글 폰트가 깨지면: PPT 내에서 텍스트 요소 선택 후 폰트 변경 (Pretendard, Noto Sans KR 등)
4. A안: 3개 SVG를 가로 배치하여 하나의 모식도로 합성
5. B안: 2개 SVG를 좌우 배치
6. 색상 코드 (통일):
   - 각질층: #D4A574
   - 표피층: #F5C5A3
   - 진피층: #FDE8D0
   - 나노복합체 외벽: #4CAF50 (green)
   - 나노복합체 중간: #1A237E (navy)
   - 약물 분자: #4A90D9 (sky blue)
   - 모발 (약한): #8B7355
   - 모발 (건강): #3E2723
7. **핵심**: 하나의 GPT 대화에서 시리즈 전체를 순서대로 생성하여 스타일 일관성 확보
