from deck import card_generator
from fastapi import FastAPI
from client import get_sticker
import os

host_a = os.getenv("GRPC_SERVER_HOST_A", "localhost")
host_b = os.getenv("GRPC_SERVER_HOST_B", "localhost")

app = FastAPI()

get_card = card_generator()

@app.get("/cards")
def get_cards():
    """Endpoint que retorna uma lista de URLs de cartas."""

    return {"cards": [
        f'{next(get_card)}',
        get_sticker(host=host_a),
        get_sticker(host=host_b,port=50052)
    ]}