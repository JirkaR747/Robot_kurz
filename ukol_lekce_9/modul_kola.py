from time import sleep, monotonic_ns
from motor import Motor
from enkoder import Enkoder
from konstanty import Konstanty
from casovac import Casovac

class ModulKola:

    zkalibrovano = False

    def __init__(self, strana, prumer_kola):
        self.__polomer_kola = prumer_kola/2.0

        if strana == Konstanty.levy or strana == Konstanty.pravy:
            self.__motor = Motor(strana)
            self.__enkoder = Enkoder(strana)
        else:
            raise AttributeError("ModulKola: Spatny argument strana")
    
    # upozorneni, tato funkce je blokujici
    # 0 vse ok
    # -1 chyba ve sberu dat

    def zkalibruj_se(self, smer, min_pwm):
        print("Kalibruji modul kola pro smer, modul kola " + str(smer))
        data = self.__zmer_data(smer, min_pwm)
        if len(data) == 0: #nastala chyba
            return -1
        self.__aproximuj_primkou(data)
        return 0

    def __zmer_data(self, smer, min_pwm):

        data = []
        error_min = 0
        error_max = 0

        for pwm in range(min_pwm, self.__motor.max_rychlost):
            #spusti motor s danou pwm
            error_min, uhlova = self.__nastav_rychlost(smer, pwm)
            print(str(pwm) + "\t" + str(uhlova))
            if error_min != 0:
                break #nastala chyba v jed_pwm, nema smysl pokracovat

            if uhlova > 0:
                data.append([pwm, uhlova])                
                break # nasli jsme min_pwm, ukoncime for loop
                #bez tohoto break by to taky fungovalo, ale bylo by to zbytecne pomale, protoze bychom sbirali vsechna data
        
        #skocime na konec rozsahu, abychom zrychlili kalibraci
        pwm = self.__motor.max_rychlost
        error_max, uhlova = self.__nastav_rychlost(smer, pwm)
        if error_max == 0:
            data.append([pwm, uhlova]) 

        self.__motor.zastav()

        if error_min == 0 and error_max ==0: #obe data jsou ok
            return data
        else:
            return []

    #vraci dve hodnoty: error, uhlova_rychlost
    #errory:
    #0 vse ok
    #- error v jed_pwm

    def __nastav_rychlost(self, smer, pwm):
        perioda_mereni = 1.1 #v sekundach - chceme vetsi nez perioda vypoctu rychlosti
        jed_error = self.__motor.jed_pwm(smer, pwm)
        if jed_error != 0:
            return jed_error, 0

        cas_posledniho_mereni = monotonic_ns()
        cas_ted = monotonic_ns()

        #nech motor pusteny po danou periodu a zajisti, ze enkoder vycita tiky
        while not Casovac.ubehl_cas(cas_ted, cas_posledniho_mereni, perioda_mereni):
            cas_ted = monotonic_ns()
            self.__enkoder.updatuj_se()
            sleep(0.005)

        uhlova = self.__enkoder.rychlost_rad_s
        return 0, uhlova
    
    def __aproximuj_primkou(self, data):

        prvni_data = data[0]
        last_data = data[1]
        
        self.__min_pwm_rozjezd = prvni_data[0]
        self.__min_uhlova_rozjezd = prvni_data[1]
        pwm2 = last_data[0]
        pwm1 = self.__min_pwm_rozjezd

        uhlova2 = last_data[1]
        uhlova1 = self.__min_uhlova_rozjezd

        rozdil_pwm = pwm2-pwm1
        rozdil_uhlova = uhlova2 - uhlova1

        self.__a_rozjezd = rozdil_pwm/ rozdil_uhlova
        self.__b_rozjezd = pwm2 - self.__a_rozjezd*uhlova2

        
    def zastav(self):
        error = self.__motor.zastav()
        return error

    #0 vse ok
    # -2 spatna rychlost
    # -3 meni se smer
    # -4 chyba i2c

    def jed_doprednou(self, dopredna):
        if dopredna > 0:
            smer = Konstanty.dopredu
        elif dopredna < 0:
            smer = Konstanty.dozadu
        else:
            smer = None

        if smer == None: 
            self.__motor.zastav()
        else:
            uhlova = self.__dopredna_na_uhlovou(dopredna)
            pwm = self.__uhlova_na_pwm(uhlova)
            print(f"dopredna: {dopredna}, uhlova: {uhlova}, pwm: {pwm}")
            error = self.__motor.jed_pwm(smer, pwm)
            return error

    def __dopredna_na_uhlovou(self, dopredna):
        return dopredna/self.__polomer_kola
    
    def __uhlova_na_pwm(self, uhlova):
        if uhlova < self.__min_uhlova_rozjezd:
            return 0
        else:
            uhlova = self.__a_rozjezd * uhlova + self.__b_rozjezd
            return uhlova
