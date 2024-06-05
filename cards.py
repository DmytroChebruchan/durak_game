from constants import CARD_SUITS, CARD_VALUES, CARD_SCORES
import random


class Card:

    def __init__(self, suit, value, score):
        self.suit = suit
        self.value = value
        self.score = score
        self.is_trump = False

    def __repr__(self):
        if self.is_trump:
            is_trump_str = " -!!! is TRUMP !!! -"
        else:
            is_trump_str = ""
        return f"{self.value} of {self.suit}" + is_trump_str


class Deck:
    trump_suit: str
    drop_out: list
    cards: list

    def __init__(self):
        self.drop_out = []
        self.trump_suit = ""
        self.cards = []
        for suit in CARD_SUITS:
            for value in CARD_VALUES:
                self.cards.append(Card(suit, value, CARD_SCORES[value]))
        random.shuffle(self.cards)

    def set_trump_suit(self):
        trump_card = self.cards[0]
        self.trump_suit = trump_card.suit

        for card in self.cards:
            if card.suit == self.trump_suit:
                card.score *= 100
                card.is_trump = True

        print(f"Trump card is {trump_card}.")

    def drop_card(self, card):
        self.drop_out.append(card)

    def initial_deal(self, players):
        for player in players:
            player.hand = []
            for _ in range(6):
                card = self.cards.pop()
                player.add_card(card)
            player.sort_hand()

    def deal_card_to_player(self, player):
        player.add_card(self.cards.pop())

    def print_trump_suit(self):
        print(f"Trump suit is {self.trump_suit}.")

    def __str__(self):
        return str(self.cards)

    def __len__(self):
        return len(self.cards)


class PairsOnTable:
    def __init__(self):
        self.pairs = []
        self.values_on_table = []
        self.cards_on_table = []

    def add_attack(self, card):
        pair = CardsPairs(card)

        self.pairs.append(pair)

        # append values to be added to table
        self.update_values_on_table(card.value)
        return pair

    def add_defend(self, card, pair):
        pair.add_defender_card(card)

        # append values to be added to table
        self.update_values_on_table(card.value)

    def update_values_on_table(self, card_value):
        self.values_on_table.append(card_value)
        self.values_on_table = list(set(self.values_on_table))

    def get_cards_on_table(self):
        piles = [pile for pile in self.pairs]
        pairs = [[pile.attacker_card, pile.defender_card] for pile in piles]
        return [card for pair in pairs for card in pair if card is not None]

    def __str__(self):
        return str(self.pairs)


class CardsPairs:
    attacker_card = None
    defender_card = None

    def __init__(self, card=None):
        if card:
            self.add_attacker_card(card)

    def add_attacker_card(self, card):
        self.attacker_card = card

    def add_defender_card(self, card):
        self.defender_card = card

    def __get__cards__(self):
        return [self.attacker_card, self.defender_card]

    def __str__(self):
        return str(self.__get__cards__())
