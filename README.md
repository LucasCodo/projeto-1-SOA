# Projeto 1 – Comunicação entre Microserviços

**Disciplina:** Arquitetura Orientada a Serviços (SOA)

Este projeto tem como objetivo implementar **comunicação síncrona e assíncrona entre microserviços**, utilizando múltiplas tecnologias, protocolos e linguagens de programação.

A aplicação simula um **álbum de figurinhas distribuído**, em que cada figurinha é fornecida por diferentes microserviços. O microserviço **MAIN** disponibiliza uma API única responsável por agregar as figurinhas consultando outros serviços — alguns via comunicação **síncrona** (gRPC/HTTP) e outros via **mensageria** (RabbitMQ/Kafka).

---

## 📌 Arquitetura Geral

A arquitetura é dividida em dois blocos principais:

### 🔵 Comunicação Síncrona (gRPC/HTTP)

Microserviços:

* **A** — implementado em *Python*
* **B** — implementado em *Go*
* **C** — implementado em *Python*
* **MAIN** — microserviço agregador

Fluxo:

1. MAIN requisita ao microserviço **C** três figurinhas.
2. O serviço **C**, de forma síncrona, consome os serviços **A** e **B**.
3. Os serviços **A** e **B** retornam figurinhas individuais.

📌 Requisito importante:
**A e B devem ser implementados em duas linguagens de programação diferentes.**

---

### 🟣 Comunicação Assíncrona (RabbitMQ/Kafka)

Além da comunicação síncrona, o sistema possui microserviços que enviam figurinhas para filas de mensageria.

* MAIN consome mensagens dessas filas para obter novas figurinhas.
* Pelo menos **três microserviços adicionais** devem publicar nessas filas.

---

## 🗂️ Estrutura dos Microserviços

| Diretório / Serviço | Protocolo             | Linguagem |
| ------------------- |-----------------------| --------- |
| `app_a_grpc`        | gRPC                  | Python    |
| `app_b_grpc`        | gRPC                  | Go        |
| `app_c_ret_grpc`    | gRPC + REST           | Python    |
| `app_a_event`       | Eventos (RabbitMQ)    | Python    |
| `appmain`           | API REST + Eventos    | Python    |

---

## ▶️ Como Executar Cada Microserviço

Abra um terminal dentro do diretório do microserviço e execute:

### 🔵 Serviços gRPC

#### `app_c_ret_grpc`

```bash
uvicorn main:app --reload
```

#### `app_a_grpc`

```bash
python main.py
```

#### `app_b_grpc`

```bash
go run ./main.go
```

---

### 🟣 Serviços Assíncronos (RabbitMQ)

#### `app_a_event`

```bash
python main.py
```

---

### 🟢 Serviço Principal (appmain)

```bash
uvicorn main:app --reload --port 8001
```

---

## 🐇 Subindo o Broker RabbitMQ

Antes de rodar os microserviços assíncronos, você deve subir um broker RabbitMQ com as seguintes variáveis de ambiente:

```env
RABBITMQ_DEFAULT_USER=user
RABBITMQ_DEFAULT_PASS=password
```

---

## 🛠️ Gerar Código gRPC

### Python

```bash
python -m grpc_tools.protoc -I=proto --python_out=. --grpc_python_out=. proto/sticker.proto
```

### Go

```bash
protoc -I proto \
  --go_out=. --go_opt=paths=source_relative \
  --go-grpc_out=. --go-grpc_opt=paths=source_relative \
  proto/sticker.proto
```

---

## 🚀 Executar Todo o Projeto em Produção

```bash
docker compose up
```