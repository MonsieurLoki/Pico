import network
import socket
import machine
import utime
from machine import Pin, PWM
import dht

# Configuration du Wi-Fi
ssid = 'linksysed'
password = 'tototiti'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Attente de la connexion
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('Waiting for connection...')
    utime.sleep(1)

if wlan.status() != 3:
    raise RuntimeError('Network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('IP Address:', status[0])

# Configuration des broches pour les LEDs et le capteur DHT11
pin_dht = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)
pin_led_green = machine.Pin(19, machine.Pin.OUT)
pin_led_red = machine.Pin(21, machine.Pin.OUT)

enable_pin = Pin(14, Pin.OUT)
pwm = PWM(enable_pin)
pwm.freq(1000)

sensor = dht.DHT11(pin_dht)

def set_fan_speed(duty_cycle):
    pwm.duty_u16(duty_cycle)
    print(f"Fan speed set to {duty_cycle / 65535 * 100:.2f}%")

def read_temperature():
    try:
        sensor.measure()
        temperature = sensor.temperature()
        return temperature
    except OSError as e:
        print("Error reading DHT11 sensor:", e)
        return None

def control_leds_and_fan(temperature):
    if temperature is not None:
        if temperature < 25:
            pin_led_green.on()
            pin_led_red.off()
            set_fan_speed(0)
        elif temperature == 25:
            pin_led_green.off()
            pin_led_red.on()
            set_fan_speed(int(65535 * 0.50))
        elif temperature == 26:
            pin_led_green.off()
            pin_led_red.on()
            set_fan_speed(int(65535 * 0.85))
        else:
            pin_led_green.off()
            pin_led_red.on()
            set_fan_speed(65535)
    else:
        pin_led_green.off()
        pin_led_red.off()
        set_fan_speed(0)

# Serveur web simple
def web_page():
    temperature = read_temperature()
    control_leds_and_fan(temperature)
    if temperature is not None:
        temp = str(temperature)
    else:
        temp = 'Error'
    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            html {{ font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}}
            .button {{ background-color: #4CAF50; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }}
            .button2 {{background-color: #555555;}}
        </style>
    </head>
    <body>
        <h1>Fan Control</h1>
        <p>Temperature: {temp}°C</p>
        <button class="button" onclick="setFanSpeed(0)">Turn Off Fan</button>
        <button class="button button2" onclick="setFanSpeed(32768)">50% Speed</button>
        <button class="button button2" onclick="setFanSpeed(65535)">100% Speed</button>
        <script>
            function setFanSpeed(speed) {{
                fetch('/set_fan?speed=' + speed);
            }}
            setInterval(() => {{
                fetch('/get_temp')
                    .then(response => response.json())
                    .then(data => {{
                        document.querySelector('p').innerText = `Temperature: ${temp}°C`;
                    }});
            }}, 2000);
        </script>
    </body>
    </html>"""
    return html

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(5)

print('Listening on', addr)

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024)
    request = str(request)
    print('Request:', request)

    if '/set_fan' in request:
        try:
            params = request.split(' ')[1]
            query = params.split('?')[1]
            speed = int(query.split('=')[1])
            set_fan_speed(speed)
            response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + web_page()
        except:
            response = 'HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n\r\n'
    elif '/get_temp' in request:
        temperature = read_temperature()
        response = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n'
        response += f'{{"temperature": {temperature}}}'
    else:
        response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + web_page()

    cl.send(response)
    cl.close()
