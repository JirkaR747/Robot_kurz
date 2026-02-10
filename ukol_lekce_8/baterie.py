

from board import P2
from analogio import AnalogIn

class Baterie:
    def __init__(self):
        self.pin = AnalogIn(P2)
        self.MAGIC = 0.00014


    
    def stav(self):
        return round(self.pin.value*self.MAGIC, 1)
        