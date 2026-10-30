# TrainerCRUD

**Python 기반 콘솔 헬스장 회원 및 운동 관리 프로그램**

TrainerCRUD는 회원 정보, 신체 정보, 운동 및 식단 기록, 운동 기구 목록과 부가 서비스를 관리하는 CLI(Command Line Interface) 프로젝트입니다. 기능별 모듈을 분리하고 JSON 파일에 데이터를 저장하는 구조로 구현했습니다.

## 주요 기능

| 구분 | 설명 |
| --- | --- |
| 회원 관리 | 회원 등록, 조회, 수정, 삭제 및 목록 관리 |
| 신체 정보 | 회원별 신체 정보 및 측정 기록 관리 |
| 운동 관리 | 운동 종류와 운동 기구 정보 관리 |
| 운동 기록 | 회원별 운동 기록 관리 |
| 식단 관리 | 회원별 식단 데이터 관리 |
| 부가 서비스 | 회원별 부가 서비스 정보 관리 |

> 세부 입력 항목과 지원 기능은 버전에 따라 달라질 수 있습니다.

## 기술 스택

- **Language:** Python
- **Interface:** CLI (콘솔 메뉴)
- **Storage:** JSON 파일
- **Version Control:** Git / GitHub

## 프로젝트 구조 (File Tree)

```text
TrainerCRUD/
├── applications/             # 기능별 비즈니스 로직
│   ├── __init__.py
│   ├── trainer_crud.py        # 회원 CRUD
│   ├── machine_list.py        # 운동 기구 관리
│   ├── extra_service.py       # 부가 서비스 관리
│   ├── details.py             # 회원 신체 정보 관리
│   ├── diet.py                # 식단 관리
│   ├── workout_crud.py        # 운동 관련 CRUD
│   └── utils.py               # 공통 유틸리티
├── data/                     # JSON 데이터 저장소
│   ├── members.json           # 전체 회원 목록
│   ├── muscles.json           # 운동 부위/종류 데이터
│   ├── workouts.json          # 운동 관련 공통 데이터
│   └── members/              # 회원별 데이터 디렉터리
│       └── <user_id>/
│           ├── details.json
│           ├── workouts.json
│           ├── diet.json
│           └── extra_service.json
├── image/                    # 프로젝트 이미지
├── interface.py              # 콘솔 메뉴 및 기능 연결
├── main.py                   # 프로그램 실행 진입점
├── file_tree.txt             # 파일 구조 안내
├── .gitignore
└── README.md
```

위 트리는 저장소의 `file_tree.txt`를 바탕으로 정리한 주요 파일 구조입니다. 실제 파일 및 회원별 데이터 디렉터리는 버전에 따라 다를 수 있습니다.

## 설치 및 실행

### 1. 저장소 복제

Windows CMD에서 다음 명령어를 실행합니다.

```cmd
git clone https://github.com/AlwaysHoon/TrainerCRUD.git
cd TrainerCRUD
```

### 2. 프로그램 실행

프로젝트 최상위 디렉터리에서 실행합니다.

```cmd
python main.py
```

Python이 설치되어 있어야 합니다. 추가 패키지 의존성은 실행 환경과 소스 코드의 import 구문을 확인해 주세요.


## 데이터 관리 방식

전체 회원 목록은 `data/members.json`에서 관리하고, 회원별 세부 정보는 `data/members/<user_id>/` 아래에 구분해 저장하는 구조입니다.

이 방식은 기능별 모듈과 회원별 데이터를 분리하기 쉬운 장점이 있습니다. 다만 JSON 파일을 직접 읽고 쓰는 방식이므로 다중 사용자 동시 수정, 접근 권한 관리, 데이터 무결성 보장 등이 필요한 운영 환경에서는 데이터베이스 도입을 고려해야 합니다.

## 설계 특징

- **모듈화:** 회원, 운동, 식단, 부가 서비스를 독립된 Python 모듈로 구성
- **CRUD 중심:** 데이터 생성(Create), 조회(Read), 수정(Update), 삭제(Delete) 기능 구현
- **파일 기반 저장:** 별도 데이터베이스 서버 없이 JSON 파일 사용
- **콘솔 인터페이스:** 터미널에서 메뉴 기반으로 조작
- **확장 가능성:** 기능별 모듈 구조를 바탕으로 기능 추가 및 저장소 교체 가능

## 저장소

- GitHub: https://github.com/AlwaysHoon/TrainerCRUD

---

> 본 프로젝트는 Python의 클래스 설계, CRUD, 파일 입출력, 모듈화 및 데이터 관리 구조를 연습하기 위해 제작되었습니다.
