from constants import CARD_SUITS


class Hand:

    def __init__(self):
        self.cards = []
        self.trump_suit = ""
        self.highest_card = None

    def card_chooser(self):
        return self.cards[0]

    def add_card_to_hand(self, card):
        self.cards.append(card)

    def drop_card_from_hand(self, card):
        self.cards.remove(card)

    def set_highest_card(self):
        if self.cards:
            self.highest_card = self.cards[0]
        else:
            self.highest_card = None

    def sort_hand(self):
        self.cards.sort(key=lambda card: card.score, reverse=True)

        suits = self.suits_trump_based()

        suit_sorted_hand = [card for suit in suits for card in self.cards if
                            card.suit == suit]
        self.cards = suit_sorted_hand

        self.set_highest_card()

    def suits_trump_based(self):
        suits = CARD_SUITS.copy()
        trump_suit_index = suits.index(self.trump_suit)
        suits.pop(trump_suit_index)
        suits.insert(0, self.trump_suit)
        return suits

    def print_hand_cards(self):
        print(self)

    def __str__(self):
        hand_str = ""
        for i, card in enumerate(self.cards):
            hand_str += f"{i + 1}. {card}\n"
        return self.cards
