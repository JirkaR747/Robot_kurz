
from time import sleep
from pca9633 import PCA9633
from konstanty_motory import KonstantyMotory

 
    

# Třída pro ovládání jednoho motoru robota
class Motor:

    def __init__(self, strana:KonstantyMotory, driver: PCA9633) -> None:
                 

        self.driver = driver

        if strana == KonstantyMotory.levy:
            self.kanal_vpred = self.driver.PWM3
            self.kanal_vzad = self.driver.PWM2
        elif strana == KonstantyMotory.pravy:
            self.kanal_vpred = self.driver.PWM1
            self.kanal_vzad = self.driver.PWM0
        else:
            raise ValueError("Strana musí být 'leva' nebo 'prava'")
        
        self.strana = strana
        self.aktualni_smer = None      # Aktuální směr jízdy
        self.aktualni_rychlost = 0     # Aktuální rychlost


    # Nastavení směru a rychlosti motoru
    def jed(self, smer:KonstantyMotory, rychlost:int):
        
         # Validace směru
        if smer not in (KonstantyMotory.dopredu, KonstantyMotory.dozadu):
            print("Chyba: smer musí být 'dopredu' nebo 'dozadu'")
            return -1

       # validace rychlosti
        if not isinstance(rychlost, int) or rychlost < 0 or rychlost > 255:
            print("Chyba: rychlost musí být int 0..255")
            return -2
      
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
        self._nastav_motor(self.aktualni_smer, 0)
        self.aktualni_rychlost = 0       

    # Interní metoda pro nastavení motoru   
    def _nastav_motor(self, smer:KonstantyMotory, rychlost:int):
        
        # Výběr kanálů podle směru
        if smer == KonstantyMotory.dopredu:
            self.driver.set_pwm(self.kanal_vpred, self.kanal_vzad, rychlost)
           
        elif smer == KonstantyMotory.dozadu:
            self.driver.set_pwm(self.kanal_vzad, self.kanal_vpred, rychlost)   
        else:
            print("Chyba: Neplatný směr motoru")
            return -1
        
      
        

   

    