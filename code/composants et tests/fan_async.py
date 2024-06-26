"""
Garage Door Controller code
Written by Michael Ruppe @ Core Electronics
    - Version 1.0 July 2022

Hosts a static webpage with three garage door control buttons (Up, Stop, Down)
Outputs: Open Drain channels to pull-down garage door controller channels.

video : https://www.youtube.com/watch?v=AK8UYh7pMGM&t=1s&ab_channel=CoreElectronics
Adapted from examples in: https://datasheets.raspberrypi.com/picow/connecting-to-the-internet-with-pico-w.pdf

"""

import time
import network
import uasyncio as asyncio
from machine import Pin

import fan_OK_74LS47_7segments as seg7
import fan_OK_lcd_1602 as lcd
import fan_OK_dht11 as dht11
import fan_OK_leds as fan_leds

enable_pin = Pin(14, Pin.OUT)


ref_temp = 24

# Hardware definitions
led = Pin("LED", Pin.OUT, value=1)
pin_up = Pin(14, Pin.OUT, value=0)		# green led
pin_down = Pin(15, Pin.OUT, value=0)   	# orange led
pin_stop = Pin(14, Pin.OUT, value=0)	# red led

# Configure your WiFi SSID and password
ssid = 'iPhone de gaspard'
password = 'tototiti'

check_interval_sec = 0.25
check_interval_sec = 1

wlan = network.WLAN(network.STA_IF)


# The following HTML defines the webpage that is served
html = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
.buttonGreen { background-color: #4CAF50; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
.buttonRed { background-color: #d11d53; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
.buttonOrange { background-color: orange; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
</style></head>
<body><center><h1>Garage Door Controller</h1></center><br><br>
<form><center>
<center> <button class="buttonGreen" name="DOOR" value="UP" type="submit">Door UP</button>
<br><br>
<center> <button class="buttonRed" name="DOOR" value="STOP" type="submit">STOP</button>
<br><br>
<center> <button class="buttonOrange" name="DOOR" value="DOWN" type="submit">Door DOWN</button></center>
</center></form>
<br><br>
<br><br>
<p>Last command issued was %s<p></body></html>
"""

def blink_led(frequency = 0.5, num_blinks = 3):
    for _ in range(num_blinks):
        led.on()
        time.sleep(frequency)
        led.off()
        time.sleep(frequency)

def control_door(cmd):
    global ref_temp
    
    if cmd == 'stop':
        pin_stop.on()
        blink_led(0.1, 1)
        pin_stop.off()
        
    if cmd == 'up':
        ref_temp += 1
    
    if cmd == 'down':
        ref_temp -= 1
        
        
async def connect_to_wifi():
    wlan.active(True)
    wlan.config(pm = 0xa11140)  # Diable powersave mode
    wlan.connect(ssid, password)

    # Wait for connect or fail
    max_wait = 15
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        blink_led(0.1, 10)
        raise RuntimeError('WiFi connection failed')
    else:
        blink_led(0.5, 2)
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])
        
        status = wlan.ifconfig()
        
        lcd.lcd.move_to(0,1)
        lcd.lcd.putstr(f'{status[0]}')
        time.sleep(3)


async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    
    # find() valid garage-door commands within the request
    request = str(request_line)
    cmd_up = request.find('DOOR=UP')
    cmd_down = request.find('DOOR=DOWN')
    cmd_stop = request.find('DOOR=STOP')
    print ('DOOR=UP => ' + str(cmd_up)) # show where the commands were found (-1 means not found)
    print ('DOOR=DOWN => ' + str(cmd_down))
    print ('DOOR=STOP => ' + str(cmd_stop))

    stateis = "" # Keeps track of the last command issued
    
    # Carry out a command if it is found (found at index: 8)
    if cmd_stop == 8:
        stateis = "Door: STOP"
        print(stateis)
        control_door('stop')
        lcd.lcd.move_to(0,1)
        lcd.lcd.putstr("cmd: STOP  ")
        
    elif cmd_up == 8:
        stateis = "Door: UP"
        print(stateis)
        control_door('up')
        lcd.lcd.move_to(0,1)
        lcd.lcd.putstr("cmd: UP    ")

        
    elif cmd_down == 8:
        stateis = "Door: DOWN"
        print(stateis)
        control_door('down')
        lcd.lcd.move_to(0,1)
        lcd.lcd.putstr("cmd: DOWN  ")
    
    response = html % stateis
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()


async def main():
    lcd.setup_lcd()

    lcd.lcd.clear()
    lcd.lcd.move_to(0,0)
    lcd.lcd.putstr("Start async fan")
    print('Connecting to WiFi...')
    asyncio.create_task(connect_to_wifi())

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))

    seg7.setup_74LS47()
#     seg7.check_74LS47()

    i = 1
    while True:
        print(i)
        await asyncio.sleep(check_interval_sec)
        i+=1
        dht11.read_and_display_data()
        print(i, "temperature:", dht11.temperature, "  humidity:", dht11.humidity)
        lcd.lcd.move_to(0,0)
        lcd.lcd.putstr(f'Temperature : {dht11.temperature}')
        
        lcd.lcd.move_to(11,1)
        lcd.lcd.putstr(f'RT:{ref_temp}')
        
        
        if dht11.temperature >ref_temp:
            fan_leds.r_led.value(1)
            fan_leds.g_led.value(0)
            enable_pin.value(1)
            
            
        if dht11.temperature <=ref_temp:
            fan_leds.r_led.value(0)
            fan_leds.g_led.value(1)
            enable_pin.value(0)
        
        seg7.displayDigit(0,dht11.temperature % 10)
        seg7.displayDigit(1,dht11.temperature // 10)


try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
