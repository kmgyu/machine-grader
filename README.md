# 🧠 Machine-Grader

_**"무씬건 그라인더 그라라라라라라라라"**_
**Machine-Grader**는 기계 학습 모델을 기반으로 제출된 답안을 자동으로 채점하는 웹 애플리케이션입니다. Flask와 SQLAlchemy를 기반으로 구축되었으며, 사용자로부터 업로드된 텍스트 또는 파일 답안을 처리하고, 정답과 비교하여 점수를 산정합니다.

---

## 🚀 Features

- 사용자 업로드 기반 답안 제출
- 학번별 점수 기록 및 랭킹 제공
- 관리자용 점수 조회 및 데이터 관리 기능 (예정에 있을지도? >_0 -☆)

---

## 🏗️ Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: SQLite (기본), MySQL/PostgreSQL (확장 가능)
- **Etc**: Jinja2, HTML/CSS

---

## 🧩 tasty한 설명 첨가
Machine-Grader는 정답과 학생의 답안을 비교해 점수를 계산합니다.

correct 폴더에 correct.csv라는 파일을 이용해 정답을 비교합니다.
현재 하나의 문제에 대한 정답만을 판별 가능합니다!

채점 후 점수가 기록되며, 랭킹에 등록됩니다.
채점 직후 등수는 모든 테스트케이스에 대한 등수이며, 랭킹은 개인별 최고 점수를 기준으로 등수가 정해집니다.

---

## 🖥️ 사용 방법

### 0. 의존성
windows11 환경에서 python 3.7.6으로 만들어졌습니다.
패키지 버전은 requirements.txt를 참고하시기 바랍니다.

### 1. 설치

```bash
git clone https://github.com/your_username/machine-grader.git
cd machine-grader
pip install -r requirements.txt
```

### 2. 실행하기
```bash
python tasty.py
```



