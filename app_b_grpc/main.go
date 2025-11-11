package main

import (
	"context"
	"log"
	"net"

	"google.golang.org/grpc"

	// ajuste o caminho abaixo para o seu go_package real
	stickerpb "github.com/LucasCodo/projeto-1-SOA/proto"
)

// Implementação do serviço
type stickerServer struct {
	stickerpb.UnimplementedStickerServiceServer
}

func (s *stickerServer) GetSticker(ctx context.Context, req *stickerpb.StickerRequest) (*stickerpb.StickerResponse, error) {
	// regra de exemplo: monta uma URL a partir do ID
	id := req.GetId()
	// url := "https://cdn.exemplo.com/stickers/" + id + ".png"
	url := "https://deckofcardsapi.com/static/img/AS.png"
	return &stickerpb.StickerResponse{Url: url}, nil
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("falha ao abrir porta: %v", err)
	}

	grpcServer := grpc.NewServer()
	stickerpb.RegisterStickerServiceServer(grpcServer, &stickerServer{})

	log.Println("gRPC server ouvindo em :50051")
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("falha ao servir: %v", err)
	}
}
