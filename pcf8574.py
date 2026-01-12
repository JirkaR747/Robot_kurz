class PCF8574:
    def __init__(self, i2c, address=0x38):
        self._i2c = i2c
        self._address = address
        self._buffer = bytearray(1)

    def read(self):
        if self._i2c.try_lock():
            try:
                self._i2c.readfrom_into(self._address, self._buffer)
                return self._buffer[0]
            finally:
                self._i2c.unlock()
        else:
            raise RuntimeError("I2C busy")

   