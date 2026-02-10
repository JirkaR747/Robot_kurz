from picoed import button_b, i2c
from random import randint, choice
from time import sleep, monotonic_ns

from konstanty import Konstanty
from motor import Motor
from enkoder import Enkoder
from casovac import Casovac
from modul_kola import ModulKola

def zmena_smeru_motoru_1s():

    inicializuj_cip_motoru()

    levy_motor = Motor(Konstanty.levy)

    while not button_b.was_pressed():

        #vygenerujeme nahodnou hodnotu PWM
        pwm = randint(80, 180)

        #vygenerujeme nahodny smer
        smer = choice([Konstanty.dopredu, Konstanty.dozadu])

        #jed_pwm nam vraci hodnotu, kde muze byt error, proto potrebujeme s ni pracovat
        jed_error = levy_motor.jed_pwm(smer, pwm)

        #nastal error
        if jed_error != 0: 
            if jed_error == -3:
                #jiny smer
                zastav_error = levy_motor.zastav()
                if zastav_error == 0: #vse OK
                    print("cekam")
                    sleep(0.1)
                    levy_motor.jed_pwm(smer, pwm)
                else:
                    print("Chyba v zastaveni motoru" + str(zastav_error))
                    break # toto vypne while smycku -> error nema cenu pokracovat
            else:
                print("Chyba ve funkci jed_pwm motoru" + str(jed_error))
                break # toto vypne while smycku -> error nema cenu pokracovat
 
        sleep(1)
    
    zastav_error = levy_motor.zastav()
    if zastav_error != 0:
        print("Chyba v zastaveni motoru" + str(zastav_error))


def zmena_smeru_motoru_5ms():

    cas_zacatku = monotonic_ns() # pouze pro print

    perioda_zmeny_pwm = 1 # cas v sekundach
    perioda_zastaveni = 0.1
    cas_posledni_zmeny = monotonic_ns()
    levy_motor = Motor(Konstanty.levy)
    levy_enkoder = Enkoder(Konstanty.levy)
    
    cas_od_zastaveni = None

    inicializuj_cip_motoru()

    while not button_b.was_pressed():
        #print("novy beh smycky")

        levy_enkoder.updatuj_se()

        cas_ted = monotonic_ns()
        if Casovac.ubehl_cas(cas_posledni_zmeny, cas_ted, perioda_zmeny_pwm):

            # zde menime pwm a volame jed_pwm
            cas_posledni_zmeny = cas_ted

            #vygenerujeme nahodnou hodnotu PWM
            pwm = randint(80, 180)
            print(str(Casovac.rozdil_tiku(cas_ted, cas_zacatku)) + " menim\t" + str(pwm) + "\t" +str(levy_enkoder.rychlost_otacky_s))

            #vygenerujeme nahodny smer
            smer = choice([Konstanty.dopredu, Konstanty.dozadu])

            #jed_pwm nam vraci hodnotu, kde muze byt error, proto potrebujeme s ni pracovat
            jed_error = levy_motor.jed_pwm(smer, pwm)

            #nastal error
            if jed_error != 0: 
                if jed_error == -3:
                    #jiny smer
                    zastav_error = levy_motor.zastav()
                    if zastav_error == 0: #vse OK
                        cas_od_zastaveni = monotonic_ns()
                    else:
                        print("Chyba v zastaveni motoru" + str(zastav_error))
                        break # toto vypne while smycku -> error nema cenu pokracovat
                else:
                    print("Chyba ve funkci jed_pwm motoru" + str(jed_error))
                    break # toto vypne while smycku -> error nema cenu pokracovat
            
        if cas_od_zastaveni != None:
            if Casovac.ubehl_cas(cas_od_zastaveni, cas_ted, perioda_zastaveni):
                print("pockal jsem " + str(Casovac.rozdil_tiku(cas_od_zastaveni, cas_ted)))
                levy_motor.jed_pwm(smer, pwm)
                cas_od_zastaveni = None

        sleep(0.005)
    
    zastav_error = levy_motor.zastav()
    if zastav_error != 0:
        print("Chyba v zastaveni motoru" + str(zastav_error))

def inicializuj_cip_motoru():
    if i2c.try_lock():
            #inicializovace cipu motoru
            i2c.writeto(0x70, b'\x00\x01')
            i2c.writeto(0x70, b'\xE8\xAA')
            i2c.unlock()
            return 0
    else:
        print("Nepodarilo se zamknout i2c") 
        return -1

def zkouska_kalibrace():
    inicializuj_cip_motoru()

    kolo = ModulKola(Konstanty.levy, 0.067)

    kolo.zkalibruj_se()

    print(kolo.__min_pwm_rozjezd, kolo.__min_uhlova_rozjezd, kolo.__a_rozjezd, kolo.__b_rozjezd)

    uhlova_test = 7.11
    pwm_test = kolo.__a_rozjezd * uhlova_test + kolo.__b_rozjezd
    print(pwm_test) 
   