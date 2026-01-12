from picoed import i2c 
from pcf8574 import PCF8574
from period import Period
from time import sleep
from picoed import display


class Senzors:
    """Reprezentuje sadu senzorů robota připojených přes PCF8574 I/O expander."""
    ObstacleRight = 0x40
    ObstacleLeft = 0x20

    LT_Right = 0x10
    LT_Middle = 0x08
    LT_Left = 0x04
    LT_All = 0x1C

    def __init__(self, ioExpander: PCF8574) -> None:
        """Inicializace vyčítání senzorů."""
        self.__periodRead = Period(timeout_ms=50)
        self.__ioExpander = ioExpander
        self.__data = -1
        self.senzorDataUpdate()

    def senzorDataUpdate(self) -> None:
        """Přečti data ze senzorů."""
        self.__dataPrev = self.__data
        self.__data = self.__ioExpander.read() ^ Senzors.LT_All
        self.show()

    def show(self, bh: int = 9, bl: int = 1) -> None:
        """Zobrazí stav senzorů na vestavěném displeji."""
        display.pixel(16, 6, bh if self.isSenzor(Senzors.ObstacleLeft) else bl)
        display.pixel(11, 6, bh if self.isSenzor(Senzors.LT_Left) else bl)
        display.pixel( 8, 6, bh if self.isSenzor(Senzors.LT_Middle) else bl)
        display.pixel( 5, 6, bh if self.isSenzor(Senzors.LT_Right) else bl)
        display.pixel( 0, 6, bh if self.isSenzor(Senzors.ObstacleRight) else bl)

    def getDataSenzors(self, mask:int) -> int:
        return self.__data & mask

    def isSenzor(self, senzor:int) -> bool:
        """Vrátí True pokud je senzor (všechny požadované) aktivní."""
        return self.getDataSenzors(senzor) == 0

    def isAnySenzor(self, senzor:int) -> bool:
        """Vrátí True pokud je alespoň jeden ze senzorů aktivní?"""
        return self.getDataSenzors(senzor) != senzor

    def update(self) -> None:
        """Periodická aktualizace senzorů."""
        if self.__periodRead.isTime():
            self.senzorDataUpdate()


if __name__ == "__main__":
    
    io = PCF8574(i2c, address=0x38)
    senzory = Senzors(io)
    while True:
        senzory.update()
        sleep(0.01)
      