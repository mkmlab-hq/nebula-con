# Python 3.12 기반 이미지 사용
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 개발용 의존성 설치 (선택사항)
COPY dev-requirements.txt .
RUN pip install --no-cache-dir -r dev-requirements.txt

# Jupyter 노트북 설치
RUN pip install --no-cache-dir jupyter notebook

# 프로젝트 파일 복사
COPY . .

# 포트 설정
EXPOSE 8000 8888

# 기본 명령어 설정
CMD ["python", "-m", "http.server", "8000"] 