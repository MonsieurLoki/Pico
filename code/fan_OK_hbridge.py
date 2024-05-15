from machine import Pin, ADC, PWM
import time


POT = ADC(0)
pin_ENABLE = PWM(Pin(14))

pin_ENABLE.freq(100)

# while True:
#     pin_ENABLE.duty_u16(65000)
#         

# speed can vary from 0 to 100
def set_fan_speed(speed):
    pin_ENABLE.duty_u16(int(speed*65000/100))
#     print(f'speed: {speed}%')
    

def crescendo():
    while True:
    #    val = POT.read_u16()
    #    print(val)
    #    pin_ENABLE.duty_u16(val)
        for i in range(65):
            val = i*1000
            print(val)
            pin_ENABLE.duty_u16(val)
            time.sleep(1)
            
             
        for i in range(65, 0, -1):
            val = i*1000
            print(val)
            pin_ENABLE.duty_u16(val)
            time.sleep(1)


def test_3_speeds():
    set_fan_speed(25)
    time.sleep(3)
    set_fan_speed(50)
    time.sleep(3)
    set_fan_speed(75)
    time.sleep(3)
    set_fan_speed(100)
    time.sleep(6)
    set_fan_speed(75)
    time.sleep(3)
    set_fan_speed(50)
    time.sleep(3)
    set_fan_speed(25)
    time.sleep(3)
    set_fan_speed(0)
    

def main():
#     crescendo()
    
    test_3_speeds()


set_fan_speed(0)

if __name__ == "__main__":
    main()



