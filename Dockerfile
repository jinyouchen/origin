FROM python:3.12-slim 
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt  # 分层安装，参考 docker-basics.pdf
COPY . .
ENV PYTHONUNBUFFERED=1
CMD ["python", "app/main.py"]