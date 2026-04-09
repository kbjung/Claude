# Gamma 프롬프트 (복사해서 입력)

---

## 프롬프트

Create a **lab meeting presentation** in **Korean** about an AI-based peptide-protein binding prediction system. Use a **clean, modern scientific/biotech style** with dark navy or teal tones. 15 slides total.

**All slide content must be in Korean.** Use the exact text below for each slide.

---

### Slide 1 – Title
- Title: AI 기반 단백질 결합 펩타이드 후보 예측 시스템
- Subtitle: 랩미팅 발표자료
- Author: 김범중 | 2026.03.23

### Slide 2 – Pipeline Overview (시스템 개요)
- Subtitle: 타겟 단백질에 특이적으로 결합하는 펩타이드 후보군을 AI 파이프라인으로 자동 도출
- Show a **horizontal process flow** with 6 steps and icons:
  1. PepMLM → 펩타이드 생성
  2. ColabFold → 구조 예측
  3. OpenMM → 구조 안정화
  4. Vina → 결합 평가
  5. PLIP → 상호작용 분석 (보조 지표 표시)
  6. PRODIGY → 친화도 예측
- Footer: 재시도: GBSA > 100 복합체 → ColabFold부터 최대 3회 재실행 | 출력: Excel(FinalScore 랭킹) + PDB zip

### Slide 3 – Model Summary (모델 요약)
- Title: 파이프라인 구성 모델 요약
- Table with columns: 모델 | 역할 | 논문/저널 | 신뢰도 근거
  - PepMLM | 타겟 서열 기반 펩타이드 후보 생성 | Nature Biotechnology 2025 | RFdiffusion 대비 히트율 우위 (38% vs 29%)
  - ColabFold | 단백질-펩타이드 복합체 3D 구조 예측 | Nature Methods 2022 | AF-Multimer 정확도 + MMseqs2 속도
  - OpenMM | 예측 구조의 물리적 안정화 | PLoS Comput. Biol. 2017 | AlphaFold2도 동일 AMBER relaxation 적용
  - AutoDock Vina | 결합 안정성 에너지 평가 (score_only) | J. Comput. Chem. 2010 | 37,000+ 인용, 가상 스크리닝 표준
  - PLIP | 상호작용 정성 분석 (보조 지표) | Nucleic Acids Res. 2015 | 2025 업데이트: PPI 분석 기능 추가
  - PRODIGY | 결합 친화도 예측 (ΔG, Kd) | Bioinformatics 2016 | Pearson r=0.73, RMSE=1.89 kcal/mol
- Note: PLIP은 FinalScore에서 제외 (보조 지표). 상세 근거는 다음 슬라이드 참조

### Slide 4 – Code Changes (pepbind06 변경 사항)
- Title: pepbind06 변경 사항
- Subtitle: pepbind05.py → pepbind06.py (2026.03.20)
- 3 numbered sections with before/after format:
  1. **Vina → score_only 모드**: 변경 전: 도킹(포즈 탐색) 수행 → 변경 후: score_only로 기존 구조 재점수화. 근거: 복합체 구조는 ColabFold + OpenMM으로 이미 확정
  2. **PLIP → 보조 지표로 전환**: 변경 전: FinalScore에 15% 가중치 → 변경 후: FinalScore에서 제외. 근거: 정성 도구, 정량 점수화 선행 사례 없음 (교수님 승인)
  3. **ADCP(CrankPep) STEP 4b 추가**: 변경 전: 해당 없음 → 변경 후: 펩타이드 전용 도킹 비교 평가용 추가 (기본 비활성화). 근거: Vina의 펩타이드 도킹 한계 보완

### Slide 5 – PLIP Exclusion Rationale (PLIP 제외 근거)
- Title: PLIP 제외 근거
- Subtitle: 왜 FinalScore에서 PLIP을 제외했는가?
- 3 cards/columns with icons:
  1. 정성 분석 도구: PLIP은 결합 패턴 탐지(정성)를 위해 설계됨. 정량 점수화에 대한 학술적 선행 사례 없음
  2. 면적 정보 손실: 소수성 결합 클러스터링 과정에서 접촉 면적 정보가 소실되어 점수화에 부적합
  3. 가중치 산정 불가: 결합 종류별 에너지 기여도를 정량적으로 산정할 근거 부족
- Conclusion: PLIP은 보조 지표(결합 분포 참고용)로 전환. 주영님 논의 + 교수님 승인 완료 (2026.03.10)

### Slide 6 – FinalScore Formula (현재 FinalScore)
- Title: 현재 FinalScore
- Show the formula prominently: FinalScore = 0.60 × norm(PRODIGY) + 0.30 × norm(Vina) + 0.10 × norm(ipTM)
- 3 metric cards:
  - PRODIGY 60%: 결합 친화도 (ΔG, Kd), 정규화 범위 [-20, 0] kcal/mol
  - Vina 30%: 결합 안정성 스코어, 정규화 범위 [-15, 0] kcal/mol
  - ipTM 10%: 구조 예측 신뢰도, 정규화 범위 [0, 1]
- Footer: 보조 지표 (FinalScore 미반영): PLIP (상호작용 정성 분석) | ADCP (펩타이드 전용 도킹, 비교 평가용)

### Slide 7 – Future Plan: ADCP Optimization (향후 계획)
- Title: 향후 계획: ADCP 기반 가중치 최적화
- Subtitle: 목표: FinalScore만으로 MOE GBVI 수준의 후보 선별력 확보 (유료 SW 의존 제거)
- **Horizontal 5-step process flow**:
  1. ADCP 도입, 후보군 랭킹 산출
  2. MOE GBVI 랭킹과 비교
  3. 경향성(상관성) 확인
  4. ADCP를 기준값(ground truth) 설정
  5. ML로 FinalScore 가중치 최적화
- Conclusion: FinalScore 랭킹 ≈ GBVI 랭킹 → MOE(유료 SW) 없이 동등한 후보 선별 가능

### Slide 8 – Timeline (타임라인)
- Title: 향후 계획: 타임라인
- Table: 단계 | 내용 | 담당 | 상태
  - 1단계 | ADCP 환경 구축 + 코드 수정 + 테스트 | 범중 | 진행 중
  - 2단계 | ADCP 결과 전달 → MOE로 GBVI 값 산출 | 주영님 | 대기
  - 3단계 | ADCP 랭킹 vs GBVI 랭킹 상관성 비교 | 범중 + 주영님 | 대기
  - 4단계 | ML 가중치 튜닝 (18-mer 200개 샘플) | 범중 | 대기
  - (장기) | MSA 직접 설정, 다중 타겟 대응 등 | - | 추후 검토
- Note: 현재 ADCP 환경 구축 및 코드 수정 테스트 중

### Slide 9 – Q&A
- Title: Q&A / 논의
- 논의 포인트:
  - ADCP-GBVI 상관성 확인 후 가중치 재배분 방향
  - ML 가중치 튜닝 시 학습 데이터 구성 (18-mer 200개)
  - 고도화 항목 우선순위

### Slide 10 – Backup: PepMLM
- Title: PepMLM 상세
- Key-value layout:
  - 모델 기반: ESM-2 마스크드 언어 모델
  - 작동 원리: 타겟 서열 뒤에 [MASK] 토큰을 붙여 펩타이드 서열을 위치별로 예측
  - 샘플링: top-k 필터링 + temperature 스케일링
  - 품질 관리: 표준 20개 아미노산만 허용, 중복 자동 제거
  - 선택 근거: 구조 정보 없이 서열만으로 생성 가능. RFdiffusion 대비 히트율 우위 (38% vs 29%)
  - 논문: Nature Biotechnology 2025

### Slide 11 – Backup: ColabFold
- Title: ColabFold 상세
- Key-value layout:
  - 모델 기반: AlphaFold-Multimer v3 + MMseqs2 MSA
  - 주요 설정: num-recycle 9, model-type alphafold2_multimer_v3, max-msa 256:512
  - 신뢰도 지표: ipTM(인터페이스 정확도), pTM(전체 구조), pLDDT(잔기별), PAE(거리 오차)
  - GPU 사용: GPU 우선, CPU 자동 폴백
  - 논문: Nature Methods 2022

### Slide 12 – Backup: OpenMM
- Title: OpenMM 상세
- Key-value layout:
  - 핵심 원리: L-BFGS 알고리즘으로 포텐셜 에너지 극소값 도달
  - 에너지 구성: 결합 + 각도 + 이면각 + 비결합(반데르발스 + 정전기)
  - Force Field: AMBER ff14SB
  - 역할: ColabFold 예측 구조의 원자 충돌/겹침 해소

### Slide 13 – Backup: AutoDock Vina
- Title: AutoDock Vina 상세
- Key-value layout:
  - score_only 모드: 기존 구조를 변경하지 않고 스코어링 함수만 적용
  - 출력값 해석: 상대적 비교를 위한 근사 점수 (절대값 해석 불가)
  - 펩타이드 한계: torsional flexibility가 높아 도킹 정확도 제한 → ADCP 보완 검토

### Slide 14 – Backup: PLIP (보조 지표)
- Title: PLIP 상세 (보조 지표)
- Key-value layout:
  - 기능: 수소결합, 소수성 접촉, 염교, π-스태킹 등 비공유 상호작용 자동 탐지
  - 클러스터링 문제: 소수성 결합 클러스터링 시 접촉 면적 정보 손실
  - 현재 역할: FinalScore에서 제외, 엑셀에 결합 분포표만 기록

### Slide 15 – Backup: PRODIGY
- Title: PRODIGY 상세
- Key-value layout:
  - 모델 유형: 구조 특징 기반 선형 회귀 모델 (White Box)
  - 학습 특징: ICs(인터페이스 접촉 6종 분류) + NIS(비상호작용 표면 특성)
  - 정확도: Pearson r = 0.73, RMSE = 1.89 kcal/mol
  - 채택 근거: PPI-Affinity(Black Box) 대비 강건성 우위
