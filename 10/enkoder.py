from digitalio import DigitalInOut
from board import P14, P15
from math import pi
from time import monotonic_ns

from konstanty import Konstanty
from casovac import Casovac

class Enkoder:

    posledni_hodnota = None
    soucet_tiku = 0
    __cas_posledniho_vypoctu = None
    rychlost_rad_s = 0
    rychlost_otacky_s = 0
    

    def __init__(self, strana, tiky_na_otocku = 40, perioda_rychlosti = 1):
        if strana == Konstanty.levy:            
            self.pin = DigitalInOut(P14)
        elif strana == Konstanty.pravy:
            self.pin = DigitalInOut(P15)
        else:
            raise AttributeError("Spatny argument strana")
        
        self.__tiky_na_otocku = tiky_na_otocku
        self.__perioda_rychlosti = perioda_rychlosti
        self.posledni_hodnota = self.pin.value
    
    def updatuj_se(self):
        
        cas_ted = monotonic_ns()
        if self.__cas_posledniho_vypoctu == None:
            self.__cas_posledniho_vypoctu = cas_ted

        aktualni_hodnota = self.pin.value

        if self.posledni_hodnota != aktualni_hodnota:
            # hura mame tik
            self.soucet_tiku = self.soucet_tiku + 1
            self.posledni_hodnota = aktualni_hodnota
        
        if Casovac.ubehl_cas(self.__cas_posledniho_vypoctu, cas_ted, self.__perioda_rychlosti):
            self.__vypocti_rychlost(cas_ted)
            
            #zresetuj se
            self.soucet_tiku = 0
            self.__cas_posledniho_vypoctu = cas_ted
    
    def __vypocti_rychlost(self, cas_ted):
        aktualni_pocet_otacek = self.soucet_tiku/self.__tiky_na_otocku
        aktualni_uhel = aktualni_pocet_otacek * 2 * pi

        rozdil_casu = Casovac.rozdil_tiku(self.__cas_posledniho_vypoctu, cas_ted)
        self.rychlost_rad_s = aktualni_uhel/rozdil_casu
        self.rychlost_otacky_s = aktualni_pocet_otacek/rozdil_casu