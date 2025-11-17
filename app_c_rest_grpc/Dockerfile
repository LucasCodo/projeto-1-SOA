FROM python:3.11-alpine
WORKDIR /app

COPY app_c_rest_grpc/ .

RUN pip install --no-cache-dir grpcio-tools fastapi[standard]

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]