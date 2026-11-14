# AGENTS.md — Antigravity 개발 및 협업 가이드

이 문서는 **업무 말투 변환기(`biztalk_antigravity`)** 프로젝트를 개발할 때 **Google Antigravity 에이전트**가 반드시 숙지하고 준수해야 하는 프로젝트 개요, 개발 원칙, 기술 규격 및 행동 규칙을 정의합니다.

---

## 1. 프로젝트 개요 (Project Overview)

- **프로젝트명**: 업무 말투 변환기 (`biztalk_antigravity`)
- **목적**: 사용자가 일상적/직설적으로 작성한 문장을 입력하면, 수신 대상(상사, 타팀 동료, 고객, 팀원)에 최적화된 비즈니스 업무 말투로 자동 변환해 주는 경량 웹 서비스
- **프로젝트 성격**: 바이브 코딩(Vibe Coding) 기반의 One Day 완성형 프로젝트
- **핵심 목표**: 완벽하고 거대한 시스템이 아니라 **"실제로 동작하고 배포 가능한 깔끔한 MVP(최소 기능 제품)"** 완성

### 주요 대상별 변환 스타일 (4종)
1. **상사 / 임원 (`boss`)**: 격식 있는 경어체, 공손하고 명확하며 결론 중심의 어조
2. **타팀 동료 (`colleague`)**: 정중하면서도 상호 협조적이고 명확한 업무 요청 어조
3. **고객 / 외부 (`client`)**: 친절하고 신뢰감을 주는 서비스 중심 비즈니스 어조
4. **팀 내 동료 (`team`)**: 간결하고 빠른 피드백이 가능한 실무적 어조

### 필수 기능 vs 제외 기능 (Scope Boundary)
- **포함 기능 (반드시 구현)**:
  - 텍스트 입력창 및 수신 대상 선택 버튼(4종)
  - Upstage Solar 모델 기반 말투 변환 API 연동
  - 변환 결과 화면 표시, 로딩 인디케이터, 클립보드 복사 기능
  - FastAPI Swagger UI(`/docs`) 및 정적 웹페이지 라우팅
- **제외 기능 (임의 구현 절대 금지)**:
  - 사용자 로그인 / 회원가입 / 인증
  - 데이터베이스 연동 및 변환 이력 저장
  - 과도한 서드파티 라이브러리 및 불필요한 설정

---

## 2. 기술 스택 및 아키텍처 (Tech Stack & Architecture)

| 영역 | 기술 스택 | 설명 / 제약사항 |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript (ES6+) | 빌드 도구 없는 순수 웹 기술 사용 (React/Vue 등 도입 금지) |
| **Backend** | Python 3.11+, FastAPI, Uvicorn | 경량 REST API 서버 구축 |
| **AI / LLM** | LangChain, `langchain-upstage`, Solar-Pro | Upstage Solar-Pro 모델을 통한 맞춤형 프롬프트 변환 |
| **Environment** | `python-dotenv` | 환경 변수(`.env`) 기반 API 키 관리 |
| **Deployment** | Vercel, Git/GitHub | 단일 저장소 프론트/백엔드 배포 구조 |

### 목표 디렉토리 구조
```text
biztalk_antigravity/
├── .agents/                    # 에이전트 스킬 및 MCP 설정
│   ├── skills/
│   │   ├── frontend-design/    # UI/UX 디자인 가이드라인
│   │   └── karpathy-guidelines/# 코드 단순성 및 신중성 지침
│   └── mcp_config.json         # MCP 서버 설정
├── backend/
│   ├── main.py                 # FastAPI 앱, CORS, 정적 파일 마운트
│   ├── routers/
│   │   └── convert.py          # POST /api/convert 엔드포인트
│   ├── services/
│   │   └── tone_converter.py   # LangChain + Upstage Solar 연동 로직
│   ├── prompts/
│   │   └── templates.py        # 4가지 대상별 프롬프트 정의
│   ├── models/
│   │   └── schemas.py          # Pydantic 요청/응답 모델
│   └── requirements.txt        # 백엔드 의존성
├── frontend/
│   ├── index.html              # 메인 UI
│   ├── css/
│   │   └── style.css           # 스타일시트
│   └── js/
│       └── app.js              # 프론트엔드 비즈니스 로직
├── .env                        # Upstage API 키 등 민감 정보 (Git 제외)
├── .gitignore                  # Git 추적 제외 목록
├── AGENTS.md                   # 본 에이전트 지침 문서
├── PRD_업무말투변환기.md        # 상세 요구사항 명세서
└── 개요서_업무말투변환기.md     # 프로젝트 개념 개요서
```

---

## 3. Antigravity 에이전트 핵심 행동 원칙

에이전트는 모든 코드 작성 및 명령 실행 시 다음 원칙을 철저히 준수해야 합니다.

### 3-1. 바이브 코딩 3원칙
1. **완료 기준을 먼저 정의하라**:
   - 코드를 무작정 늘리지 말고, PRD의 완료 체크리스트 항목만 정확히 충족합니다.
   - 요청받지 않은 기능을 선제적으로 추가하지 않습니다.
2. **조사 먼저, 구현 나중**:
   - 외부 라이브러리(`langchain-upstage` 등) 연동 시 사전에 최신 사용법과 인터페이스를 확인한 후 구현합니다.
3. **버그는 분석 먼저, 수정 나중**:
   - 에러 발생 시 섣부른 코드 수정을 하지 않고 원인을 단계별로 분석한 뒤 사용자에게 원인과 수정 방향을 공유합니다.

### 3-2. Karpathy Guidelines 준수 (코드 단순성 및 외과적 수정)
- **Simplicity First**: 단일 기능에 불필요한 추상화 레이어나 디자인 패턴을 과도하게 도입하지 않습니다. 50줄로 작성 가능한 코드를 200줄로 만들지 마십시오.
- **Surgical Changes**: 기존에 정상 작동하는 코드나 관련 없는 설정을 건드리지 않고, 수정이 필요한 대상만 정밀하게 변경합니다.
- **Think Before Coding**: 불분명한 요구사항이 있다면 가정을 세우지 말고 먼저 질문하여 확인합니다.

### 3-3. 프론트엔드 디자인 원칙 (`frontend-design` 스킬 반영)
- 진부하거나 인공적인 AI 기본 템플릿 느낌(과도한 그라디언트, 무의미한 카드 나열, 통일감 없는 둥근 모서리 등)을 피합니다.
- 직장인이 매일 켜두고 쓰는 전문 비즈니스 도구 느낌의 직관적이고 군더더기 없는 레이아웃을 지향합니다.
- 명확한 타이포그래피 계층, 누르기 쉬운 대상 선택 탭, 한눈에 들어오는 변환 결과창 및 복사 인터랙션을 구현합니다.

---

## 4. 안전 및 보안 절대 규칙 (Security & Guardrails)

Antigravity 글로벌 지침에 따라 아래 항목은 **예외 없이 절대 금지**됩니다.

1. **민감 정보 보호**:
   - `.env`, `credentials`, API 키 파일의 내용을 터미널에 출력하거나 대화창에 노출하지 않습니다.
   - `.env` 파일이 Git에 커밋되지 않도록 `.gitignore` 상태를 항상 점검합니다.
2. **파괴적 Git 명령 금지**:
   - `git push --force`, `git reset --hard`, `git clean -fd` 등 히스토리를 파괴하는 명령은 절대 실행하지 않습니다.
   - 사용자 확인 없는 자동 커밋 및 원격 푸시를 수행하지 않습니다.
3. **시스템 보호**:
   - 프로젝트 루트(`C:\vibecoding\biztalk_antigravity`)를 벗어난 시스템 경로나 상위 디렉터리에 접근하거나 파일을 수정하지 않습니다.
4. **환경 호환성**:
   - 운영체제는 **Windows (PowerShell)** 환경이므로 Bash 전용 명령어(예: `export`, `rm -rf`, 세미콜론 연결 등) 대신 PowerShell 호환 명령어를 사용합니다.

---

## 5. 단계별 개발 절차 및 검증 루프 (Plan → Build → Verify)

### STEP 1. 환경 준비 및 의존성 구성
- 가상환경(`.venv`) 활성화 및 `requirements.txt` 패키지 설치
  - 필요 패키지: `fastapi`, `uvicorn`, `langchain`, `langchain-upstage`, `python-dotenv`, `pydantic`
- `.env`에 `UPSTAGE_API_KEY` 설정 확인 (키 내용 자체는 노출하지 않음)

### STEP 2. 백엔드 구현 및 단위 검증
1. `models/schemas.py`: `ConvertRequest`, `ConvertResponse` Pydantic 모델 작성
2. `prompts/templates.py`: 수신 대상 4종(`boss`, `colleague`, `client`, `team`) 시스템 프롬프트 정의
3. `services/tone_converter.py`: `ChatUpstage` 모델 연동 및 체인 실행 함수 구현
4. `routers/convert.py`: `POST /api/convert` 라우터 구현 및 예외 처리
5. `main.py`: CORS 설정, Health Check (`GET /health`), API 라우터 등록 및 정적 파일 마운트
6. **검증**: `uvicorn` 실행 후 `http://localhost:8000/docs`에서 API 직접 호출 테스트

### STEP 3. 프론트엔드 구현 및 연동 검증
1. `frontend/index.html`: 입력 텍스트영역, 수신 대상 선택 탭/버튼, 변환 버튼, 결과 영역, 복사 버튼 배치
2. `frontend/css/style.css`: 정돈된 비즈니스 톤의 반응형 UI 스타일링
3. `frontend/js/app.js`: 버튼 선택 상태 토글, API 통신 비동기 호출(`fetch`), 로딩 스피너 및 클립보드 복사 로직 구현
4. **검증**: 로컬 브라우저에서 실제 변환 호출 및 클립보드 복사 동작 확인

### STEP 4. 배포 준비
- Vercel 설정을 위한 `vercel.json` 및 라우팅 점검
- Git 저장소 정리 및 커밋 전 불필요한 캐시(`__pycache__`) 배제 점검

---

## 6. 에이전트 소통 규약
- 모든 응답과 커뮤니케이션은 **한국어**로 작성합니다.
- 중요한 구조 변경이나 5단계 이상의 복합 작업은 착수 전 계획을 먼저 설명합니다.
- 코드 변경 후에는 반드시 **검증 결과(서버 실행 로그, 엔드포인트 응답 상태 등)**를 사용자에게 명확히 보고합니다.

---

## 7. @PRD_업무말투변환기.md 문서와 AGENTS.md 문서 항상 최신화 하기
* 모든 변경사항이 발생하면 (예를 들어 기능이나 요구사항이 변경 되거나, 화면명세가 변경되거나, Source Code가 변경 되거나 라이브러리 버전이 변경되면) 관련된 markdown 문서들도 반드시 업데이트 합니다. 
* 구현이 완료된 사항들은 `@PRD_업무말투변환기.md\2. 완료 체크리스트`에 모두 체크표시를 해서 완료 되었음을 반드시 표시하세요.
* `@PRD_업무말투변환기.md\8. 단계별 구현 순서` 에서도 단계별로 구현이 완료되면 체크표시를 해서 완료 되었음을 반드시 표시하세요.

---

## 8. 계획서(Plan).md 문서의 저장 위치
* 계획서(Plan).md 문서는 모두 현재 프로젝트 루트 아래에 plan 폴더를 생성하여 작성하세요.
