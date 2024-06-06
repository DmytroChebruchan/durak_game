from cards import PairsOnTable, Card


def print_divider():
    print("-" * 50)


def initial_greetings():
    print_divider()
    print("Welcome to the game of fool! This is the game for 2 players.")
    print_divider()
    print_divider()


def check_card_as_defender(
    pile: PairsOnTable, defending_card: Card, trump_suit
):
    pair = pile.pairs[-1]
    attacker_card = pair.attacker_card

    if attacker_card.suit == trump_suit:
        return attacker_card.score < defending_card.score
    if attacker_card.suit == defending_card.suit:
        return attacker_card.score < defending_card.score
    else:
        return defending_card.suit == trump_suit
