# ED-B Fibronectin 타겟 펩타이드 설계 — 초기 리서치 정리

> 작성일: 2026-05-11 | 출처: PI(정우진 교수) ChatGPT 리서치 내용 정리  
> 작업자: 김범중 | 파일 생성: EDB_peptide_design_brief.md (최초 버전)

---

## 1. 타겟 단백질 요약

| 항목 | 내용 |
|------|------|
| **타겟** | ED-B domain of Fibronectin (Extra Domain B) |
| **PDB ID** | 2FNB (Human fibronectin ED-B domain, NMR 구조) |
| **도메인 특성** | Fibronectin에 alternative splicing으로 삽입되는 **oncofetal domain** |
| **발현 패턴** | 정상 성인 조직: 거의 미발현 / 종양 혈관 신생 조직: 고발현 → 종양 특이성 高 |
| **표면 특성** | 전체적으로 **산성(acidic) 표면**, 예외적으로 노출된 소수성 패치(hydrophobic patch) 존재 |
| **임상 의의** | Angiogenesis marker로 알려짐; 3종의 monoclonal antibody가 ED-B 표면에 결합 (in vivo accessible) |
| **주의사항** | 2FNB 서열 앞쪽에 MRGSE 태그 포함 → 논문/UniProt 번호와 PDB 번호 불일치 가능; **PDB chain A 번호 기준** 사용 |

---

## 2. 1순위 타겟: Solvent-Exposed Hydrophobic Patch

ED-B 표면에서 **특이적 recognition site**로 보고된 소수성 패치.

### 핵심 잔기 (2FNB PDB chain A numbering)

| 잔기 | 단일문자 | 역할 |
|------|----------|------|
| **Ile35** | I | 소수성 패치 구성 |
| **Phe54** | F | **Primary anchor** ★ |
| **Ile78** | I | 소수성 패치 구성 |
| **Leu80** | L | 소수성 패치 구성 |

### F54가 Primary Anchor인 이유

- Epitope-like segment 1 (46–61) **안에 위치**하여 hydrophobic patch와 antibody epitope 영역이 겹침
- 구조 기반 docking의 **1차 anchor**로 가장 적합
- F54 중심 + I35/I78/L80 보조 contact + 주변 산성 잔기 보완 전략이 설계 우선순위

---

## 3. 2순위 타겟: Antibody Epitope-like Segments

RCSB 설명에 따르면 ED-B에 결합하는 monoclonal antibody 3종의 epitope 인접 영역.  
> 세 segment는 서로 반대 면에 위치 → 한 항체가 동시에 인식하는 epitope가 아닌, **구조상 별도 표면 후보**로 접근

| Segment | Residue Range | Sequence |
|---------|---------------|----------|
| **Epitope-like segment 1** | 46–61 | `EGIPIFEDFVDSSVGY` |
| **Epitope-like segment 2** | 62–76 | `YTVTGLEPGIDYDIS` |
| **Epitope-like segment 3** | 82–95 | `NGGESAPTTLTQQT` |

---

## 4. 펩타이드 설계 방향

### 컨셉: Surface Binder (ECM Retention)

> EDB-FN 결합 펩타이드는 "효소 억제제"처럼 깊은 pocket에 꽂는 방식이 아니라,  
> **tumor ECM에 붙어 retention을 주는 surface binder**로 설계

### 추천 형태

| 형태 | 이유 |
|------|------|
| **Cyclic peptide** | EDB 표면은 넓고 얕음 → 선형 펩타이드는 진화도/선택성↓ |
| **Constrained peptide** | 구조 고정으로 entropy penalty 감소 |
| **Stapled peptide** | 알파-헬릭스 고정, hydrocarbon staple 등 |

### 설계 컨셉 요약

```
[중앙부] Hydrophobic residues → ED-B hydrophobic patch anchoring (F54 중심)
[주변부] Lys / Arg / His    → 산성 표면과 electrostatic complementarity
[구조화] Cyclization / Disulfide / Stapling → entropy penalty 감소
[목적]   강한 signaling 조절이 아닌 tumor vascular ECM retention
```

---

## 5. 피해야 할 방향

| 방향 | 이유 |
|------|------|
| **Fibronectin 전체에 붙는 펩타이드** | 정상 ECM에도 결합 → 선택성 저하 |
| **RGD / integrin-binding motif** | 너무 비특이적 |
| **Collagen/fibronectin generic binder** | Tumor selectivity 약화 |

---

## 6. 다음 단계 액션 플랜

| 단계 | 작업 내용 | 도구 / 방법 |
|------|-----------|-------------|
| **Step 1** | 2FNB 구조 분석 — I35/F54/I78/L80 hydrophobic patch 시각화 | PyMOL / UCSF ChimeraX |
| **Step 2** | 펩타이드 후보 시퀀스 생성 | **PepMLM** (언어모델 기반 생성) |
| **Step 3** | AI 파이프라인 실행 | ColabFold (구조 예측) → AutoDock Vina (도킹) → PRODIGY (결합 에너지) |
| **Step 4** | MOE 결과와 비교 분석 | 기존 MOE 도킹 결과 vs. AI 파이프라인 결과 비교 |
| **Step 5** | 교수님 보고용 비교 문서 작성 | 결과 정리 보고서 (.pptx / .docx) |

### Step 1 세부 체크리스트 (2FNB 구조 분석)

- [ ] RCSB에서 2FNB PDB 파일 다운로드
- [ ] PyMOL에서 chain A 로드
- [ ] I35, F54, I78, L80 선택 → surface 모드로 hydrophobic patch 시각화
- [ ] Epitope-like segment 1 (46–61) 위치 확인 및 F54 overlap 검증
- [ ] 표면 electrostatic potential map 생성 (APBS 플러그인)

---

## 7. 참고 메모

- **PI 지시 (2026-05-11 카톡)**: ChatGPT 리서치 결과를 공유하며 AI 파이프라인 적용 타당성 검토 요청
- 2FNB NMR 구조이므로 multiple conformer 존재 → representative model (MODEL 1) 사용 권장
- PepMLM 시퀀스 생성 시 cyclic backbone 제약 조건 명시 필요
- PRODIGY 결합 에너지 예측은 crystal 구조 기반 최적화 도구 → NMR 구조 적용 시 결과 해석 주의
