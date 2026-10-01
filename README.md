<div align="center">

# ⚙️ PUMP AI TEAM

### 파인블랭킹 프레스 유압펌프 이상탐지

**진동과 전류로 이상을 찾고, 정상 운전변화의 오경보를 줄입니다.**

2026 제6회 K-인공지능 제조데이터 분석 경진대회 · 과제 ③

[실험 계획](docs/EXPERIMENT_PLAN.md) · [팀 협업 안내](docs/TEAM_WORKFLOW.md) · [평가 기준](docs/EVALUATION.md)

</div>

---

## 📌 프로젝트 소개

진동 2채널과 전류 1채널로 이상을 탐지하고 정상 운전변화의 오경보를 줄이는 KAMP 과제 ③ 협업 프로젝트입니다.

| 항목 | 내용 |
|---|---|
| 설비 | 파인블랭킹 프레스 유압펌프 |
| 입력 | 진동 2채널 + 전류 1채널 |
| 데이터 | 정상 20,000행 / 이상 600행, 정리 전 기준 |
| 기록 간격 | 구간 내부 약 0.1초, 구간 사이 공백 존재 |
| 평가 | Precision · Recall · F1 · AP · FP/FN · 판정 커버리지 |

> 정상과 이상이 서로 다른 날짜에 기록되었습니다. 내부 평가만으로 새로운 날짜·설비의 성능을 보증하지 않습니다. AI0/AI1의 정확한 상·하부 대응과 센서 단위는 추가 확인이 필요합니다.

## ✨ 현재 상태

- 공통 데이터 점검·기록 조각 분할·학습/검증/시험 배정 도구를 제공합니다.
- 협업 규칙, 실험 계획, Issue/PR 양식, 데이터 없는 자동 테스트를 포함합니다.
- 기존 실험 모델의 이식과 재학습은 아직 완료하지 않았습니다. 이 저장소에 새로운 성능 수치를 주장하지 않습니다.
- 기존 분석에서 반복 확인한 데이터이므로 여기서 만든 test도 새 외부 검증 데이터가 아닙니다.

## 🚀 실행 방법

Python 3.12를 권장합니다. 현재 준비 도구는 표준 라이브러리만 사용합니다.

```bash
git clone https://github.com/goddesse12-coder/pump-ai-team.git
cd pump-ai-team
python -m unittest discover -s tests -v
```

공개 저장소이므로 누구나 clone할 수 있습니다. 직접 push하려면 팀원 초대 수락과 GitHub 인증이 필요합니다. 아래 원본 파일을 준비한 뒤 실행합니다.

```bash
python scripts/prepare_data.py --data-dir data/raw --output-dir outputs/preparation
```

`data/raw/`에 다음 두 파일을 직접 넣습니다.

- `press_data_normal.csv`
- `outlier_data.csv`

다른 위치의 파일도 `--data-dir`로 지정할 수 있습니다. 원본 CSV는 Git 추적에서 제외합니다. 팀 내 원본 전달과 대회 제출용 데이터 패키징은 별도로 관리합니다.

실행하면 `audit.json`, `segments.csv`, `rows.csv`가 만들어집니다. 모두 Git에서 제외되는 로컬 출력입니다. 파일 해시와 분할 설정이 같아야 팀 간 결과를 비교할 수 있습니다.

## 📏 공통 평가 원칙

1. 시간과 파일명은 분할·추적에만 사용하고 모델 특징에서 제외합니다.
2. 겹치는 창을 만들기 전에 기록 조각 단위로 분할합니다.
3. 정상과 이상 각각 시간순 70/15/15로 배정합니다. 이는 같은 두 세션 안의 내부 평가이며 날짜 holdout이 아닙니다.
4. 스케일러·특징 선택·예상 진동 회귀는 학습 데이터에서만 적합합니다.
5. 임계값·증강 강도·경보 규칙은 개발 데이터 안에서 결정합니다.
6. 짧은 조각은 점검 단계에서 제외하지 않습니다. 모델 단계에서 보류하면 보류율과 라벨별 개수를 보고합니다.
7. 조각은 수집 단위입니다. 프레스 사이클이나 독립 고장 사건으로 단정하지 않습니다.

## 🗂️ 프로젝트 구조

```text
pump-ai-team/
├── .github/                 # Issue·PR 양식과 자동 검사
├── configs/split.json       # 공통 분할 설정
├── data/raw/                # 원본 CSV, Git 추적 제외
├── data/processed/          # 전처리 데이터, Git 추적 제외
├── docs/                    # 실험·평가·협업 안내
├── experiments/TEMPLATE.md  # 실험 기록 양식
├── scripts/prepare_data.py  # 데이터 준비 실행
├── src/pump_data.py         # 점검·조각화·분할
├── tests/test_data.py       # 자동 테스트
└── requirements.txt
```

| 경로 | 역할 |
|---|---|
| `src/pump_data.py` | 데이터 검증과 공통 분할 |
| `scripts/prepare_data.py` | 준비 도구 실행 진입점 |
| `configs/split.json` | 공유 분할 설정 |
| `docs/EXPERIMENT_PLAN.md` | 모델 개선 실험과 우선순위 |
| `docs/TEAM_WORKFLOW.md` | GitHub 초보자용 공동 작업 순서 |
| `docs/EVALUATION.md` | 공정한 평가와 데이터 한계 |
| `experiments/TEMPLATE.md` | 실험 기록 복사용 양식 |
| `tests/` | 분할·중복 처리 검증 |

## 🧪 모델 개발 계획

기준 모델 Logistic Regression / LightGBM → 예상 진동 잔차 특징 → 강한 이상·지속 이상 경보 → 진동·전류 불일치 → 정상 학습 보조 모델 순으로 하나씩 비교합니다. 자세한 내용은 [실험 계획](docs/EXPERIMENT_PLAN.md)을 참고하세요.

팀원은 [협업 안내](docs/TEAM_WORKFLOW.md)를 먼저 읽고 Issue 하나를 맡아 별도 브랜치에서 작업합니다.

| 단계 | 확인할 질문 | 비교 실험 |
|---|---|---|
| E00 | 복잡한 모델이 필요한가? | Logistic / LightGBM |
| E01 | 부하 증가와 이상을 구분할 수 있는가? | 예상 진동 잔차 추가 |
| E02 | 탐지 지연과 오경보를 함께 줄일 수 있는가? | 강한 이상 / 지속 이상 경보 |
| E03 | 전류만 이상할 때 무엇을 확인하는가? | 센서별 판단 불일치 |
| E04 | 새로운 이상을 보완할 수 있는가? | PCA / IF / AE 보조 모델 |

## 🤝 협업 규칙

```text
main                         검증된 기준 버전
└── develop                  팀 작업 통합
    ├── feat/preprocessing   전처리
    ├── feat/load-residual   예상 진동 잔차
    ├── feat/alarm-policy    경보 정책
    └── analysis/errors     오류 분석
```

같은 저장소에 초대된 팀원이 기능별 브랜치로 작업합니다. 기능 PR은 `develop`으로, 검증된 통합 결과는 `main`으로 보냅니다. 브랜치 보호는 별도 설정 사항이며 문서만으로 강제되지 않습니다.

```bash
git switch develop
git pull --ff-only
git switch -c feat/load-residual
# 작업과 테스트 후
git add src tests experiments
git commit -m "feat: add load-conditioned vibration residual"
git push -u origin feat/load-residual
```

1. Issue에 가설·담당자·완료 조건을 적습니다.
2. 한 브랜치에서 한 가지 변경을 진행합니다.
3. 공통 분할과 평가 기준으로 실험을 기록합니다.
4. `develop`으로 PR을 열고 다른 팀원의 검토를 받습니다.
5. 통합 검증이 끝난 버전을 `main`에 반영합니다.

| 커밋 접두어 | 용도 | 예시 |
|---|---|---|
| `feat` | 기능·특징 추가 | `feat: add current roughness` |
| `fix` | 오류 수정 | `fix: reset alarm history after gaps` |
| `docs` | 문서 수정 | `docs: clarify evaluation coverage` |
| `test` | 검증 추가 | `test: reject conflicting timestamps` |
| `refactor` | 코드 구조 정리 | `refactor: separate feature extraction` |
| `chore` | 환경·설정 변경 | `chore: pin tested dependencies` |

## 👥 담당 영역

아래는 분담 제안입니다. 팀원 이름과 GitHub 아이디는 확정 후 추가합니다.

| 영역 | 맡을 일 | 담당자 |
|---|---|---|
| 데이터 | 전처리·분할·커버리지 | 미정 |
| 모델 | 기준 모델·잔차 특징·보조 탐지 | 미정 |
| 검증 | FP/FN·경보 지연·비교 실험 | 미정 |
| 통합 | PR 검토·재현성·제출 자료 | 미정 |
