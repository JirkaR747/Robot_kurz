from picoed import button_b, button_a
from pca9633 import PCA9633
from podvozek import Podvozek
from picoed import i2c
from time import sleep


from konstanty import Konstanty




# -1 error v inicializace robotast_start
def main():
    driver_motor = PCA9633(i2c,0x70)
    muj_povozek=Podvozek(driver_motor)
    korekce_rychlosti = 0
    leva_strana=False
    prava_strana=False
    centralni_strana=False
    MAX_KOREKCE = 30      # omezí, aby se to "neurvalo"
    KROK_KOREKCE = 5
    MAX_LOST = 8          # po tolika cyklech bez čáry zkusíme "search"

    korekce = 0
    lost_count = 0
    posledni_strana = None

    vic_zatoc=0
    

    if not driver_motor.inicializace_ok:
        print("Motoroy se nezinicializovaly spravne")
        return -1
    
    aktualni_stav = Konstanty.st_vycti_senzory

    while not button_a.was_pressed():
        data = muj_povozek.senzory.vycti()
        muj_povozek.senzory.vypis(data)
        print(f"Data ze senzoru: {data}")
        sleep(0.1)
        
   
    while not button_b.was_pressed():

        # 1) načti senzory jednou
        data = muj_povozek.senzory.vycti()
        muj_povozek.senzory.vypis(data)
        
        leva = muj_povozek.senzory.cara(data, Konstanty.levy)
        prava = muj_povozek.senzory.cara(data, Konstanty.pravy)
        stred = muj_povozek.senzory.cara(data, Konstanty.centralni)

        # 2) reakce na čáru
        if stred and not leva and not prava:
            # ideál: jedu rovně
            korekce = 0
            lost_count = 0
            posledni_strana = None
            muj_povozek.jed_dopredu(0)

        elif leva and not prava:
            # čára vlevo → doleva
            korekce = 0
            lost_count = 0
            posledni_strana = Konstanty.levy
            muj_povozek.zatoc_doleva(0)

        elif prava and not leva:
            # čára vpravo → doprava
            korekce = 0
            lost_count = 0
            posledni_strana = Konstanty.pravy
            muj_povozek.zatoc_doprava(0)

        elif leva and stred and prava:
            # křižovatka / široká čára → drž rovně
            korekce = 0
            lost_count = 0
            muj_povozek.jed_dopredu(0)

        else:
            # 3) NIC nevidím → LOST LINE
            lost_count += 1
            

            if lost_count > MAX_LOST:
                print(f"Ztraceno! Zkouším hledat čáru{lost_count}, poslední strana: {posledni_strana}, korekce: {korekce}")
                korekce = min(korekce + KROK_KOREKCE, MAX_KOREKCE)
                if posledni_strana == Konstanty.levy:
                    print(f"Krátká ztráta, zatáčím doleva: {korekce}")
                    muj_povozek.zatoc_doleva(korekce)
                elif posledni_strana == Konstanty.pravy:
                    print(f"Krátká ztráta, zatáčím doprava: {korekce}")
                    muj_povozek.zatoc_doprava(korekce)
                else:
                    if lost_count > MAX_LOST+10:
                        print(f"Dlouhá ztráta, zastavuji.")
                    # nevíme, kam – radši stop (bezpečně)
                     #   muj_povozek.stop()

                # po delší ztrátě zkus "search"
        
   
    sleep(0.1)
    

         
        
       
    
    muj_povozek.stop()

if __name__ == "__main__":  
    main()