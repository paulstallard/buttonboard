import buttonboard
import random
import subprocess
import time


def say(string):
    print(string)
    subprocess.run(["espeak", "-ven-us+croak", string], stderr=subprocess.DEVNULL)


def show_sequence(board, seq):
    delay = 0.3
    for button in seq:
        board.light_on(button)
        print(f"{button}")
        time.sleep(delay)
        board.board_clear()
        time.sleep(delay)


def capture_sequence(board, seq):
    for button in seq:
        if not board.press_release(button):
            say("ooops, bad luck")
            for _ in range(5):
                board.light_on(button)
                time.sleep(0.1)
                board.board_clear()
                time.sleep(0.1)
            return False
    return True


def simon_game(board):
    say("Hit any key to start")
    board.wait_any_button()
    sequence = []
    for _ in range(10):
        sequence.append(random.randint(1, 6))
        show_sequence(board, sequence)
        if not capture_sequence(board, sequence):
            break
    score = len(sequence) - 1
    say(f"Your score was {score}")
    return score


def main():
    board = buttonboard.ButtonBoard()
    highscore = 0
    while True:
        score = simon_game(board)
        if score > highscore:
            say("Congratulations, that's a new high score")
            highscore = score
        else:
            say(f"The high score remains at {highscore}")


if __name__ == "__main__":
    main()
