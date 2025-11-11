import grpc
from concurrent import futures
import sticker_pb2, sticker_pb2_grpc


suits = 'CDSH'
cards = 'A234567890JQK'
class StickerService(sticker_pb2_grpc.StickerServiceServicer):
    def GetSticker(self, request, context):
        return sticker_pb2.StickerResponse(url='https://deckofcardsapi.com/static/img/AS.png')

        #{'url': 'https://deckofcardsapi.com/static/img/AS.png'}

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    sticker_pb2_grpc.add_StickerServiceServicer_to_server(StickerService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()