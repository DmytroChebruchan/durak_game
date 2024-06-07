from additional_functions import print_divider
from cards import PairsOnTable


class Round:
    piles_on_table: PairsOnTable
    attacker, defender = None, None

    def __init__(self, players, deck, first_round=False):
        self.players = players
        self.deck = deck
        self.type = "running"

        if first_round:
            self.set_attacker_for_1st_round()

    def set_attacker_for_1st_round(self):
        player_1_lowest_trump = self.players[0].get_lowest_trump_score_in_hand()
        player_2_lowest_trump = self.players[1].get_lowest_trump_score_in_hand()

        if player_1_lowest_trump > player_2_lowest_trump:
            self.players[0].turn_to_move = True
        else:
            self.players[1].turn_to_move = True

        print(f"{self.players[0].name} goes first.")

    def start_round(self):
        print("Round started.")
        print_divider()
        print(f"Deck length is {len(self.deck)}")
        print_divider()

        [player.hand.sort_hand() for player in self.players]
        self.deck.print_trump_suit()
        self.set_roles()

        self.piles_on_table = PairsOnTable()
        # running terns of players
        while True:
            print_divider()
            print(f"There are {len(self.piles_on_table.pairs)} pairs on table.")
            print_divider()

            self.attacker.attack(self.piles_on_table)

            self.defender.react_to_attack(self.piles_on_table)

            if len(self.piles_on_table.pairs) > 5:
                break

            if not self.will_attacker_attack():
                print(f"{self.attacker.name} will not add cards.")
                break

        drop_needed = all([not player.take_cards for player in self.players])
        self.complete_round(drop_needed)

    def will_attacker_attack(self):
        can_attacker_attack = self.attacker.check_if_can_add_attacking_card(
            self.piles_on_table
        )
        if can_attacker_attack is False:
            return False

        chosen_to_attack = self.attacker.if_adds_attacking_cards()
        return chosen_to_attack

    def set_roles(self):
        self.attacker, self.defender = (
            (self.players[0], self.players[1])
            if self.players[0].turn_to_move
            else (self.players[1], self.players[0])
        )
        self.attacker.take_cards, self.attacker.take_cards = False, False

        print_divider()
        print(
            f"Attacker: {self.attacker.name}\n"
            f"Defender: {self.defender.name}"
        )

    def complete_round(self, drop_needed=True):
        if drop_needed:
            self.drop_cards_from_table()
            self.switch_turns_to_move()
            print(f"{self.defender.name} defended all cards.")
        else:
            cards_on_table = self.piles_on_table.get_cards_on_table()
            self.defender.hand.extend_hand(cards_on_table)
            print(f"{self.defender.name} takes cards to hand.")

        self.deal_balance_cards()

        self.check_if_game_finished()
        self.defender.take_cards = False
        print("Round is ended.")
        print_divider()
        print_divider()

    def deal_balance_cards(self):
        for player in self.players:
            while len(player.hand.cards) < 6 and len(self.deck.cards) > 0:
                self.deck.deal_card_to_player(player)

    def check_if_game_finished(self):
        if not self.players[0].hand:
            print(f"{self.players[1].name} wins!")
            self.type = "final"
        elif not self.players[1].hand:
            print(f"{self.players[0].name} wins!")
            self.type = "final"

    def switch_turns_to_move(self):
        if self.players[0].turn_to_move:
            self.players[0].turn_to_move = False
            self.players[1].turn_to_move = True
        else:
            self.players[0].turn_to_move = True
            self.players[1].turn_to_move = False

    def drop_cards_from_table(self):
        self.piles_on_table.drop_cards_from_table(self.deck)
