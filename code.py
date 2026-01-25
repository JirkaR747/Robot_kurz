from picoed import button_b, button_a
from pca9633 import PCA9633
from podvozek import Podvozek
from picoed import i2c
from time import sleep


from konstanty import Konstanty




from time import sleep
from picoed import button_a, button_b
from konstanty import Konstanty




def clamp(value, minimum, maximum):
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


def main(muj_povozek):
    # Parametry chování
    KROK_KOREKCE = 5
    MAX_KOREKCE = 30
    MAX_BEZ_KOREKCE = 8     # po kolika cyklech zkusíme zvýšíme zatáčení
    stav = Konstanty.ST_START
    korekce = 0
    lost_count = 0
    posledni_strana = None  # Konstanty.levy / Konstanty.pravy / Konstanty.centralni

    # vyčisti eventy tlačítek
    button_a.was_pressed()
    button_b.was_pressed()

    while True:

        # --- univerzální STOP ---
        if button_b.was_pressed():
            stav = Konstanty.ST_STOP

        # --- čtení senzorů (jen když dává smysl) ---
        data = muj_povozek.senzory.vycti()
        muj_povozek.senzory.vypis(data)

        if data == -1:
            # I2C problém -> bezpečný stav
            stav = Konstanty.ST_ERROR

        # Stavové přepínání
        if stav == Konstanty.ST_START:
            # Před startem jen ukazujeme senzory, nic nejede
            muj_povozek.stop()

            if button_a.was_pressed():
                # start
                korekce = 0
                lost_count = 0
                posledni_strana = None
                stav = Konstanty.ST_JED

            
            

        if stav == Konstanty.ST_STOP:
            muj_povozek.stop()
            # Konec programu / nebo čekej na A pro restart
            # return
            stav = Konstanty.ST_START
           
            

        if stav == Konstanty.ST_ERROR:
            muj_povozek.stop()
            # v erroru zůstaň dokud se nestiskne A (restart) nebo B (stop)
            if button_a.was_pressed():
                stav = Konstanty.ST_START
            
            

        # --- vyhodnocení čáry (pro RUN i LOST) ---
        leva = muj_povozek.senzory.cara(data, Konstanty.levy)
        prava = muj_povozek.senzory.cara(data, Konstanty.pravy)
        stred = muj_povozek.senzory.cara(data, Konstanty.centralni)

        # --- ST_JED: normální sledování čáry ---
        if stav == Konstanty.ST_JED:
            if stred and not leva and not prava:
                # ideál – rovně
                korekce = 0
                lost_count = 0
                posledni_strana = None
                muj_povozek.jed_dopredu(0)

            elif leva and not prava:
                # čára vlevo -> zatoč doleva
                korekce = 0
                lost_count = 0
                posledni_strana = Konstanty.levy
                muj_povozek.zatoc_doleva(0)

            elif prava and not leva:
                # čára vpravo -> zatoč doprava
                korekce = 0
                lost_count = 0
                posledni_strana = Konstanty.pravy
                muj_povozek.zatoc_doprava(0)


            else:
                # nic nevidím -> přepni do Zatoč víc
                lost_count = 0
                korekce = 0
                stav = Konstanty.ST_ZATOC_VIC

            
           

        # --- ST_ZATOC_VIC: dohledávání čáry bez trhání ---
        if stav == Konstanty.ST_ZATOC_VIC:

            if stred or leva or prava:
                stav = Konstanty.ST_JED
                korekce = 0
                lost_count = 0
                
                continue
           
            lost_count += 1
            

            if lost_count > MAX_BEZ_KOREKCE:

                # provedeme "search pattern"
                korekce = clamp(korekce + KROK_KOREKCE, 0, MAX_KOREKCE)

                if posledni_strana == Konstanty.levy:
                    muj_povozek.zatoc_doleva(korekce)
                elif posledni_strana == Konstanty.pravy:
                    muj_povozek.zatoc_doprava(korekce)
                else:
                    print("Neznámá poslední strana, kroužím doleva")
                   
               

            

            

   
        sleep(0.01)
    
 

if __name__ == "__main__":  

    driver = PCA9633(i2c,0x70)
    muj_povozek = Podvozek(driver)

    main(muj_povozek)