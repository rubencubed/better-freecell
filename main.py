import itertools
import random


class Card:
    def __init__(self, rank, suit):
        self.rank: int = rank
        self.suit: str = suit

    def __str__(self):
        if self.rank == 1:
            return f'Ace of {self.suit}s'
        if self.rank == 11:
            return f'Jack of {self.suit}s'
        if self.rank == 12:
            return f'Queen of {self.suit}s'
        if self.rank == 13:
            return f'King of {self.suit}s'
        return f'{self.rank} of {self.suit}s'


class Stack:
    def __init__(self, type):
        self.type = type
        self.cards: list[Card] = []

    def add_card(self, new_card: Card):
        self.cards.append(new_card)


class Game:
    def __init__(self):
        self.foundations: list[Stack] = []
        self.freecells: list[Stack] = []
        self.cascades: list[Stack] = []

    def normal_deal(self):
        for x in range(4):
            self.foundations.append(Stack('foundation'))

        for x in range(4):
            self.freecells.append(Stack('freecell'))

        for x in range(8):
            self.cascades.append(Stack('cascade'))

        deck = list(itertools.product(
            range(1, 4), ['Spade', 'Heart', 'Diamond', 'Club']))
        random.shuffle(deck)

        for i, card in enumerate(deck):
            self.cascades[i % 8].add_card(Card(card[0], card[1]))
