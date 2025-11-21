import itertools
import random


def card_generator():
    suits = 'CDSH'  # C=Clubs (♣), D=Diamonds (♦), S=Spades (♠), H=Hearts (♥)
    cards = 'A234567890JQK'  # A=Ás, 0=10, J=Valete, Q=Dama, K=Rei

    while True:
        # Cria e embaralha o baralho
        deck = [rank + suit for rank, suit in itertools.product(cards, suits)]
        random.shuffle(deck)

        # Entrega cada carta
        for card in deck:
            yield card
