# 팀 협업 안내

## 저장소 개설

현재 저장소는 사용자 선택에 따라 공개(Public)입니다: https://github.com/goddesse12-coder/pump-ai-team . 팀원을 Collaborator로 초대하면 같은 저장소의 기능별 브랜치에서 협업할 수 있습니다. 원본 센서 데이터와 로컬 환경은 업로드하지 않습니다. 조직은 GitHub에서 공동 소유하는 팀 공간이며 필수는 아닙니다.

이 프로젝트의 로컬 폴더 이름은 `fineblanking-pump-anomaly`입니다. 원격 저장소 주소는 GitHub에서 실제 생성된 주소를 사용하세요. 개인 계정 또는 조직 이름을 임의로 넣지 마세요.

GitHub에서 빈 저장소를 만들 때 README/.gitignore 자동 생성을 끄면 로컬 파일과 첫 커밋이 충돌하지 않습니다. 저장소 화면의 안내에 따라 원격을 연결하고 `main`을 push합니다. 이 프로젝트에는 로그인 정보가 포함되지 않습니다.

## 매일 작업 순서

1. GitHub Issues에서 작업을 등록하고 담당자를 정합니다.
2. 최신 `develop`을 받은 뒤 기능별 브랜치를 만듭니다.
3. 한 브랜치에서 한 가지 실험 또는 수정만 진행합니다.
4. 코드와 실험 기록을 커밋하고 브랜치를 push합니다.
5. Pull Request를 열어 다른 팀원에게 검토를 요청합니다.
6. 테스트와 검토가 끝나면 `develop`으로 합칩니다. 통합 검증 후 `main`으로 PR을 보냅니다.

```bash
git switch develop
git pull --ff-only
git switch -c feat/load-residual
# 작업 후
python -m unittest discover -s tests -v
git add src scripts tests docs experiments configs
git commit -m "Add load-conditioned vibration residual experiment"
git push -u origin feat/load-residual
```

## 담당 작업 예시

| 작업 | 브랜치 예시 | 산출물 |
|---|---|---|
| 공통 전처리·분할 | `feat/preprocessing` | 동일한 분할 manifest와 커버리지 |
| 기준 모델 이식 | `feat/baselines` | Logistic / LightGBM 동일조건 비교 |
| 예상 진동 잔차 | `feat/load-residual` | 기존 특징 대비 추가 효과 |
| 경보 정책 | `feat/alarm-policy` | 오경보·탐지율·지연 비교 |
| 오류 분석 | `analysis/error-cases` | FP/FN 조건과 파형 |

담당자 이름은 팀에서 확정합니다. 이 표는 GitHub Issue를 실제 생성한 목록이 아닙니다.

## 충돌 줄이기

- `main`에서 직접 동시에 작업하지 않습니다.
- 데이터 분할 설정 변경은 반드시 팀 합의 후 PR로 진행합니다.
- 원본 데이터, 가상환경, 모델 파일, 대형 결과 파일을 커밋하지 않습니다.
- 작은 요약 결과는 `experiments/`의 Markdown으로 기록합니다.
- 노트북의 공통 처리 코드는 Python 모듈로 옮겨 중복 수정을 줄입니다.

## 권장 GitHub 설정

저장소 설정에서 PR 검토 1명과 CI 통과를 병합 조건으로 설정하는 것을 권장합니다. 계정 요금제와 조직 정책에 따라 사용할 수 있는 보호 설정이 다릅니다. 현재 이 안내는 원격 보호 규칙이 실제 설정되었다는 뜻이 아닙니다.
