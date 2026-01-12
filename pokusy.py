from picoed import i2c 
from time import sleep


# Inicializace motorů
def init_motoru():
    if i2c.try_lock():
        i2c.writeto(0x70, b'\x00\x01')
        i2c.writeto(0x70, b'\xE8\xAA')
        i2c.unlock()
        sleep(0.1)
        return 0
    else:
        print("Nepodarilo se zamknout i2c")
        return -1
    

# Třída pro ovládání jednoho motoru robota
class Motor:

    def __init__(self, strana):

        if strana == "leva":
            self.kanal_vpred = b"\x05"
            self.kanal_vzad = b"\x04"
        elif strana == "prava":
            self.kanal_vpred = b"\x03"
            self.kanal_vzad = b"\x02"
        else:
            raise ValueError("Strana musí být 'leva' nebo 'prava'")
        
        self.strana = strana
        self.aktualni_smer = None      # Aktuální směr jízdy
        self.aktualni_rychlost = 0     # Aktuální rychlost


    # Nastavení směru a rychlosti motoru
    def jed(self, smer, rychlost):
        
         # Validace směru
        if smer not in ("dopredu", "dozadu"):
            print("Chyba: smer musí být 'dopredu' nebo 'dozadu'")
            return -1

       # validace rychlosti
        if not isinstance(rychlost, int) or rychlost < 0 or rychlost > 255:
            print("Chyba: rychlost musí být int 0..255")
            return -1
      
        # Ochrana proti okamžité změně směru
        if (self.aktualni_smer is not None and self.aktualni_smer != smer and self.aktualni_rychlost > 0):                                          
            self.stop()
            sleep(0.1)  # Krátká pauza pro zastavení motoru
        # Nastavení motoru
        self._nastav_motor(smer, rychlost)

        # Aktualizace aktuálního směru a rychlosti
        self.aktualni_smer = smer
        self.aktualni_rychlost = rychlost


    # Zastavení motoru
    def stop(self):
        # Zastaví motor
        self._nastav_motor("dopredu", 0)
        self._nastav_motor("dozadu", 0)
        self.aktualni_rychlost = 0       

    # Interní metoda pro nastavení motoru   
    def _nastav_motor(self, smer, rychlost):
        
        # Výběr kanálů podle směru
        if smer == "dopredu":
            kanal_on = self.kanal_vpred
            kanal_off = self.kanal_vzad
        elif smer == "dozadu":
            kanal_on = self.kanal_vzad
            kanal_off = self.kanal_vpred
        else:
            print("Chyba: Neplatný směr motoru")
            return -1
        
        # Odeslání příkazů přes I2C
        if i2c.try_lock():
            # Nejdřív vypni opačný směr (nastaví na 0)
            i2c.writeto(0x70, kanal_off + bytes([0]))
            # Pak zapni požadovaný směr
            i2c.writeto(0x70, kanal_on + bytes([rychlost]))
            i2c.unlock()
        else:
            print("Nepodarilo se zamknout i2c")
            return -1
        

   
if __name__ == "__main__":

    inicializace = init_motoru()
    if inicializace == 0:
        levy_motor = Motor("leva")
        pravy_motor = Motor("prava")
        
        levy_motor.jed("dopredu", 127)
        pravy_motor.jed("dopredu", 127)
        sleep(1)
        levy_motor.stop()
        pravy_motor.stop()
        
        levy_motor.jed("dozadu", 127)
        pravy_motor.jed("dozadu", 127)
        sleep(1)

        levy_motor.stop()
        pravy_motor.stop()
    