# ED-B Fibronectin 펩타이드 설계 — Workplan

> 작성일: 2026-05-11 04:06 KST | 버전: v1 (최초 작성)  
> 이전 버전: 없음  
> 작업자: 김범중  
> 성격: **동적 운영 문서** — 진행 상태·할 일·코드 적용·이슈·결정 로그.  
> 정적 설계 사양은 `01 설계 사양/EDB_peptide_design_brief.md` 참조.

---

## 1. 현재 상태 요약

| 항목 | 상태 |
|------|------|
| 단계 | **Step 1 — 2FNB 구조 분석 준비 중** |
| Brief 작성 | ✅ 완료 (2026-05-11) |
| Workplan 작성 | ✅ 본 문서 (2026-05-11) |
| PI 컨센서스 | 카톡으로 ED-B FN 타겟 확정 (2026-05-11) |
| 다음 마일스톤 | 2FNB PDB 시각화 및 hydrophobic patch 검증 |

---

## 2. pepbind06.py — EDB 적용 변경 포인트

> 현재 `pepbind06.py`는 PD-L1 타겟·4-mer·50개 후보로 세팅되어 있음.  
> 아래 변수만 EDB용으로 교체하면 1차 실행 가능.

### 2-1. 입력/하이퍼파라미터 변경

| 변수 | 현재값 (PD-L1) | EDB용 권장값 | 메모 |
|------|---------------|-------------|------|
| `TARGET_SEQUENCE` | PD-L1 220 aa | **2FNB chain A 91 aa** | RCSB에서 PDB 다운 후 chain A FASTA 추출 |
| `PEPTIDE_LENGTH` | 4 | **8~14** | 4-mer는 patch (I35/F54/I78/L80) 동시 접촉 어려움 |
| `NUM_PEPTIDES` | 50 | **150~300** | 부위 특이성 미지원 → 다수 생성 + 후처리 필터 |
| `PEPMLM_TOP_K` | 10 | 10 (유지) | 1차 실행 후 다양성 부족하면 15~20으로 상향 |
| `PEPMLM_TEMPERATURE` | 1.0 | 1.0 (유지) | 동상 |
| `MAX_RETRY_ROUNDS` | 3 | 3 (유지) | NMR multi-model 환경에서 GBSA 실패 가능성 ↑ |

### 2-2. FinalScore 가중치 — 변경 없음

```
FinalScore = 0.50 × PRODIGY + 0.25 × Vina + 0.15 × PLIP(보조) + 0.10 × ipTM
※ pepbind06.py 기본값 그대로 사용. EDB 데이터 누적 후 v2에서 조정 검토.
```

> 주의: `모델별_검증근거_정리_20260508_2042.docx` 기준 PLIP은 보조지표이며,  
> 실 코드는 0.50/0.25/0.15/0.10 (또는 v2: 0.60/0.30/0/0.10) 중 운영본 확인 필요.

---

## 3. 부위 특이성 후처리 (신규 추가 필요)

PepMLM은 "F54에 결합" 식의 좌표 지정 불가 → ColabFold 결과에서 후처리 필터 추가.

| 위치 | 추가 로직 | 통과 기준 |
|------|----------|----------|
| STEP 3 후 (3.5 신규) | 펩타이드 ↔ **F54 / I35 / I78 / L80** 잔기 간 최소 거리 산출 | 최소 거리 ≤ 5 Å인 후보만 통과 |
| STEP 5 (PLIP) 활용 | hydrophobic 접촉 페어 좌표가 patch 영역에 위치하는지 검증 | F54 hydrophobic 접촉 ≥ 1개 |
| STEP 6 (PRODIGY) | 통과 후보만 ΔG 계산 (자원 절약) | — |

> 구현 위치: `pepbind06.py`의 STEP 3 ColabFold 출력 처리 직후, `Bio.PDB`로 거리 계산 함수 신규 작성.  
> Step 1 시각화 결과로 patch 영역을 정확히 확인한 뒤 잔기 번호 재검증할 것.

---

## 4. 5-Step 액션 플랜 + 세부 체크리스트

### Step 1. 2FNB 구조 분석 (현재 단계)

- [ ] RCSB에서 `2FNB.pdb` 다운로드 → `03 구조 분석/raw/`
- [ ] PyMOL/ChimeraX로 chain A 로드 (MODEL 1 사용)
- [ ] I35 / F54 / I78 / L80 surface mode 시각화
- [ ] Epitope-like segment 1 (46–61) 영역 표시 및 F54 overlap 검증
- [ ] APBS plugin으로 electrostatic potential map 생성 (산성 표면 확인)
- [ ] chain A FASTA 추출 → workplan 부록 또는 `03 구조 분석/2FNB_chainA.fasta` 저장
- [ ] 시각화 이미지 저장 → `03 구조 분석/figures/`

### Step 2. 펩타이드 후보 시퀀스 생성 (PepMLM)

- [ ] `pepbind06.py` 사본을 `04 파이프라인 실행/`에 복사 (`pepbind06_EDB_v1.py` 등)
- [ ] 2-1 표대로 변수 교체
- [ ] PepMLM 실행 (NUM_PEPTIDES=200, PEPTIDE_LENGTH=10 1차안)
- [ ] 출력 서열 저장 → `04 파이프라인 실행/run01/peptide_candidates.csv`

### Step 3. AI 파이프라인 실행 (ColabFold → Vina → PRODIGY)

- [ ] ColabFold 멀티머 실행 (Colab Pro+ 또는 로컬 RTX 3070)
- [ ] OpenMM 정제 (GBSA > 100 인 후보 자동 재시도)
- [ ] **부위 필터 후처리** (3장 참조)
- [ ] Vina score_only / PLIP / PRODIGY 실행
- [ ] FinalScore 산출 → `04 파이프라인 실행/run01/results.xlsx`

### Step 4. MOE 결과와 비교 분석

- [ ] 기존 MOE 도킹 결과 위치 확인 (PI에게 요청 필요)
- [ ] 비교 메트릭 정의: 결합 잔기 일치도 / 도킹 score 상관 / Top-N overlap
- [ ] 비교 표 작성 → `05 보고 자료/EDB_MOE_vs_AI_compare_*.xlsx`

### Step 5. 교수님 보고용 비교 문서

- [ ] PPT 또는 docx 보고서 초안 작성
- [ ] 핵심 figure: 2FNB patch 시각화 / FinalScore Top-10 / MOE-AI 비교
- [ ] PI 컨펌 후 본 보고

---

## 5. 검증 전략 — `모델별_검증근거_정리.docx` Tier 매핑

| Tier | 정의 | EDB 프로젝트 적용 |
|------|------|-----------------|
| Tier 1 | 각 모델 단독 신뢰성 | docx로 완료 |
| **Tier 2** | 기지 복합체 retrospective | L19 / BC-1 등 ED-B 항체 PDB로 FinalScore 상관 검증 |
| Tier 3 | End-to-end wet-lab | 본 파이프라인 EDB 후보 합성 + SPR/BLI 측정 |

> EDB는 기지 binder가 다수 존재 → **Tier 2 retrospective benchmark 후보로 적합**.  
> docx 10.3절 권장 단기 과제(1~2개월)와 직접 정합.

---

## 6. 이슈 / 결정 로그

| 일자 | 분류 | 내용 |
|------|------|------|
| 2026-05-11 | 결정 | 타겟: ED-B FN, PDB 2FNB, chain A 번호 기준 사용 |
| 2026-05-11 | 결정 | 1차 anchor: F54, 보조 contact: I35/I78/L80 |
| 2026-05-11 | 결정 | 설계 컨셉: cyclic / constrained surface binder (pocket binder ✗) |
| 2026-05-11 | 이슈 | PepMLM 부위 특이성 미지원 → 후처리 거리 필터로 대응 |
| 2026-05-11 | TODO | MOE 기존 결과 위치/포맷 PI 확인 필요 |

---

## 7. 다음 마일스톤

| 시점 | 마일스톤 |
|------|---------|
| 1주 이내 | Step 1 완료 (2FNB patch 시각화) |
| 2주 이내 | Step 2~3 1차 실행 (Top-10 후보 도출) |
| 3~4주 | Step 4 MOE 비교 |
| 1개월 내 | Step 5 PI 보고 (간이 보고서) |
| 1~2개월 | Tier 2 retrospective benchmark 별도 진행 |

---

## 8. 참고 자료

### 8-1. 본 프로젝트 폴더 내

| 자료 | 위치 |
|------|------|
| 설계 사양 (Brief) | `01 설계 사양/EDB_peptide_design_brief.md` |
| PI 카톡 | `00 참고 자료/KakaoTalk_20260511_002343758.png` |
| ChatGPT 리서치 1 (타겟 사이트) | `00 참고 자료/Snipaste_2026-05-11_00-26-28.png` |
| ChatGPT 리서치 2 (PDB residue 분석) | `00 참고 자료/Snipaste_2026-05-11_00-26-42.png` |

### 8-2. 외부 코드 저장소 (★ 중요)

| 자료 | 위치 |
|------|------|
| **펩타이드 파이프라인 코드 폴더** | `C:\Users\kbjoo\Documents\GitHub\Study\graduate_school\peptide_binding_mvp\notebooks\` |
| **현재 운영 최신 버전** | `pepbind06.py` ★ (앞으로 코드 업데이트는 이 폴더에 저장) |
| 사용 안 함 | `pepbind07.py` (ADCP 모듈 적용 버전 — 본 시스템에 부적합 판단) |
| 가이드 문서 | `GUIDE_pepbind06.md` |
| Conda env 정의 | `pepbind_full.yml`, `pepbind_min.yml` |
| 파이프라인 운영 규칙 | `RULES.md` |
| 인수인계 컨텍스트 | `reports/handover_context.md` |

### 8-3. 외부 검증 자료

| 자료 | 위치 |
|------|------|
| 파이프라인 검증 보고서 | `01_연구과제/AI 기반 펩타이드.../02 파이프라인 모델 설명서/모델별_검증근거_정리_20260508_2042.docx` |
| GBSA 이상값 조사 | `01_연구과제/AI 기반 펩타이드.../07 클로드 인수인계 문서/GBSA_이상값_조사_보고서_(2차_분석).pdf` |

---

## 9. Claude 모델 분리 정책 (Opus ↔ Sonnet 협업)

| 모델 | 담당 |
|------|------|
| **Opus (현재 섹션)** | 창의적/논리적 사고, 설계, 의사결정, 핸드오프 작성 |
| **Sonnet (별도 섹션)** | 실제 문서 작성·코드 변경·반복 작업 실행 |

> 두 섹션 간 소통은 **본 폴더의 마크다운 파일을 공유 매체**로 사용.  
> Opus 핸드오프 → `02 진행 관리/대화요약_to_Sonnet_*.md`  
> Sonnet 보고 → `02 진행 관리/대화요약_to_Opus_*.md`  
> Workplan(본 문서)을 single source of truth로 동기화.

---

## 10. 변경 이력

| 일자 | 버전 | 변경 내용 |
|------|------|----------|
| 2026-05-11 04:06 | v1 | 최초 작성 |
| 2026-05-11 | v1 보강 | 외부 코드 저장소 위치(GitHub/Study 경로) + pepbind06=최신 / pepbind07 미사용 정책 / Opus-Sonnet 모델 분리 정책 추가 |
