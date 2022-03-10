import buttonboard
import random
import time
import sys


# Attempt to simulate a rolling dice
def roll_dice(board, number):
    others = list(range(1,7))
    others.remove(number)
    random.shuffle(others)
    for roll in others:
        board.show_dice(roll)
        time.sleep(0.1)
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
