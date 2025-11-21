FROM python:3.11-alpine
WORKDIR /app

COPY appmain/ .

RUN pip install --no-cache-dir nicegui httpx pydantic-settings fastapi[standard] faststream[rabbit]

EXPOSE 8001
CMD ["uvicorn", "main:fastapi_app", "--host", "0.0.0.0", "--port", "8001"]