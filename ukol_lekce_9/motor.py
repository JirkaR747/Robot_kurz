from picoed import i2c 

from konstanty import Konstanty

class Motor:

    posledni_smer = None
    max_rychlost = 150

    def __init__(self, strana):
        if strana == Konstanty.levy:
            self.kanal_A = b"\x05"
            self.kanal_B = b"\x04"
        elif strana == Konstanty.pravy:
            self.kanal_A = b"\x03"
            self.kanal_B = b"\x02"
        else:
            raise AttributeError("Spatny argument strana")
        
        self.strana = strana
  
    # 0 vse ok
    # -1 spatny smer
    # -2 spatna rychlost
    # -3 meni se smer
    # -4 chyba i2c
    def jed_pwm(self, smer, rychlost):

        if self.posledni_smer == None:
            self.posledni_smer = smer

        rychlost = int(rychlost)
        if rychlost < 0 or rychlost > self.max_rychlost:
            return -2
    
        kanal_on = ""
        kanal_off = ""

        if smer == Konstanty.dopredu:
            kanal_on = self.kanal_A
            kanal_off = self.kanal_B
        elif smer == Konstanty.dozadu:
            kanal_on = self.kanal_B
            kanal_off = self.kanal_A
        else:
            return -1
    
        if smer != self.posledni_smer:
            return -3
        else:
            if i2c.try_lock():    
                i2c.writeto(0x70, kanal_off + bytes([0]))
                i2c.writeto(0x70, kanal_on + bytes([rychlost]))
                i2c.unlock()
                return 0
            else:
                return -4
    

    # 0 vse OK
    # -1 nepodarilo se zamknout i2c
    def zastav(self):
        if i2c.try_lock():
            i2c.writeto(0x70, self.kanal_A + bytes([0]))
            i2c.writeto(0x70, self.kanal_B + bytes([0]))
            self.posledni_smer = None
            i2c.unlock()
            return 0
        else:
            print("Nepodarilo se zamknout i2c") 
            return -1

