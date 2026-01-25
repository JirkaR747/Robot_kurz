from time import sleep

# PCA9633 driver class
class PCA9633:
    def __init__(self, i2c, address=0x70):
       
        self.address = address
        self.PWM0 = b"\x02"
        self.PWM1 = b"\x03"
        self.PWM2 = b"\x04"
        self.PWM3 = b"\x05"
        self.max_pwm_value = 200
        self.i2c = i2c
        self.inicializace_ok = self.inicializace_zarizeni()==0
        
     

    # Nastavení PWM pro daný kanál
    def set_pwm(self, pwm_on,pwm_off, value):
        value = max(0, min(value, self.max_pwm_value)) # omezit na max hodnotu
        if self .i2c.try_lock() & self.inicializace_ok:            
            self.i2c.writeto(self.address,pwm_off + bytes([0]))
            self.i2c.writeto(self.address,pwm_on + bytes([value]))
            self.i2c.unlock()
            return 0
        else:
            print("Nepodarilo se zamknout i2c")
            return -1
       

    # Inicializace zařízení PCA9633
    def inicializace_zarizeni(self):
        
        if self .i2c.try_lock():
            self.i2c.writeto(self.address, b'\x00\x01')
            self.i2c.writeto(self.address, b'\xE8\xAA')
            self.i2c.unlock()
            sleep(0.1)
            return 0
        else:
            print("Nepodarilo se zamknout i2c")
            return -1    