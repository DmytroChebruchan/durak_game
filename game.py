from additional_functions import print_divider
from cards import Deck, PairsOnTable
from player import User
from round import Round


class Game:
    piles_on_table: PairsOnTable
    attacker, defender = None, None

    def __init__(self):
        self.status = "in progress"
        self.first_round_indicator = True
        self.deck = Deck()
        self.deck.set_trump_suit()

        self.p1 = User("Player 1", "human", trump_suit=self.deck.trump_suit)
        self.p2 = User("Player 2", "human", trump_suit=self.deck.trump_suit)
        # self.p2 = Computer("Computer", "computer")

        self.players = [self.p1, self.p2]
        for player in self.players:
            player.trump_suit = self.deck.trump_suit

        self.deck.initial_deal(self.players)

        if not self.check_if_trump_in_hands():
            self.__init__()

    def check_if_trump_in_hands(
        self,
    ):
        for player in self.players:
            suits_of_player = set(card.suit for card in player.hand.cards)
            if self.deck.trump_suit in suits_of_player:
                print(
                    f"{player.name} has the lowest card of "
                    f"{self.deck.trump_suit} in hand."
                )
                print_divider()
                return True
        return False

    def start_round(self):
        round_object = Round(
            self.players, self.deck, self.first_round_indicator
        )
        round_object.start_round()
        self.first_round_indicator = False
        if round_object.type == "final":
            self.status = "finished"
            return
