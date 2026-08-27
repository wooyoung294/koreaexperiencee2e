# KoreaExperience E2E

KoreaExperience 웹 서비스의 핵심 사용자 흐름을 검증하는 E2E 자동화 프로젝트입니다.

- 테스트 프레임워크: `pytest`, `pytest-bdd`
- 브라우저 자동화: `Playwright Python`
- 설계 방식: `Page Object Model (POM)`
- 리포트: `Allure Report`
- 기본 테스트 URL: `https://koreaexperience.kr/ko`

## 테스트 범위

| Feature | Scenario | 주요 검증 |
| --- | --- | --- |
| 홈 팝업 | 오늘 안 보기 선택 시 팝업 숨김 날짜 저장 | 팝업 이미지 로드, Local Storage 날짜 저장 |
| 홈 팝업 | 영어 선택 시 영어 홈 팝업 표시 | 언어 변경, 영어 팝업 이미지 로드 |
| 홈 검색 | 맛집 검색 결과 노출 | 검색어 입력, 검색 결과 제목 노출 |
| K-Perks 상세 | 제천국제음악영화제 상세 정보 노출 | 카드 이동, 소개·프로그램·지역·상태·기간 노출 |
| 로그인 | 이메일 계정 로그인 | 자체 로그인 성공 및 로그인 UI 노출 |

모든 시나리오는 Playwright `expect` 기반 assertion으로 결과를 직접 검증합니다.

## 프로젝트 구조

```text
koreaexperiencee2e/
├── case/                  # Feature 시나리오와 pytest 연결
├── common/                # 공통 Action/Expect 베이스
├── components/            # 여러 페이지에서 사용하는 UI 컴포넌트 POM
├── configs/               # 환경별 테스트 데이터
├── features/              # Gherkin Feature/Scenario
├── pages/                 # Page Object
├── steps/                 # pytest-bdd Step Definition
├── conftest.py            # 브라우저, 로그인 세션, 영상, Allure fixture
├── pytest.ini             # pytest 실행 및 marker 설정
├── pyproject.toml         # Python 패키지와 개발 도구 설정
└── .env.example           # 환경변수 예시
```

`conftest.py`가 `steps/*_steps.py`를 자동으로 등록하므로 새로운 Step 파일을 별도로 plugin 목록에 추가할 필요가 없습니다.

## 설치

Python 3.11 이상이 필요합니다. 

## 환경변수

Git에서 제외된 `.env`에 실행 환경과 테스트 전용 로그인 계정을 설정합니다.

```env
BASE_URL=https://koreaexperience.kr/ko
HEADLESS=true
BROWSER=chromium
IGNORE_HTTPS_ERRORS=false
ID=your_login_email
PASSWORD=your_login_password
```

`ID`와 `PASSWORD`가 없으면 `@login` 시나리오는 skip되며 일반 시나리오는 비로그인 상태로 실행됩니다.

## 로그인 세션과 테스트 독립성

- 최초 일반 시나리오 실행 전 이메일 로그인을 한 번 수행합니다.
- 쿠키, Local Storage, IndexedDB 인증 상태는 프로세스 메모리에만 저장합니다.
- 각 시나리오는 새로운 BrowserContext를 사용하고 저장된 인증 상태만 주입받습니다.
- 통과한 시나리오가 끝나면 갱신된 인증 상태를 다음 시나리오에 전달합니다.
- `@login` 시나리오는 저장된 인증 상태를 주입받지 않아 항상 비로그인 상태에서 시작합니다.
- 인증 상태 파일은 디스크에 저장하지 않습니다.

## 실행

전체 테스트:

```powershell
pytest
```

브라우저 표시:

```powershell
pytest --headed
```

Marker 실행:

```powershell
pytest -m smoke
pytest -m login
pytest -m popup
```

다른 브라우저나 URL 사용:

```powershell
pytest --browser firefox
pytest --base-url https://koreaexperience.kr/ko
```

## Marker

| Marker | 용도 |
| --- | --- |
| `login` | 저장된 인증 상태 없이 실제 로그인 검증 |
| `popup` | 홈 팝업 검증을 위해 `home-popup-dismissed` 제거 |
| `smoke` | 핵심 기능 스모크 테스트 |
| `regression` | 전체 회귀 테스트 분류 |

## Allure 리포트

테스트를 실행하면 `allure-results/`가 매번 초기화되고 새 결과가 생성됩니다.

```powershell
allure serve allure-results
```

정적 HTML 생성:

```powershell
allure generate allure-results --clean -o allure-report
```

Allure 목록에는 Gherkin 시나리오명이 한글 테스트 제목으로 표시됩니다.
