# Hardware Test
# Blink and LED (GP15) slowly/quickly while a button (GP16) is not-pressed/pressed
from machine import Pin
from time import sleep_ms

led = Pin(15, Pin.OUT)
button = Pin(16, Pin.IN, Pin.PULL_UP)
print("test")
while True:
    if button.value() == 0: # button pressed
        delay = 100 # short delay
        print("le bouton est pressé")
    else:
        delay = 1000 # long delay
        print("le bouton n'est pas pressé")
    led.toggle()
    sleep_ms(delay)
