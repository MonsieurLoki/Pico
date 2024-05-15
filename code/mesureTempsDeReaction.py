from machine import Pin, Timer
import utime
import random

Led = Pin(0, Pin.OUT)
BP = Pin(20, Pin.IN, Pin.PULL_UP)
flag = 0

def BP_pressed(pin):
    global flag
    BP.irq(handler = None)
    Led.value(0)
    TpsSTOP = utime.ticks_ms()
    TpsReact = utime.ticks_diff(TpsSTOP, TpsSTART) / 1000
    print("Temps de réaction: %2.2f s" %TpsReact)
    flag = 1
    utime.sleep(3)
    
Led.value(0)
while True:
    flag = 0
    tpsRand = random.randint(1,5)
    utime.sleep(tpsRand)
    Led.value(1)
    TpsSTART = utime.ticks_ms()
    BP.irq(trigger = Pin.IRQ_FALLING, handler = BP_pressed)
    
    while flag == 0:
        pass



  

