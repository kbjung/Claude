# 기술 모식도 A안 — AI 이미지 생성 프롬프트

> **총 6개 프롬프트**: 행1-좌 3장 + 행1-우 3장 (각각 개별 생성)
> **텍스트는 AI가 아닌 PPT에서 직접 입력** (한국어 깨짐 방지)

---

## 사용 방법

### 나노바나나2
1. 나노바나나2 열기
2. 아래 프롬프트를 **그대로** 복사 → 붙여넣기
3. 생성된 이미지 다운로드
4. PPT에서 해당 위치에 삽입 → 위에 텍스트 오버레이

### ChatGPT (GPT-4o)
1. ChatGPT 열기
2. **"아래 설명대로 이미지를 만들어줘"** 라고 먼저 입력
3. 바로 이어서 아래 프롬프트 붙여넣기
4. 생성된 이미지 다운로드

### 공통 팁
- 비율: **정사각형 (1:1)** 권장 (PPT에서 3개를 나란히 배치)
- 결과가 마음에 안 들면: "좀 더 심플하게" / "플랫 디자인으로" / "배경을 흰색으로" 등 추가 요청

---

## 행1-좌: 기존 탈모 치료의 구조적 한계 (3장)

> 창업선도대학 계획서 "나. 연구개발 대상 기술·제품의 필요성" 중 **기존 탈모 치료의 구조적 한계** 파트 기반

### 프롬프트 1-1: 경구 Finasteride의 한계

```
A clean medical infographic icon on a light pink background (#fce4ec). An oral pill/capsule in the center with red warning arrows radiating outward toward a faded human body silhouette, representing systemic side effects spreading throughout the entire body from oral medication. Small red caution symbols near the body's head and lower body areas. The concept is: oral drug causes unwanted systemic exposure beyond the target area.

Style: Clean flat design, minimal medical infographic, soft pastel pink/red tones, professional scientific presentation style. NO text, NO labels, NO words anywhere. Square format (1:1 ratio).
```

### 프롬프트 1-2: Minoxidil 외용제의 한계

```
A clean medical infographic icon on a light pink background (#fce4ec). A topical dropper bottle applying liquid onto a simplified scalp cross-section. The liquid pools on the skin surface and does NOT penetrate down to the hair follicle below. A red "X" mark showing the drug is blocked at the surface layer. The hair follicle deep below remains unreached. The concept is: topical treatment that cannot reach the target (hair follicle) and has no mechanism to inhibit DHT.

Style: Clean flat design, minimal medical infographic, soft pastel pink/red tones, professional scientific presentation style. NO text, NO labels, NO words anywhere. Square format (1:1 ratio).
```

### 프롬프트 1-3: 핀쥬베(국소 Fin)의 한계

```
A clean medical infographic icon on a light pink background (#fce4ec). A spray bottle misting solution onto a scalp surface cross-section. The solution forms a thin polymer film/coating sitting ONLY on the very top surface of the skin. A dotted arrow pointing downward from the film toward the hair follicle deep below is BLOCKED — the film has no ability to push the drug deeper. The polymer layer just sits on the surface. The concept is: a carrier that only increases surface retention but cannot deliver drugs deep into the follicle and has no therapeutic function itself.

Style: Clean flat design, minimal medical infographic, soft pastel pink/red tones, professional scientific presentation style. NO text, NO labels, NO words anywhere. Square format (1:1 ratio).
```

---

## 행1-우: 경피 전달 기술 기반 차세대 치료 전략의 필요성 (3장)

> **핵심 관점**: "우리 기술이 이렇게 좋다"(차별점)가 아니라 **"기존 한계를 극복하려면 이런 기능이 필요하다"(필요성/당위성)**
> - 좌측 한계 ↔ 우측 필요성이 1:1 대응
> - 창업선도대학 계획서 "경피 전달 기술 기반 차세대 치료 전략의 필요성" 파트 기반

### 프롬프트 2-1: 모낭 심부까지 약물을 전달하는 경피 전달 기술 필요

> 대응 한계: 경구 Fin → 전신 노출 / Minoxidil → 표면 체류

```
A clean medical infographic icon on a light blue background (#e3f2fd). A simplified scalp cross-section showing clear skin layers (epidermis at top, dermis in middle, hair follicle bulb at bottom). A series of small blue arrow-shaped particles traveling DOWN through all layers, successfully reaching the hair follicle bulb (dermal papilla) at the very bottom. The penetration path is highlighted with a glowing blue trail. A green checkmark at the bottom near the follicle. The concept is: a delivery technology that can penetrate through the skin barrier and reach deep into the hair follicle is NEEDED.

Style: Clean flat design, minimal medical infographic, soft pastel blue/green tones, professional scientific presentation style. NO text, NO labels, NO words anywhere. Square format (1:1 ratio).
```

### 프롬프트 2-2: 전신 노출 없이 국소에만 작용하는 전달 시스템 필요

> 대응 한계: 경구 Fin → 전신 부작용 (성기능 저하 등)

```
A clean medical infographic icon on a light blue background (#e3f2fd). A split comparison showing the NEED for localized treatment. LEFT HALF: a human body silhouette with red ripple/wave lines spreading throughout the entire body from head to toe (representing systemic drug exposure — the problem). RIGHT HALF: the same human body silhouette but clean and healthy, with ONLY a small blue glowing circle on the scalp area where treatment is applied locally — the rest of the body is completely unaffected. A blue arrow pointing from left to right, showing the desired transition. The concept is: a localized delivery system that confines drug action to the scalp without systemic exposure is NEEDED.

Style: Clean flat design, minimal medical infographic, soft pastel blue/green tones, professional scientific presentation style. NO text, NO labels, NO words anywhere. Square format (1:1 ratio).
```

### 프롬프트 2-3: 운반체 자체가 치료 기능을 갖는 carrier-free 전략 필요

> 대응 한계: 핀쥬베 → 고분자가 표면 체류만 증가, 자체 치료능 없음

```
A clean medical infographic icon on a light blue background (#e3f2fd). A split comparison showing the NEED for a therapeutic carrier. LEFT HALF: a simple hollow sphere/capsule (representing a conventional passive carrier) that is empty and gray — it just holds the drug with no therapeutic value of its own. A small red minus sign nearby. RIGHT HALF: the same sphere/capsule shape but now filled with green/blue healing glow radiating outward — the carrier itself emits therapeutic energy (anti-inflammatory aura). A drug molecule is attached to it AND the carrier glows independently. A blue arrow pointing from left to right showing the needed upgrade. The concept is: a carrier-free strategy where the delivery material itself has intrinsic therapeutic activity (not just a passive vehicle) is NEEDED.

Style: Clean flat design, minimal medical infographic, soft pastel blue/green tones, professional scientific presentation style. NO text, NO labels, NO words anywhere. Square format (1:1 ratio).
```

---

## PPT 편집 가이드

### AI 이미지 삽입 후 텍스트 오버레이

행1-좌 (기존 탈모 치료의 구조적 한계) — 각 아이콘 아래 텍스트:

| 위치 | 라벨 (볼드) | 설명 |
|------|-----------|------|
| 좌측 | 경구 Finasteride | 전신 노출에 따른 성기능 저하, 내분비계 이상 등 부작용 → 장기 복용 중단율 높음 |
| 중앙 | Minoxidil 외용제 | 비기전적 치료제 (DHT 미억제), 중단 시 효과 소실, 모낭 심부 도달 제한 |
| 우측 | 핀쥬베 (국소 Fin) | 고분자의 역할이 두피 표면 체류 증가에 국한, 모낭 심부 전달 및 자체 치료능 없음 |

행1-우 (경피 전달 기술 기반 차세대 치료 전략의 필요성) — 각 아이콘 아래 텍스트:

> **관점**: "~가 필요하다" (필요성/당위성). 좌측 한계와 1:1 대응.

| 위치 | 대응 한계 | 라벨 (볼드) | 설명 |
|------|---------|-----------|------|
| 좌측 | 경구 Fin / Minoxidil | 모낭 심부까지 도달하는 경피 전달 기술 필요 | 물리적 자극 없이 표피→진피→모유두까지 약물 직접 전달 |
| 중앙 | 경구 Fin 전신 부작용 | 전신 노출 없는 국소 전달 시스템 필요 | 두피에만 작용, 전신순환 유입 최소화 → 부작용 구조적 배제 |
| 우측 | 핀쥬베 (수동적 운반체) | 운반체 자체가 치료 기능을 갖는 소재 필요 | 기존 나노운반체의 비효율성 극복 → carrier-free delivery 전략 |

### PPT 도형으로 직접 만드는 파트

| 파트 | 만드는 방법 |
|------|-----------|
| 타이틀 바 | 사각형 도형 (진한 남색 #16213e) + 흰색 볼드 텍스트 |
| 행1 섹션 라벨 | 좌: "❌ 기존 탈모 치료의 구조적 한계" / 우: "✅ 경피 전달 기술 기반 차세대 치료 전략의 필요성" |
| 중간 연결 바 | 사각형 도형 (진한 남색) + "▼ 한계 극복을 위한 솔루션: 펩타이드 기반 이중기능 경피 전달 시스템 ▼" |
| 하단 3단계 번호 | 원형 도형 안에 ①②③ + 단계 제목 + 설명 텍스트 + 화살표(➤) |
| 하단 파이프라인 바 | 사각형 3칸: 🧬 탈모 치료제 | 🧫 피부암 치료제 | 🧴 비의약 두피케어 |

### 솔루션 파트 (행2~3) 내용 점검

> 솔루션은 **행1의 필요성을 충족시키는 3단계 기술 검증**으로 구성되어야 함

| 단계 | 현재 PPT 내용 | 적절성 | 수정 제안 |
|------|-------------|--------|---------|
| ① 경피 전달 (Delivery) | 피부 투과 펩타이드가 finasteride를 모낭 심부까지 직접 전달 | ✅ 적절 | — (유지) |
| ② 이중 기능 (Dual-function) | 운반체 펩타이드 자체가 항염 치료 활성 발휘하여 finasteride와 시너지 | ✅ 적절 | — (유지) |
| ③ 치료 효능 (Efficacy) | 경구 대비 1/40 투여량으로 Minoxidil 동등 이상 효능 | ✅ 적절 | — (유지) |
| 피부암 적응증 확장 | (현재 별도 칸으로 존재) | ⚠️ 검토 | 플랫폼 투트랙 전략이므로 파이프라인 바에서 표현하는 것이 적절. 솔루션 흐름(①→②→③)과 별개 |

### 실제 실험 이미지 삽입 (기존 데이터)

| 위치 | 삽입할 이미지 | 출처 |
|------|------------|------|
| 행3-① 경피 전달 | 피부투과 형광 이미지 (표피→진피 투과 확인) | 논문 (2023 Self-Assembled SPP, Figure 6) / 이노베어 |
| 행3-② 이중기능 | 모유두 세포 내부 전달 확인 이미지 | 논문 (2026 Topical Carrier-Free, Figure 3c) |
| 행3-③ 치료 효능 | 모발 성장 효능 비교 그래프 | 논문 (2026 Topical Carrier-Free, Figure 4b/4c) |
