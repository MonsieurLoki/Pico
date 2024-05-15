#
# Basic 7-segment display test
#

from machine import Pin
import time


# 74LS47 nr 0 (digit for the units)
A0_PIN = 5
B0_PIN = 4
C0_PIN = 3
D0_PIN = 2

# 74LS47 nr 1 (digit for the tens)
A1_PIN = 9
B1_PIN = 8
C1_PIN = 7
D1_PIN = 6

def setup_74LS47():
    global A0, B0, C0, D0
    global A1, B1, C1, D1
    
    A0 = Pin(A0_PIN, Pin.OUT)
    B0 = Pin(B0_PIN, Pin.OUT)
    C0 = Pin(C0_PIN, Pin.OUT)
    D0 = Pin(D0_PIN, Pin.OUT)
    
    A1 = Pin(A1_PIN, Pin.OUT)
    B1 = Pin(B1_PIN, Pin.OUT)
    C1 = Pin(C1_PIN, Pin.OUT)
    D1 = Pin(D1_PIN, Pin.OUT)
       
def getBits(digit):
    d = digit
    bit1 = d % 2
    d = d // 2
    bit2 = d % 2
    d = d // 2
    bit3 = d % 2
    d = d // 2
    bit4 = d % 2

    return [bit1, bit2, bit3, bit4]

def displayDigit(nr_7segment,digit):
    global A0, B0, C0, D0 
    global A1, B1, C1, D1 

    bits = getBits(digit)

    if nr_7segment == 0:
        A0.off()
        B0.off()
        C0.off()
        D0.off()

        if bits[0] > 0: A0.on()
        if bits[1] > 0: B0.on()
        if bits[2] > 0: C0.on()
        if bits[3] > 0: D0.on()
    
    if nr_7segment == 1:
        A1.off()
        B1.off()
        C1.off()
        D1.off()

        if bits[0] > 0: A1.on()
        if bits[1] > 0: B1.on()
        if bits[2] > 0: C1.on()
        if bits[3] > 0: D1.on()
    
    #print(f'nr_7segment:{nr_7segment}, digit:{digit} -> {bits[3]}{bits[2]}{bits[1]}{bits[0]}')
    
def spinner():
    delay = 0.2
    for i in range(5):
        displayDigit(0,10)
        displayDigit(1,10)
        time.sleep(delay)
        displayDigit(0,12)
        displayDigit(1,12)
        time.sleep(delay)
        displayDigit(0,11)
        displayDigit(1,11)
        time.sleep(delay)

def blank_7segments():
    displayDigit(0,15)
    displayDigit(1,15)
    
def test_7segments_OK():
    for i in range(5):
        displayDigit(0,8)
        displayDigit(1,8)
        time.sleep(1)
        blank_7segments()
        time.sleep(0.1)

#    blink_7segments(8)

def blink_7segments(digit):    
    for i in range(5):
        displayDigit(0,digit)
        displayDigit(1,digit)
        time.sleep(0.1)
        blank_7segments()
        time.sleep(0.1)

def countdown_7segment():
    # countdown
    i = 0
    while i<1:
        for digit in range(9,-1,-1):
            print(digit)
            displayDigit(0,digit)
            displayDigit(1,digit)
            time.sleep(1)
        i += 1

def check_74LS47_10_to_15():
    # check digits from 10 to 15
    for digit in range(10,16):
        print(digit)
        displayDigit(0,digit)
        displayDigit(1,digit)
        time.sleep(1)

def check_74LS47():
    # this is the opportunity to make some adjustments...

    print("test 7segments (diodes) are OK")
    test_7segments_OK()
    
    print("countdown")
    countdown_7segment()
    blink_7segments(0)
              
    blank_7segments()
    time.sleep(1)

    print("check digits 10 to 15")
    check_74LS47_10_to_15()

    blank_7segments()
    time.sleep(1)
    
    spinner()
    blank_7segments()
        

#- main ------------------------------------------------------------
def main():
    #try:
    setup_74LS47()
    check_74LS47()

    # except KeyboardInterrupt:
    #     # Handle Ctrl+C gracefully
    #     print("KeyboardInterrupt")    
    #     print("machine reset")
    #     machine.reset()

if __name__ == "__main__":
    main()

