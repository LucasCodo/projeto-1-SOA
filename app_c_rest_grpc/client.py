import grpc
import sticker_pb2, sticker_pb2_grpc

def get_sticker(host:str = 'localhost' ,port: int = 50051):
    with grpc.insecure_channel(f'{host}:{port}') as channel:
        stub = sticker_pb2_grpc.StickerServiceStub(channel)
        try:
            result = stub.GetSticker(sticker_pb2.StickerRequest())
            return result.name
        except grpc.RpcError as e:
            print(f'{e}')

if __name__ == '__main__':
    #get_sticker(50052)
    get_sticker(port=50053)