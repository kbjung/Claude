# pepbind05.py 모델 사용 분석 보고서

## 요약

pepbind05.py는 6개의 AI/계산화학 모델을 다단계 파이프라인으로 통합하여 타겟 단백질에 특이적으로 결합하는 펩타이드 후보를 자동 도출합니다. 각 모델의 호출 방식, 입출력, GPU 사용 여부, 에러 핸들링을 아래 정리했습니다.

---

## 1. PepMLM (ESM-2 기반 펩타이드 생성)

### 함수명
- `load_esm_mlm()` (라인 887-896)
- `generate_peptides_with_mlm()` (라인 899-1033)

### 입력 파라미터/파일
- **tokenizer**: HuggingFace AutoTokenizer (facebook/esm2_t12_35M_UR50D)
- **model**: HuggingFace AutoModelForMaskedLM (ESM-2)
- **target_sequence** (str): 타겟 단백질 서열 (예: PD-L1, 길이 198)
- **num_peptides** (int): 생성할 펩타이드 개수 (기본: 50)
- **peptide_len** (int): 각 펩타이드 길이 (기본: 4 아미노산)
- **top_k** (int): 각 위치별 상위 k개 아미노산 샘플링 (기본: 10)
- **temperature** (float): 샘플링 온도 (기본: 1.0)

### 출력 파라미터/파일
- **반환값**: `list[str]` - 생성된 펩타이드 서열 목록
  - 예: ['LPAK', 'MVDG', 'SYTR', ...]
- **부수 파일**: 없음 (콘솔 출력만)

### GPU 사용 여부
**YES (강제)**
- 모델을 DEVICE(cuda 또는 cpu)로 로드
- torch.no_grad() 컨텍스트에서 실행
- logits = outputs.logits를 temperature로 나누고 softmax 적용

### 특수 옵션/모드
```python
# 프롬프트 형식 (타겟 컨텍스트 사용)
prompt = f"{target_tokens} {mask_tokens}"
# 예: "A F K L V [MASK] [MASK] [MASK] [MASK]"
```

- **top-k 필터링**: 각 위치에서 확률 상위 k개만 남긴 후 재정규화
- **temperature scaling**: logits을 temperature로 나눈 후 softmax
  - <1.0 → 보수적 (고확률 위주)
  - 1.0 → 기본 분포
  - >1.0 → 탐색적 (저확률도 선택)
- **중복 제거**: seen set으로 생성된 펩타이드 중복 확인
- **표준 아미노산 검증**: 표준 20개(ACDEFGHIKLMNPQRSTVWY)만 허용, X/B/Z 등 제외

### 에러 핸들링/폴백 로직
```python
# 1) 마스크 토큰 확인
if mask_token is None:
    raise ValueError("토크나이저에 [MASK] 토큰이 없습니다.")

# 2) 샘플링 재시도 루프
while len(peptides) < num_peptides and attempt < num_peptides * 5:
    # 실패한 샘플(비표준 AA 또는 길이 오류)은 건너뛰고 계속 시도

# 3) 최대 시도 횟수 초과
if len(peptides) < num_peptides:
    # 경고만 출력하고 생성된 펩타이드로 계속 진행 (중단 X)
```

---

## 2. ColabFold (AF-Multimer 기반 구조 예측)

### 함수명
- `prepare_colabfold_batch_csv()` (라인 1056-1073)
- `run_colabfold_batch_with_progress()` (라인 1076-1347)

### 입력 파라미터/파일
- **csv_path** (Path): ColabFold 배치 입력 CSV 파일
  - 형식: `id,sequence`
  - 예: `complex_0,AAAA...AAAA:LPAK`
  - sequence 형식: `target_seq:peptide_seq`
- **out_dir** (Path): ColabFold 출력 디렉토리
- **total_complexes** (int): 전체 복합체 개수 (진행률 표시용)

### 출력 파라미터/파일
- **반환값**: `list[Path]` - rank_001 PDB 파일 목록
  - 파일명 예: `complex_0_unrelaxed_rank_001_alphafold2_multimer_v3_model_1_seed_0.pdb`
- **부수 파일**:
  - `colabfold_batch.log` (GPU 모드 로그)
  - `colabfold_batch_cpu.log` (CPU 폴백 로그)
  - `log.txt` (colabfold_batch 자체 로그)

### GPU 사용 여부
**YES (권장, CPU 폴백 가능)**

실행 명령어:
```bash
colabfold_batch \
  --num-recycle 9 \
  --model-type alphafold2_multimer_v3 \
  --rank ptm \
  --max-msa 256:512 \
  --num-models 5 \
  --stop-at-score 0.5 \
  batch_complexes.csv \
  output_dir/
```

환경변수:
- `XLA_PYTHON_CLIENT_PREALLOCATE=false`
- `XLA_PYTHON_CLIENT_MEM_FRACTION=0.8`

### 특수 옵션/모드
```python
# GPU 우선 시도
try:
    rank1_files = _run_on_device("GPU", extra_env=None, log_name="colabfold_batch.log")
except RuntimeError:
    # OOM 감지 시 CPU 폴백
    if is_oom and COLABFOLD_CPU_FALLBACK:
        cpu_env = {
            "CUDA_VISIBLE_DEVICES": "",
            "JAX_PLATFORMS": "cpu",
        }
        rank1_files = _run_on_device("CPU", extra_env=cpu_env, log_name="colabfold_batch_cpu.log")
```

### 에러 핸들링/폴백 로직

#### 1) Idle Timeout (진행 없음)
```python
if (now - last_progress_time) > max_idle_min * 60:  # 기본: 60분
    # rank_001 파일 수가 증가 않으면 강제 종료
    proc.terminate()
    raise RuntimeError(f"ColabFold idle timeout {max_idle_min}분 초과")
```

#### 2) Total Timeout (전체 시간)
```python
if (now - start_time) > max_total_min * 60:  # 기본: 1440분(24시간)
    proc.terminate()
    raise RuntimeError(f"ColabFold total timeout {max_total_min}분 초과")
```

#### 3) MSA 서버 오류 (즉시 감지)
```python
msa_keywords = (
    "Timeout while submitting to MSA server",
    "Error while submitting to MSA server",
    "HTTPSConnectionPool", "timed out",
    ...
)
# tail 100줄에서 키워드 검색 → 발견 시 즉시 종료
if any(k in tail_text for k in msa_keywords):
    proc.terminate()
    raise RuntimeError(f"ColabFold MSA 서버 오류 감지")
```

#### 4) Out of Memory (GPU)
```python
# GPU 실패 후 로그에서 OOM 키워드 확인
oom_keywords = ("RESOURCE_EXHAUSTED", "Out of memory", "CUDA_ERROR_OUT_OF_MEMORY")
if is_oom and COLABFOLD_CPU_FALLBACK:
    # CPU 폴백으로 한 번 더 시도
```

#### 5) 진행률 모니터링
```python
# 30초마다 rank_001 파일 개수 확인
rank1_files = list(out_dir.glob("*rank_001*.*pdb"))
done = len(rank1_files)
print(f"[진행 상황] {done}/{total_complexes} 완료")
```

---

## 3. OpenMM (구조 정제: Minimization + MD)

### 함수명
- `openmm_minimize_and_md()` (라인 1589-1737)
- `_get_openmm_platform()` (라인 1355-1390)
- `_write_pdb_with_missing_oxt()` (라인 1394-1587)
- `compute_openmm_gbsa_binding_energy()` (라인 1808-1955)

### 입력 파라미터/파일 (Minimization + MD)

**함수**: `openmm_minimize_and_md(in_pdb, out_pdb, md_time_ps, timestep_fs, restraint_k)`

- **in_pdb** (Path): ColabFold 출력 PDB
- **out_pdb** (Path): 정제된 PDB 출력 경로
- **md_time_ps** (float): MD 길이 (기본: 100.0 ps)
- **timestep_fs** (float): MD timestep (기본: 2.0 fs)
- **restraint_k** (float): Cα position restraint 강도 (기본: 1.0 kcal/mol/Å²)

### 출력 파라미터/파일

**Minimization + MD**:
- **반환값**: `Path` - 정제된 PDB 파일 경로
- **부수 파일**:
  - `{stem}__openmm_prep.pdb` (OXT 보정 임시 파일)

**GBSA 에너지 계산**:
- **반환값**: `dict` 포함:
  ```python
  {
      "status": "정상" | "실패: ..." | "단일체" | "OpenMM미설치",
      "ligand_chain": str | None,
      "E_complex": float | None,    # kcal/mol
      "E_receptor": float | None,
      "E_peptide": float | None,
      "GBSA_bind": float | None,    # E_complex - (E_receptor + E_peptide)
  }
  ```

### GPU 사용 여부
**YES (권장, CPU 폴백)**

Platform 선택 순서:
```python
# GPU 우선
gpu_platforms = ["CUDA", "OpenCL", "HIP", "Metal"]
# 실패 시 CPU
cpu_platforms = ["CPU", "Reference"]
```

### 특수 옵션/모드

#### Minimization + MD 파이프라인
```python
# 1) OXT 보정 (C-말단 산소 추가)
prep_pdb = _write_pdb_with_missing_oxt(in_pdb, prep_pdb)

# 2) ForceField 로드 (다단계 폴백)
ff_candidates = [
    (["amber14-all.xml", "implicit/obc2.xml"], "amber14-all + GBSA(OBC2)"),
    (["amber14-all.xml"], "amber14-all"),
    (["amber99sb.xml"], "amber99sb"),
    (["charmm36.xml"], "charmm36"),
]

# 3) Position Restraint (Cα, N, C만)
for atom in topology.atoms():
    if atom.name in ("CA", "N", "C"):
        restraint.addParticle(atom.index, (x0, y0, z0))

# 4) Integrator & Simulation
integrator = openmm.LangevinMiddleIntegrator(300K, 1.0/ps, 2.0*fs)
simulation = app.Simulation(topology, system, integrator, platform, properties)

# 5) Minimization
simulation.minimizeEnergy(maxIterations=2000)

# 6) Short MD
n_steps = int(100.0 ps * 1000.0 / 2.0 fs) = 50000 steps
simulation.step(n_steps)
```

#### GBSA 에너지 계산 (Single-Trajectory MM-GBSA)
```python
# 1) Complex 전체 minimization
E_complex, minimized_positions = _openmm_potential_energy_kcal(
    modeller_complex, ff, minimize=True, minimize_max_iterations=200
)

# 2) Receptor (minimized positions에서 ligand 삭제)
# ★ 재최적화 없음: 복합체 최적화 좌표 그대로 사용
E_receptor = _openmm_potential_energy_kcal(modeller_rec, ff, minimize=False)

# 3) Peptide (minimized positions에서 receptor 삭제)
# ★ 재최적화 없음: 복합체 최적화 좌표 그대로 사용
E_peptide = _openmm_potential_energy_kcal(modeller_lig, ff, minimize=False)

# 4) Binding Energy
GBSA_bind = E_complex - (E_receptor + E_peptide)
```

### 에러 핸들링/폴백 로직

#### PDB 로드 & ForceField 매칭
```python
for xmls, desc in ff_candidates:
    try:
        ff = app.ForceField(*xmls)
        modeller = app.Modeller(pdb.topology, pdb.positions)
        modeller.addHydrogens(ff)  # 여기서 실패 가능
        print(f"[OK] ForceField: {desc}")
        break
    except Exception as e:
        print(f"[WARN] {desc} 실패 → 다음 후보로")
        continue

if modeller is None or ff is None:
    raise RuntimeError("ForceField 로드 실패")
```

#### Platform 초기화
```python
try:
    simulation = app.Simulation(topology, system, integrator, platform, properties)
except Exception as e:
    print(f"[WARN] GPU 플랫폼 초기화 실패 → CPU로 폴백")
    platform = _get_openmm_platform(prefer_gpu=False)
    simulation = app.Simulation(topology, system, integrator, platform, {})
```

#### GBSA 계산 실패 처리
```python
try:
    # 에너지 계산
except Exception as e:
    return {
        "status": f"실패: {type(e).__name__}: {e}",
        "ligand_chain": None,
        "E_complex": None,
        "E_receptor": None,
        "E_peptide": None,
        "GBSA_bind": None,
    }
finally:
    # 임시 파일 정리
    if pdb_for_calc != pdb_path:
        Path(pdb_for_calc).unlink()
```

---

## 4. AutoDock Vina (분자 도킹)

### 함수명
- `run_vina_on_rank1()` (라인 2408-2625)
- `prepare_pdbqt()` (라인 2258-2310)
- `split_complex_to_receptor_ligand()` (라인 2113-2135)
- `parse_vina_score_from_stdout()` (라인 2313-2355)

### 입력 파라미터/파일

**함수 인자**:
- **rank1_pdbs** (list[Path]): ColabFold 또는 정제된 rank_001 PDB 파일 목록
- **vina_dir** (Path): Vina 출력 디렉토리

**Vina 명령어**:
```bash
vina \
  --receptor receptor.pdbqt \     # rigid receptor
  --ligand ligand.pdbqt \          # rigid ligand (펩타이드)
  --center_x X --center_y Y --center_z Z \  # 도킹 상자 중심
  --size_x SX --size_y SY --size_z SZ \     # 도킹 상자 크기
  --out output_vina.pdbqt
```

### 출력 파라미터/파일

- **반환값**: None (부수 파일로 결과 기록)
- **부수 파일**:
  - `complex_0/complex_0_vina_out.pdbqt` (도킹 결과, 여러 포즈 포함)
  - `complex_0/complex_0_vina_stdout.txt` (stdout/stderr 로그)
  - `complex_0/receptor.pdbqt` (receptor PDBQT)
  - `complex_0/ligand.pdbqt` (ligand PDBQT)
  - `vina_summary.xlsx` (복합체별 점수 + 상태)

### GPU 사용 여부
**NO (CPU only)**

Vina는 CPU 기반 도킹 알고리즘입니다.

### 특수 옵션/모드

#### 1) 자동 Receptor/Ligand 할당
```python
# 체인 residue 개수 기반
chain_counts = get_chain_residue_counts(pdb)
# 예: {'A': 198, 'B': 4}

# Receptor = 가장 큰 체인 (또는 prefer_receptor='A')
# Ligand = 가장 작은 체인
rec_chain, lig_chain = auto_assign_receptor_ligand(chain_counts, prefer_receptor="A")
```

#### 2) PDBQT 변환
```bash
# Receptor (rigid)
obabel -ipdb receptor.pdb -xr -opdbqt -O receptor.pdbqt

# Ligand (merge roots to single rigid ligand)
obabel -ipdb ligand.pdb -opdbqt -O ligand_raw.pdbqt
# merge_ligand_roots() → ligand.pdbqt (단일 ROOT 구조)
```

#### 3) 도킹 상자 계산
```python
# ligand의 모든 원자 좌표 기반
box = compute_box_from_ligand(lig_pdb, padding=10.0)
# 반환: {"center_x": ..., "center_y": ..., "center_z": ...,
#        "size_x": ..., "size_y": ..., "size_z": ...}
```

### 에러 핸들링/폴백 로직

#### 1) 체인 검증
```python
chain_counts = get_chain_residue_counts(complex_pdb)

if len(chain_counts) == 1:
    status = "스킵: 단일체 구조(리간드 체인 없음)"
    # Vina 도킹 불가 → 로그만 기록

if rec_chain is None or lig_chain is None:
    status = "스킵: 리간드 체인 자동 탐지 실패"
```

#### 2) 체인 분리 실패
```python
try:
    rec_pdb, lig_pdb = split_complex_to_receptor_ligand(...)
except ValueError as e:
    status = f"스킵: 체인 분리 실패({e})"
```

#### 3) PDBQT 변환 실패
```python
# obabel 실행 실패
if rec_res.returncode != 0:
    raise RuntimeError(f"receptor PDBQT 변환 실패: code={rec_res.returncode}")
```

#### 4) Vina 실행 실패
```python
if result.returncode != 0:
    status = f"실패: Vina 실행 에러(code={result.returncode})"

    # PDBQT parsing 오류 감지
    if "PDBQT parsing error" in (result.stdout or result.stderr):
        status += " (PDBQT parsing error: flex residue/ligand 태그 문제)"
```

#### 5) 점수 파싱 실패
```python
best_score = parse_vina_score_from_stdout(result.stdout)

# 파싱 모드 1: mode 테이블에서 affinity 열
# "mode | affinity | rmsd l.b. | rmsd u.b."
# "1    | -7.5     | 0.0      | 0.0"

# 파싱 모드 2: fallback "REMARK VINA RESULT:"
# REMARK VINA RESULT: -7.5

if best_score is None:
    status = "파싱실패: stdout에서 점수 패턴 없음"
```

#### 6) 요약 엑셀 병합
```python
if xlsx_path.exists():
    df_existing = pd.read_excel(xlsx_path)
    new_complexes = set(df_new["complex"].tolist())
    df_existing = df_existing[~df_existing["complex"].isin(new_complexes)]
    df_merged = pd.concat([df_existing, df_new])  # 중복 제거 후 병합
```

---

## 5. PLIP (단백질-리간드 상호작용 분석)

### 함수명
- `run_plip_on_rank1()` (라인 2631-2707)
- `load_plip_scores()` (라인 3133-3329)

### 입력 파라미터/파일

**함수 인자**:
- **rank1_pdbs** (list[Path]): rank_001 PDB 파일 목록
- **plip_dir** (Path): PLIP 출력 디렉토리

**PLIP 명령어**:
```bash
plip -f complex.pdb \
     -o output_subdir \
     -x -t \  # -x: XML 생성, -t: TXT 리포트 생성
     --chains [['A'], ['B']]  # receptor chain A, ligand chain B
```

### 출력 파라미터/파일

- **반환값**: None (부수 파일로 결과 기록)
- **부수 파일** (각 complex별 서브디렉토리):
  - `complex_0_plip/` (PLIP 출력 디렉토리)
    - `report.xml` (XML 형식 상호작용 정보)
    - `report.txt` (텍스트 리포트)
    - `complex_0_plip.log` (stdout/stderr)
  - `plip_summary.xlsx` (복합체별 상호작용 점수)
  - `plip_parse_debug.txt` (파싱 디버그 로그)

### GPU 사용 여부
**NO (CPU only)**

PLIP는 스크립트 기반 상호작용 분석 도구입니다.

### 특수 옵션/모드

#### 1) 자동 Receptor/Ligand 할당
```python
chain_counts = get_chain_residue_counts(pdb)
rec_chain, lig_chain = auto_assign_receptor_ligand(chain_counts, prefer_receptor="A")

# chains_expr = "[[\'A\'], [\'B\']]" 형식
chains_expr = f"[['{rec_chain}'], ['{lig_chain}']]"
```

#### 2) 상호작용 파싱 (XML 우선, txt 폴백)
```python
# 1) XML 파싱 (report.xml 또는 plip_*.xml)
for xml_path in subdir.rglob("*.xml"):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    hbond = sum(1 for _ in root.iter("hydrogen_bond"))
    hydrophobic = sum(1 for _ in root.iter("hydrophobic_interaction"))
    saltbridge = sum(1 for _ in root.iter("salt_bridge"))

    # 가중치 적용 점수 계산
    total = (hbond * PLIP_WEIGHT_HBOND +
             hydrophobic * PLIP_WEIGHT_HYDROPHOBIC +
             saltbridge * PLIP_WEIGHT_SALTBRIDGE)
    break

# 2) 텍스트 파싱 (XML 실패 시)
# "hydrogen bond: 3"
# "hydrophobic interaction: 5"
# "salt bridge: 1"
```

#### 3) 가중치 설정
```python
PLIP_WEIGHT_HBOND       = 1.0   # 기준값
PLIP_WEIGHT_HYDROPHOBIC = 0.5   # 상대적으로 약함
PLIP_WEIGHT_SALTBRIDGE  = 3.0   # 가장 강함
```

### 에러 핸들링/폴백 로직

#### 1) 채인 검증
```python
if rec_chain is None or lig_chain is None:
    status = "스킵: PLIP용 리간드 체인 자동 탐지 실패"
    log_file.write_text(f"{status}\nchains={chain_counts}\n")
    continue
```

#### 2) PLIP 실행 실패
```python
if result.returncode != 0:
    print(f"[ERROR] PLIP 실패: {pdb.name} (code={result.returncode})")
    # stdout/stderr를 로그로 저장하고 계속 진행
```

#### 3) 상호작용 파일 찾기 실패
```python
# XML 파싱 실패
except Exception as e:
    debug_lines.append(f"{base}\treport_xml_parse_error\t{e}")

# TXT 파싱 실패
except Exception as e:
    debug_lines.append(f"{base}\treport_txt_parse_error\t{e}")

if source is None:
    status = "실패: PLIP 요약 파일(xml/txt)을 찾지 못함"
    metrics[base] = {"total": None, "hbond": None, ...}
```

#### 4) 요약 엑셀 생성
```python
# 기존 파일이 있으면 병합
if xlsx_path.exists():
    df_existing = pd.read_excel(xlsx_path)
    new_complexes = set(df_new["complex"].tolist())
    df_existing = df_existing[~df_existing["complex"].isin(new_complexes)]
    df_merged = pd.concat([df_existing, df_new])
```

---

## 6. PRODIGY (단백질-펩타이드 친화도 예측)

### 함수명
- `run_prodigy_on_rank1()` (라인 2713-2848)
- `load_prodigy_scores()` (라인 2932-3023)
- `parse_prodigy_dg_from_stdout()` (라인 646-705)

### 입력 파라미터/파일

**함수 인자**:
- **rank1_pdbs** (list[Path]): rank_001 PDB 파일 목록
- **out_dir** (Path): PRODIGY 출력 디렉토리

**PRODIGY 명령어**:
```bash
prodigy complex.pdb \
        --selection A B  # receptor chain A, ligand chain B
```

### 출력 파라미터/파일

- **반환값**: `pd.DataFrame` 포함:
  ```
  complex | PRODIGY_status | PRODIGY_dG
  --------|----------------|----------
  complex_0 | 정상 | -10.2
  ```
- **부수 파일**:
  - `complex_0_prodigy.txt` (stdout 리포트)
  - `complex_0_prodigy.stderr.txt` (stderr 로그)
  - `prodigy_summary.xlsx` (복합체별 ΔG 값)

### GPU 사용 여부
**NO (CPU only)**

PRODIGY는 ML 기반 점수화 도구로 GPU를 사용하지 않습니다.

### 특수 옵션/모드

#### 1) 자동 Receptor/Ligand 할당
```python
chain_counts = get_chain_residue_counts(pdb_path)
rec_chain, lig_chain = auto_assign_receptor_ligand(chain_counts, prefer_receptor="A")

# PRODIGY 호출
cmd = [PRODIGY_SCRIPT, str(pdb_path), "--selection", rec_chain, lig_chain]
```

#### 2) ΔG 파싱 (stdout에서)
```python
# 패턴 1: "Predicted ΔG (kcal/mol) = -10.2"
# 패턴 2: "Predicted deltaG = -10.2"
# 패턴 3: "deltaG = -10.2"

import re
pattern = r'(?:ΔG|deltaG|dG)\s*[=:]\s*(-?\d+\.?\d*)'
```

### 에러 핸들링/폴백 로직

#### 1) 채인 검증
```python
if rec_chain is None or lig_chain is None:
    status = "스킵: PRODIGY용 리간드 체인 자동 탐지 실패"
    records.append({"complex": complex_name, "PRODIGY_status": status, "PRODIGY_dG": None})
    continue
```

#### 2) PRODIGY 실행 실패
```python
if result.returncode != 0:
    status = f"실패: PRODIGY 실행 에러(code={result.returncode})"
    print(f"[ERROR] {status}: {complex_name}")
```

#### 3) "No contacts found for selection"
```python
if "no contacts found for selection" in stdout_text.lower():
    status = "실패: No contacts found for selection(선택된 체인 간 접촉 없음)"
    dg = None
```

#### 4) ΔG 파싱 실패
```python
dg = parse_prodigy_dg_from_stdout(stdout_text)

if dg is None:
    status = "파싱실패: stdout에서 ΔG 패턴 없음"
```

#### 5) 요약 엑셀 생성 + 숫자 포맷
```python
df_new.to_excel(xlsx_path, index=False)

# 셀 포맷 설정 (ΔG는 소수 2자리)
wb = load_workbook(xlsx_path)
ws = wb.active
for cell in ws["C"]:  # PRODIGY_dG 컬럼 (3번째)
    if isinstance(cell.value, (int, float)):
        cell.number_format = "0.00"
wb.save(xlsx_path)
```

---

## 7. 최종 평가 및 FinalScore 계산

### 함수명
- `build_and_save_final_table()` (라인 3388-3822)
- `fixed_range_norm()` (라인 3332-3364)

### 입력 데이터
각 복합체별 6개 지표:
1. **ipTM** (ColabFold) - 인터페이스 신뢰도 [0-1]
2. **Vina_score** (AutoDock) - 도킹 에너지 [kcal/mol]
3. **PLIP_weighted_total** (PLIP) - 가중치 적용 상호작용 수
4. **PRODIGY_dG** (PRODIGY) - 결합 자유에너지 [kcal/mol]
5. **GBSA_bind** (OpenMM) - MM-GBSA 결합 에너지 [kcal/mol]

### FinalScore 계산 (2026.03.10 교수님 승인)

```python
# ★ PLIP은 이제 보조 지표로만 사용 (FinalScore 제외)
# 근거: PLIP 점수화 부적합 (정성 도구, 선행 사례 없음)

# 정규화 (고정 범위 기반)
iptm_norm = fixed_range_norm(iptm_vals, 0.0, 1.0, higher_is_better=True)
vina_norm = fixed_range_norm(vina_vals, -15.0, 0.0, higher_is_better=False)
prodigy_norm = fixed_range_norm(prodigy_vals, -20.0, 0.0, higher_is_better=False)
plip_norm = fixed_range_norm(plip_vals, 0.0, 30.0, higher_is_better=True)  # 보조용

# FinalScore 계산 (3개 지표)
FinalScore = (0.50 * prodigy_norm[base] +
              0.25 * vina_norm[base] +
              0.10 * iptm_norm[base])

# 또는 (ADCP 도입 후 재결정 예정)
```

### 정규화 함수
```python
def fixed_range_norm(value_dict, vmin, vmax, higher_is_better=True):
    """
    고정 범위 [vmin, vmax]로 0-1 정규화

    - higher_is_better=True: vmin→0, vmax→1
    - higher_is_better=False: vmin→1, vmax→0 (에너지는 작을수록 좋음)
    """
    out = {}
    for k, v in value_dict.items():
        if v is None:
            continue
        x = max(min(v, vmax), vmin)  # clip
        if higher_is_better:
            s = (x - vmin) / (vmax - vmin)
        else:
            s = (vmax - x) / (vmax - vmin)
        out[k] = s
    return out
```

### 계산 조건
```python
# 다음 조건을 모두 만족할 때만 FinalScore 계산
if (len(chain_counts) == 1) or not (vina_ok and plip_ok and prodigy_ok):
    final_score = None
else:
    final_score = (0.50 * prodigy_norm.get(base, 0.0) +
                   0.25 * vina_norm.get(base, 0.0) +
                   0.10 * iptm_norm.get(base, 0.0))

# 조건:
# 1) 단일체 구조 X (복합체 형성 필수)
# 2) Vina_status = "정상" ✓ (값도 유효해야 함)
# 3) PRODIGY_status = "정상" ✓
# 4) PLIP_status = "정상" ✓ (보조용이지만 계산 조건은 유지)
```

---

## 8. 파이프라인 전체 흐름도

```
[STEP 1] 워크스페이스 초기화
    ↓
[STEP 2] PepMLM (ESM-2, GPU)
    ↓ 펩타이드 50개 생성
[STEP 3] ColabFold (GPU, CPU fallback)
    ↓ rank_001 PDB 50개
[STEP 3b] OpenMM (minimize + MD + GBSA)
    ↓ 정제 구조 + 에너지
[STEP 4] Vina (CPU)
    ↓ 도킹 점수 50개
[STEP 5] PLIP (CPU)
    ↓ 상호작용 정보
[STEP 6] PRODIGY (CPU)
    ↓ ΔG 값 50개
[STEP 7] 실패 복합체 재시도 (캐시 기반)
    ↓ GBSA > 100 복합체 재실행
[STEP 8] 최종 평가 + FinalScore 계산
    ↓
[출력] Excel + PDB zip
```

---

## 9. 주요 설정값 및 임계값

| 설정 | 기본값 | 용도 |
|------|--------|------|
| NUM_PEPTIDES | 50 | PepMLM 생성 펩타이드 개수 |
| PEPTIDE_LENGTH | 4 | 펩타이드 길이 |
| PEPMLM_TOP_K | 10 | top-k 샘플링 |
| PEPMLM_TEMPERATURE | 1.0 | 온도 스케일링 |
| COLABFOLD_MAX_MSA | 256:512 | MSA 깊이 제한 |
| COLABFOLD_MAX_IDLE_MIN | 60 | idle timeout (분) |
| COLABFOLD_MAX_TOTAL_MIN | 1440 | 전체 시간 제한 (분) |
| REFINE_MD_TIME_PS | 100.0 | MD 길이 (ps) |
| REFINE_TIMESTEP_FS | 2.0 | timestep (fs) |
| REFINE_RESTRAINT_K | 1.0 | restraint 강도 (kcal/mol/Å²) |
| GBSA_FAILURE_THRESHOLD | 100.0 | 재시도 판정 (kcal/mol) |
| MAX_RETRY_ROUNDS | 3 | 최대 재시도 횟수 |
| PRODIGY_DG_RANGE | (-20.0, 0.0) | ΔG 정규화 범위 |
| VINA_SCORE_RANGE | (-15.0, 0.0) | Vina 정규화 범위 |
| PLIP_TOTAL_RANGE | (0.0, 30.0) | PLIP 정규화 범위 |
| IPTM_RANGE | (0.0, 1.0) | ipTM 정규화 범위 |
| W_PRODIGY | 0.50 | PRODIGY 가중치 |
| W_VINA | 0.25 | Vina 가중치 |
| W_PLIP | 0.15 | PLIP 가중치 (현재 미사용) |
| W_IPTM | 0.10 | ipTM 가중치 |

---

## 10. 환경 요구사항

### 필수 소프트웨어
| 도구 | 환경변수 | 버전 예 |
|------|---------|--------|
| ColabFold | COLABFOLD_CMD | colabfold_batch |
| AutoDock Vina | VINA_CMD | vina (1.2.3+) |
| PLIP | PLIP_CMD | plip |
| PRODIGY | PRODIGY_SCRIPT | prodigy |
| Open Babel | OBABEL_CMD | obabel |

### Python 라이브러리
```
torch, transformers (PepMLM용)
openmm (구조 정제용)
biopython (PDB 파싱)
pandas, openpyxl (Excel 생성)
```

### GPU (권장)
- NVIDIA GPU + CUDA (ColabFold, PepMLM)
- RTX 3070 8GB / 32GB RAM 권장

---

## 11. 변경 이력

| 날짜 | 모델 | 변경 내용 |
|------|------|---------|
| 2026.03.10 | PLIP | FinalScore에서 제외 → 보조 지표로 전환 |
| 2026.03.10 | - | 재시도 기능(STEP 7) 확정 |
| 2026.03.10 | ADCP | 도입 검토 시작 (진행 중) |

---

이 분석은 2026년 3월 20일 기준 pepbind05.py (4,572줄)를 완독하여 작성했습니다.
