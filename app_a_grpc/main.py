import grpc
from concurrent import futures
import sticker_pb2, sticker_pb2_grpc
from deck import card_generator

get_card = card_generator()
class StickerService(sticker_pb2_grpc.StickerServiceServicer):
    def GetSticker(self, request, context):
        # {'url': 'https://deckofcardsapi.com/static/img/AS.png'}
        return sticker_pb2.StickerResponse(
            url=f'https://deckofcardsapi.com/static/img/{next(get_card)}.png')


def serve():
    port = 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    sticker_pb2_grpc.add_StickerServiceServicer_to_server(StickerService(), server)
    server.add_insecure_port(f'[::]:{port}')
    print(f"Running on port {port}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

