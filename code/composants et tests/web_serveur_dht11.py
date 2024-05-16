# Simple HTTP Server Example
# Control an LED and read a Button using a web browser

import time
import network
import socket
import utime

from machine import Pin
from dht import DHT11, InvalidChecksum

# Initialize LED, Button, and Wi-Fi connection
led = Pin(15, Pin.OUT)
button = Pin(16, Pin.IN, Pin.PULL_UP)
ssid = 'linksysed'
password = 'tototiti'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# HTML for the web control panel
html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>
        html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
        .buttonGreen { background-color: #4CAF50; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
        .buttonRed { background-color: #D11D53; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
    </style>
</head>
<body>
    <center><h1>Control Panel</h1></center>
    <br><br>
    <form>
        <center>
        <button class="buttonGreen" name="led" value="on" type="submit">LED ON</button>
        <br><br>
        <button class="buttonRed" name="led" value="off" type="submit">LED OFF</button>
    </form>
    <br><br>
    <br><br>
    <p>%s<p>
</body>
</html>
"""

# Wait for connection or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Waiting for connection...')
    time.sleep(1)
    
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('Network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('IP Address:', status[0])
    
# Open socket
addr = socket.getaddrinfo('0.0.0.0', 8083)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('Listening on', addr)

# Initialize DHT11 sensor
pin = Pin(0, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

# Initialize GPIO pin for the fan
gpio_28 = Pin(28, Pin.OUT)
gpio_28.value(0)  # Start with the fan off

while True:
    try:
        # Accept client connection
        cl, addr = s.accept()
        print('Client connected from', addr)
        
        # Receive request
        request = cl.recv(1024)
        print('Request:', request)
        request = str(request)
        led_on = request.find('led=on')
        led_off = request.find('led=off')
        
        # Get current time
        (year, month, day, hour, minute, second, millis, _tzinfo) = utime.localtime()
        print("Date: %d-%02d-%02d Time: %02d:%02d:%02d" % (year, month, day, hour, minute, second))
        
        # Get temperature and humidity readings
        try:
            temperature = "Temperature: {}".format(sensor.temperature)
            humidity = "Humidity: {}".format(sensor.humidity)
        except InvalidChecksum:
            print("Checksum from the sensor was invalid")
        
        # Control fan based on temperature
        try:
            temperature_value = float(temperature.split(":")[1].strip())
            if temperature_value > 23:
                gpio_28.value(1)  # Turn on the fan
            else:
                gpio_28.value(0)  # Turn off the fan
        except ValueError:
            print("Temperature value is invalid.")
        
        # Control LED based on request
        if led_on == 8:
            print("LED ON")
            led.value(1)
        elif led_off == 8:
            print("LED OFF")
            led.value(0)
            gpio_28.value(0)  # Turn off the fan when LED is turned off
        
        # Update LED state
        led_state = "LED is OFF" if led.value() == 0 else "LED is ON"
        
        # Check button state
        if button.value() == 1:
            button_state = "Button is NOT pressed"
        else:
            button_state = "Button is pressed"
        
        # Send response to client
        state_info = led_state + " and " + button_state + "<br>" + temperature + "<br>" + humidity
        response = html % state_info
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        time.sleep(1)  # Add a delay to allow the socket to release
        print('Connection closed')
