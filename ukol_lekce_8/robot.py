from picoed import i2c

from konstanty import Konstanty
from senzory import Senzory
from ovladac_svetel import OvladacSvetel
from modul_kola import ModulKola

class Robot:

    _zinicializovano = False

    def __init__(self, rozchod_kol, prumer_kola):
        self._levy_kolo = ModulKola(Konstanty.levy, prumer_kola)
        self._pravy_kolo = ModulKola(Konstanty.pravy, prumer_kola)
        self._senzory = Senzory()
        self._svetla = OvladacSvetel()
        self._d = rozchod_kol/2.0
    
    # 0 vse OK
    # -1 nepodarilo se zamknout i2c
    def inicializace(self):

        if i2c.try_lock():
            #inicializovace cipu motoru
            i2c.writeto(0x70, b'\x00\x01')
            i2c.writeto(0x70, b'\xE8\xAA')
            self._zinicializovano = True
            i2c.unlock()
            return 0
        else:
            return -1

    # 0 vse OK
    # -1 funkce zavolana pred inicializaci robota
    def jed(self, dopredna, uhlova):
        error1 = 0
        error2 = 0
        if not self._zinicializovano:
            return -1, -1
        #DU9
        # pouzijte self._d pro polovinu rozchodu kol
        # odkomentujte nasledujicich 5 radku
        else:
             dopredna_leveho_kola = dopredna - uhlova * self._d
             dopredna_praveho_kola = dopredna + uhlova * self._d
             print(f"dopredna leveho kola: {dopredna_leveho_kola}, dopredna praveho kola: {dopredna_praveho_kola}")
             error1 = self._levy_kolo.jed_doprednou(dopredna_leveho_kola)
             error2 = self._pravy_kolo.jed_doprednou(dopredna_praveho_kola)
             return error1, error2
  
    def zastav(self):
        error1 = self._levy_kolo.zastav()
        error2 = self._pravy_kolo.zastav() 
        return error1, error2

    # 0 0 pokud kalibrace probehla uspesne
    # jinak propagace erroru z modulu kola
    def zkalibruj_se(self, min_pwm):
        error1 = self._levy_kolo.zkalibruj_se(Konstanty.dopredu, min_pwm)
        error2 = self._pravy_kolo.zkalibruj_se(Konstanty.dozadu, min_pwm)
        return error1, error2
