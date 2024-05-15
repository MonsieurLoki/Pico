# Source: Electrocredible.com, Language: MicroPython
#https://electrocredible.com/raspberry-pi-pico-lcd-16x2-i2c-pcf8574-micropython/

import utime
from machine import Pin,I2C

from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

def setup_lcd():
    global lcd

    I2C_ADDR     = 0x27
    I2C_NUM_ROWS = 2
    I2C_NUM_COLS = 16

    SDA_GPIO = 16
    SCL_GPIO = 17


    i2c = I2C(0, sda=Pin(SDA_GPIO), scl=Pin(SCL_GPIO), freq=200000)
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)    

def check_lcd():
    global lcd

    print("check LDC")
    lcd.clear()
    for i in range(10):
        print(i)
        lcd.move_to(0,0)
        lcd.putstr("LCD check")
        lcd.move_to(0,1)
        str = "test {}".format(i)
        lcd.putstr(str)
        i += 1
        utime.sleep(0.5)
        
#---- main ----------------------------
    

def main():
    setup_lcd()
    check_lcd()
    

if __name__ == "__main__":
    main()
