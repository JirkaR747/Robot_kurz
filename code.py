from picoed import i2c
from pca9633 import PCA9633
from motor import Motor
from time import sleep



if __name__ == "__main__":
    adress = 0x70
    driver = PCA9633(i2c,adress)
    motor_levy = Motor("leva", driver)
    motor_pravy = Motor("prava", driver)

    motor_levy.jed("dopredu", 100)
    motor_pravy.jed("dopredu", 100)
    sleep(2)
    motor_levy.stop()
    motor_pravy.stop()
    sleep(1)
    motor_levy.jed("dozadu", 150)
    motor_pravy.jed("dozadu", 150)
    sleep(2)
    motor_levy.stop()
    motor_pravy.stop()
   