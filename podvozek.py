from motor import Motor
from pca9633 import PCA9633
from konstanty_motory import KonstantyMotory
from senzory import Senzory

# Třída pro ovládání podvozku robota
class Podvozek:

    pomalu_rychlost = 60
    normalne_rychlost = 100
    rychle_rychlost = 125

    def __init__(self, driver_motor: PCA9633) -> None:
        self.levy_motor = Motor(KonstantyMotory.levy, driver_motor)
        self.pravy_motor = Motor(KonstantyMotory.pravy, driver_motor)
        self.senzory = Senzory()

    # Pohyb vpřed
    def jed_dopredu(self, uprav_rychlost:int):
        self.levy_motor.jed(KonstantyMotory.dopredu, self.normalne_rychlost + uprav_rychlost)
        self.pravy_motor.jed(KonstantyMotory.dopredu, self.normalne_rychlost + uprav_rychlost)

    # Pohyb vzad
    def jed_dozadu(self, uprav_rychlost:int):
        self.levy_motor.jed(KonstantyMotory.dozadu, self.normalne_rychlost + uprav_rychlost)
        self.pravy_motor.jed(KonstantyMotory.dozadu, self.normalne_rychlost + uprav_rychlost)

    # Zatáčení doleva
    def zatoc_doleva(self, uprav_rychlost:int):
        self.levy_motor.jed(KonstantyMotory.dopredu, self.pomalu_rychlost - uprav_rychlost)
        self.pravy_motor.jed(KonstantyMotory.dopredu, self.rychle_rychlost + uprav_rychlost)

    # Zatáčení doprava
    def zatoc_doprava(self, uprav_rychlost:int):
        self.levy_motor.jed(KonstantyMotory.dopredu, self.rychle_rychlost + uprav_rychlost)
        self.pravy_motor.jed(KonstantyMotory.dopredu, self.pomalu_rychlost - uprav_rychlost)

    # Zastavení podvozku
    def stop(self):
        self.levy_motor.stop()
        self.pravy_motor.stop()