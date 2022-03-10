import buttonboard
import random
import time
import sys


# Attempt to simulate a rolling dice
def roll_dice(board, number):
    sleep = .05
    for x in range(1, 8):
        board.show_dice(random.randint(1, 6))
        time.sleep(sleep*x)
    board.show_dice(number)


def main():
    board = buttonboard.ButtonBoard()

    board.show_dice(1)
    while True:
        board.wait_any_button()
        d = random.randint(1, 6)
        roll_dice(board, d)
        print(f"Rolled: {d}")


if __name__ == "__main__":
    main()
