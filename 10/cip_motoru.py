from picoed import i2c
from time import sleep

class CipMotoru:

    povedla_se_inicializace = False

    def __init__(self):
        if i2c.try_lock():
            #inicializovace cipu motoru
            i2c.writeto(0x70, b'\x00\x01')
            i2c.writeto(0x70, b'\xE8\xAA')
            self.povedla_se_inicializace = True
            i2c.unlock()
        else:
            print("Nepodarilo se zamknout i2c") 

        sleep(0.1)
    
    def zresetuj_se(self):
        #....