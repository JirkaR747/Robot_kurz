from picoed import i2c, display
from konstanty import Konstanty

class Senzory:
    # tyto masky musí odpovídat skutečnému zapojení PCF8574
    # (zatím vycházím z toho, že řešíš bity 2/3/4)
    MASK_LEVY = 0x04      # bit2
    MASK_STRED = 0x08     # bit3
    MASK_PRAVY = 0x10     # bit4

    def vycti(self):
        if not i2c.try_lock():
            return -1
        try:
            buf = bytearray(1)
            i2c.readfrom_into(0x38, buf)
            return buf[0]          # int 0..255
        finally:
            i2c.unlock()

    def cara(self, value, senzor):
        if value == -1:
            return False

        if senzor == Konstanty.levy:
            mask = self.MASK_LEVY
        elif senzor == Konstanty.centralni:
            mask = self.MASK_STRED
        elif senzor == Konstanty.pravy:
            mask = self.MASK_PRAVY
        else:
            return False

        # PCF8574 bývá často "active-low" -> aktivní = 0
        return (value & mask) != 0

    def vypis(self, value):
        display.pixel(display.width-1, 0, 255 if self.cara(value, Konstanty.levy) else 0)
        display.pixel(int(display.width/2), 0, 255 if self.cara(value, Konstanty.centralni) else 0)
        display.pixel(0, 0, 255 if self.cara(value, Konstanty.pravy) else 0)
