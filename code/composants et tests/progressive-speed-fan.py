import dht
import machine
import utime
from machine import Pin, PWM
import time
import network
import uasyncio as asyncio

# Configuration des broches pour les LEDs et le capteur DHT11
pin_dht = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Broche de données du capteur DHT11 (GPIO 18)
pin_led_green = machine.Pin(19, machine.Pin.OUT)  # LED verte (GPIO 19)
pin_led_red = machine.Pin(21, machine.Pin.OUT)   # LED rouge (GPIO 21)

# Configuration des broches pour les décodeurs 74LS47
decoder_1_A = machine.Pin(9, machine.Pin.OUT)  # Bit d'entrée A du premier décodeur (GPIO 9)
decoder_1_B = machine.Pin(8, machine.Pin.OUT)  # Bit d'entrée B du premier décodeur (GPIO 8)
decoder_1_C = machine.Pin(7, machine.Pin.OUT)  # Bit d'entrée C du premier décodeur (GPIO 7)
decoder_1_D = machine.Pin(6, machine.Pin.OUT)  # Bit d'entrée D du premier décodeur (GPIO 6)

decoder_2_A = machine.Pin(5, machine.Pin.OUT)  # Bit d'entrée A du deuxième décodeur (GPIO 5)
decoder_2_B = machine.Pin(4, machine.Pin.OUT)  # Bit d'entrée B du deuxième décodeur (GPIO 4)
decoder_2_C = machine.Pin(3, machine.Pin.OUT)  # Bit d'entrée C du deuxième décodeur (GPIO 3)
decoder_2_D = machine.Pin(2, machine.Pin.OUT)  # Bit d'entrée D du deuxième décodeur (GPIO 2)

# Configuration de la broche GPIO 14 pour PWM (contrôle du ventilateur)
enable_pin = Pin(14, Pin.OUT)
pwm = PWM(enable_pin)
pwm.freq(1000)

# Fonction pour régler la vitesse du ventilateur
def set_fan_speed(duty_cycle):
    pwm.duty_u16(duty_cycle)
    print(f"Vitesse du ventilateur réglée à {duty_cycle / 65535 * 100:.2f}%")

# Initialisation des décodeurs 74LS47
def set_decoder_inputs(decoder, value):
    decoder[0].value(value & 0b0001)
    decoder[1].value(value & 0b0010)
    decoder[2].value(value & 0b0100)
    decoder[3].value(value & 0b1000)

# Initialisation du capteur DHT11
sensor = dht.DHT11(pin_dht)

# Lecture de la température
def read_temperature():
    try:
        # Lecture des données depuis le capteur
        sensor.measure()
        # Récupération de la température
        temperature = sensor.temperature()
        return temperature
    except OSError as e:
        print("Erreur lors de la lecture du capteur DHT11:", e)
        return None

# Fonction pour contrôler les LEDs et le ventilateur en fonction de la température
def control_leds_and_fan(temperature):
    if temperature is not None:
        if temperature < 25:
            # Température en dessous de 25°C
            pin_led_green.on()
            pin_led_red.off()
            set_fan_speed(0)  # Éteindre le ventilateur
        elif temperature == 25:
            # Température de 25°C
            pin_led_green.off()
            pin_led_red.on()
            set_fan_speed(int(65535 * 0.50))  # 50% de vitesse
        elif temperature == 26:
            # Température de 26°C
            pin_led_green.off()
            pin_led_red.on()
            set_fan_speed(int(65535 * 0.85))  # 85% de vitesse
        else:
            # Température de 27°C ou plus
            pin_led_green.off()
            pin_led_red.on()
            set_fan_speed(65535)  # 100% de vitesse
    else:
        # En cas d'erreur de lecture de température, éteindre les LEDs et le ventilateur par sécurité
        pin_led_green.off()
        pin_led_red.off()
        set_fan_speed(0)

# Fonction pour afficher un nombre sur les deux afficheurs à sept segments
def display_number(number):
    # Affichage des dizaines
    set_decoder_inputs([decoder_1_A, decoder_1_B, decoder_1_C, decoder_1_D], number // 10)
    # Affichage des unités
    set_decoder_inputs([decoder_2_A, decoder_2_B, decoder_2_C, decoder_2_D], number % 10)

# Hardware definitions for web server
led = Pin("LED", Pin.OUT, value=1)
pin_up = Pin(14, Pin.OUT, value=0)
pin_down = Pin(15, Pin.OUT, value=0)
pin_stop = Pin(14, Pin.OUT, value=0)

# Configure your WiFi SSID and password
ssid = 'linksysed'
password = 'tototiti'

check_interval_sec = 0.25

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
<p>Last command issued was %s<p><br><br>
<p>Current Temperature: %s°C<p></body></html>
"""

def blink_led(frequency=0.5, num_blinks=3):
    for _ in range(num_blinks):
        led.on()
        time.sleep(frequency)
        led.off()
        time.sleep(frequency)

def control_door(cmd):
    if cmd == 'stop':
        pin_stop.on()
        blink_led(0.1, 1)
        pin_stop.off()
    if cmd == 'up':
        pin_up.on()
        blink_led(0.1, 1)
        pin_up.off()
    if cmd == 'down':
        pin_down.on()
        blink_led(0.1, 1)
        pin_down.off()

async def connect_to_wifi():
    wlan.active(True)
    wlan.config(pm=0xa11140)  # Disable powersave mode
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        await asyncio.sleep(1)

    if wlan.status() != 3:
        blink_led(0.1, 10)
        raise RuntimeError('WiFi connection failed')
    else:
        blink_led(0.5, 2)
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])

async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)

    while await reader.readline() != b"\r\n":
        pass
    
    request = str(request_line)
    cmd_up = request.find('DOOR=UP')
    cmd_down = request.find('DOOR=DOWN')
    cmd_stop = request.find('DOOR=STOP')

    stateis = ""  # Keeps track of the last command issued
    
    if cmd_stop == 8:
        stateis = "Door: STOP"
        print(stateis)
        control_door('stop')
    elif cmd_up == 8:
        stateis = "Door: UP"
        print(stateis)
        control_door('up')
    elif cmd_down == 8:
        stateis = "Door: DOWN"
        print(stateis)
        control_door('down')

    temperature = read_temperature()
    temperature_str = str(temperature) if temperature is not None else "N/A"

    response = html % (stateis, temperature_str)
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()

async def main():
    print('Connecting to WiFi...')
    await connect_to_wifi()

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))

    while True:
        temperature = read_temperature()
        control_leds_and_fan(temperature)
        if temperature is not None:
            print("Température: {}°C".format(temperature))
            display_number(temperature)  # Afficher la température
        await asyncio.sleep(2)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
