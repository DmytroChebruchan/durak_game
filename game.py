from cards import Deck, PairsOnTable
from player import User


class Game:
    piles_on_table: PairsOnTable

    def __init__(self):

        self.deck = Deck()
        self.deck.set_trump_suit()

        self.p1 = User("Player 1", "human")
        self.p2 = User("Player 2", "human")
        # self.p2 = Computer("Computer", "computer")

        self.players = [self.p1, self.p2]

        for player in self.players:
            player.trump_suit = self.deck.trump_suit

        self.deck.initial_deal(self.players)

        self.status = "in progress"

        if self.is_trump_suit_in_hand():
            self.start_round()
        else:
            self.__init__()

    def is_trump_suit_in_hand(
        self,
    ):
        for player in self.players:
            suits_of_player = set(card.suit for card in player.hand)
            if self.deck.trump_suit in suits_of_player:
                print(f"Player has {self.deck.trump_suit} in hand.")
                return True
        return False

    def set_attacker_for_1st_round(self):
        player_1_highest_card = self.players[0].hand[0]
        player_2_highest_card = self.players[1].hand[0]

        if player_1_highest_card.score > player_2_highest_card.score:
            self.players[0].turn_to_move = True
        else:
            self.players[1].turn_to_move = True

        print(f"{self.players[0].name} goes first.")

    def start_round(self):
        print("Round started.")
        self.set_attacker_for_1st_round()
        
        attacker, defender = (
            (self.players[0], self.players[1])
            if self.players[0].turn_to_move
            else (self.players[0], self.players[1])
        )

        print(f"Attacker: {attacker.name}")
        print(f"Defender: {defender.name}")
        while True:
            self.piles_on_table = PairsOnTable()

            attacker.attack(self.piles_on_table)
            defender.defend(self.piles_on_table)

            if not attacker.if_adds_cards():
                print(f"{attacker.name} will not add cards.")
                break

        self.complete_round()

    def complete_round(self):
        return
