FROM python:3.11-alpine
WORKDIR /app

COPY app_a_grpc/ .

RUN pip install --no-cache-dir grpcio-tools

EXPOSE 50051
CMD python main.py