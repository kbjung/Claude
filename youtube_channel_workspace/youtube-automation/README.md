# YouTube Automation

유튜브 채널 콘텐츠 자동화 파이프라인 프로젝트

## 채널 구성

| 채널 | 콘텐츠 | 자동화 수준 | 상태 |
|------|--------|------------|------|
| 힐링 음악 (Healing Retriever) | 힐링 음악 + 영상 롱폼 | 전체 자동화 | 개발 예정 |
| AI 뉴스 쇼츠 | AI 뉴스 요약 쇼츠 | 전체 자동화 | 개발 예정 |
| 창업 도전기 | 창업 과정, AI 활용기 | 반자동화 | 기획 단계 |
| AI 활용법 강좌 | AI 도구 강좌 | 반자동화 | 미래 확장 |

## 폴더 구조

```
youtube-automation/
├── docs/                    # 계획 문서 및 인수인계
├── healing-music/           # 힐링 영상 자동화
│   ├── src/                 # 소스 코드
│   ├── config/              # 설정 파일
│   └── output/              # 생성 영상 (git 제외)
├── ai-news-shorts/          # AI 뉴스 쇼츠 자동화
│   ├── src/
│   ├── config/
│   └── output/
├── common/                  # 공통 유틸 (업로드, FFmpeg 등)
├── .gitignore
└── README.md
```

## 기술 스택

- **언어:** Python
- **영상 처리:** FFmpeg
- **업로드:** YouTube Data API v3
- **AI:** Claude API (스크립트 생성), TTS API (음성 합성)
- **소스:** Pexels/Pixabay API (영상), YouTube Audio Library (음악)

## 실행 순서

1. 힐링 영상 자동화 → 2. AI 뉴스 쇼츠 → 3. 창업 도전기 반자동화 → 4. AI 강좌 확장
