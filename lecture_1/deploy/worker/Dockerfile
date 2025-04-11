# docker build --platform linux/amd64 -t fastapi-server:0.0.1 .
# docker tag fastapi-server:0.0.1 0hyeon/fastapi-server:0.0.1
# docker push 0hyeon/fastapi-server:0.0.1

# FastAPI 애플리케이션을 위한 Python 베이스 이미지
FROM python:3.10-slim

# 작업 디렉터리 설정
WORKDIR /app

# 종속성 파일 복사
COPY requirements.txt /app/

# 필요한 종속성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . /app/

# 포트 8000을 열어서 FastAPI 서버를 실행할 수 있도록 설정
EXPOSE 8000

# FastAPI 애플리케이션을 Uvicorn 서버로 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
