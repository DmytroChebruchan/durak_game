from constants import CARD_SUITS, CARD_VALUES, CARD_SCORES
import random


class Card:

    def __init__(self, suit, value, score):
        self.suit = suit
        self.value = value
        self.score = score

    def __repr__(self):
        return f"{self.value} of {self.suit}"


class Deck:
    trump_suit: str
    drop_out: list
    cards: list

    def __init__(self):
        self.cards = []
        for suit in CARD_SUITS:
            for value in CARD_VALUES:
                self.cards.append(Card(suit, value, CARD_SCORES[value]))
        random.shuffle(self.cards)

    def add_card(self, card):
        self.cards.append(card)

    def set_trump_suit(self):
        trump_card = self.cards[0]
        self.trump_suit = trump_card.suit

        for card in self.cards:
            if card.suit == self.trump_suit:
                card.score *= 100

        print(f"Trump card is {trump_card}.")

    def drop_card(self, card):
        self.drop_out.append(card)

    def initial_deal(self, players):
        for player in players:
            for _ in range(6):
                player.add_card(self.cards.pop())
            player.sort_hand()

    def deal_card_to_player(self, player):
        player.add_card(self.cards.pop())

    def __str__(self):
        return str(self.cards)

    def __len__(self):
        return len(self.cards)


class PairsOnTable:
    def __init__(self):
        self.pairs = []
        self.values_on_table = []

    def add_attack(self, card):
        pair = CardsPairs(card)

        self.pairs.append(pair)

        # append values to be added to table
        self.values_on_table.append(card.value)
        return pair

    def add_defend(self, card, pair):
        pair.add_defender_card(card)

        # append values to be added to table
        self.values_on_table.append(card.value)

    def __str__(self):
        return str(self.pairs)


class CardsPairs:
    def __init__(self, card=None):
        self.pair = {}
        if card:
            self.add_attacker_card(card)

    def add_attacker_card(self, card):
        self.pair["attacker"] = card

    def add_defender_card(self, card):
        self.pair["defender"] = card

    def __str__(self):
        return str(self.pair)
