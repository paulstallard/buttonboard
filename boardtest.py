import buttonboard
import time


def main():
    b = buttonboard.ButtonBoard()

    while True:
        buttons = b.get_buttons()
        print(buttons)
        b.board_clear()
        for number in buttons:
            b.light_on(number)
        time.sleep(1)


if __name__ == "__main__":
    main()
