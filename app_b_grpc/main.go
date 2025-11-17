package main

import (
	"context"
	"log"
	"math/rand"
	"net"
	"time"

	"google.golang.org/grpc"

	// ajuste o caminho abaixo para o seu go_package real
	stickerpb "github.com/LucasCodo/projeto-1-SOA/proto"
)

// Implementação do serviço
type stickerServer struct {
	stickerpb.UnimplementedStickerServiceServer
	cardGen <-chan string // canal de cartas
}

// Método gRPC
func (s *stickerServer) GetSticker(ctx context.Context, req *stickerpb.StickerRequest) (*stickerpb.StickerResponse, error) {
	// obtém a próxima carta do gerador
	card := <-s.cardGen

	return &stickerpb.StickerResponse{Name: card}, nil
}

// cardGenerator devolve um canal de strings que gera cartas infinitamente.
func cardGenerator() <-chan string {
	out := make(chan string)

	go func() {
		suits := []rune{'C', 'D', 'S', 'H'}
		cards := []rune{'A', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K'}

		for {
			// Cria o baralho
			var deck []string
			for _, rank := range cards {
				for _, suit := range suits {
					deck = append(deck, string(rank)+string(suit))
				}
			}

			// Embaralha o baralho
			rand.Shuffle(len(deck), func(i, j int) {
				deck[i], deck[j] = deck[j], deck[i]
			})

			// Envia cada carta pelo canal
			for _, card := range deck {
				out <- card
			}
		}
	}()

	return out
}

func main() {
	rand.Seed(time.Now().UnixNano())

	// inicializa o gerador de cartas
	gen := cardGenerator()

	lis, err := net.Listen("tcp", ":50052")
	if err != nil {
		log.Fatalf("falha ao abrir porta: %v", err)
	}

	server := &stickerServer{cardGen: gen}

	grpcServer := grpc.NewServer()
	stickerpb.RegisterStickerServiceServer(grpcServer, server)

	log.Println("gRPC server ouvindo em :50052")
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("falha ao servir: %v", err)
	}
}
