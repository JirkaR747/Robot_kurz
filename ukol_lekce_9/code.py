from picoed import button_b, button_a, display
from time import sleep
from math import pi
from baterie import Baterie


from robot import Robot
from konstanty import Konstanty

# 0 vse ok
# -1 chyba inicializace robota
# -2 chyba v kalibraci

def inicializace(muj_robot):

    error = muj_robot.inicializace()
    if error != 0:
        print("Robot se nezinicializoval:" + str(error))
        return -1
    
    #tento zastav se tady hodi mit, protoze kdyz robot selze v predchozim behu, tak tady ta funkce zastavi motory
    muj_robot.zastav()

    #dobrovolny krok vycitat napeti
    baterie=Baterie()
    
    if baterie.stav() < 5.5:    #baterie je slaba, ale stale pouzitelna, upozorni uzivatele
        
        while not button_b.was_pressed(): 
            display.show(baterie.stav())
            sleep(0.1)
        display.clear()

        if baterie.stav() < 3.9:
         return -3          #baterie je tak slaba, ze by se mohl robot pri pohybu vypnout, nelze pokračovat
        
        
    


         
    
    


    #kalibrace
    min_pwm = 50
    error1, error2 = muj_robot.zkalibruj_se(min_pwm)
    if error1 != 0 or error2 != 0:
        print("Error v kalibraci:" + str(error1) + " " + str(error2))
        return -2 
    else:
        return 0



def main():
    muj_robot = Robot(0.154, 0.067)
    error = inicializace(muj_robot)
    if error != 0:
        return error

    while not button_a.was_pressed():
        sleep(0.1)
        
    #zkouska pohybu
    muj_robot.jed(0.2, 0)
    sleep(1)
    muj_robot.zastav()
    muj_robot.jed(0, pi/2) # otocka o 90 stupnu
    sleep(1)
    muj_robot.zastav()


if __name__ == "__main__":
    main()