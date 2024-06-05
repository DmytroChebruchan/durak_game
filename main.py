from game import Game


def main():
    game = Game()

    game.set_attacker_for_1st_round()
    game.start_round()

    while game.status == "in progress":
        game.start_round()


if "__main__" == __name__:
    main()
