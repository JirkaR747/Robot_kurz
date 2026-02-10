from picoed import button_b, display
from time import sleep, monotonic_ns
from board import P14, P15
from digitalio import DigitalInOut
from enkoder import Enkoder
from math import fabs
from konstanty_motory import KonstantyMotory
from motor import Motor
from picoed import i2c
from pca9633 import PCA9633

def rozdil_casu(posledni_cas_ns: int, cas_ted_ns: int):
        return fabs(cas_ted_ns - posledni_cas_ns)/1000000000.0

def main():    
    levy_enkoder = Enkoder(P14)
    pravy_enkoder = Enkoder(P15)
    
    driver = PCA9633(i2c,0x70)
    levy_motor=Motor(KonstantyMotory.levy, driver)
    pravy_motor=Motor(KonstantyMotory.pravy, driver)
    levy_motor.jed(KonstantyMotory.dopredu,0)
    pravy_motor.jed(KonstantyMotory.dopredu,0)

    cas_minule = monotonic_ns()
    cas_minule_motor = monotonic_ns()

    perioda_mereni = 0.5  # sekundy
    perioda_zmeny_otacek=5.0  # sekundy
    r_levy=0
    r_pravy=0

    while not button_b.was_pressed():
        cas_ted = monotonic_ns()
        cas_ted_motor = monotonic_ns()
        levy_enkoder.pocet_tiku()
        pravy_enkoder.pocet_tiku()

        presny_rozdil_casu = rozdil_casu(cas_ted, cas_minule)
        presny_rozdil_casu_motor = rozdil_casu(cas_ted, cas_minule_motor)  

        if presny_rozdil_casu_motor > perioda_zmeny_otacek:
            r_levy += 10
            r_pravy += 10
           
            levy_motor.jed(KonstantyMotory.dopredu,r_levy)
            pravy_motor.jed(KonstantyMotory.dopredu,r_pravy)
            cas_minule_motor = cas_ted_motor
            print(f"pwm: levý {r_levy}, pravý {r_pravy}") 
        
        if  presny_rozdil_casu > perioda_mereni:
             rychlost_levy = (float(levy_enkoder.soucet_tiku)/40)*6.28 / float(presny_rozdil_casu)
             rychlost_pravy = (float(pravy_enkoder.soucet_tiku)/40) / float(presny_rozdil_casu)
             print(f"levý: {rychlost_levy}, pravý: {rychlost_pravy}")
             #print(f"tiky levý: {levy_enkoder.soucet_tiku}, tiky pravý: {pravy_enkoder.soucet_tiku}")
             #print(f"čas: {presny_rozdil_casu}")

             levy_enkoder.soucet_tiku = 0
             pravy_enkoder.soucet_tiku = 0
             cas_minule = cas_ted
       
        sleep(0.005)

    levy_motor.stop()
    pravy_motor.stop()
     

if __name__ == "__main__":
    main() 