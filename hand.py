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

    def set_highers_card(self):
        if self.cards:
            self.highest_card = self.cards[0]
        else:
            self.highest_card = None

    def sort_hand(self):
        self.cards.sort(key=lambda c: c.score, reverse=True)

        suits = CARD_SUITS.copy()
        suits.pop(suits.index(self.trump_suit))
        suits.insert(0, self.trump_suit)

        suit_sorted_hand = []
        for suit in suits:
            for card in self.cards:
                if card.suit == suit:
                    suit_sorted_hand.append(card)
        self.cards = suit_sorted_hand

        self.set_highers_card()

    def print_hand_cards(self):
        print(self)

    def __str__(self):
        hand_str = ""
        for i, card in enumerate(self.cards):
            hand_str += f"{i + 1}. {card}\n"
        return self.cards
