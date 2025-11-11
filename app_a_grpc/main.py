import grpc
import sticker_pb2, sticker_pb2_grpc

def get_sticker():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = sticker_pb2_grpc.StickerServiceStub(channel)
        try:
            result = stub.GetSticker(sticker_pb2.StickerRequest())
            print(f'{result}')
        except grpc.RpcError as e:
            print(f'{e}')

if __name__ == '__main__':
    get_sticker()

