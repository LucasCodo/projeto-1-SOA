import itertools
import random


def card_generator():
    suits = 'CDSH'  # C=Clubs (♣), D=Diamonds (♦), S=Spades (♠), H=Hearts (♥)
    cards = 'A234567890JQK'  # A=ACE, 0=TEN, J=JACK, Q=QUEEN, K=KING

    while True:
        # Cria e embaralha o baralho
        deck = [rank + suit for rank, suit in itertools.product(cards, suits)]
        random.shuffle(deck)

        # Entrega cada carta
        for card in deck:
            yield card
