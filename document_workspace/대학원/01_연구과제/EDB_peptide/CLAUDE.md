# EDB_peptide 폴더 작업 규칙

> 이 문서는 `대학원/01_연구과제/EDB_peptide/` 폴더 작업 시 자동 로드되는 규칙입니다.  
> 상위 규칙(`대학원/CLAUDE.md`) + 본 문서가 함께 적용됩니다.  
> 작성: 2026-05-11 14:16 KST

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **타겟** | ED-B Fibronectin (oncofetal domain, 종양 혈관 ECM) |
| **PDB** | 2FNB (chain A, NMR multi-model) |
| **1차 anchor** | F54 (hydrophobic patch I35/F54/I78/L80 중심) |
| **설계 컨셉** | Cyclic / Constrained surface binder (pocket binder 아님) |
| **상위 프로젝트** | 펩타이드 파이프라인 (`01_연구과제/AI 기반 펩타이드-단백질 결합 후보 예측/`) |
| **사용 코드** | `pepbind06.py` (GitHub/Study 별도 경로) |

상세 설계 사양은 `01 설계 사양/EDB_peptide_design_brief.md` 참조.

---

## 2. 폴더 구조 및 역할

| 폴더 | 역할 | 비고 |
|------|------|------|
| `00 참고 자료/` | PI 카톡, ChatGPT 리서치 캡처, 외부 자료 | 원본 보존 |
| `01 설계 사양/` | Design Brief (정적 문서) | 핵심 설계 결정만, 거의 변경 없음 |
| `02 진행 관리/` | Workplan + Opus-Sonnet 핸드오프 문서 | 운영 문서, 자주 갱신 |
| `03 구조 분석/` | 2FNB PDB, PyMOL 스크립트, 시각화 결과 | Step 1 산출물 |
| `04 파이프라인 실행/` | pepbind06_EDB 사본, 실행 결과 (.xlsx 등) | Step 2~3 산출물 |
| `05 보고 자료/` | MOE 비교, 교수님 보고용 자료 | Step 4~5 산출물 |

---

## 3. Opus-Sonnet 핸드오프 규칙 ★ 핵심

본 프로젝트는 **두 Claude 모델을 분리 사용**한다.

| 모델 | 담당 | 산출물 |
|------|------|--------|
| **Opus 섹션** | 창의적/논리적 사고, 설계, 의사결정, 핸드오프 작성 | `대화요약_to_Sonnet_*.md` (작업 지시서) |
| **Sonnet 섹션** | 실제 문서 작성, 코드 변경, 반복 실행 | `대화요약_to_Opus_*.md` (결과 보고서) |

### 3-1. 표준 워크플로우 (3-Step Loop)

```
[Opus]   작업 정의 → 핸드오프(to_Sonnet) 작성 → workplan 갱신 → 종료
                              ↓ (파일 시스템 = 공유 매체)
[Sonnet] 핸드오프 읽기 → 작업 실행 → workplan 체크박스 갱신 → 보고서(to_Opus) 작성 → 종료
                              ↓
[Opus]   보고서 + workplan 검토 → 다음 작업 정의 → 반복
```

### 3-2. 파일명 규칙 (대학원 공통 규칙 적용)

| 파일 | 형식 |
|------|------|
| Opus → Sonnet | `대화요약_to_Sonnet_[작업명]_YYYYMMDD_HHMM.md` |
| Sonnet → Opus | `대화요약_to_Opus_[작업명]_YYYYMMDD_HHMM.md` |
| Workplan | `EDB_peptide_workplan_YYYYMMDD_HHMM.md` (반복 수정 → 새 버전 저장) |

### 3-3. 템플릿 사용

| 양식 | 위치 |
|------|------|
| Opus가 작성할 때 | `02 진행 관리/_template_to_Sonnet.md` |
| Sonnet이 작성할 때 | `02 진행 관리/_template_to_Opus.md` |

→ **신규 핸드오프/보고서를 만들 때는 반드시 해당 템플릿을 복사해서 시작.** 빈 양식이 보장하는 섹션을 임의로 생략하지 말 것.

### 3-4. 섹션 시작 시 표준 프롬프트 (사용자가 매번 입력하는 한 줄)

| 섹션 | 시작 프롬프트 |
|------|--------------|
| Sonnet | "EDB_peptide 폴더의 CLAUDE.md와 최신 to_Sonnet 핸드오프를 읽고 진행해줘. 완료 후 to_Opus 보고서와 workplan 갱신." |
| Opus | "EDB_peptide 폴더의 최신 to_Opus 보고서와 workplan을 읽고 다음 단계를 설계해줘." |

---

## 4. Single Source of Truth = Workplan

- 진행 상태·체크리스트·이슈 로그·결정 기록은 **모두 workplan에 누적**한다.
- Opus와 Sonnet 모두 workplan을 갱신할 권한을 가진다.
- 핸드오프 문서는 **단일 작업 단위의 일회성 메시지**이고, 영구 기록은 workplan에 남긴다.

---

## 5. 코드 작업 시 주의사항

| 항목 | 규칙 |
|------|------|
| **메인 코드** | `pepbind06.py` (위치: `C:\Users\kbjoo\Documents\GitHub\Study\graduate_school\peptide_binding_mvp\notebooks\`) |
| **사용 금지** | `pepbind07.py` (ADCP 적용 버전, 본 시스템에 부적합) |
| **수정 방법** | EDB 전용 사본을 `04 파이프라인 실행/` 폴더에 두고 변경 (원본 보호) |
| **Conda env** | `pepbind_openmm` (Python 3.11) |
| **부위 특이성** | PepMLM은 좌표 지정 불가 → ColabFold 후처리에서 F54/I35/I78/L80 거리 필터 적용 |

---

## 6. 금지 사항

- ❌ `pepbind07.py` 사용
- ❌ Pocket binder 컨셉 (효소 억제제식 설계)
- ❌ RGD / integrin-binding motif 사용
- ❌ Brief 문서의 정적 설계 결정을 임의 변경 (PI 컨센서스 사항)
- ❌ 핸드오프 양식 없이 자유 형식으로 작업 인수인계
- ❌ Workplan 갱신 없이 작업 완료 처리

---

## 7. 변경 이력

| 일자 | 변경 내용 |
|------|----------|
| 2026-05-11 14:16 | 최초 작성 — 3-Tier CLAUDE.md 구조의 3번째 계층 신규 추가 |
