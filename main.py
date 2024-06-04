from game import Game


def main():
    game = Game()
    game.start_round()
    game.set_attacker_for_1st_round()

    while game.status == "in_progress":
        game.start_round()


if "__main__" == __name__:
    main()
