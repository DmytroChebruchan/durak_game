from cards import Card, PairsOnTable
from constants import CARD_SUITS


class Player:
    def __init__(self, name, player_type):
        self.name = name
        self.hand = []
        self.type = player_type
        self.turn_to_move = False
        self.trump_suit = ""

    def add_card(self, card):
        self.hand.append(card)

    def drop_card(self, card):
        self.hand.remove(card)

    def sort_hand(self):

        self.hand.sort(key=lambda c: c.score, reverse=True)

        suits = CARD_SUITS
        suits.pop(suits.index(self.trump_suit))
        suits.insert(0, self.trump_suit)

        suit_sorted_hand = []
        for suit in suits:
            for card in self.hand:
                if card.suit == suit:
                    suit_sorted_hand.append(card)

    def get_hand(self):
        hand_str = ""
        for i, card in enumerate(self.hand):
            hand_str += f"{i + 1}. {card}\n"
        print(f"{self.name}'s hand: \n{hand_str}")
        return self.hand

    def attack(self, pairs_on_table: PairsOnTable):
        print(f'{self.name} attacks.')

        self.get_hand()

        attacking_card = self.card_chooser()

        # remove card from hand
        self.hand.remove(attacking_card)

        print(f"{self.name} is attacking with {attacking_card}.")

        pairs_on_table.add_attack(card=attacking_card)
        self.sort_hand()

    def card_chooser(self) -> Card:
        return self.hand[0]

    def defend(self, pile: PairsOnTable):
        print(f'{self.name} defends.')

        self.get_hand()
        defend_or_take = input("Would you like to defend or take? ")
        if defend_or_take == "take":
            return
        defending_card = self.card_chooser()

        pile.pairs[-1].add_defender_card(defending_card)

        self.sort_hand()

    def if_adds_cards(self):
        return False

    def __str__(self):
        return self.name


class User(Player):

    def card_chooser(self) -> Card:
        attacking_card_index = input("Pick a card to attack: ")
        attacking_card = self.hand[int(attacking_card_index) - 1]
        return attacking_card

    def if_adds_cards(self):
        input_add = input("Would you like to add cards? (y/n) ")
        if input_add == "y":
            return True
        return False

    def defend(self, pile: PairsOnTable):
        print(f'{self.name} defends.')

        self.get_hand()
        defend_or_take = input("Would you like to defend or take? ")
        if defend_or_take == "take":
            return
        defending_card = self.card_chooser()

        pile.pairs[-1].add_defender_card(defending_card)


class Computer(Player):
    def card_chooser(self) -> Card:
        return self.hand[0]

    def if_adds_cards(self):
        return False

    def defend(self, pile: PairsOnTable):
        print(f'{self.name} defends.')

        self.get_hand()
        defend_or_take = input("Would you like to defend or take? ")
        if defend_or_take == "take":
            return
        defending_card = self.card_chooser()

        pile.pairs[-1].add_defender_card(defending_card)
