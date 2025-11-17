FROM golang:1.25-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY app_b_grpc/ ./app_b_grpc
COPY proto/ ./proto
RUN go build -o app ./app_b_grpc

FROM alpine:latest

WORKDIR /app
COPY --from=builder /app .

EXPOSE 50052
CMD ["./app"]
