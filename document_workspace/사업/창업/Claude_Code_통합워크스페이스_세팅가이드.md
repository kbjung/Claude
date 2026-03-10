# Claude Code 통합 워크스페이스 세팅 가이드

> 모든 작업을 Claude Code CLI 하나에서 수행하기 위한 실전 구축 가이드

---

## 1. 전체 아키텍처

```
Claude Code CLI (중앙 허브)
    │
    ├── 직접 수행: 텍스트 작성, 구조설계, 파일관리, 문서생성(docx/pptx)
    │
    ├── Gemini API 호출 ──→ 나노바나나 이미지 생성 → assets/에 저장
    ├── OpenAI API 호출 ──→ GPT 이미지 생성 → assets/에 저장
    │
    ├── Task (서브에이전트)
    │   ├── 조사 에이전트 → research/ 에 결과 저장
    │   ├── 작성 에이전트 → drafts/ 에 초안 저장
    │   ├── 교수 평가 에이전트 → eval/ 에 평가 저장
    │   ├── 대표 평가 에이전트 → eval/ 에 평가 저장
    │   └── 고객 평가 에이전트 → eval/ 에 평가 저장
    │
    └── STATUS.md 자동 업데이트 (비서 기능)
```

---

## 2. 초기 세팅 순서

### Step 1: 프로젝트 폴더 생성

```bash
mkdir -p ~/workspace/startup-project
cd ~/workspace/startup-project

# 시스템 폴더
mkdir -p _system/agents _system/templates _system/scripts
mkdir -p _tracker/log

# 작업 폴더 (필요할 때 추가)
mkdir -p 01-proposal/{research,drafts,assets,eval,final}
mkdir -p 02-company-intro/{research,drafts,assets,eval,final}
mkdir -p 03-market-research/{research,drafts,eval,final}
```

### Step 2: API 키 환경변수 설정

```bash
# ~/.bashrc 또는 ~/.zshrc 에 추가
export GEMINI_API_KEY="your-gemini-api-key-here"
export OPENAI_API_KEY="your-openai-api-key-here"
```

```bash
source ~/.bashrc  # 적용
```

### Step 3: Python 패키지 설치

```bash
pip install google-genai openai Pillow requests
```

### Step 4: Claude Code 실행

```bash
cd ~/workspace/startup-project
claude
```
→ CLAUDE.md가 자동 로드됩니다.

---

## 3. 핵심 파일 구성

### 3-1. CLAUDE.md (프로젝트 루트에 배치 — 자동 로드)

```markdown
# 창업팀 프로젝트 관리 시스템

## 나의 역할
당신은 창업팀의 프로젝트 매니저이자 실무 담당자입니다.
매 세션 시작 시 반드시 _tracker/STATUS.md를 읽고 현황을 파악한 후,
현재 우선순위와 다음 액션을 제안하세요.

## 작업 규칙
1. 모든 산출물은 해당 작업 폴더의 하위에 저장
2. 작업 완료 시 STATUS.md 자동 업데이트
3. 결정사항은 _tracker/decisions.md에 기록
4. 이미지가 필요하면 _system/scripts/ 의 API 스크립트 활용

## 문서 톤 & 스타일
- 제안서/기획서: 격식체, 명확한 근거 기반
- 회사소개서: 비전 중심, 설득적 톤
- 시장조사: 객관적, 데이터 중심

## 용어 사전
(프로젝트별로 업데이트)
| 용어 | 정의 | 비고 |
|------|------|------|

## 평가 기준
모든 결과물은 3관점 평가 통과 필수 (16/20 이상)
- 교수: 논리구조, 근거신뢰성, 용어정확성, 완성도
- 대표: 시장분석, 차별화, 실행가능성, 투자매력
- 고객: 문제공감, 솔루션명확성, 가치제안, 신뢰감
평가 가이드: _system/agents/eval-*.md 참조

## 외부 API 사용
- 나노바나나 (도식도/인포그래픽): _system/scripts/gemini_image.py
- GPT 이미지 (표지/일러스트): _system/scripts/gpt_image.py
- 사용 시 반드시 스크립트를 통해 호출, 브라우저 전환 없음

## 멀티 에이전트 운용
복합 작업 시 Task로 서브에이전트를 생성하여 병렬 처리:
- 조사 Task → _system/agents/researcher.md 가이드 전달
- 작성 Task → _system/agents/writer.md 가이드 전달
- 평가 Task → _system/agents/eval-{role}.md 가이드 전달
```

### 3-2. _tracker/STATUS.md

```markdown
# 프로젝트 현황 대시보드
최종 업데이트: YYYY-MM-DD HH:MM

## 전체 진행률

| # | 작업 | 상태 | 진행률 | 다음 액션 | 마감 |
|---|------|------|--------|----------|------|
| 1 | 제안서 v1 | ⚪ 미착수 | 0% | 시장조사 시작 | |
| 2 | 회사소개서 | ⚪ 미착수 | 0% | 제안서 후 착수 | |

## 오늘 할 일
1. (세션 시작 시 Claude가 자동 제안)

## 의존성
- 회사소개서 ← 제안서 기술 섹션 완료 필요

## 최근 결정사항
- (날짜와 함께 기록)
```

---

## 4. API 연동 스크립트

### 4-1. 나노바나나 이미지 생성 (_system/scripts/gemini_image.py)

```python
#!/usr/bin/env python3
"""
나노바나나(Gemini) 이미지 생성 스크립트
Claude Code에서 호출: python _system/scripts/gemini_image.py "프롬프트" output.png
"""
import sys
import os
import base64
from google import genai
from google.genai import types

def generate_image(prompt: str, output_path: str, model: str = "gemini-2.5-flash-image"):
    """Gemini API로 이미지 생성 후 파일 저장"""
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]
        )
    )

    # 응답에서 이미지 추출
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image_data = part.inline_data.data
            with open(output_path, "wb") as f:
                f.write(image_data)
            print(f"이미지 저장 완료: {output_path}")
            return output_path

    print("이미지 생성 실패: 응답에 이미지가 없습니다")
    return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법: python gemini_image.py '프롬프트' output.png [모델명]")
        print("모델: gemini-2.5-flash-image (기본) | gemini-3-pro-image-preview (프로)")
        sys.exit(1)

    prompt = sys.argv[1]
    output = sys.argv[2]
    model = sys.argv[3] if len(sys.argv) > 3 else "gemini-2.5-flash-image"

    generate_image(prompt, output, model)
```

### 4-2. GPT 이미지 생성 (_system/scripts/gpt_image.py)

```python
#!/usr/bin/env python3
"""
GPT 이미지 생성 스크립트
Claude Code에서 호출: python _system/scripts/gpt_image.py "프롬프트" output.png
"""
import sys
import os
import base64
from openai import OpenAI

def generate_image(prompt: str, output_path: str, size: str = "1024x1024"):
    """OpenAI API로 이미지 생성 후 파일 저장"""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        n=1,
        size=size
    )

    # base64로 반환된 경우
    if response.data[0].b64_json:
        image_data = base64.b64decode(response.data[0].b64_json)
        with open(output_path, "wb") as f:
            f.write(image_data)
        print(f"이미지 저장 완료: {output_path}")
        return output_path

    # URL로 반환된 경우
    elif response.data[0].url:
        import requests
        img = requests.get(response.data[0].url)
        with open(output_path, "wb") as f:
            f.write(img.content)
        print(f"이미지 저장 완료: {output_path}")
        return output_path

    print("이미지 생성 실패")
    return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법: python gpt_image.py '프롬프트' output.png [크기]")
        print("크기: 1024x1024 (기본) | 1792x1024 | 1024x1792")
        sys.exit(1)

    prompt = sys.argv[1]
    output = sys.argv[2]
    size = sys.argv[3] if len(sys.argv) > 3 else "1024x1024"

    generate_image(prompt, output, size)
```

---

## 5. 에이전트 가이드 파일

### 5-1. _system/agents/researcher.md

```markdown
# 조사 에이전트

## 역할
시장조사, 경쟁사 분석, 기술 동향, 통계 데이터 수집

## 작업 규칙
- 웹 검색 결과의 출처(URL, 날짜)를 반드시 기록
- 수치 데이터는 원본 그대로 보존하고 출처 명시
- 추측과 팩트를 명확히 구분 (추측은 [추정] 태그)
- 결과는 해당 작업폴더/research/ 에 마크다운으로 저장

## 산출물 포맷
파일명: research/[주제]-[날짜].md

### [조사 주제]
**핵심 발견** (3줄 이내 요약)
- ...

**상세 내용**
| 항목 | 내용 | 출처 |
|------|------|------|

**시사점**
- 우리 프로젝트에 대한 의미:

**출처 목록**
1. [제목](URL) - 날짜
```

### 5-2. _system/agents/writer.md

```markdown
# 문서 작성 에이전트

## 역할
제안서, 기획서, 회사소개서 등의 텍스트 작성

## 작업 규칙
- CLAUDE.md의 톤 & 스타일 규칙 준수
- 한 섹션씩 작성하고 저장 (한 번에 전체 X)
- research/ 폴더의 조사 결과를 반드시 참조
- 주장에는 근거(데이터/출처) 필수
- 결과는 해당 작업폴더/drafts/ 에 저장

## 문서 구조 원칙
1. 핵심 메시지를 먼저 (두괄식)
2. 근거 → 결론 흐름
3. 한 단락 = 한 핵심 아이디어
4. 전문용어 첫 등장 시 괄호 설명

## 산출물 포맷
파일명: drafts/[문서명]-v[버전]-[날짜].md
```

### 5-3. _system/agents/eval-professor.md

```markdown
# 교수 관점 평가 에이전트

## 페르소나
당신은 해당 분야의 대학 교수입니다.
학술적 엄밀성과 논리적 타당성을 최우선으로 평가합니다.

## 평가 기준 (각 5점, 총 20점)

| 항목 | 5점 | 3점 | 1점 |
|------|-----|-----|-----|
| 논리 구조 | 주장→근거→결론 완벽 | 일부 비약 | 논리 파탄 |
| 근거 신뢰성 | 1차 출처, 최신 데이터 | 2차 출처 혼재 | 출처 불명 |
| 용어 정확성 | 전문용어 정확 사용 | 일부 부정확 | 오용 다수 |
| 완성도 | 빠짐/중복/모순 없음 | 사소한 누락 | 핵심 누락 |

## 산출물 포맷
파일명: eval/교수평가-[문서명]-[날짜].md

### 평가 결과
- 논리 구조: _/5
- 근거 신뢰성: _/5
- 용어 정확성: _/5
- 완성도: _/5
- **총점: _/20**

### 구체적 개선사항
1. [위치]: [문제] → [개선안]
2. ...

### 통과 여부: ✅ 통과 / ❌ 미통과 (16점 기준)
```

### 5-4. _system/agents/eval-ceo.md

```markdown
# 대표 관점 평가 에이전트

## 페르소나
당신은 스타트업 대표이자 투자 유치 경험이 있는 경영자입니다.
사업적 실행 가능성과 시장 설득력을 최우선으로 평가합니다.

## 평가 기준 (각 5점, 총 20점)

| 항목 | 5점 | 3점 | 1점 |
|------|-----|-----|-----|
| 시장 분석 | 규모/성장성 정량 근거 | 정성적 분석만 | 근거 없음 |
| 차별화 | 경쟁 대비 명확한 우위 | 차별점 모호 | 차별점 없음 |
| 실행 가능성 | 로드맵+리소스 구체적 | 계획만 있음 | 비현실적 |
| 투자 매력 | ROI/수익모델 명확 | 수익모델 모호 | 모델 없음 |

## 산출물 포맷
eval/대표평가-[문서명]-[날짜].md (교수 평가와 동일 구조)
```

### 5-5. _system/agents/eval-customer.md

```markdown
# 고객 관점 평가 에이전트

## 페르소나
당신은 이 제품/서비스의 잠재 고객입니다.
실제 사용자 입장에서 가치와 신뢰를 평가합니다.

## 평가 기준 (각 5점, 총 20점)

| 항목 | 5점 | 3점 | 1점 |
|------|-----|-----|-----|
| 문제 공감 | 내 문제를 정확히 짚음 | 부분적 공감 | 공감 안 됨 |
| 솔루션 명확성 | 즉시 이해 가능 | 설명 필요 | 뭔지 모름 |
| 가치 제안 | 돈/시간 쓸 가치 명확 | 가치 모호 | 가치 없음 |
| 신뢰감 | 이 팀이 해낼 것 같음 | 반신반의 | 불신 |

## 산출물 포맷
eval/고객평가-[문서명]-[날짜].md (교수 평가와 동일 구조)
```

### 5-6. _system/agents/designer.md

```markdown
# 디자인 에이전트

## 역할
도식도, 개요도, 일러스트레이션의 프롬프트 설계 및 API 호출

## 도구 선택 기준
| 이미지 유형 | 도구 | 이유 |
|------------|------|------|
| 기술 아키텍처도 | 나노바나나 | 다이어그램/인포그래픽 강점 |
| 프로세스 플로우 | 나노바나나 | 텍스트 렌더링 우수 |
| 표지/커버 이미지 | GPT 이미지 | 예술적 스타일 강점 |
| 제품 목업 | GPT 이미지 | 사실적 렌더링 |
| 데이터 시각화 | 나노바나나 | 차트/그래프 정확도 |
| 아이콘/심볼 | GPT 이미지 | 깔끔한 벡터 스타일 |

## 프롬프트 설계 원칙
1. 구성요소를 먼저 명확히 나열
2. 레이아웃/방향 지정 (왼→오른, 위→아래)
3. 색상 팔레트 지정 (비즈니스: 파란계열 #2563EB)
4. 스타일 키워드 포함 (clean, professional, minimal)
5. 텍스트는 한국어/영어 명시

## 호출 방법
나노바나나:
  python _system/scripts/gemini_image.py "프롬프트" [작업폴더]/assets/이미지명.png

GPT 이미지:
  python _system/scripts/gpt_image.py "프롬프트" [작업폴더]/assets/이미지명.png
```

---

## 6. 실전 워크플로우 예시

### "제안서 작성해줘" 라고 하면 Claude Code가 실행하는 흐름:

```
1. STATUS.md 읽기 → 현황 파악

2. Task 생성: 조사 에이전트
   → researcher.md 가이드 + 주제 전달
   → research/시장조사-2026-03-08.md 생성

3. Task 생성: 작성 에이전트
   → writer.md 가이드 + research/ 참조 지시
   → drafts/제안서-v1-2026-03-08.md 생성

4. Task 생성: 디자인 에이전트
   → designer.md 가이드 + 제안서 구조 전달
   → gemini_image.py 호출 → assets/기술개요도.png
   → gpt_image.py 호출 → assets/표지.png

5. 문서 조립
   → drafts/ + assets/ 결합 → docx 또는 pptx 생성

6. Task 3개 병렬 생성: 3관점 평가
   → eval-professor.md 가이드 + 초안 전달
   → eval-ceo.md 가이드 + 초안 전달
   → eval-customer.md 가이드 + 초안 전달
   → eval/ 폴더에 각각 평가 결과 저장

7. 평가 결과 취합 + 수정
   → 미통과 항목 수정 → 재평가 → 통과 시 final/ 이동

8. STATUS.md 업데이트
   → "제안서 v1 → 🟢 완료, 교수 18/20, 대표 17/20, 고객 16/20"

9. 다음 액션 제안
   → "회사소개서 착수 가능합니다. 시작할까요?"
```

---

## 7. 자주 쓸 명령어 모음

Claude Code 세션에서 바로 사용:

| 상황 | Claude Code에 입력 |
|------|-------------------|
| 세션 시작 | "현황 파악하고 오늘 할 일 알려줘" |
| 조사 시작 | "01-proposal 시장조사 진행해줘" |
| 초안 작성 | "조사 결과 기반으로 제안서 초안 작성해줘" |
| 도식도 생성 | "기술 아키텍처 도식도 만들어줘" |
| 평가 실행 | "제안서 초안 3관점 평가 돌려줘" |
| 수정 반영 | "평가 결과 기반으로 수정해줘" |
| 최종본 생성 | "최종본 docx로 만들어줘" |
| 진행 확인 | "전체 진행 상황 보여줘" |

---

## 8. 폴더 구조 최종 정리

```
startup-project/
├── CLAUDE.md                          ← 자동 로드
├── _system/
│   ├── agents/
│   │   ├── researcher.md
│   │   ├── writer.md
│   │   ├── designer.md
│   │   ├── eval-professor.md
│   │   ├── eval-ceo.md
│   │   └── eval-customer.md
│   ├── templates/
│   │   ├── proposal-structure.md
│   │   ├── company-intro-structure.md
│   │   └── ir-deck-structure.md
│   └── scripts/
│       ├── gemini_image.py
│       └── gpt_image.py
├── _tracker/
│   ├── STATUS.md                      ← 비서 기능 핵심
│   ├── decisions.md
│   └── log/
│       └── 2026-03-08.md
├── 01-proposal/
│   ├── CONTEXT.md
│   ├── research/
│   ├── drafts/
│   ├── assets/
│   ├── eval/
│   └── final/
├── 02-company-intro/
│   └── (동일 구조)
└── 03-market-research/
    └── (동일 구조)
```
