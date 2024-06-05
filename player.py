from additional_functions import print_divider  # Assuming these imports are necessary
from cards import Card, PairsOnTable
from constants import CARD_SUITS


class BasePlayer:
    def __init__(self, name, player_type):
        self.name = name
        self.type = player_type
        self.hand = []
        self.take_cards = False
        self.turn_to_move = False
        self.trump_suit = ""
        self.highest_card = None

    def __str__(self):
        return self.name

    def card_chooser(self):
        return self.hand[0]

    def add_card(self, card):
        self.hand.append(card)

    def drop_card(self, card):
        self.hand.remove(card)

    def sort_hand(self):
        self.hand.sort(key=lambda c: c.score, reverse=True)

        suits = CARD_SUITS.copy()
        suits.pop(suits.index(self.trump_suit))
        suits.insert(0, self.trump_suit)

        suit_sorted_hand = []
        for suit in suits:
            for card in self.hand:
                if card.suit == suit:
                    suit_sorted_hand.append(card)
        if suit_sorted_hand:
            self.highest_card = suit_sorted_hand[0]
        else:
            self.highest_card = None
        self.hand = suit_sorted_hand

    def get_hand(self):
        hand_str = ""
        for i, card in enumerate(self.hand):
            hand_str += f"{i + 1}. {card}\n"
        print(f"{self.name}'s hand: \n{hand_str}")
        return self.hand

    def attack(self, pairs_on_table: PairsOnTable):
        print(f"{self.name} attacks.")
        attacking_card = self.card_chooser()
        print_divider()
        self.hand.remove(attacking_card)
        pairs_on_table.add_attack(card=attacking_card)
        self.sort_hand()
        print(f"{self.name} is attacking with \n{attacking_card}.")

    def defend(self, pile: PairsOnTable):
        print(f"{self.name} defends.")
        self.get_hand()
        if not self.can_defend(pile):
            print(f"{self.name} cannot defend and takes.")
            self.take_cards = True
            return
        return True

    def can_defend(self, pile):
        attacking_card = pile.pairs[-1].attacker_card
        attacking_suit = attacking_card.suit

        if attacking_suit == self.trump_suit:
            return self.highest_card.score > attacking_card.score

        hand_of_trump_suit = [card for card in self.hand if card.suit == self.trump_suit]
        if len(hand_of_trump_suit):
            return True

        hand_of_attacking_suit = [card for card in self.hand if
                                  card.suit == attacking_suit]
        if len(hand_of_attacking_suit):
            highest_card = max(hand_of_attacking_suit, key=lambda c: c.value)
            return highest_card.value > attacking_card.value


        return self.highest_card.value > attacking_card.value

    def if_can_add_attacking_card(self, pile: PairsOnTable):
        values_in_hand = set([card.value for card in self.hand])
        values_on_table = set(pile.values_on_table)
        return bool(values_in_hand & values_on_table)


class User(BasePlayer):
    def card_chooser(self, attacking_card=None) -> Card:
        self.get_hand()
        if attacking_card:
            attacking_card_index = attacking_card
        else:
            attacking_card_index = int(input(f"{self.name} pick a card: "))
        attacking_card = self.hand[attacking_card_index - 1]
        return attacking_card

    def if_adds_attacking_cards(self):
        print(f"{self.name} to make a move.")
        print("Your hand: ")
        self.get_hand()
        input_add = input("Would you like to add cards (1)?")
        return input_add == "1"

    def defend(self, pile: PairsOnTable):
        if super().defend(pile) is None:
            return

        while True:
            defend_or_take = input("Would you like to defend(1) or take("
                                   "take)? ")

            if defend_or_take == "take":
                print('You took the cards.')
                self.take_cards = True
                return

            print('You chose to defend.')
            defending_card = self.card_chooser(defend_or_take)
            if check_card_as_defender(pile, defending_card, self.trump_suit):
                break
            else:
                print(f"{self.name} cannot defend with {defending_card}.")
                print(f'Attacking card is {pile.pairs[-1].attacker_card}.')

        self.drop_card(defending_card)
        pile.pairs[-1].add_defender_card(defending_card)
        print(f"{self.name} is defending with card: \n", defending_card)
        self.take_cards = False

    def get_lowest_trump_score_in_hand(self) -> int:
        hand_of_trump_suit = [card for card in self.hand if card.suit == self.trump_suit]
        if len(hand_of_trump_suit):
            return min(hand_of_trump_suit, key=lambda c: c.value).score
        return 0


def check_card_as_defender(pile: PairsOnTable, defending_card: Card, trump_suit):
    pair = pile.pairs[-1]
    attacker_card = pair.attacker_card
    if attacker_card.suit == trump_suit:
        return attacker_card.score < defending_card.score
    if attacker_card.suit == defending_card.suit:
        return attacker_card.score < defending_card.score
    else:
        return defending_card.suit == trump_suit
