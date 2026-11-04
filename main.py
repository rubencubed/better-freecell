import itertools
import random
from functools import reduce
from typing import Literal

red_suits = {'Hearts', 'Diamonds'}
black_suits = {'Clubs', 'Spades'}

Color = Literal['red', 'black']
SuitName = Literal['Hearts', 'Diamonds', 'Clubs', 'Spades']

class Suit:
    def __init__(self, color: Color, name: SuitName):
        self.color = color
        self.name = name


class Card:
    def __init__(self, rank: int, suit: str, next=None, prev=None):
        self.rank = rank
        self.suit = suit
        self.next: Card | None = next
        self.prev: Card | None = prev

    def next_card_is_legit(self, game_type='normal'):
        if self.next == None:
            return True

        if game_type == 'normal':
            if self.next.rank != self.rank - 1:
                return False

            if self.suit in red_suits and self.next.suit in red_suits:
                return False

            if self.suit in black_suits and self.next.suit in black_suits:
                return False

            return True

    # move to game probably
    def can_move(self, moveable_cards: int):
        cards_below = 0
        card = self
        while card is not None:
            cards_below += 1
            if cards_below == moveable_cards:
                return False

            if not card.next_card_is_legit():
                return False

            card = card.next

        # if this point is reached, card can be moved
        return True

    def __str__(self):
        if self.rank == 1:
            return f'Ace of {self.suit}'
        if self.rank == 11:
            return f'Jack of {self.suit}'
        if self.rank == 12:
            return f'Queen of {self.suit}'
        if self.rank == 13:
            return f'King of {self.suit}'
        return f'{self.rank} of {self.suit}'


class Stack:
    def __init__(self):
        # top card of the stack is the head, bottom is tail
        self.card_tail: Card | None = None

    def can_add_card(self, card: Card) -> bool:
        return True

    def add_card(self, card):
        if not self.can_add_card(card):
            return
        
        if self.card_tail is None:
            self.card_tail = card
        else:
            card.prev = self.card_tail
            self.card_tail.next = card
            self.card_tail = card


class Freecell(Stack):
    def can_add_card(self, card: Card):
        if self.card_tail is None and card.next is None:
            return True
        return False


class Foundation(Stack):
    def can_add_card(self, card: Card):
        if card.next is None:
            if self.card_tail is None and card.rank == 1:
                return True
            if self.card_tail is not None and self.card_tail.rank == card.rank - 1 and self.card_tail.suit == card.suit:
                return True
        return False


class Cascade(Stack):
    def can_add_card(self, card: Card):
        if self.card_tail is None:
            return True
        if self.card_tail.rank - 1 == card.rank:
            if self.card_tail.suit in red_suits and card.suit in black_suits:
                return True
            if self.card_tail.suit in black_suits and card.suit in red_suits:
                return True
        return False


class Game:
    def __init__(self, number_of_suits=4, number_of_freecells=4, number_of_cascades=8):
        self.foundations = [Foundation() for _ in range(number_of_suits)]
        self.freecells = [Freecell() for _ in range(number_of_freecells)]
        self.cascades = [Cascade() for _ in range(number_of_cascades)]

    def deal(self):
        deck = list(itertools.product(
            range(1, 13), ['Spades', 'Hearts', 'Diamonds', 'Clubs']))
        random.shuffle(deck)

        for i, card in enumerate(deck):
            self.cascades[i % 8].add_card(Card(card[0], card[1]))

    def calc_moveable_cards(self):
        open_freecells = reduce(lambda open_cells, stack: open_cells +
                                (0 if stack.card_tail else 1), self.freecells, initial=0)
        open_cascades = reduce(lambda open_cells, stack: open_cells +
                               (0 if stack.card_tail else 1), self.cascades, initial=0)
        return (open_freecells + 1) * (2 ** open_cascades)

    def move_card(self, card: Card, new_stack_index: int):
        moveable_cards = self.calc_moveable_cards()
        if not card.can_move(moveable_cards):
            return

    def is_in_winning_state(self):
        return False

class GameSansFoundations(Game):
    pass

class GameSansFreecells(Game):
    pass

# import itertools
# import random
# from functools import reduce


# class Card:
#     def __init__(self, rank, suit, next=None, prev=None):
#         self.rank: int = rank
#         self.suit: str = suit
#         self.next: Card | None = next
#         self.prev: Card | None = prev

#     def next_card_is_legit(self, game_type='normal'):
#         if self.next == None:
#             return True

#         if game_type == 'normal':
#             if self.next.rank != self.rank - 1:
#                 return False

#             red = {'Hearts', 'Diamonds'}
#             black = {'Clubs', 'Spades'}

#             if self.suit in red and self.next.suit in red:
#                 return False

#             if self.suit in black and self.next.suit in black:
#                 return False

#             return True

#     def can_move(self, moveable_cards: int):
#         cards_below = 0
#         card = self
#         while card is not None:
#             cards_below += 1
#             if cards_below == moveable_cards:
#                 return False

#             if not card.next_card_is_legit():
#                 return False

#             card = card.next

#         # if this point is reached, card can be moved
#         return True

#     def __str__(self):
#         if self.rank == 1:
#             return f'Ace of {self.suit}'
#         if self.rank == 11:
#             return f'Jack of {self.suit}'
#         if self.rank == 12:
#             return f'Queen of {self.suit}'
#         if self.rank == 13:
#             return f'King of {self.suit}'
#         return f'{self.rank} of {self.suit}'


# class Stack:
#     def __init__(self, type):
#         # top card of the stack is the head, bottom is tail
#         self.card_tail: Card | None = None
#         self.type = type

#     def add_card(self, card):
#         if self.card_tail is None:
#             self.card_tail = card
#         else:
#             card.prev = self.card_tail
#             self.card_tail.next = card
#             self.card_tail = card

#     def __str__(self):
#         if self.card_tail is None:
#             return f'Stack of type {self.type} is empty'
#         output = f'Stack of type {self.type} has:'
#         card = self.card_tail
#         while card:
#             output += '\n' + card.__str__()
#             card = card.prev
#         return output


# class Game:
#     def __init__(self, game_type='normal'):
#         self.game_type = game_type
#         if game_type == 'normal':
#             self.foundations = [Stack('foundation') for _ in range(4)]
#             self.freecells = [Stack('freecell') for _ in range(4)]
#             self.cascades = [Stack('cascade') for _ in range(8)]

#             deck = list(itertools.product(
#                 range(1, 13), ['Spades', 'Hearts', 'Diamonds', 'Clubs']))
#             random.shuffle(deck)

#             for i, card in enumerate(deck):
#                 self.cascades[i % 8].add_card(Card(card[0], card[1]))

#     def calc_moveable_cards(self):
#         open_freecells = reduce(lambda open_cells, stack: open_cells +
#                                 (0 if stack.card_tail else 1), self.freecells, initial=0)
#         open_cascades = reduce(lambda open_cells, stack: open_cells +
#                                (0 if stack.card_tail else 1), self.cascades, initial=0)
#         return (open_freecells + 1) * (2 ** open_cascades)

#     def move_card(self, card: Card, new_stack_index: int):
#         moveable_cards = self.calc_moveable_cards()
#         if not card.can_move(moveable_cards):
#             return


# card = Card(1, 'Hearts')
# stack = Stack('foundation')
# stack.add_card(card)
# print(stack)