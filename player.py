from additional_functions import (
    print_divider,
    check_card_as_defender,
)
from cards import Card, PairsOnTable
from hand import Hand


class BasePlayer:
    def __init__(self, name, player_type):
        self.name = name
        self.type = player_type
        self.hand = Hand()
        self.take_cards = False
        self.turn_to_move = False
        self.trump_suit = ""
        self.highest_card = None

    def __str__(self):
        return self.name

    def attack(self, pairs_on_table: PairsOnTable):
        print(f"{self.name} attacks.")

        attacking_card = self.hand.card_chooser()
        print_divider()

        self.hand.cards.remove(attacking_card)
        pairs_on_table.add_attack(card=attacking_card)

        self.hand.sort_hand()

        print(f"{self.name} is attacking with \n{attacking_card}.")
        print_divider()

    def react_to_attack(self, pile: PairsOnTable):
        print(f"{self.name} reacts to attack.")
        self.hand.print_hand_cards()

        if not self.check_if_can_defend(pile):
            print(f"{self.name} cannot defend and takes.")
            self.take_cards = True
            return False

        while True:
            user_input = self.request_player_for_input(
                'Would you like to defend(num_of_card) or take("take")?'
            )

            if user_input.lower() == "take":
                self.set_take_cards()
                return

            print("You chose to defend.")
            defending_card = self.hand.cards[int(user_input) - 1]

            if check_card_as_defender(pile, defending_card, self.trump_suit):
                break

            print(f"{self.name} cannot defend with {defending_card}.")
            print(f"Attacking card is {pile.pairs[-1].attacker_card}.")

        self.hand.drop_card_from_hand(defending_card)
        pile.pairs[-1].add_defender_card(defending_card)
        self.take_cards = False

        print(f"{self.name} is defending with card: \n", defending_card)
        print_divider()

    def check_if_can_defend(self, pile):
        attacking_card = pile.pairs[-1].attacker_card
        attacking_suit = attacking_card.suit

        if attacking_suit == self.trump_suit:
            return self.highest_card.score > attacking_card.score

        hand_of_trump_suit = self.hand.get_hand_of_trump_suit()
        if len(hand_of_trump_suit):
            return True

        hand_of_attacking_suit = self.hand.get_hand_of_suit(attacking_suit)
        if len(hand_of_attacking_suit):
            highest_card = max(hand_of_attacking_suit, key=lambda c: c.value)
            return highest_card.value > attacking_card.value

        return False

    def check_if_can_add_attacking_card(self, pile: PairsOnTable):
        values_in_hand = set([card.value for card in self.hand.cards])
        values_on_table = set(pile.values_on_table)
        return bool(values_in_hand & values_on_table)

    @staticmethod
    def request_player_for_input(text):
        reply = input(text)
        return reply

    def set_take_cards(self):
        print("You took the cards.")
        self.take_cards = True

    # TODO: refactor name and usage based on context, make easier to understand
    def card_chooser(self, attacking_card_index=None) -> Card:
        self.hand.print_hand_cards()

        if not attacking_card_index:
            attacking_card_index = int(
                self.request_player_for_input(f"{self.name} pick a card: ")
            )
        attacking_card = self.hand.cards[attacking_card_index - 1]
        return attacking_card

    def if_adds_attacking_cards(self):
        print(f"{self.name} to make a move.")
        print("Your hand: ")
        self.hand.print_hand_cards()
        input_add = self.request_player_for_input(
            "Would you like to add cards (1)?"
        )
        return input_add == "1"

    def get_lowest_trump_score_in_hand(self) -> int:
        hand_of_trump_suit = [
            card for card in self.hand.cards if card.suit == self.trump_suit
        ]
        if len(hand_of_trump_suit):
            return min(hand_of_trump_suit, key=lambda c: c.value).score
        return 0


class User(BasePlayer):
    pass


class Computer(BasePlayer):
    def request_player_for_input(self, text):
        pass

    def react_to_attack(self, pile: PairsOnTable):
        pass

    def if_adds_attacking_cards(self):
        return False

