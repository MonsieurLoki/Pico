from machine import Pin
from time import sleep
m_led = Pin(25, Pin.OUT)
g_led = Pin(19, Pin.OUT)
y_led = Pin(20, Pin.OUT)
r_led = Pin(21, Pin.OUT)

    

def main():
    i = 0;

    while True:
        print(i)
        m_led.value(1)
        r_led.value(1)
        y_led.value(1)
        g_led.value(1)
        sleep(0.5)
        m_led.value(0)
        r_led.value(0)
        y_led.value(0)
        g_led.value(0)
        sleep(0.5)
        i += 1
    

if __name__ == "__main__":
    main()


