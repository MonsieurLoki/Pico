from machine import Pin, ADC, PWM
import time


POT = ADC(0)
LED = PWM(Pin(14))

LED.freq(100)

while True:
    LED.duty_u16(65000)
        


while True:
#    val = POT.read_u16()
#    print(val)
#    LED.duty_u16(val)
    for i in range(65):
        val = i*1000
        print(val)
        LED.duty_u16(val)
        time.sleep(1)
        
         
    for i in range(65, 0, -1):
        val = i*1000
        print(val)
        LED.duty_u16(val)
        time.sleep(1)
         
    
