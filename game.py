from additional_functions import print_decider
from cards import Deck, PairsOnTable
from player import User


class Game:
    piles_on_table: PairsOnTable
    attacker, defender = None, None

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

        print_decider()

        print("Round started.")
        self.set_attacker_for_1st_round()

        self.attacker, self.defender = (
            (self.players[0], self.players[1])
            if self.players[0].turn_to_move
            else (self.players[0], self.players[1])
        )
        print_decider()
        print(f"Attacker: {self.attacker.name}")
        print(f"Defender: {self.defender.name}")
        print_decider()

        while True:
            self.piles_on_table = PairsOnTable()

            self.attacker.attack(self.piles_on_table)
            print_decider()

            self.defender.defend(self.piles_on_table)
            print_decider()

            if not self.attacker.if_adds_cards():
                print(f"{self.attacker.name} will not add cards.")
                break

        self.complete_round()

    def complete_round(self, drop_needed=True):
        if drop_needed:
            self.drop_cards_from_table()
            self.switch_turns_to_move()
        else:
            cards_on_table = [pile.values() for pile in self.piles_on_table.pairs]
            self.defender.hand.extend(cards_on_table)
            self.deal_balance_cards()

        self.check_if_game_finished()

    def deal_balance_cards(self):
        for player in self.players:
            while len(player.hand) < 6 and len(self.deck.cards) > 0:
                self.deck.deal_card_to_player(player)

    def check_if_game_finished(self):
        if not self.players[0].hand:
            print(f"{self.players[1].name} wins!")
            self.status = "finished"
        elif not self.players[1].hand:
            print(f"{self.players[0].name} wins!")
            self.status = "finished"

    def switch_turns_to_move(self):
        if self.players[0].turn_to_move:
            self.players[0].turn_to_move = False
            self.players[1].turn_to_move = True
        else:
            self.players[0].turn_to_move = True
            self.players[1].turn_to_move = False

    def drop_cards_from_table(self):
        cards_on_table = [pile.values() for pile in self.piles_on_table.pairs]
        for card in cards_on_table:
            self.deck.drop_card(card)
