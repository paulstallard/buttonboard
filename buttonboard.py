import atexit
import smbus
import time


class ButtonBoard:
    DEVICE = 0x20
    IODIRA = 0x00
    OLATA = 0x14
    GPIOA = 0x12
    GPPUA = 0x0C
    IODIRB = 0x01
    OLATB = 0x15
    GPIOB = 0x13
    GPPUB = 0x0D

    _BL = 0x01
    _ML = 0x02
    _TL = 0x04
    _BR = 0x10
    _MR = 0x20
    _TR = 0x40
    _M = 0x08
    masks = [_TR, _MR, _BR, _M, _BL, _ML, _TL]

    n_buttons = 7

    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(self.DEVICE, self.IODIRA, 0x00)
        self.bus.write_byte_data(self.DEVICE, self.IODIRB, 0xFF)
        self.bus.write_byte_data(self.DEVICE, self.GPPUB, 0xFF)
        self.board_clear()
        atexit.register(self.board_clear)

    def _get_switches_register(self):
        return self.bus.read_byte_data(self.DEVICE, self.GPIOB)

    def _get_debounced_switches_register(self):
        switches = self._get_switches_register()
        while True:
            time.sleep(0.01)
            now_switches = self._get_switches_register()
            if switches == now_switches:
                return switches
            switches = now_switches

    def _get_lights_register(self):
        return self.bus.read_byte_data(self.DEVICE, self.OLATA)

    def _put_lights_register(self, v):
        self.bus.write_byte_data(self.DEVICE, self.OLATA, v)

    def get_buttons(self):
        inp = self._get_debounced_switches_register()
        on = []
        for n, m in enumerate(self.masks):
            if not inp & m:
                on.append(n)
        return on

    def board_clear(self):
        self._put_lights_register(0)

    def xwhack(self, number):
        import random

        time.sleep(0.2 * random.random())

    def light_on(self, number):
        assert number >= 0 and number < self.n_buttons
        on = self._get_lights_register()
        self._put_lights_register(on | self.masks[number])

    def whack(self, number):
        assert number >= 0 and number < self.n_buttons
        self.light_on(number)
        buttons = self.get_buttons()
        while number not in buttons:
            buttons = self.get_buttons()
        self.board_clear()

    def flash(self, delay=0.3):
        for _ in range(2):
            self._put_lights_register(0xFF)
            time.sleep(delay)
            self.board_clear()
            time.sleep(delay)

    def show_dice(self, number):
        assert number >= 1 and number <= 6
        if number == 1:
            lights = self._M
        elif number == 2:
            lights = self._TL | self._BR
        elif number == 3:
            lights = self._TL | self._BR | self._M
        elif number == 4:
            lights = self._BL | self._TL | self._BR | self._TR
        elif number == 5:
            lights = self._BL | self._TL | self._BR | self._TR | self._M
        else:
            lights = self._BL | self._TL | self._BR | self._TR | self._ML | self._MR
        self._put_lights_register(lights)

    def wait_any_button(self):
        while True:
            if self.get_buttons():
                return

    def wait_no_buttons(self):
        while True:
            if not self.get_buttons():
                return

    def press_release(self, number):
        assert number >= 0 and number < self.n_buttons
        while True:
            buttons = self.get_buttons()
            if buttons:
                if buttons == [number]:
                    break
                print(f"Should have hit {number}, but {buttons}")
                return False
        self.light_on(number)
        self.wait_no_buttons()
        self.board_clear()
        return True
