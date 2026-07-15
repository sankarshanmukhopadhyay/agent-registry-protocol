FROM python:3.12-slim
WORKDIR /app
COPY scripts/requirements.txt scripts/requirements.txt
RUN pip install --no-cache-dir -r scripts/requirements.txt
COPY . .
EXPOSE 8000
CMD ["python3","-m","uvicorn","reference.app:app","--host","0.0.0.0","--port","8000"]
