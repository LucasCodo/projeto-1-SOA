import grpc
import sticker_pb2, sticker_pb2_grpc

def get_sticker(port: int = 50051):
    with grpc.insecure_channel(f'localhost:{port}') as channel:
        stub = sticker_pb2_grpc.StickerServiceStub(channel)
        try:
            result = stub.GetSticker(sticker_pb2.StickerRequest())
            print(f'{result}')
            return result.url
        except grpc.RpcError as e:
            print(f'{e}')

if __name__ == '__main__':
    #get_sticker(50052)
    get_sticker(50053)