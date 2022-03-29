import buttonboard
import time


def main():
    b = buttonboard.ButtonBoard()

    # Validate that the _XX labels and number assignments match correctly
    for n, mask in enumerate([b._TL, b._ML, b._BL, b._M, b._TR, b._MR, b._BR]):
        b._put_lights_register(mask)
        b.press_release(n)
        b.board_clear()

    while True:
        buttons = b.get_buttons()
        print(buttons)
        b.board_clear()
        for number in buttons:
            b.light_on(number)
        time.sleep(1)


if __name__ == "__main__":
    main()
