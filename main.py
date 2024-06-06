from game import Game
from additional_functions import initial_greetings


def main():
    game = Game()
    initial_greetings()
    while game.status == "in progress":
        game.start_round()


if "__main__" == __name__:
    main()
