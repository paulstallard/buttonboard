import buttonboard
from say import say
import time
import random


def random_different(last_value, n_buttons):
    # returns a random number between 0 and n_buttons-1, avoiding last_value
    return (last_value + 1 + random.randint(0, n_buttons - 2)) % n_buttons


def whackamole(board):
    say("Hit the first mole to start")
    button = 3
    board.whack(button)
    start_time = time.perf_counter()
    for _ in range(20):
        button = random_different(button, 7)
        board.whack(button)
    elapsed_time = time.perf_counter() - start_time
    board.flash()
    return elapsed_time


def main():
    highscore = -1.00

    board = buttonboard.ButtonBoard()

    while True:
        elapsed_time = whackamole(board)

        say(f"{elapsed_time:.2f} seconds,,,")

        diff_to_hs = round(elapsed_time - highscore, 2)

        if highscore == -1.0:
            say("you have set the first highscore")
            highscore = elapsed_time
        elif diff_to_hs > 0:
            say(f"Bad luck, you missed the highscore by {diff_to_hs:.2f} seconds")
        elif diff_to_hs < 0:
            say(f"Well done, you beat the highscore by {-diff_to_hs:.2f} seconds")
            highscore = elapsed_time
        else:
            say("you have equaled the highscore")


if __name__ == "__main__":
    main()
