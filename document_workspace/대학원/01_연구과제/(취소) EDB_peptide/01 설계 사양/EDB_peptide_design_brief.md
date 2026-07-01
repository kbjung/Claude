# ED-B Fibronectin 타겟 펩타이드 설계 — Design Brief

> 작성일: 2026-05-11 | 보강일: 2026-05-11 04:06 KST  
> 출처: PI(정우진 교수) ChatGPT 리서치 내용 정리  
> 작업자: 김범중  
> 성격: **정적 문서 (Design Brief)** — 핵심 설계 의사결정 기록용. 진행 관리·할 일·이슈는 `02 진행 관리/EDB_peptide_workplan_*.md` 참조

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

## 6. 5-Step 큰 그림

| Step | 작업 |
|------|------|
| 1 | 2FNB 구조 분석 — I35/F54/I78/L80 hydrophobic patch 시각화 |
| 2 | 펩타이드 후보 시퀀스 생성 (PepMLM) |
| 3 | AI 파이프라인 실행 (ColabFold → Vina → PRODIGY) |
| 4 | MOE 도킹 결과와 비교 분석 |
| 5 | 교수님 보고용 비교 문서 작성 |

> 운영 디테일(체크리스트·진행 상태·이슈 로그·코드 적용 매핑)은  
> `02 진행 관리/EDB_peptide_workplan_*.md` 참조

---

## 7. 2FNB 입력 데이터 메모

| 항목 | 내용 |
|------|------|
| **PDB ID** | 2FNB |
| **구조 유형** | Solution NMR (multi-model) → 첫 번째 conformer (MODEL 1) 사용 권장 |
| **chain** | A |
| **잔기 수** | 91 aa (앞부분 MRGSE 발현 태그 포함 → 분석 시 chain A 번호 기준) |
| **서열 입력** | RCSB에서 `2FNB.pdb` 다운로드 후 chain A FASTA를 파이프라인 `TARGET_SEQUENCE`에 입력 |
| **Epitope-like seg 1** | residue 46–61 : `EGIPIFEDFVDSSVGY` (F54 포함) |
| **Epitope-like seg 2** | residue 62–76 : `YTVTGLEPGIDYDIS` |
| **Epitope-like seg 3** | residue 82–95 : `NGGESAPTTLTQQT` |

---

## 8. 기지 ED-B Binder (Tier 2 retrospective 검증 후보)

본 파이프라인의 FinalScore가 실측 결합 강도와 상관하는지 검증하기 위한 **레퍼런스 binder 후보 목록**. 해당 binder의 결합 부위·친화도 데이터를 우리 시스템 점수와 비교하여 시스템 정합성을 사전 평가한다.

| 후보 | 종류 | 비고 |
|------|------|------|
| **L19** | scFv (Philogen) | ED-B 표적 임상 시험 진입 항체. 구조·친화도 데이터 풍부 |
| **BC-1** | mAb | ED-B 인접 영역 결합. ED-B-FN 전반 검증용 baseline |
| **AP39 / 기타 항체** | mAb | 검토 필요 — 추후 PDB 데이터 확보 시 추가 |

> **주의**: 본 표는 후보군 명단이며 실제 사용 가능한 PDB·친화도 데이터 확보 여부는 별도 조사 필요. 진행 상황은 workplan 문서에 기록.

---

## 9. 참고 메모

- **PI 지시 (2026-05-11 카톡)**: ChatGPT 리서치 결과 공유 + AI 파이프라인 적용 타당성 검토 요청
- 2FNB NMR 구조 → multiple conformer 존재 → MODEL 1 사용 권장
- PepMLM은 부위 특이성 직접 지정 불가 → ColabFold 결과에서 F54 patch 접촉 잔기 후처리 필터 필요
- PRODIGY는 단백질-단백질 학습 모델 → 펩타이드-단백질 외삽 한계 존재 (모델별_검증근거_정리 7.4절)
- 본 파이프라인 학술적 근거: `09_ai/...` 또는 `01_연구과제/AI 기반 펩타이드.../02 파이프라인 모델 설명서/모델별_검증근거_정리_20260508_2042.docx`
