from deck import card_generator
from fastapi import FastAPI
from client import get_sticker


app = FastAPI()

get_card = card_generator()

@app.get("/cards")
def get_cards():
    """Endpoint que retorna uma lista de URLs de cartas."""

    return {"cards": [
        f'{next(get_card)}',
        get_sticker(),
        get_sticker(50052)
    ]}