FROM python:3.11-alpine
WORKDIR /app

COPY app_a_event/ .

RUN pip install --no-cache-dir faststream[rabbit]

CMD python main.py