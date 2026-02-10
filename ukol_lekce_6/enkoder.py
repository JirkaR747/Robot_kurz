from digitalio import DigitalInOut

class Enkoder:

    posledni_hodnota = None
    soucet_tiku = 0

    def __init__(self, pin):
        self.pin = DigitalInOut(pin)
        self.posledni_hodnota = self.pin.value
    
    def pocet_tiku(self):
        
        aktualni_hodnota = self.pin.value

        if self.posledni_hodnota != aktualni_hodnota:
            # hura mame tik
            self.soucet_tiku = self.soucet_tiku + 1
            self.posledni_hodnota = aktualni_hodnota
        