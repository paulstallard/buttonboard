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

    BUT_TR = 0x40
    BUT_MR = 0x20
    BUT_BR = 0x10
    BUT_BL = 0x01
    BUT_ML = 0x02
    BUT_TL = 0x04
    BUT_M = 0x08
    BUTS = [BUT_TR, BUT_MR, BUT_BR, BUT_M, BUT_BL, BUT_ML, BUT_TL]

    LIGHT_BL = 1
    LIGHT_ML = 2
    LIGHT_TL = 4
    LIGHT_M = 8
    LIGHT_BR = 16
    LIGHT_MR = 32
    LIGHT_TR = 64
    LIGHTS = [LIGHT_TR, LIGHT_MR, LIGHT_BR, LIGHT_M, LIGHT_BL, LIGHT_ML, LIGHT_TL]

    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(self.DEVICE, self.IODIRA, 0x00)
        self.bus.write_byte_data(self.DEVICE, self.IODIRB, 0xFF)
        self.bus.write_byte_data(self.DEVICE, self.GPPUB, 0xFF)
        self.board_clear()
        atexit.register(self.board_clear)

    def board_clear(self):
        self.bus.write_byte_data(self.DEVICE, self.OLATA, 0)

    def xwhack(self, number):
        import random
        time.sleep(0.2 * random.random())

    def whack(self, number):
        self.bus.write_byte_data(self.DEVICE, self.OLATA, self.LIGHTS[number])
        a = self.bus.read_byte_data(self.DEVICE, self.GPIOB)
        while a + self.BUTS[number] != 0xFF:
            a = self.bus.read_byte_data(self.DEVICE, self.GPIOB)
        self.board_clear()

    def flash(self, delay=0.3):
        self.bus.write_byte_data(self.DEVICE, self.OLATA, 0xFF)
        time.sleep(delay)
        self.board_clear()
        time.sleep(delay)
        self.bus.write_byte_data(self.DEVICE, self.OLATA, 0xFF)
        time.sleep(delay)
        self.board_clear()

    def show_dice(self, number):
        if number == 1:
            lights = self.LIGHT_M
        elif number == 2:
            lights = self.LIGHT_TL | self.LIGHT_BR
        elif number == 3:
            lights = self.LIGHT_TL | self.LIGHT_BR | self.LIGHT_M
        elif number == 4:
            lights = self.LIGHT_BL | self.LIGHT_TL | self.LIGHT_BR | self.LIGHT_TR
        elif number == 5:
            lights = self.LIGHT_BL | self.LIGHT_TL | self.LIGHT_BR | self.LIGHT_TR | self.LIGHT_M
        else:
            lights = self.LIGHT_BL | self.LIGHT_TL | self.LIGHT_BR | self.LIGHT_TR | self.LIGHT_ML | self.LIGHT_MR
        self.bus.write_byte_data(self.DEVICE, self.OLATA, lights)

    def wait_any_button(self):
        a = self.bus.read_byte_data(self.DEVICE, self.GPIOB)
        while( a == 0xFF ) :
            a = self.bus.read_byte_data(self.DEVICE, self.GPIOB)
