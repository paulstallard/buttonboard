import buttonboard
import random
from say import say
import subprocess
import time


def show_sequence(board, seq):
    delay = 0.3
    for button in seq:
        board.light_on(button)
        time.sleep(delay)
        board.board_clear()
        time.sleep(delay)


def capture_sequence(board, seq):
    for button in seq:
        if not board.press_release(button):
            say("oops, bad luck")
            for _ in range(5):
                board.light_on(button)
                time.sleep(0.1)
                board.board_clear()
                time.sleep(0.1)
            return False
    return True


def simon_game(board):
    time.sleep(1)
    sequence = []
    while True:
        sequence.append(random.randint(0, 6))
        show_sequence(board, sequence)
        if not capture_sequence(board, sequence):
            break
        time.sleep(0.5)
    return len(sequence) - 1


def main():
    board = buttonboard.ButtonBoard()
    highscore = 0
    while True:
        say("Hit any key to start")
        board.wait_any_button()
        score = simon_game(board)
        say(f"Your score was {score}")
        if score > highscore:
            say("Congratulations, that's a new high score")
            highscore = score
        else:
            say(f"The high score remains at {highscore}")


if __name__ == "__main__":
    main()
