from neopixel import NeoPixel
from board import P0
from time import sleep
from konstanty import Konstanty

class OvladacSvetel:
    
    prave_PS = 3
    leve_PS = 0
    bila_slaba = (55,55,55)
    zadna = (0,0,0)
    stav = None
    perioda_blikani = 0.5
    cas_minule = 0

    def __init__(self):
        self.svetla = NeoPixel(P0, 8)
        self.svetla.auto_write = True

    def rozsvitPredniSvetla(self):
        self.svetla[self.prave_PS] = self.bila_slaba
        self.svetla[self.leve_PS] = self.bila_slaba
        self.stav = Konstanty.sviti

    def zhasniPredniSvetla(self):
        self.svetla[self.prave_PS] = self.zadna
        self.svetla[self.leve_PS] = self.zadna
        self.stav = Konstanty.zhasnuto

    def blikej(self):
        self.rozsvitPredniSvetla()
        sleep(0.5)
        self.zhasniPredniSvetla()
        sleep(0.5)
    
    def update(self):
        if self.stav == None:
            self.prepni_se()

        if rozdil_casu(cas_ted, cas_minule) > perioda_blikani:
            self.prepni_se()
            self.cas_minule = cas_ted

    def prepni_se(self):
        if self.stav == None:
            self.stav = Konstanty.sviti
            self.rozsvitPredniSvetla()
            self.cas_minule = monoti
            return
        
        if self.stav == Konstanty.sviti:
            self.zhasniPredniSvetla()
        elif self.stav == Konstanty.zhasnuto:
            self.rozsvitPredniSvetla()

