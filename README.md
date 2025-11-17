# projeto-1-SOA
Primeiro projeto para disciplina de Arquitetura Orientada a Serviços

uvicorn main:app --reload

python main.py

go run ./main.go

python -m grpc_tools.protoc -I=proto --python_out=. --grpc_python_out=. proto/sticker.proto
protoc -I proto --go_out=. --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=paths=source_relative proto/sticker.proto
